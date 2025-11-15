"""Authentication views for user login and logout."""
import logging
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    """Custom login view with remember me checkbox support."""
    
    template_name = "accounts/login.html"
    
    def form_valid(self, form):
        """Handle valid login form submission."""
        remember_me = self.request.POST.get('remember_me', False)
        
        logger.info(f"Login attempt for user: {form.get_user().username}, remember_me: {remember_me}")
        
        response = super().form_valid(form)
        
        if remember_me:
            self.request.session.set_expiry(2592000)  # 30 days
            logger.info(f"User {form.get_user().username} logged in with remember me (30 days)")
        else:
            self.request.session.set_expiry(1209600)  # 2 weeks
            logger.info(f"User {form.get_user().username} logged in without remember me (2 weeks)")
        
        return response


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
