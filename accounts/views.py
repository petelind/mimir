"""Authentication views for user login and logout."""
import logging
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
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


def _handle_remember_me(request, remember_me):
    """
    Configure session expiry based on remember me checkbox.
    
    Internal helper for login_view.
    
    :param request: Django request object with authenticated user
    :param remember_me: bool - Remember me checkbox state. Example: True  
    :return: None
    
    Side Effects:
        - Sets request.session.set_expiry(2592000) if remember_me=True (30 days)
        - Sets request.session.set_expiry(1209600) if remember_me=False (2 weeks)
    """
    if remember_me:
        request.session.set_expiry(2592000)  # 30 days
        logger.info(f"User {request.user.username} logged in with remember me (30 days session)")
    else:
        request.session.set_expiry(1209600)  # 2 weeks  
        logger.info(f"User {request.user.username} logged in without remember me (2 weeks session)")


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Display login form and handle authentication.
    
    Custom implementation without Django Forms per SAO.md architecture.
    
    Template: accounts/login.html
    Context:
        errors: dict - Field-specific and non-field errors
        username: str - Preserved username on error
    
    :param request: Django request object
    :return: Rendered login template or redirect to dashboard
    """
    logger.info(f"Login page accessed via {request.method}")
    
    # GET request - display form
    if request.method == 'GET':
        logger.info("Displaying login form")
        return render(request, 'accounts/login.html', {
            'errors': {},
            'username': ''
        })
    
    # POST request - handle login
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    remember_me = request.POST.get('remember_me') == 'on'
    
    logger.info(f"Login attempt for username: {username}, remember_me: {remember_me}")
    
    # Validate input
    errors = _validate_login_data(username, password)
    if errors:
        logger.warning(f"Login validation failed for username: {username}, errors: {list(errors.keys())}")
        return render(request, 'accounts/login.html', {
            'errors': errors,
            'username': username
        })
    
    # Authenticate
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # Successful authentication
        auth_login(request, user)
        logger.info(f"User {username} authenticated successfully")
        
        # Handle remember me
        _handle_remember_me(request, remember_me)
        
        # Redirect to dashboard
        logger.info(f"Redirecting user {username} to dashboard")
        return redirect('/dashboard/')
    else:
        # Authentication failed
        logger.warning(f"Authentication failed for username: {username}")
        errors = {
            '__all__': ['Invalid username or password. Please try again.']
        }
        return render(request, 'accounts/login.html', {
            'errors': errors,
            'username': username
        })


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


@login_required
def onboarding(request):
    """
    Onboarding stub page (FOB-ONBOARDING-1).
    
    Placeholder view for first-time user onboarding. Full implementation
    tracked separately in onboarding.feature issues #12-16.
    
    Template: accounts/onboarding.html
    Context: None
    
    :param request: Django request object
    :return: Rendered onboarding stub template
    """
    logger.info(f"User {request.user.username} accessed onboarding stub")
    return render(request, 'accounts/onboarding.html')
