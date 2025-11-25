"""URL configuration for accounts app."""
from django.urls import path
from .views import (
    login_view, 
    custom_logout_view, 
    onboarding, 
    register,
    password_reset_request,
    password_reset_confirm,
    skip_onboarding,
    TourView
)

# URL convention: /auth/user/{action}/
urlpatterns = [
    path('user/login/', login_view, name='login'),
    path('user/logout/', custom_logout_view, name='logout'),
    path('user/register/', register, name='register'),
    path('user/onboarding/', onboarding, name='onboarding'),
    path('user/onboarding/skip/', skip_onboarding, name='onboarding_skip'),
    path('user/onboarding/tour/', TourView.as_view(), name='onboarding_tour'),
    path('user/password-reset/', password_reset_request, name='password_reset'),
    path('user/password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]
