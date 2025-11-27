"""Integration tests for onboarding welcome screen and skip behavior.

Covers FOB-ONBOARDING-1 / Scenario ONBOARD-01 Welcome screen
for the /auth/user/onboarding/ entrypoint.

NO MOCKING per integration test rules.
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from accounts.models import UserOnboardingState


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
        # Steps overview markers
        assert 'data-testid="onboarding-step-1"' in content
        assert 'data-testid="onboarding-step-2"' in content
        assert 'data-testid="onboarding-step-3"' in content
        # CTAs and Skip Tour UI (ONBOARD-04)
        assert 'data-testid="onboarding-begin-journey-button"' in content
        assert 'data-testid="onboarding-skip-link-top"' in content
        # Skip confirmation modal markup
        assert 'id="onboardingSkipModal"' in content
        assert 'data-testid="onboarding-skip-confirm"' in content
        assert 'data-testid="onboarding-skip-cancel"' in content

    def test_anonymous_user_is_redirected_to_login(self):
        """Anonymous user should be redirected to login when accessing onboarding."""
        client = Client()

        response = client.get(reverse("onboarding"))

        assert response.status_code == 302
        assert response.url.startswith("/auth/user/login/")

    def test_skip_onboarding_marks_completed_and_redirects_to_dashboard(self):
        """ONBOARD-04: Skip onboarding marks state completed and redirects.

        Given Maria is in onboarding
        When she confirms Skip Tour
        Then onboarding is marked complete and she is redirected to dashboard.
        """

        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        # Act: POST to skip endpoint
        response = client.post(reverse("onboarding_skip"), follow=False)

        # Assert redirect to dashboard
        assert response.status_code == 302
        assert response.url == "/dashboard/"

        # Assert onboarding state in database
        state = UserOnboardingState.objects.get(user=user)
        assert state.is_completed is True
        assert state.current_step == 0
        assert state.completed_at is not None
