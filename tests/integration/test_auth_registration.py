"""Integration tests for user registration (AUTH-03).

Tests from docs/features/act-0-auth/authentication.feature

NO MOCKING per .windsurf/rules/do-not-mock-in-integration-tests.md
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestUserRegistration:
    """Test AUTH-03: First-time user registration."""
    
    def test_register_new_user_redirects_to_onboarding(self):
        """
        Test successful registration redirects to onboarding.
        
        Scenario: AUTH-03 First-time user registration
        Given: Maria is on the FOB registration page
        When: she enters username, email, and password
        And: she clicks [Create Account]
        Then: account is created
        And: she is auto-logged in
        And: she is redirected to FOB-ONBOARDING-1
        """
        # Arrange
        client = Client()
        register_url = reverse('register')
        
        # Act
        response = client.post(register_url, {
            'username': 'maria',
            'email': 'maria@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
        }, follow=False)
        
        # Assert - Should redirect to onboarding
        assert response.status_code == 302, f"Expected 302 redirect, got {response.status_code}"
        assert response.url == '/auth/user/onboarding/', f"Expected redirect to onboarding, got {response.url}"
        
        # Assert - User should be created
        assert User.objects.filter(username='maria').exists(), "User should be created in database"
        user = User.objects.get(username='maria')
        assert user.email == 'maria@example.com', "Email should be saved"
        
        # Assert - User should be auto-logged in
        response_after = client.get('/auth/user/onboarding/')
        assert response_after.wsgi_request.user.is_authenticated, "User should be auto-logged in"
        assert response_after.wsgi_request.user.username == 'maria', "Logged in user should be maria"
    
    def test_register_with_duplicate_username_shows_error(self):
        """
        Test registration with existing username shows error.
        
        Scenario: Duplicate username
        Given: User "maria" already exists
        When: New user tries to register with username "maria"
        Then: Error message shown: "This username is already taken"
        """
        # Arrange
        client = Client()
        User.objects.create_user(username='maria', password='Existing123')
        register_url = reverse('register')
        
        # Act
        response = client.post(register_url, {
            'username': 'maria',
            'email': 'new@example.com',
            'password': 'NewPass123',
            'password_confirm': 'NewPass123',
        })
        
        # Assert - Should stay on page
        assert response.status_code == 200
        
        # Assert - Should show error
        content = response.content.decode('utf-8')
        assert 'already taken' in content.lower() or 'exists' in content.lower()
        
        # Assert - User not authenticated
        assert not response.wsgi_request.user.is_authenticated
    
    def test_register_with_duplicate_email_shows_error(self):
        """
        Test registration with existing email shows error.
        
        Scenario: Duplicate email
        Given: Email "maria@example.com" already registered
        When: New user tries to register with same email
        Then: Error message shown
        """
        # Arrange
        client = Client()
        User.objects.create_user(
            username='existing',
            email='maria@example.com',
            password='Existing123'
        )
        register_url = reverse('register')
        
        # Act
        response = client.post(register_url, {
            'username': 'newuser',
            'email': 'maria@example.com',
            'password': 'NewPass123',
            'password_confirm': 'NewPass123',
        })
        
        # Assert
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'already' in content.lower() or 'registered' in content.lower()
    
    def test_register_with_password_mismatch_shows_error(self):
        """
        Test registration with mismatched passwords shows error.
        
        Scenario: Password mismatch
        Given: User on registration page
        When: Password and confirm password don't match
        Then: Error message: "Passwords do not match"
        """
        # Arrange
        client = Client()
        register_url = reverse('register')
        
        # Act
        response = client.post(register_url, {
            'username': 'maria',
            'email': 'maria@example.com',
            'password': 'Password123',
            'password_confirm': 'DifferentPass123',
        })
        
        # Assert
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'do not match' in content.lower() or 'match' in content.lower()
        
        # Assert - User not created
        assert not User.objects.filter(username='maria').exists()
    
    def test_register_with_short_password_shows_error(self):
        """
        Test registration with password < 8 chars shows error.
        
        Scenario: Password too short
        Given: User on registration page
        When: Password is less than 8 characters
        Then: Error message shown
        """
        # Arrange
        client = Client()
        register_url = reverse('register')
        
        # Act
        response = client.post(register_url, {
            'username': 'maria',
            'email': 'maria@example.com',
            'password': 'short',
            'password_confirm': 'short',
        })
        
        # Assert
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert '8 characters' in content.lower() or 'too short' in content.lower()
        
        # Assert - User not created
        assert not User.objects.filter(username='maria').exists()
    
    def test_register_with_invalid_email_shows_error(self):
        """
        Test registration with invalid email format shows error.
        
        Scenario: Invalid email
        Given: User on registration page
        When: Email format is invalid (no @ or no domain)
        Then: Error message shown
        """
        # Arrange
        client = Client()
        register_url = reverse('register')
        
        # Act
        response = client.post(register_url, {
            'username': 'maria',
            'email': 'invalid-email',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
        })
        
        # Assert
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'valid email' in content.lower() or 'email' in content.lower()
    
    def test_register_with_short_username_shows_error(self):
        """
        Test registration with username < 3 chars shows error.
        
        Scenario: Username too short
        Given: User on registration page
        When: Username is less than 3 characters
        Then: Error message shown
        """
        # Arrange
        client = Client()
        register_url = reverse('register')
        
        # Act
        response = client.post(register_url, {
            'username': 'ab',
            'email': 'maria@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
        })
        
        # Assert
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert '3' in content or 'between' in content.lower()
    
    def test_get_register_page_displays_form(self):
        """
        Test GET request to register shows form.
        
        Scenario: User visits registration page
        Given: User navigates to registration URL
        Then: Registration form is displayed with all fields
        """
        # Arrange
        client = Client()
        register_url = reverse('register')
        
        # Act
        response = client.get(register_url)
        
        # Assert
        assert response.status_code == 200
        assert response.templates[0].name == 'accounts/register.html'
        content = response.content.decode('utf-8')
        assert 'username' in content.lower()
        assert 'email' in content.lower()
        assert 'password' in content.lower()
        assert 'data-testid="register-form"' in content
    
    def test_registration_link_visible_on_login_page(self):
        """
        Test that registration link is visible on login page.
        
        Scenario: User on login page
        Then: "Sign Up" or "Create Account" link is visible
        """
        # Arrange
        client = Client()
        login_url = reverse('login')
        
        # Act
        response = client.get(login_url)
        
        # Assert
        content = response.content.decode('utf-8')
        assert 'register' in content.lower() or 'sign up' in content.lower()
