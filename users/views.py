import csv
import os
from audioop import reverse

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import TravelResponse

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from datetime import datetime


def home(request):
    return render(request, 'users/home.html')


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
        travel_response = TravelResponse.objects.get(user=request.user)
    except TravelResponse.DoesNotExist:
        return render(request, 'travel/travel.html', {'travel_response': None})

    # travel_response가 존재할 경우에는 HttpResponse 객체 반환
    return (render(request, 'travel/travel.html', {'travel_response': travel_response}))

@login_required
def recommend_view(request):
    try:
        travel_response = TravelResponse.objects.get(user=request.user)  # 관련 이름이 'travelresponse'인 경우
    except TravelResponse.DoesNotExist:
        # 사용자에 대한 TravelResponse가 없는 경우 처리
        travel_response = None
    csv_file_path = r'C:\Users\chltm\PycharmProjects\djangoProject1\Django-registration-and-login-system\키워드.csv'
    os.chdir(r"C:\Users\chltm\PycharmProjects\djangoProject1\Django-registration-and-login-system")
    selected_rows = []

    # CSV 파일 읽기
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        # CSV 파일의 각 행에 대해 반복
        for row in csv_reader:
            #print(f"Comparing: {row.get('나라')} with {travel_response.country}")
            # 특정 조건을 만족하는 경우 해당 행을 선택
            if '나라' in row and row['나라'] == travel_response.country:
                if '기간' in row and row['기간'] == travel_response.duration:
                    if '키워드' in row and row['키워드'] == travel_response.travel_style:
                        selected_rows.append(row)

    return render(request, 'travel/recommend.html',
                  {'travel_response': travel_response, 'selected_rows': selected_rows})


def get_row_by_id(travel_id):
    with open(r'C:\Users\chltm\PycharmProjects\djangoProject1\Django-registration-and-login-system\키워드.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['사이트주소'] == travel_id:
                return row
    return None


@login_required
def site_view(request, travel_id):
    # travel_id에 해당하는 행을 CSV 파일에서 가져옴
    row_data = get_row_by_id(travel_id)
    print(row_data)

    if row_data and '기간' in row_data:
        travel_duration = int(row_data['기간'].split('박')[0])  # '3박4일'에서 '3'을 추출하고 숫자로 변환
        travel_range = range(1, travel_duration + 1)
    else:
        travel_range = []
    # 가져온 데이터를 템플릿으로 전달
    return render(request, 'travel/site.html', {'travel_id': travel_id, 'row_data': row_data, 'travel_duration': travel_duration})


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
        companions = request.POST.get('companions')

        # TravelResponse 모델 업데이트
        travel_response.companions = companions

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
        travel_schedule = request.POST.get('travel_schedule')

        # TravelResponse 모델 업데이트
        travel_response.travel_schedule = travel_schedule

        # 업데이트된 모델 저장
        travel_response.save()

        return redirect('recommend')  # 저장 후 여행 폼으로 리디렉션


