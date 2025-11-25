"""Integration tests for ONBOARD-01 onboarding welcome screen.

Covers FOB-ONBOARDING-1 / Scenario ONBOARD-01 Welcome screen
for the /auth/user/onboarding/ entrypoint.

NO MOCKING per integration test rules.
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestOnboardingWelcomeView:
    """Integration tests for onboarding welcome view."""

    def test_authenticated_user_sees_onboarding_welcome(self):
        """Authenticated user should see ONBOARD-01 welcome screen."""
        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        response = client.get(reverse("onboarding"))

        assert response.status_code == 200
        # Correct template
        assert any(
            t.name == "onboarding/welcome.html" for t in response.templates
        ), "onboarding/welcome.html should be used for onboarding view"

        content = response.content.decode("utf-8")
        # Root test id for ONBOARD-01
        assert 'data-testid="onboarding-welcome"' in content
        # Hero copy
        assert "Welcome to FOB" in content
        # Steps overview markers (will be implemented in template step)
        assert 'data-testid="onboarding-step-1"' in content
        assert 'data-testid="onboarding-step-2"' in content
        assert 'data-testid="onboarding-step-3"' in content
        # CTAs
        assert 'data-testid="onboarding-begin-journey-button"' in content
        assert 'data-testid="onboarding-skip-button"' in content

    def test_anonymous_user_is_redirected_to_login(self):
        """Anonymous user should be redirected to login when accessing onboarding."""
        client = Client()

        response = client.get(reverse("onboarding"))

        assert response.status_code == 302
        assert response.url.startswith("/auth/user/login/")
