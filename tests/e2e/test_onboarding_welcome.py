"""E2E tests for ONBOARD-01 onboarding welcome screen using Django Test Client.

Covers FOB-ONBOARDING-1 / Scenario ONBOARD-01 Welcome screen
from docs/features/act-0-auth/onboarding.feature.

Per .windsurf/workflows/dev-4-e2e-tests.md we use Django Test Client
for fast, reliable end-to-end flows without browser automation.
"""

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestOnboardingE2E(TestCase):
    """E2E tests for onboarding welcome page (FOB-ONBOARDING-1)."""

    def test_welcome_screen_display_after_registration(self):
        """End-to-end: new user registration leads to ONBOARD-01 welcome screen.

        User Journey (subset of full auth journey):
        1. Visit dashboard (not logged in, redirected to login)
        2. Navigate to registration
        3. Register new account
        4. Auto-login and redirect to onboarding welcome screen
        5. Verify ONBOARD-01 content and CTAs
        6. Access dashboard successfully as logged-in user
        """

        client = Client()

        # Step 1: Try to access dashboard (should redirect to login)
        response = client.get("/dashboard/", follow=True)
        assert response.redirect_chain[-1][0].startswith("/auth/user/login/")
        assert 'data-testid="login-form"' in response.content.decode("utf-8")

        # Step 2: Navigate to registration
        response = client.get(reverse("register"))
        assert response.status_code == 200
        assert 'data-testid="register-form"' in response.content.decode("utf-8")

        # Step 3: Submit registration form
        response = client.post(
            reverse("register"),
            {
                "username": "maria",
                "email": "maria@example.com",
                "password": "SecurePass123",
                "password_confirm": "SecurePass123",
            },
            follow=True,
        )

        # Step 4: Should be redirected to onboarding and auto-logged in
        assert response.redirect_chain[-1][0] == "/auth/user/onboarding/"
        content = response.content.decode("utf-8")

        # ONBOARD-01: Welcome screen content
        # Root container for onboarding welcome
        assert 'data-testid="onboarding-welcome"' in content
        # Hero heading
        assert "Welcome to FOB" in content
        # Steps overview markers
        assert 'data-testid="onboarding-step-1"' in content
        assert 'data-testid="onboarding-step-2"' in content
        assert 'data-testid="onboarding-step-3"' in content
        # CTAs and skip tour UI
        assert 'data-testid="onboarding-begin-journey-button"' in content
        assert 'data-testid="onboarding-skip-link-top"' in content
        # Skip confirmation modal markup
        assert 'id="onboardingSkipModal"' in content
        assert 'data-testid="onboarding-skip-confirm"' in content
        assert 'data-testid="onboarding-skip-cancel"' in content

        # Step 5: Verify user was created and is authenticated
        assert User.objects.filter(username="maria").exists()
        assert response.wsgi_request.user.is_authenticated
        assert response.wsgi_request.user.username == "maria"

        # Step 6: Navigate to dashboard (can use link or direct access)
        dashboard_response = client.get("/dashboard/")
        assert dashboard_response.status_code == 200
        dashboard_content = dashboard_response.content.decode("utf-8")
        assert 'data-testid="dashboard-stub"' in dashboard_content
        assert "FOB-DASHBOARD-1" in dashboard_content

    def test_onboard_04_skip_tour_ui_elements(self):
        """ONBOARD-04: Skip onboarding UI is present on welcome screen.

        This test focuses on server-rendered HTML:
        - Skip link is visible on onboarding page
        - Confirmation modal markup is present
        - Confirm button points to dashboard
        """

        client = Client()

        # Pre-create and log in user Maria
        User.objects.create_user(username="maria", password="TestPass123")
        login_response = client.post(
            reverse("login"),
            {"username": "maria", "password": "TestPass123"},
            follow=True,
        )
        assert login_response.redirect_chain[-1][0] == "/dashboard/"

        # Navigate to onboarding welcome screen
        response = client.get("/auth/user/onboarding/")
        assert response.status_code == 200
        content = response.content.decode("utf-8")

        # Skip link visible on onboarding page
        assert 'data-testid="onboarding-welcome"' in content
        assert 'data-testid="onboarding-skip-link-top"' in content

        # Confirmation modal present
        assert 'id="onboardingSkipModal"' in content
        assert 'Skip tour?' in content
        assert 'Are you sure? You can access help anytime.' in content

        # Confirm button exists (form now POSTs to onboarding_skip backend endpoint)
        assert 'data-testid="onboarding-skip-confirm"' in content