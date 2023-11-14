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
        # 만약 객체가 없다면, 새로운 객체를 생성
        travel_response = TravelResponse.objects.create(user=request.user)

    if request.method == 'POST':
        # 폼 데이터 가져오기
        country = request.POST.get('country')
        duration = request.POST.get('duration')
        companions = request.POST.get('companions')
        travel_style = request.POST.get('travel_style')
        travel_schedule = request.POST.get('travel_schedule')

        # TravelResponse 모델 업데이트
        travel_response.country = country
        travel_response.duration = duration
        travel_response.companions = companions
        travel_response.travel_style = travel_style
        travel_response.travel_schedule = travel_schedule

        # 업데이트된 모델 저장
        travel_response.save()

        return redirect('recommend')

    return render(request, 'travel/travel.html', {'travel_response': travel_response})
@login_required
def recommend_view(request):
    try:
        travel_response = TravelResponse.objects.get(user=request.user)  # 관련 이름이 'travelresponse'인 경우
    except TravelResponse.DoesNotExist:
        # 사용자에 대한 TravelResponse가 없는 경우 처리
        travel_response = None
    csv_file_path = r'C:\Users\chltm\PycharmProjects\djangoProject1\Django-registration-and-login-system\통합 문서1.csv'
    os.chdir(r"C:\Users\chltm\PycharmProjects\djangoProject1\Django-registration-and-login-system")
    selected_rows = []

    # CSV 파일 읽기
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        # CSV 파일의 각 행에 대해 반복
        for row in csv_reader:
            # print(f"Comparing: {row.get('나라')} with {travel_response.country}")
            # 특정 조건을 만족하는 경우 해당 행을 선택
            if '나라' in row and row['나라'] == travel_response.country:
                if '기간' in row and row['기간'] == travel_response.duration:
                    print("gd")
                    selected_rows.append(row)

    return render(request, 'travel/recommend.html',
                  {'travel_response': travel_response, 'selected_rows': selected_rows})

@login_required
def plan_view(request):
    return render(request, 'travel/plan.html')


@login_required
def save_response(request):
    if request.method == 'POST':
        # 사용자에 대한 TravelResponse 인스턴스를 가져오거나 생성
        travel_response, created = TravelResponse.objects.get_or_create(user=request.user)

        # 폼 데이터 가져오기
        country = request.POST.get('country')
        duration = request.POST.get('duration')
        companions = request.POST.get('companions')
        travel_style = request.POST.get('travel_style')
        travel_schedule = request.POST.get('travel_schedule')

        # TravelResponse 모델 업데이트
        travel_response.country = country
        travel_response.duration = duration
        travel_response.companions = companions
        travel_response.travel_style = travel_style
        travel_response.travel_schedule = travel_schedule

        # 업데이트된 모델 저장
        travel_response.save()

        return redirect('/')  # 저장 후 여행 폼으로 리디렉션

    # POST 요청이 아니면 다른 처리 또는 에러 핸들링이 필요할 수 있습니다.
    return redirect('travel')  # 일단은 여행 폼으로 리디렉션


def get_row_by_id(travel_id):
    with open(r'C:\Users\chltm\PycharmProjects\djangoProject1\Django-registration-and-login-system\통합 문서1.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['주소'] == travel_id:
                return row
    return None


@login_required
def site_view(request, travel_id):
    # travel_id에 해당하는 행을 CSV 파일에서 가져옴
    row_data = get_row_by_id(travel_id)

    # 가져온 데이터를 템플릿으로 전달
    return render(request, 'travel/site.html', {'travel_id': travel_id, 'row_data': row_data})


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
