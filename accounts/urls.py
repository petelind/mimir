"""URL configuration for accounts app."""
from django.urls import path
from .views import login_view, custom_logout_view, onboarding

# URL convention: /auth/user/{action}/
urlpatterns = [
    path('user/login/', login_view, name='login'),
    path('user/logout/', custom_logout_view, name='logout'),
    path('user/onboarding/', onboarding, name='onboarding'),
]
