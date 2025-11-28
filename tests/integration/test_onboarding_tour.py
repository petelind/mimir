"""Integration tests for onboarding tour view and functionality.

Covers FOB-ONBOARDING-1 / Scenario ONBOARD-03 Tour of features
for the /auth/user/onboarding/tour/ entrypoint.

NO MOCKING per integration test rules.
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from accounts.models import UserOnboardingState, get_or_create_onboarding_state


@pytest.mark.django_db
class TestOnboardingTourView:
    """Integration tests for onboarding tour view."""

    def test_authenticated_user_sees_tour_page(self):
        """Authenticated user should see ONBOARD-03 tour page with all feature cards."""
        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        response = client.get(reverse("onboarding_tour"))

        assert response.status_code == 200
        # Correct template
        assert any(
            t.name == "onboarding/tour.html" for t in response.templates
        ), "onboarding/tour.html should be used for tour view"

        content = response.content.decode("utf-8")
        # Root test id for ONBOARD-03
        assert 'data-testid="tour-page"' in content
        # Enhanced progress header
        assert 'data-testid="tour-progress-header"' in content
        assert 'data-testid="tour-progress-indicator"' in content
        assert 'data-testid="tour-header"' in content
        assert 'data-testid="tour-features-grid"' in content
        assert "Step 2 of 3 - Feature Tour" in content
        assert "Discover FOB's Features" in content
        # All 4 feature cards with enhanced structure
        assert 'data-testid="tour-card-workflows"' in content
        assert 'data-testid="tour-card-activities"' in content
        assert 'data-testid="tour-card-artifacts"' in content
        assert 'data-testid="tour-card-sync"' in content
        # Feature card attributes
        assert 'data-feature="workflows"' in content
        assert 'data-feature="activities"' in content
        assert 'data-feature="artifacts"' in content
        assert 'data-feature="sync"' in content
        # Enhanced feature content
        assert "Workflows" in content
        assert "Activities" in content
        assert "Artifacts" in content
        assert "Sync" in content
        assert "Organize activities into structured processes that guide your team from start to finish" in content
        assert "Define specific tasks with clear responsibilities, timelines, and expected outcomes" in content
        assert "Track deliverables and maintain a complete record of your team's work products" in content
        assert "Collaborate via Homebase and keep your entire team aligned with real-time updates" in content
        # Feature badges
        assert "Process Management" in content
        assert "Task Management" in content
        assert "Deliverable Tracking" in content
        assert "Team Collaboration" in content
        # Enhanced continue section
        assert 'data-testid="tour-continue-section"' in content
        assert 'data-testid="tour-continue-button"' in content
        assert "Continue Your Journey" in content
        assert "Ready to start using these powerful features?" in content
        # Feature code marker
        assert 'data-testid="tour-feature-code"' in content
        assert "FOB-ONBOARDING-1-TOUR" in content
        # Accessibility attributes
        assert 'role="main"' in content
        assert 'aria-label="Feature Tour"' in content
        assert 'role="article"' in content
        assert 'aria-label="Workflows Feature"' in content

    def test_anonymous_user_is_redirected_to_login(self):
        """Anonymous user should be redirected to login when accessing tour."""
        client = Client()

        response = client.get(reverse("onboarding_tour"))

        assert response.status_code == 302
        assert response.url.startswith("/auth/user/login/")

    def test_tour_access_updates_onboarding_state_to_step_2(self):
        """Accessing tour should update onboarding state to current_step=2."""
        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        # Create initial onboarding state
        initial_state = get_or_create_onboarding_state(user)
        assert initial_state.current_step == 0  # Default initial step

        response = client.get(reverse("onboarding_tour"))

        assert response.status_code == 200
        
        # Check that state was updated to step 2
        updated_state = UserOnboardingState.objects.get(user=user)
        assert updated_state.current_step == 2

    def test_tour_display_with_existing_onboarding_state(self):
        """Tour should display correctly even with existing onboarding state."""
        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        # Set up existing onboarding state
        state = get_or_create_onboarding_state(user)
        state.current_step = 1
        state.save()

        response = client.get(reverse("onboarding_tour"))

        assert response.status_code == 200
        content = response.content.decode("utf-8")
        
        # Should still show all tour content
        assert 'data-testid="tour-page"' in content
        assert 'data-testid="tour-progress-indicator"' in content
        assert 'data-testid="tour-card-workflows"' in content
        
        # State should be updated to step 2
        updated_state = UserOnboardingState.objects.get(user=user)
        assert updated_state.current_step == 2

    def test_tour_view_logs_access(self):
        """Tour view should log access at appropriate level."""
        # This test would require log capture setup
        # For now, just ensure the view doesn't crash
        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        response = client.get(reverse("onboarding_tour"))
        
        assert response.status_code == 200
        # Logging verification would require log capture infrastructure


@pytest.mark.django_db  
class TestTourViewFunctionality:
    """Additional tests for tour view edge cases and behavior."""

    def test_tour_view_handles_missing_onboarding_state(self):
        """Tour should handle case where onboarding state doesn't exist."""
        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com", 
            password="SecurePass123",
        )
        client.force_login(user)

        # Delete any existing onboarding state
        UserOnboardingState.objects.filter(user=user).delete()

        response = client.get(reverse("onboarding_tour"))

        assert response.status_code == 200
        # Should create new state and set to step 2
        state = UserOnboardingState.objects.get(user=user)
        assert state.current_step == 2

    def test_tour_page_content_structure(self):
        """Verify tour page has proper HTML structure and accessibility."""
        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        response = client.get(reverse("onboarding_tour"))
        
        assert response.status_code == 200
        content = response.content.decode("utf-8")
        
        # Check for proper semantic structure (enhanced template)
        assert '<h1 class="display-4 fw-bold mb-3">' in content  # Enhanced header
        assert '<div class="card feature-card h-100"' in content  # Enhanced feature cards
        assert '<div class="card-body text-center p-4">' in content  # Enhanced padding
        assert '<main role="main" aria-label="Feature Tour">' in content  # Semantic main
        assert '<header class="text-center mb-5"' in content  # Semantic header
        assert '<section aria-label="Feature Overview"' in content  # Semantic section
        assert '<footer class="tour-continue-section"' in content  # Semantic footer
        
        # Check for icons (Font Awesome) - same icons but enhanced structure
        assert 'fa-solid fa-sitemap' in content  # Workflows
        assert 'fa-solid fa-tasks' in content    # Activities
        assert 'fa-solid fa-folder-open' in content  # Artifacts
        assert 'fa-solid fa-sync' in content     # Sync
        assert 'fa-solid fa-arrow-right' in content  # Continue button
        assert 'fa-solid fa-sparkles' in content  # Enhanced header icon
        assert 'fa-solid fa-lightbulb' in content  # Enhanced footer icon
        
        # Check for enhanced feature structure
        assert 'feature-icon bg-primary bg-gradient' in content
        assert 'feature-icon bg-success bg-gradient' in content
        assert 'feature-icon bg-warning bg-gradient' in content
        assert 'feature-icon bg-info bg-gradient' in content

    def test_tour_continue_button_has_tooltip(self):
        """Continue button should have proper tooltip attributes."""
        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        response = client.get(reverse("onboarding_tour"))
        
        assert response.status_code == 200
        content = response.content.decode("utf-8")
        
        # Check for enhanced tooltip attributes
        continue_button = 'data-testid="tour-continue-button"'
        assert continue_button in content
        assert 'data-bs-toggle="tooltip"' in content
        assert 'data-bs-placement="top"' in content  # Enhanced placement
        assert 'aria-label="Continue to next onboarding step"' in content  # Enhanced accessibility
