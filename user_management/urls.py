from django.contrib import admin

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from users.views import (CustomLoginView, ResetPasswordView, ChangePasswordView, travel_view, robby_view,
                         recommend_view,site_view,
                         plan_view1,save_plan1
                         ,plan_view2,save_plan2,plan_view3,save_plan3,plan_view4,save_plan4,plan_view5,save_plan5)
from users.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('users.urls')),
    path('', robby_view, name='users-home'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    re_path(r'^oauth/', include('social_django.urls', namespace='social')),

    path('travel', travel_view, name='travel'),

    path('recommend', recommend_view, name='recommend'),


    path('recommend/<str:travel_id>/', site_view, name='site'),

    path('travel/plan1', plan_view1, name='plan1'),
    path('save1', save_plan1, name='save_plan1'),

    path('travel/plan2', plan_view2, name='plan2'),
    path('save2',save_plan2, name='save_plan2'),

    path('travel/plan3', plan_view3, name='plan3'),
    path('save3', save_plan3, name='save_plan3'),

    path('travel/plan4', plan_view4, name='plan4'),
    path('save4', save_plan4, name='save_plan4'),

    path('travel/plan5', plan_view5, name='plan5'),
    path('save5', save_plan5, name='save_plan5'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
