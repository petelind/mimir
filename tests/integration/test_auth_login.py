"""Integration tests for user authentication login scenarios.

Tests AUTH-01 (valid credentials) and AUTH-02 (invalid credentials) from
docs/features/act-0-auth/authentication.feature

NO MOCKING per .windsurf/rules/do-not-mock-in-integration-tests.md
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestLoginValidCredentials:
    """Test AUTH-01: Login with valid credentials."""
    
    def test_login_with_valid_credentials_redirects_to_dashboard(self):
        """
        Test successful login redirects to dashboard.
        
        Scenario: AUTH-01 Login with valid credentials
        Given: Maria is on the FOB login page
        When: she enters valid email and password
        And: she clicks [Login]
        Then: she is authenticated
        And: she is redirected to FOB-DASHBOARD-1
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(
            username='maria',
            email='maria@example.com',
            password='ValidPass123'
        )
        login_url = reverse('login')
        
        # Act
        response = client.post(login_url, {
            'username': 'maria',
            'password': 'ValidPass123',
        }, follow=False)
        
        # Assert - Should redirect to dashboard
        assert response.status_code == 302, f"Expected 302 redirect, got {response.status_code}"
        assert response.url == '/dashboard/', f"Expected redirect to /dashboard/, got {response.url}"
        
        # Assert - User should be authenticated
        # Check by making authenticated request
        response_after = client.get('/dashboard/')
        assert response_after.wsgi_request.user.is_authenticated, "User should be authenticated after login"
        assert response_after.wsgi_request.user.username == 'maria', "Logged in user should be maria"
    
    def test_login_with_remember_me_sets_long_session(self):
        """
        Test remember me checkbox sets 30-day session.
        
        Scenario: AUTH-01 with remember me
        Given: Maria is on login page
        When: she enters valid credentials
        And: she checks remember me
        Then: session expires in 30 days (2592000 seconds)
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(
            username='maria',
            password='ValidPass123'
        )
        login_url = reverse('login')
        
        # Act
        response = client.post(login_url, {
            'username': 'maria',
            'password': 'ValidPass123',
            'remember_me': 'on',  # Checkbox checked
        })
        
        # Assert - Session should be 30 days
        session_expiry = client.session.get_expiry_age()
        assert session_expiry == 2592000, f"Expected 30-day session (2592000s), got {session_expiry}s"
    
    def test_login_without_remember_me_sets_default_session(self):
        """
        Test login without remember me sets 2-week session.
        
        Scenario: AUTH-01 without remember me
        Given: Maria is on login page  
        When: she enters valid credentials
        And: she does NOT check remember me
        Then: session expires in 2 weeks (1209600 seconds)
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(
            username='maria',
            password='ValidPass123'
        )
        login_url = reverse('login')
        
        # Act - No remember_me in POST data
        response = client.post(login_url, {
            'username': 'maria',
            'password': 'ValidPass123',
        })
        
        # Assert - Session should be 2 weeks
        session_expiry = client.session.get_expiry_age()
        assert session_expiry == 1209600, f"Expected 2-week session (1209600s), got {session_expiry}s"


@pytest.mark.django_db
class TestLoginInvalidCredentials:
    """Test AUTH-02: Login with invalid credentials."""
    
    def test_login_with_wrong_password_shows_error(self):
        """
        Test login with incorrect password displays error.
        
        Scenario: AUTH-02 Login with invalid credentials
        Given: Maria is on the FOB login page
        When: she enters invalid credentials
        And: she clicks [Login]
        Then: she sees "Invalid email or password" error
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(
            username='maria',
            password='CorrectPass123'
        )
        login_url = reverse('login')
        
        # Act - Wrong password
        response = client.post(login_url, {
            'username': 'maria',
            'password': 'WrongPassword',
        })
        
        # Assert - Should stay on login page (200)
        assert response.status_code == 200, f"Expected 200 (stay on page), got {response.status_code}"
        
        # Assert - Should show error message
        content = response.content.decode('utf-8')
        assert 'Invalid' in content or 'invalid' in content, "Error message should contain 'Invalid'"
        
        # Assert - User should NOT be authenticated
        assert not response.wsgi_request.user.is_authenticated, "User should not be authenticated with wrong password"
    
    def test_login_with_nonexistent_username_shows_error(self):
        """
        Test login with non-existent username displays error.
        
        Scenario: AUTH-02 with non-existent user
        Given: Maria is on login page
        When: she enters username that doesn't exist
        Then: she sees error (same as wrong password for security)
        """
        # Arrange
        client = Client()
        login_url = reverse('login')
        
        # Act - Non-existent username
        response = client.post(login_url, {
            'username': 'nonexistent',
            'password': 'SomePassword123',
        })
        
        # Assert - Should stay on login page
        assert response.status_code == 200
        
        # Assert - Should show error
        content = response.content.decode('utf-8')
        assert 'Invalid' in content or 'invalid' in content
        
        # Assert - User not authenticated
        assert not response.wsgi_request.user.is_authenticated
    
    def test_login_with_empty_username_shows_validation_error(self):
        """
        Test login with empty username shows field validation.
        
        Scenario: AUTH-02 with empty username
        Given: Maria is on login page
        When: she leaves username empty
        Then: she sees "This field is required" error
        """
        # Arrange
        client = Client()
        login_url = reverse('login')
        
        # Act - Empty username
        response = client.post(login_url, {
            'username': '',
            'password': 'SomePassword',
        })
        
        # Assert
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'required' in content.lower() or 'empty' in content.lower()
    
    def test_login_with_empty_password_shows_validation_error(self):
        """
        Test login with empty password shows field validation.
        
        Scenario: AUTH-02 with empty password
        Given: Maria is on login page
        When: she leaves password empty
        Then: she sees "This field is required" error
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(username='maria', password='Pass123')
        login_url = reverse('login')
        
        # Act - Empty password
        response = client.post(login_url, {
            'username': 'maria',
            'password': '',
        })
        
        # Assert
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'required' in content.lower() or 'empty' in content.lower()
    
    def test_get_login_page_displays_form(self):
        """
        Test GET request to login shows form.
        
        Scenario: User visits login page
        Given: Maria navigates to login URL
        Then: she sees login form with username and password fields
        """
        # Arrange
        client = Client()
        login_url = reverse('login')
        
        # Act
        response = client.get(login_url)
        
        # Assert
        assert response.status_code == 200
        assert response.templates[0].name == 'accounts/login.html'
        content = response.content.decode('utf-8')
        assert 'username' in content.lower()
        assert 'password' in content.lower()
        assert 'data-testid="login-form"' in content
