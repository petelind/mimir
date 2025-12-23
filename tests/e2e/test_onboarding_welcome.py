"""E2E tests for onboarding welcome page.

Tests the first-time user experience after registration.

IMPORTANT: These tests run in SYNC mode (not async) to avoid
pytest-asyncio conflicts with Django ORM operations.
"""
import pytest
from playwright.sync_api import Page


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestOnboardingWelcomeE2E:
    """End-to-end tests for onboarding welcome page."""
    
    def test_unauthenticated_user_redirected_to_login(self, page: Page, live_server_url: str):
        """
        Test E2E-ONBOARD-02: Unauthenticated access redirects to login.
        
        Given: User is not authenticated
        When: User tries to access a protected page
        Then: User is redirected to login page
        """
        # Try to access dashboard without authentication
        page.goto(f"{live_server_url}/dashboard/")
        
        # Wait for redirect
        page.wait_for_load_state('networkidle')
        
        # Should be redirected to login with next parameter
        assert '/auth/user/login/' in page.url
        assert 'next=' in page.url or page.url.endswith('/auth/user/login/')
