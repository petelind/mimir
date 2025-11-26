"""E2E tests for authentication user journeys using Django Test Client.

Tests complete flows from authentication.feature using Django's Test Client.
Faster, more reliable, and better Django integration than browser-based tests.

Per updated .windsurf/workflows/dev-4-e2e-tests.md
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.core import mail
import re


@pytest.mark.django_db
class TestAuthenticationE2E:
    """E2E tests for complete authentication user journeys."""
    
    def test_e2e_new_user_registration_to_dashboard(self):
        """
        E2E: Complete new user journey from registration to dashboard.
        
        User Journey:
        1. Visit dashboard (not logged in, redirected to login)
        2. Click "Sign Up" link
        3. Register new account
        4. Auto-logged in and redirected to onboarding
        5. Click "Skip to Dashboard"
        6. See dashboard content
        """
        client = Client()
        
        # Step 1: Try to access dashboard (should redirect to login)
        response = client.get('/dashboard/', follow=True)
        assert response.redirect_chain[-1][0].startswith('/auth/user/login/')
        assert 'data-testid="login-form"' in response.content.decode('utf-8')
        
        # Step 2: Navigate to registration
        response = client.get(reverse('register'))
        assert response.status_code == 200
        assert 'data-testid="register-form"' in response.content.decode('utf-8')
        
        # Step 3: Submit registration form
        response = client.post(reverse('register'), {
            'username': 'maria',
            'email': 'maria@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
        }, follow=True)
        
        # Step 4: Should be redirected to onboarding and auto-logged in
        assert response.redirect_chain[-1][0] == '/auth/user/onboarding/'
        content = response.content.decode('utf-8')
        assert 'data-testid="onboarding-welcome"' in content
        assert 'FOB-ONBOARDING-1' in content
        
        # Verify user was created and is authenticated
        assert User.objects.filter(username='maria').exists()
        assert response.wsgi_request.user.is_authenticated
        assert response.wsgi_request.user.username == 'maria'
        
        # Step 5 & 6: Navigate to dashboard (can use link or direct access)
        dashboard_response = client.get('/dashboard/')
        assert dashboard_response.status_code == 200
        dashboard_content = dashboard_response.content.decode('utf-8')
        assert 'data-testid="dashboard-stub"' in dashboard_content
        assert 'FOB-DASHBOARD-1' in dashboard_content
    
    def test_e2e_login_with_invalid_then_valid_credentials(self):
        """
        E2E: User tries invalid credentials, then logs in successfully.
        
        User Journey:
        1. Visit login page
        2. Enter wrong password
        3. See error message, form preserved
        4. Enter correct password
        5. Redirected to dashboard
        """
        client = Client()
        
        # Setup: Create test user
        User.objects.create_user(username='maria', password='CorrectPass123')
        
        # Step 1: Go to login
        response = client.get(reverse('login'))
        assert response.status_code == 200
        assert 'data-testid="login-form"' in response.content.decode('utf-8')
        
        # Step 2 & 3: Enter wrong password and see error
        response = client.post(reverse('login'), {
            'username': 'maria',
            'password': 'WrongPassword',
        })
        
        assert response.status_code == 200  # Stays on page
        content = response.content.decode('utf-8')
        assert 'data-testid="login-error-message"' in content
        assert 'Invalid' in content or 'invalid' in content
        # Username should be preserved
        assert 'value="maria"' in content
        
        # Step 4 & 5: Enter correct password and get redirected
        response = client.post(reverse('login'), {
            'username': 'maria',
            'password': 'CorrectPass123',
        }, follow=True)
        
        assert response.redirect_chain[-1][0] == '/dashboard/'
        assert response.wsgi_request.user.is_authenticated
        assert response.wsgi_request.user.username == 'maria'
    
    def test_e2e_password_reset_complete_flow(self):
        """
        E2E: Complete password reset flow.
        
        User Journey:
        1. Navigate from login to password reset
        2. Submit email for reset
        3. See success message
        4. Extract reset link from email
        5. Set new password
        6. Login with new password successfully
        """
        client = Client()
        
        # Setup: Create test user
        user = User.objects.create_user(
            username='maria',
            email='maria@example.com',
            password='OldPass123'
        )
        
        # Step 1: Go to login, find forgot password link
        login_response = client.get(reverse('login'))
        content = login_response.content.decode('utf-8')
        assert 'Forgot password' in content or 'forgot' in content.lower()
        
        # Navigate to password reset
        reset_response = client.get(reverse('password_reset'))
        assert reset_response.status_code == 200
        assert 'data-testid="password-reset-form"' in reset_response.content.decode('utf-8')
        
        # Step 2 & 3: Submit email and see success
        response = client.post(reverse('password_reset'), {
            'email': 'maria@example.com',
        })
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="reset-success-message"' in content
        assert 'sent' in content.lower() or 'email' in content.lower()
        
        # Step 4: Extract reset link from email
        assert len(mail.outbox) == 1
        email_body = mail.outbox[0].body
        match = re.search(r'/auth/user/password-reset-confirm/([^/]+)/([^/\s]+)/', email_body)
        assert match, "Reset link should be in email"
        uidb64, token = match.groups()
        
        # Step 5: Use reset link to set new password
        confirm_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        
        # GET the confirm page
        confirm_response = client.get(confirm_url)
        assert confirm_response.status_code == 200
        confirm_content = confirm_response.content.decode('utf-8')
        assert 'data-testid="new-password-input"' in confirm_content
        
        # POST new password
        response = client.post(confirm_url, {
            'password': 'NewPass456',
            'password_confirm': 'NewPass456',
        })
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="reset-complete-message"' in content
        assert 'success' in content.lower()
        
        # Step 6: Login with new password
        login_response = client.post(reverse('login'), {
            'username': 'maria',
            'password': 'NewPass456',
        }, follow=True)
        
        assert login_response.redirect_chain[-1][0] == '/dashboard/'
        assert login_response.wsgi_request.user.is_authenticated
        
        # Verify old password doesn't work
        client2 = Client()
        old_login = client2.post(reverse('login'), {
            'username': 'maria',
            'password': 'OldPass123',
        })
        assert old_login.status_code == 200  # Stays on page (error)
        assert not old_login.wsgi_request.user.is_authenticated
    
    def test_e2e_logout_and_cannot_access_dashboard(self):
        """
        E2E: User logs in, logs out, cannot access protected page.
        
        User Journey:
        1. Login successfully
        2. Access dashboard (works)
        3. Logout
        4. Try to access dashboard again
        5. Redirected to login
        """
        client = Client()
        
        # Setup: Create user
        User.objects.create_user(username='maria', password='TestPass123')
        
        # Step 1: Login
        login_response = client.post(reverse('login'), {
            'username': 'maria',
            'password': 'TestPass123',
        }, follow=True)
        
        assert login_response.redirect_chain[-1][0] == '/dashboard/'
        
        # Step 2: Access dashboard successfully
        dashboard_response = client.get('/dashboard/')
        assert dashboard_response.status_code == 200
        assert 'FOB-DASHBOARD-1' in dashboard_response.content.decode('utf-8')
        
        # Step 3: Logout
        logout_response = client.post(reverse('logout'), follow=True)
        assert logout_response.redirect_chain[-1][0] == '/auth/user/login/'
        
        # Verify logout message
        messages = list(logout_response.context['messages'])
        assert len(messages) == 1
        assert 'logged out' in str(messages[0]).lower()
        
        # Step 4 & 5: Try to access dashboard, get redirected
        dashboard_attempt = client.get('/dashboard/', follow=True)
        assert dashboard_attempt.redirect_chain[-1][0].startswith('/auth/user/login/')
        assert not dashboard_attempt.wsgi_request.user.is_authenticated
    
    def test_e2e_registration_validation_errors(self):
        """
        E2E: Registration form shows validation errors and recovers.
        
        User Journey:
        1. Go to registration
        2. Submit with mismatched passwords
        3. See error message
        4. Form fields preserved (except passwords)
        5. Fix error and submit successfully
        """
        client = Client()
        
        # Step 1: Go to registration
        response = client.get(reverse('register'))
        assert response.status_code == 200
        
        # Step 2 & 3: Submit with mismatched passwords
        response = client.post(reverse('register'), {
            'username': 'maria',
            'email': 'maria@example.com',
            'password': 'Pass123456',
            'password_confirm': 'DifferentPass',
        })
        
        assert response.status_code == 200  # Stays on page
        content = response.content.decode('utf-8')
        
        # Step 3: See validation error
        assert 'data-testid="password-confirm-field-error"' in content
        assert 'do not match' in content.lower() or 'match' in content.lower()
        
        # Step 4: Verify fields preserved (username and email)
        assert 'value="maria"' in content
        assert 'value="maria@example.com"' in content
        
        # Step 5: Fix and submit successfully
        response = client.post(reverse('register'), {
            'username': 'maria',
            'email': 'maria@example.com',
            'password': 'Pass123456',
            'password_confirm': 'Pass123456',
        }, follow=True)
        
        assert response.redirect_chain[-1][0] == '/auth/user/onboarding/'
        assert User.objects.filter(username='maria').exists()
        assert response.wsgi_request.user.is_authenticated
