"""E2E tests for authentication user journeys.

Tests complete flows from authentication.feature using Playwright.
Uses Django LiveServerTestCase + Playwright for full browser testing.

Per .windsurf/rules/do-e2e-tests.md and AUTH_IMPLEMENTATION_PLAN.md
"""
import pytest
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, Page, expect
import re


@pytest.mark.django_db
class TestAuthenticationE2E(StaticLiveServerTestCase):
    """E2E tests for complete authentication user journeys."""
    
    @classmethod
    def setUpClass(cls):
        """Set up Playwright browser for all tests."""
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up Playwright resources."""
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()
    
    def setUp(self):
        """Create new browser context for each test."""
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
    
    def tearDown(self):
        """Close browser context after each test."""
        self.page.close()
        self.context.close()
    
    def test_e2e_new_user_registration_to_dashboard(self):
        """
        E2E: Complete new user journey from registration to dashboard.
        
        User Journey:
        1. Visit site (redirected to login)
        2. Click "Sign Up"
        3. Register new account
        4. Auto-logged in
        5. Redirected to onboarding
        6. Skip to dashboard
        7. See dashboard content
        """
        page = self.page
        
        # Step 1: Visit dashboard (not logged in, should redirect to login)
        page.goto(f'{self.live_server_url}/dashboard/')
        expect(page).to_have_url(re.compile(r'.*/auth/user/login/.*'))
        
        # Step 2: Click Sign Up link
        page.click('text=Sign Up')
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/register/')
        
        # Step 3: Fill registration form
        page.fill('[data-testid="register-username-input"]', 'maria')
        page.fill('[data-testid="register-email-input"]', 'maria@example.com')
        page.fill('[data-testid="register-password-input"]', 'SecurePass123')
        page.fill('[data-testid="register-password-confirm-input"]', 'SecurePass123')
        
        # Step 4: Submit registration
        page.click('[data-testid="register-submit-button"]')
        
        # Step 5: Should be redirected to onboarding
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/')
        expect(page.locator('[data-testid="onboarding-stub"]')).to_be_visible()
        
        # Step 6: Click Skip to Dashboard
        page.click('text=Skip to Dashboard')
        
        # Step 7: Should see dashboard
        expect(page).to_have_url(f'{self.live_server_url}/dashboard/')
        expect(page.locator('[data-testid="dashboard-stub"]')).to_be_visible()
        expect(page.locator('text=FOB-DASHBOARD-1')).to_be_visible()
    
    def test_e2e_login_with_invalid_then_valid_credentials(self):
        """
        E2E: User tries invalid credentials, then logs in successfully.
        
        User Journey:
        1. Visit login page
        2. Enter wrong password
        3. See error message
        4. Enter correct password
        5. Redirected to dashboard
        """
        page = self.page
        
        # Setup: Create test user
        User.objects.create_user(username='maria', password='CorrectPass123')
        
        # Step 1: Go to login
        page.goto(f'{self.live_server_url}/auth/user/login/')
        
        # Step 2: Enter wrong password
        page.fill('[data-testid="login-username-input"]', 'maria')
        page.fill('[data-testid="login-password-input"]', 'WrongPassword')
        page.click('[data-testid="login-submit-button"]')
        
        # Step 3: Should see error
        expect(page.locator('[data-testid="login-error-message"]')).to_be_visible()
        expect(page.locator('text=Invalid')).to_be_visible()
        
        # Step 4: Enter correct password
        page.fill('[data-testid="login-password-input"]', 'CorrectPass123')
        page.click('[data-testid="login-submit-button"]')
        
        # Step 5: Should be on dashboard
        expect(page).to_have_url(f'{self.live_server_url}/dashboard/')
    
    def test_e2e_password_reset_complete_flow(self):
        """
        E2E: Complete password reset flow.
        
        User Journey:
        1. Click "Forgot password?" on login
        2. Enter email
        3. See success message
        4. Extract reset link from email (simulated)
        5. Set new password
        6. Login with new password
        """
        page = self.page
        
        # Setup: Create test user
        user = User.objects.create_user(
            username='maria',
            email='maria@example.com',
            password='OldPass123'
        )
        
        # Step 1: Go to login and click Forgot password
        page.goto(f'{self.live_server_url}/auth/user/login/')
        page.click('text=Forgot password?')
        
        # Step 2: Enter email for reset
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/password-reset/')
        page.fill('[data-testid="reset-email-input"]', 'maria@example.com')
        page.click('[data-testid="reset-submit-button"]')
        
        # Step 3: See success message
        expect(page.locator('[data-testid="reset-success-message"]')).to_be_visible()
        
        # Step 4: Simulate getting reset link
        # In real scenario, would extract from email
        # For E2E test, we'll directly construct the URL using session data
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # Note: In production, use proper token generator
        # For this E2E test, we'll use a test token
        import secrets
        token = secrets.token_urlsafe(32)
        
        # Store in session (simulating what the view does)
        from django.contrib.sessions.backends.db import SessionStore
        session = SessionStore()
        session[f'password_reset_{uid}'] = {
            'token': token,
            'user_id': user.pk,
            'timestamp': 'test'
        }
        session.save()
        
        # Step 5: Visit reset confirmation page
        reset_confirm_url = f'{self.live_server_url}/auth/user/password-reset-confirm/{uid}/{token}/'
        
        # Need to set session cookie for the token to work
        # This is a limitation of the test - in real usage, user clicks email link
        page.goto(f'{self.live_server_url}/auth/user/login/')  # Get session
        page.context.add_cookies([{
            'name': 'sessionid',
            'value': session.session_key,
            'url': self.live_server_url
        }])
        
        page.goto(reset_confirm_url)
        
        # Should see password form
        expect(page.locator('[data-testid="new-password-input"]')).to_be_visible()
        
        # Set new password
        page.fill('[data-testid="new-password-input"]', 'NewPass456')
        page.fill('[data-testid="new-password-confirm-input"]', 'NewPass456')
        page.click('[data-testid="reset-confirm-submit-button"]')
        
        # Step 6: See success and login with new password
        expect(page.locator('[data-testid="reset-complete-message"]')).to_be_visible()
        page.click('text=Sign In')
        
        # Login with new password
        page.fill('[data-testid="login-username-input"]', 'maria')
        page.fill('[data-testid="login-password-input"]', 'NewPass456')
        page.click('[data-testid="login-submit-button"]')
        
        # Should reach dashboard
        expect(page).to_have_url(f'{self.live_server_url}/dashboard/')
    
    def test_e2e_logout_and_cannot_access_dashboard(self):
        """
        E2E: User logs in, logs out, cannot access protected page.
        
        User Journey:
        1. Login
        2. Visit dashboard (accessible)
        3. Logout (when navigation implemented)
        4. Try to access dashboard
        5. Redirected to login
        """
        page = self.page
        
        # Setup: Create user
        User.objects.create_user(username='maria', password='TestPass123')
        
        # Step 1: Login
        page.goto(f'{self.live_server_url}/auth/user/login/')
        page.fill('[data-testid="login-username-input"]', 'maria')
        page.fill('[data-testid="login-password-input"]', 'TestPass123')
        page.click('[data-testid="login-submit-button"]')
        
        # Step 2: On dashboard
        expect(page).to_have_url(f'{self.live_server_url}/dashboard/')
        
        # Step 3: Logout (directly visit logout URL since no nav yet)
        page.goto(f'{self.live_server_url}/auth/user/logout/')
        
        # Should be redirected to login with success message
        expect(page).to_have_url(re.compile(r'.*/auth/user/login/.*'))
        
        # Step 4: Try to access dashboard again
        page.goto(f'{self.live_server_url}/dashboard/')
        
        # Step 5: Should be redirected to login
        expect(page).to_have_url(re.compile(r'.*/auth/user/login/.*'))
    
    def test_e2e_registration_validation_errors(self):
        """
        E2E: Registration form shows validation errors.
        
        User Journey:
        1. Go to registration
        2. Submit with mismatched passwords
        3. See error
        4. Fix and submit successfully
        """
        page = self.page
        
        # Step 1: Go to registration
        page.goto(f'{self.live_server_url}/auth/user/register/')
        
        # Step 2: Fill with mismatched passwords
        page.fill('[data-testid="register-username-input"]', 'maria')
        page.fill('[data-testid="register-email-input"]', 'maria@example.com')
        page.fill('[data-testid="register-password-input"]', 'Pass123456')
        page.fill('[data-testid="register-password-confirm-input"]', 'DifferentPass')
        page.click('[data-testid="register-submit-button"]')
        
        # Step 3: See validation error
        expect(page.locator('[data-testid="password-confirm-field-error"]')).to_be_visible()
        expect(page.locator('text=do not match')).to_be_visible()
        
        # Step 4: Fix and submit
        page.fill('[data-testid="register-password-confirm-input"]', 'Pass123456')
        page.click('[data-testid="register-submit-button"]')
        
        # Should succeed and go to onboarding
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/')
