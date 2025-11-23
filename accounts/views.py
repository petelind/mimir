"""Authentication views for user login and logout."""
import logging
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


def _validate_login_data(username, password):
    """
    Validate login form data.
    
    Internal helper for login_view.
    
    :param username: str - Username from form. Example: "maria"
    :param password: str - Password from form. Example: "test123"
    :return: dict - Validation errors. Example: {"username": ["This field is required."]}
    
    Validation Rules:
        - Username: Required, non-empty
        - Password: Required, non-empty
    """
    errors = {}
    
    if not username:
        errors['username'] = ['This field is required.']
        logger.debug("Validation error: Username is empty")
    
    if not password:
        errors['password'] = ['This field is required.']
        logger.debug("Validation error: Password is empty")
    
    return errors


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login view - skeleton only."""
    raise NotImplementedError("Login view pending")


def custom_logout_view(request):
    """Custom logout view with success message."""
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, "You have been logged out successfully")
        logger.info(f"User {username} logged out successfully")
    else:
        logger.warning("Logout attempted by unauthenticated user")
    
    return redirect(reverse('login'))
