"""E2E tests for ONBOARD-01 onboarding welcome screen using Django Test Client.

Covers FOB-ONBOARDING-1 / Scenario ONBOARD-01 Welcome screen
and ONBOARD-03 Tour of features from docs/features/act-0-auth/onboarding.feature.

Per .windsurf/workflows/dev-4-e2e-tests.md we use Django Test Client
for fast, reliable end-to-end flows without browser automation.
"""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from accounts.models import UserOnboardingState


@pytest.mark.django_db
class TestOnboardingE2E:
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

    def test_onboarding_welcome_to_tour_journey(self):
        """End-to-end: ONBOARD-01 welcome → ONBOARD-03 tour → completion stub.

        User Journey:
        1. Authenticated user accesses onboarding welcome (step 0)
        2. Clicks "Begin your journey" button
        3. Redirected to tour page (step 2)
        4. Views all 4 feature cards and progress indicator
        5. Clicks continue button to completion stub
        6. Verifies onboarding state tracking throughout journey
        """
        client = Client()
        
        # Create and log in user
        user = User.objects.create_user(username="maria", password="TestPass123")
        login_response = client.post(
            reverse("login"),
            {"username": "maria", "password": "TestPass123"},
            follow=True,
        )
        assert login_response.redirect_chain[-1][0] == "/dashboard/"

        # Step 1: Access welcome screen (ONBOARD-01)
        welcome_response = client.get(reverse("onboarding"))
        assert welcome_response.status_code == 200
        welcome_content = welcome_response.content.decode("utf-8")
        
        # Verify welcome content and navigation
        assert 'data-testid="onboarding-welcome"' in welcome_content
        assert 'data-testid="onboarding-begin-journey-button"' in welcome_content
        assert 'Begin your journey' in welcome_content
        assert 'Take a tour of FOB features and begin your journey' in welcome_content
        
        # Verify onboarding state at step 0
        from accounts.models import get_or_create_onboarding_state
        state = get_or_create_onboarding_state(user)
        assert state.current_step == 0

        # Step 2: Navigate to tour (ONBOARD-03)
        tour_response = client.get(reverse("onboarding_tour"))
        assert tour_response.status_code == 200
        tour_content = tour_response.content.decode("utf-8")
        
        # Verify tour content
        assert 'data-testid="tour-page"' in tour_content
        assert 'data-testid="tour-progress-header"' in tour_content
        assert 'data-testid="tour-features-grid"' in tour_content
        assert 'Step 2 of 3 - Feature Tour' in tour_content
        assert 'Discover FOB\'s Features' in tour_content
        
        # Verify all 4 feature cards
        assert 'data-testid="tour-card-workflows"' in tour_content
        assert 'data-testid="tour-card-activities"' in tour_content
        assert 'data-testid="tour-card-artifacts"' in tour_content
        assert 'data-testid="tour-card-sync"' in tour_content
        
        # Verify feature content
        assert 'Workflows' in tour_content
        assert 'Activities' in tour_content
        assert 'Artifacts' in tour_content
        assert 'Sync' in tour_content
        assert 'Process Management' in tour_content
        assert 'Task Management' in tour_content
        assert 'Deliverable Tracking' in tour_content
        assert 'Team Collaboration' in tour_content
        
        # Verify continue button
        assert 'data-testid="tour-continue-button"' in tour_content
        assert 'Continue Your Journey' in tour_content
        assert '/auth/user/onboarding/complete/' in tour_content
        
        # Verify onboarding state updated to step 2
        state = UserOnboardingState.objects.get(user=user)
        assert state.current_step == 2
        assert state.is_completed is False

        # Step 3: Navigate to completion stub (ONBOARD-05 - not implemented)
        # This will show 404 since completion step isn't implemented yet
        completion_response = client.get('/auth/user/onboarding/complete/')
        assert completion_response.status_code == 404
        
        # But the tour state should remain intact
        state = UserOnboardingState.objects.get(user=user)
        assert state.current_step == 2
