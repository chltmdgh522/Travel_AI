

from django.urls import path
from .views import home, profile, RegisterView, robby_view


urlpatterns = [
    path('home', home, name='users-home'),
    path('', robby_view, name='users-robby'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]
