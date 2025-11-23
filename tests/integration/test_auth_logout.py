"""Integration tests for user logout (AUTH-05).

Tests from docs/features/act-0-auth/authentication.feature

NO MOCKING per .windsurf/rules/do-not-mock-in-integration-tests.md
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestLogout:
    """Test AUTH-05: User logout."""
    
    def test_logout_clears_session_and_redirects_to_login(self):
        """
        Test logout clears session and redirects to login.
        
        Scenario: AUTH-05 Logout
        Given: Maria is authenticated
        When: she clicks [Logout]
        Then: she is logged out
        And: she is redirected to login page
        And: she sees "You have been logged out successfully" message
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(
            username='maria',
            password='TestPass123'
        )
        
        # Login first
        login_url = reverse('login')
        client.post(login_url, {
            'username': 'maria',
            'password': 'TestPass123',
        })
        
        # Verify user is logged in
        dashboard_response = client.get('/dashboard/')
        assert dashboard_response.wsgi_request.user.is_authenticated
        
        # Act - Logout
        logout_url = reverse('logout')
        response = client.post(logout_url, follow=True)
        
        # Assert - Redirected to login
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == '/auth/user/login/'
        
        # Assert - Success message present
        messages = list(response.context['messages'])
        assert len(messages) == 1
        assert 'logged out' in str(messages[0]).lower()
        assert messages[0].level_tag == 'success'
        
        # Assert - User is not authenticated
        assert not response.wsgi_request.user.is_authenticated
    
    def test_logout_when_not_authenticated_redirects_safely(self):
        """
        Test logout when not authenticated still redirects.
        
        Scenario: Logout without being logged in
        Given: User is not authenticated
        When: They access logout URL
        Then: Redirected to login without error
        """
        # Arrange
        client = Client()
        logout_url = reverse('logout')
        
        # Act
        response = client.post(logout_url, follow=True)
        
        # Assert - Redirected to login
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == '/auth/user/login/'
        
        # Assert - No crash, handled gracefully
        assert not response.wsgi_request.user.is_authenticated
    
    def test_logout_prevents_access_to_protected_pages(self):
        """
        Test that after logout, user cannot access protected pages.
        
        Scenario: Access protection after logout
        Given: Maria was logged in
        When: She logs out
        Then: She cannot access dashboard
        And: She is redirected to login page
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(
            username='maria',
            password='TestPass123'
        )
        
        # Login
        login_url = reverse('login')
        client.post(login_url, {
            'username': 'maria',
            'password': 'TestPass123',
        })
        
        # Logout
        logout_url = reverse('logout')
        client.post(logout_url)
        
        # Act - Try to access protected page
        dashboard_response = client.get('/dashboard/', follow=True)
        
        # Assert - Redirected to login (Django's @login_required behavior)
        assert dashboard_response.redirect_chain[-1][0].startswith('/auth/user/login/')
        assert not dashboard_response.wsgi_request.user.is_authenticated
    
    def test_logout_clears_remember_me_session(self):
        """
        Test logout clears session even with remember me.
        
        Scenario: Logout with remember me session
        Given: Maria logged in with remember me
        When: She logs out
        Then: Session is cleared
        And: She cannot access protected pages
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(
            username='maria',
            password='TestPass123'
        )
        
        # Login with remember me
        login_url = reverse('login')
        client.post(login_url, {
            'username': 'maria',
            'password': 'TestPass123',
            'remember_me': 'on',
        })
        
        # Verify session was set to 30 days
        assert client.session.get_expiry_age() == 2592000
        
        # Act - Logout
        logout_url = reverse('logout')
        client.post(logout_url)
        
        # Assert - User is not authenticated
        dashboard_response = client.get('/dashboard/')
        assert not dashboard_response.wsgi_request.user.is_authenticated
    
    def test_logout_link_visible_when_authenticated(self):
        """
        Test logout link/button is visible when user is authenticated.
        
        This test will be expanded when navigation is implemented.
        For now, verify logout URL exists.
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(
            username='maria',
            password='TestPass123'
        )
        
        # Login
        login_url = reverse('login')
        client.post(login_url, {
            'username': 'maria',
            'password': 'TestPass123',
        })
        
        # Act - Get dashboard (or any authenticated page)
        response = client.get('/dashboard/')
        
        # Assert - User is authenticated
        assert response.wsgi_request.user.is_authenticated
        
        # Note: Logout link will be in navigation when implemented
        # For now, just verify logout URL is accessible
        logout_url = reverse('logout')
        assert logout_url == '/auth/user/logout/'
