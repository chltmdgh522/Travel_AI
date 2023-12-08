import csv
import os
from audioop import reverse
import difflib
from konlpy.tag import Okt
import pandas as pd
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from sklearn.linear_model import LogisticRegression

from .models import SurveyData
from .models import TravelResponse
from .models import TravelDestination
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from sklearn.feature_extraction.text import CountVectorizer

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from datetime import datetime


def home(request):
    return render(request, 'users/home.html')
def robby_view(request):
    return render(request, 'users/robby.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def travel_view(request):
    # 사용자에 대한 TravelResponse 인스턴스 가져오기
    try:
        travel_response = TravelResponse.objects.get(user=request.user)  # 관련 이름이 'travelresponse'인 경우
    except TravelResponse.DoesNotExist:
        # 사용자에 대한 TravelResponse가 없는 경우 처리
        travel_response = None
        return render(request, 'travel/travel.html', {'travel_response': None})

    travel_from_db = TravelDestination.objects.values('country', 'name', 'keyword', 'latitude', 'longitude', 'id')

    matching_country_travels = [travel for travel in travel_from_db if
                                travel['country'] == travel_response.country or travel['country'] == '역사'
                                or travel['country'] == '자연'
                                or travel['country'] == 'SNS'
                                or travel['country'] == '문화'
                                or travel['country'] == '관광'
                                or travel['country'] == '먹방']

    recommendations = ai1(travel_response, matching_country_travels)

    return render(request, 'travel/travel.html',
                  {'travel_response': travel_response, 'recommendations': recommendations})


# @login_required
# def recommend_view(request):
#     try:
#         travel_response = TravelResponse.objects.get(user=request.user)  # 관련 이름이 'travelresponse'인 경우
#     except TravelResponse.DoesNotExist:
#         # 사용자에 대한 TravelResponse가 없는 경우 처리
#         travel_response = None
#     csv_file_path = r'C:\Users\chltm\PycharmProjects\djangoProject1\Django-registration-and-login-system\키워드.csv'
#     os.chdir(r"C:\Users\chltm\PycharmProjects\djangoProject1\Django-registration-and-login-system")
#     selected_rows = []
#
#     # CSV 파일 읽기
#     with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
#         csv_reader = csv.DictReader(csvfile)
#
#         # CSV 파일의 각 행에 대해 반복
#         for row in csv_reader:
#             #print(f"Comparing: {row.get('나라')} with {travel_response.country}")
#             # 특정 조건을 만족하는 경우 해당 행을 선택
#             if '나라' in row and row['나라'] == travel_response.country:
#                 if '기간' in row and row['기간'] == travel_response.duration:
#                     if '키워드' in row and row['키워드'] == travel_response.travel_style:
#                         selected_rows.append(row)
#
#     return render(request, 'travel/recommend.html',
#                   {'travel_response': travel_response, 'selected_rows': selected_rows})


def modelAi(user_response):
    # 사용자가 선택한 여행 응답
    user_response = {
        'country': user_response.country,
        'companion': user_response.companion,
        'age': user_response.age,
        'preference': 0,
        'destination': ''
    }

    # 사용자 응답을 특성으로 가지는 데이터 생성
    user_data = [
        [user_response['country'], user_response['companion'], user_response['age'],
         user_response['preference'], user_response['destination']]
    ]

    # 데이터프레임 생성
    columns = ['country', 'companion', 'age', 'preference', 'destination']
    user_df = pd.DataFrame(user_data, columns=columns)

    # 원핫 인코딩
    user_df_encoded = pd.get_dummies(user_df, columns=[
        'country', 'companion', 'age', 'preference', 'destination'])
    user_df_encoded = user_df_encoded.astype(int)

    # survey 모델에서 데이터 가져오기
    survey_data = SurveyData.objects.all()

    # 가져온 데이터를 전처리하여 특성과 레이블로 분리
    processed_data = []

    for entry in survey_data:
        processed_row = {
            'country': entry.country,
            'destination': entry.destination,
            'age': entry.age,
            'companion': entry.companion,
            'preference': entry.preference,
        }
        processed_data.append(processed_row)

    X = pd.DataFrame(processed_data, columns=[
        'country', 'destination', 'age', 'companion', 'preference'])
    y = (X['preference'] >= 3).astype(int)  # preference가 3 이상인 경우 1, 아니면 0으로 변환

    # 원핫 인코딩 적용
    X_encoded = pd.get_dummies(
        X, columns=['country', 'destination', 'age', 'companion'])
    X_encoded = X_encoded.astype(int)

    # 모델 초기화 및 학습
    model = LogisticRegression()
    model.fit(X_encoded, y)

    matching_columns = [
        col for col in X_encoded.columns if col in user_df_encoded.columns]

    # 사용자 데이터에서 필요한 열만 선택
    user_df_encoded_subset = user_df_encoded[matching_columns]

    # 모델에 학습된 데이터와 사용자 데이터 일치 여부 확인
    is_matching = X_encoded.eq(user_df_encoded_subset.iloc[0]).sum(axis=1) >= 3

    # 일치하는 경우에만 preference가 3 이상인 결과 출력
    matched_indices = is_matching[is_matching].index

    matched_data_from_model = X_encoded.loc[matched_indices]

    original_values = set()  # 중복을 허용하지 않는 set으로 변경

    for index, row in matched_data_from_model.iterrows():
        current_original_value = set()  # 현재 행에 대한 set을 초기화
        for column in matched_data_from_model.columns:
            if column.startswith('destination_') and row[column] == 1:
                current_original_value.add(column.split('_')[1])
        original_values.update(current_original_value)  # 현재 행의 set을 전체 set에 추가

    return list(original_values)  # set을 다시 리스트로 변환


@login_required
def recommend_view(request):
    try:
        travel_response = TravelResponse.objects.get(user=request.user)  # 관련 이름이 'travelresponse'인 경우
    except TravelResponse.DoesNotExist:
        # 사용자에 대한 TravelResponse가 없는 경우 처리
        travel_response = None

    survey_data = modelAi(travel_response)

    print(survey_data)

    travel_from_db = TravelDestination.objects.values('country', 'name', 'keyword', 'latitude', 'longitude', 'id')

    matching_country_travels = [travel for travel in travel_from_db if
                                travel['country'] == travel_response.country
                                or travel['country'] == '역사'
                                or travel['country'] == '자연'
                                or travel['country'] == 'SNS'
                                or travel['country'] == '문화'
                                or travel['country'] == '관광'
                                or travel['country'] == '먹방']

    recommendations = ai1(travel_response, matching_country_travels)
    print("dd")
    # 데이터프레임 생성
    # 여러 데이터프레임을 저장할 빈 데이터프레임 생성
    result_df = pd.DataFrame(columns=['name', 'age', 'country'])  # 필요한 열을 추가
    result=[]
    for df in recommendations:
        for index, row in df.iterrows():
            for a in survey_data:
                if row['name'] == a:
                    result.append(row)

    # 결과 데이터프레임 생성
    result_df = pd.DataFrame(result)
    rows = result_df.to_dict(orient='records')
    for row in rows:
        print("1")
        print(row['name'])

    # 템플릿에 전달할 컨텍스트 생성
    return render(request, 'travel/recommend.html',
                  {'travel_response': travel_response, 'recommendations': rows})


def ai1(travel_response, travel_from_db):
    # QuerySet을 Pandas DataFrame으로 변환
    travels_df = pd.DataFrame(list(travel_from_db))
    # 한글 자연어 처리를 위한 형태소 분석기(Okt) 사용
    okt = Okt()

    # keyword을 형태소로 분리한 후 공백으로 합치는 함수 정의
    def tokenize(keyword):
        return ' '.join(okt.morphs(keyword))

    # keyword에 대해 형태소 분석 및 벡터화
    travels_df['Tokenized_keyword'] = travels_df['keyword'].apply(tokenize)

    # TF-IDF 벡터화
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(
        travels_df['Tokenized_keyword'])

    # 코사인 유사도 계산
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    def recommend_travel_genre(title, travel_duration, cosine_sim=cosine_sim):
        idx = travels_df.loc[travels_df['country'] == title].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # travel_duration에 따라 추천하는 개수를 조절
        num_recommendations = travel_duration * 3
        sim_scores = sim_scores[1:num_recommendations + 1]  # 계산된 수에 맞게 범위 조절

        travel_indices = [i[0] for i in sim_scores]

        group_size = travel_duration
        num_groups = len(travel_indices) // group_size
        recommended_groups = []
        for i in range(num_groups):
            start_index = i * group_size
            end_index = (i + 1) * group_size
            recommended_travels = travels_df[['country', 'keyword', 'name', 'latitude', 'longitude']].iloc[
                travel_indices[start_index:(start_index + 1)]]

            recommended_groups.append(recommended_travels)


        return recommended_groups

    input_travel = travel_response.travel_style
    input_duration = int(travel_response.duration.split('박')[0])

    # 여행 추천
    recommendations = recommend_travel_genre(input_travel, input_duration)

    return recommendations


def ai(travel_response, travel_from_db):
    # QuerySet을 Pandas DataFrame으로 변환
    travels_df = pd.DataFrame(list(travel_from_db))
    travel_duration = int(travel_response.duration.split('박')[0])
    # 한글 자연어 처리를 위한 형태소 분석기(Okt) 사용
    okt = Okt()

    # keyword을 형태소로 분리한 후 공백으로 합치는 함수 정의
    def tokenize(keyword):
        return ' '.join(okt.morphs(keyword))

    # keyword에 대해 형태소 분석 및 벡터화
    travels_df['Tokenized_keyword'] = travels_df['keyword'].apply(tokenize)

    # TF-IDF 벡터화
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(
        travels_df['Tokenized_keyword'])

    # 코사인 유사도 계산
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    def recommend_travel_genre(title, travel_duration, cosine_sim=cosine_sim):
        idx = travels_df.loc[travels_df['country'] == title].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # travel_duration에 따라 추천하는 개수를 조절
        num_recommendations = travel_duration * 3
        sim_scores = sim_scores[1:num_recommendations + 1]  # 계산된 수에 맞게 범위 조절

        travel_indices = [i[0] for i in sim_scores]

        group_size = travel_duration
        num_groups = len(travel_indices) // group_size
        recommended_groups = []
        for i in range(num_groups):
            start_index = i * group_size
            end_index = (i + 1) * group_size
            recommended_travels = travels_df[['country', 'keyword', 'name', 'latitude', 'longitude', 'id']].iloc[
                travel_indices[start_index:end_index]]
            recommended_groups.append(recommended_travels)
        return recommended_groups

    input_travel = travel_response.travel_style
    input_duration = int(travel_response.duration.split('박')[0])

    # 여행 추천
    recommendations = recommend_travel_genre(input_travel, input_duration)
    # print(f"Recommendations for {input_travel}:")
    # print(recommendations[0])

    return recommendations


@login_required
def site_view(request, travel_id):
    try:
        travel_response = TravelResponse.objects.get(user=request.user)  # 관련 이름이 'travelresponse'인 경우
    except TravelResponse.DoesNotExist:
        # 사용자에 대한 TravelResponse가 없는 경우 처리
        travel_response = None

    travel_from_db = TravelDestination.objects.values('country', 'name', 'keyword', 'latitude', 'longitude', 'id')

    matching_country_travels = [travel for travel in travel_from_db if
                                travel['country'] == travel_response.country or travel['country'] == '역사'
                                or travel['country'] == '자연'
                                or travel['country'] == 'SNS'
                                or travel['country'] == '문화'
                                or travel['country'] == '관광'
                                or travel['country'] == '먹방']

    recommendations = ai(travel_response, matching_country_travels)

    result = recommendations[int(travel_id) - 1]
    print(result.name)

    # 가져온 데이터를 템플릿으로 전달
    return render(request, 'travel/site.html',
                  {'travel_id': travel_id, 'results': result, 'travel_response': travel_response})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def plan_view1(request):
    return render(request, 'travel/plan1.html')


@login_required
def save_plan1(request):
    # 사용자에 대한 TravelResponse 인스턴스를 가져오거나 생성
    travel_response, created = TravelResponse.objects.get_or_create(user=request.user)

    # 폼 데이터 가져오기
    country = request.POST.get('country')

    # TravelResponse 모델 업데이트
    travel_response.country = country

    # 업데이트된 모델 저장
    travel_response.save()

    return redirect('travel/plan2')  # 저장 후 여행 폼으로 리디렉션\


@login_required
def plan_view2(request):
    return render(request, 'travel/plan2.html')


@login_required
def save_plan2(request):
    if request.method == 'POST':
        # 사용자에 대한 TravelResponse 인스턴스를 가져오거나 생성
        travel_response, created = TravelResponse.objects.get_or_create(user=request.user)

        # 폼 데이터 가져오기
        departure_date_str = request.POST.get('departure_date')
        arrival_date_str = request.POST.get('arrival_date')

        # 문자열을 datetime 객체로 변환 (형식 "%m/%d/%Y")
        departure_date = datetime.strptime(departure_date_str, "%m/%d/%Y")
        arrival_date = datetime.strptime(arrival_date_str, "%m/%d/%Y")

        # TravelResponse 모델 업데이트
        travel_response.arrival_date = arrival_date
        travel_response.departure_date = departure_date

        # 여행 기간 계산
        duration = arrival_date - departure_date

        # 업데이트된 모델 저장
        travel_response.duration = f"{duration.days}박{duration.days + 1}일"
        travel_response.save()

        return redirect('travel/plan3')  # 저장 후 여행 폼으로 리디렉션


@login_required
def plan_view3(request):
    return render(request, 'travel/plan3.html')


@login_required
def save_plan3(request):
    if request.method == 'POST':
        # 사용자에 대한 TravelResponse 인스턴스를 가져오거나 생성
        travel_response, created = TravelResponse.objects.get_or_create(user=request.user)

        # 폼 데이터 가져오기
        companions = request.POST.get('companion')

        # TravelResponse 모델 업데이트
        travel_response.companion = companions

        # 업데이트된 모델 저장
        travel_response.save()

        return redirect('travel/plan4')  # 저장 후 여행 폼으로 리디렉션


@login_required
def plan_view4(request):
    return render(request, 'travel/plan4.html')


@login_required
def save_plan4(request):
    if request.method == 'POST':
        # 사용자에 대한 TravelResponse 인스턴스를 가져오거나 생성
        travel_response, created = TravelResponse.objects.get_or_create(user=request.user)

        # 폼 데이터 가져오기
        travel_style = request.POST.get('travel_style')

        # TravelResponse 모델 업데이트
        travel_response.travel_style = travel_style

        # 업데이트된 모델 저장
        travel_response.save()

        return redirect('travel/plan5')  # 저장 후 여행 폼으로 리디렉션


@login_required
def plan_view5(request):
    return render(request, 'travel/plan5.html')


@login_required
def save_plan5(request):
    if request.method == 'POST':
        # 사용자에 대한 TravelResponse 인스턴스를 가져오거나 생성
        travel_response, created = TravelResponse.objects.get_or_create(user=request.user)

        # 폼 데이터 가져오기
        age = request.POST.get('age')

        # TravelResponse 모델 업데이트
        travel_response.age = age

        # 업데이트된 모델 저장
        travel_response.save()

        return redirect('recommend')  # 저장 후 여행 폼으로 리디렉션
