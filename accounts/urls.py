"""URL configuration for accounts app."""
from django.urls import path
from .views import CustomLoginView, custom_logout_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),
]
