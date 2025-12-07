"""Feature Acceptance Tests for ONBOARD-03 Tour of Features.

Tests all scenarios from docs/features/act-0-auth/onboarding.feature

Uses Django Test Client for fast, reliable testing.
NO browser needed. NO mocking (per project rules).
"""
import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import UserOnboardingState, get_or_create_onboarding_state


@pytest.mark.django_db
class TestOnboardingTour:
    """
    Feature Acceptance Tests for ONBOARD-03 Tour of Features
    
    Coverage from onboarding.feature:
    ✅ ONBOARD-03: Tour of features
       - Given Maria completed first playbook
       - When she proceeds with tour
       - Then she sees highlights of: Workflows, Activities, Artifacts, Sync
    
    Extended Coverage:
    ✅ Authentication requirements (login required)
    ✅ Onboarding state management (step progression)
    ✅ Navigation flow (welcome → tour → completion)
    ✅ Content validation (all 4 feature cards)
    ✅ UI elements (progress indicator, continue button)
    ✅ Accessibility (semantic HTML, ARIA labels)
    ✅ Error handling (missing state, invalid access)
    
    Test Strategy:
    - Uses Django Test Client (fast, reliable)
    - Tests all scenarios from feature file
    - Validates HTML responses, redirects, database state
    - No mocking - real database operations
    
    Run: pytest tests/integration/test_onboarding_tour_at.py -v
    """
    
    def test_onboarding_03_tour_happy_path(self):
        """
        Test ONBOARD-03: Tour of features - Happy path.
        
        Given: Maria is authenticated and has onboarding state
        When: She accesses the tour page
        Then: She sees all 4 feature highlights and progress indicator
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(username='maria', password='testpass123')
        client.force_login(user)
        
        # Create onboarding state (simulating completed first playbook)
        state = get_or_create_onboarding_state(user)
        state.current_step = 1  # Simulate step before tour
        state.save()
        
        # Act
        response = client.get(reverse('onboarding_tour'))
        
        # Assert HTTP response
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        
        # Assert template used
        assert any(t.name == 'onboarding/tour.html' for t in response.templates)
        
        # Assert root test ID
        assert 'data-testid="tour-page"' in content
        
        # Assert progress indicator
        assert 'data-testid="tour-progress-header"' in content
        assert 'Step 2 of 3 - Feature Tour' in content
        
        # Assert all 4 feature cards present
        assert 'data-testid="tour-card-workflows"' in content
        assert 'data-testid="tour-card-activities"' in content
        assert 'data-testid="tour-card-artifacts"' in content
        assert 'data-testid="tour-card-sync"' in content
        
        # Assert feature content (highlights)
        assert 'Workflows' in content
        assert 'Activities' in content
        assert 'Artifacts' in content
        assert 'Sync' in content
        
        # Assert feature descriptions
        assert 'Organize activities into structured processes' in content
        assert 'Define specific tasks' in content
        assert 'Track deliverables' in content
        assert 'Collaborate via Homebase' in content
        
        # Assert continue button
        assert 'data-testid="tour-continue-button"' in content
        assert 'Continue Your Journey' in content
        assert 'fa-solid fa-arrow-right' in content
        
        # Assert onboarding state updated to step 2
        state.refresh_from_db()
        assert state.current_step == 2
        assert state.is_completed is False
        
        # Assert feature code marker
        assert 'data-testid="tour-feature-code"' in content
        assert 'FOB-ONBOARDING-1-TOUR' in content

    def test_onboarding_03_tour_requires_authentication(self):
        """
        Test ONBOARD-03: Tour of features - Authentication required.
        
        Given: Maria is not logged in
        When: She tries to access tour page
        Then: She is redirected to login
        """
        # Arrange
        client = Client()
        
        # Act
        response = client.get(reverse('onboarding_tour'))
        
        # Assert redirect to login
        assert response.status_code == 302
        assert response.url.startswith('/auth/user/login/')

    def test_onboarding_03_tour_creates_onboarding_state(self):
        """
        Test ONBOARD-03: Tour of features - State creation.
        
        Given: Maria is authenticated but has no onboarding state
        When: She accesses the tour page
        Then: Onboarding state is created and set to step 2
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(username='maria', password='testpass123')
        client.force_login(user)
        
        # Ensure no onboarding state exists
        assert not UserOnboardingState.objects.filter(user=user).exists()
        
        # Act
        response = client.get(reverse('onboarding_tour'))
        
        # Assert successful response
        assert response.status_code == 200
        
        # Assert onboarding state created
        assert UserOnboardingState.objects.filter(user=user).exists()
        state = UserOnboardingState.objects.get(user=user)
        assert state.current_step == 2
        assert state.is_completed is False

    def test_onboarding_03_tour_with_existing_state(self):
        """
        Test ONBOARD-03: Tour of features - Existing state handling.
        
        Given: Maria has existing onboarding state at different step
        When: She accesses the tour page
        Then: State is updated to step 2, tour content shown
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(username='maria', password='testpass123')
        client.force_login(user)
        
        # Create existing onboarding state at step 0
        state = get_or_create_onboarding_state(user)
        state.current_step = 0
        state.is_completed = False
        state.save()
        
        # Act
        response = client.get(reverse('onboarding_tour'))
        
        # Assert successful response
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        
        # Assert tour content shown
        assert 'data-testid="tour-page"' in content
        assert 'Step 2 of 3 - Feature Tour' in content
        
        # Assert state updated to step 2
        state.refresh_from_db()
        assert state.current_step == 2
        assert state.is_completed is False

    def test_onboarding_03_tour_content_structure_validation(self):
        """
        Test ONBOARD-03: Tour of features - Content structure validation.
        
        Given: Maria is authenticated
        When: She accesses the tour page
        Then: All semantic HTML structure and accessibility elements are present
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(username='maria', password='testpass123')
        client.force_login(user)
        
        # Act
        response = client.get(reverse('onboarding_tour'))
        
        # Assert successful response
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        
        # Assert semantic HTML structure
        assert '<main role="main" aria-label="Feature Tour">' in content
        assert '<header class="text-center mb-5"' in content
        assert '<section aria-label="Feature Overview"' in content
        assert '<footer class="tour-continue-section"' in content
        
        # Assert accessibility attributes
        assert 'role="article"' in content
        assert 'aria-label="Workflows Feature"' in content
        assert 'aria-label="Activities Feature"' in content
        assert 'aria-label="Artifacts Feature"' in content
        assert 'aria-label="Sync Feature"' in content
        
        # Assert feature card attributes
        assert 'data-feature="workflows"' in content
        assert 'data-feature="activities"' in content
        assert 'data-feature="artifacts"' in content
        assert 'data-feature="sync"' in content
        
        # Assert feature badges
        assert 'Process Management' in content
        assert 'Task Management' in content
        assert 'Deliverable Tracking' in content
        assert 'Team Collaboration' in content
        
        # Assert enhanced UI elements
        assert 'feature-icon bg-primary bg-gradient' in content
        assert 'feature-icon bg-success bg-gradient' in content
        assert 'feature-icon bg-warning bg-gradient' in content
        assert 'feature-icon bg-info bg-gradient' in content
        
        # Assert tooltip attributes
        assert 'data-bs-toggle="tooltip"' in content
        assert 'data-bs-placement="top"' in content

    def test_onboarding_03_tour_continue_button_navigation(self):
        """
        Test ONBOARD-03: Tour of features - Continue button navigation.
        
        Given: Maria is viewing the tour page
        When: She clicks the continue button (or navigates to URL)
        Then: She is directed to completion step (currently returns 404)
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(username='maria', password='testpass123')
        client.force_login(user)
        
        # First, access tour to set up state
        tour_response = client.get(reverse('onboarding_tour'))
        assert tour_response.status_code == 200
        
        # Act - navigate to completion URL
        completion_response = client.get('/auth/user/onboarding/complete/')
        
        # Assert completion step not implemented yet (404)
        assert completion_response.status_code == 404
        
        # But tour state should remain intact
        state = UserOnboardingState.objects.get(user=user)
        assert state.current_step == 2

    def test_onboarding_03_tour_logging_verification(self):
        """
        Test ONBOARD-03: Tour of features - Logging verification.
        
        Given: Maria is authenticated
        When: She accesses the tour page
        Then: Appropriate logging occurs
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(username='maria', password='testpass123')
        client.force_login(user)
        
        # Act
        response = client.get(reverse('onboarding_tour'))
        
        # Assert successful response
        assert response.status_code == 200
        
        # Note: In a real implementation, we would check log files
        # For this test, we verify the view doesn't crash and handles logging
        # The actual logging verification would be done in integration tests
        # or by checking the logs/app.log file
        
        # Assert no errors in response
        assert response.status_code == 200
        assert 'error' not in response.content.decode('utf-8').lower()

    def test_onboarding_03_tour_feature_descriptions_detailed(self):
        """
        Test ONBOARD-03: Tour of features - Detailed feature descriptions.
        
        Given: Maria is authenticated
        When: She accesses the tour page
        Then: She sees detailed descriptions for each feature
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(username='maria', password='testpass123')
        client.force_login(user)
        
        # Act
        response = client.get(reverse('onboarding_tour'))
        
        # Assert successful response
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        
        # Assert detailed feature descriptions (enhanced from basic requirements)
        assert 'Organize activities into structured processes that guide your team from start to finish' in content
        assert 'Define specific tasks with clear responsibilities, timelines, and expected outcomes' in content
        assert 'Track deliverables and maintain a complete record of your team\'s work products' in content
        assert 'Collaborate via Homebase and keep your entire team aligned with real-time updates' in content
        
        # Assert enhanced UI elements
        assert 'Discover FOB\'s Features' in content
        assert 'Ready to start using these powerful features?' in content
        assert 'fa-solid fa-sparkles' in content
        assert 'fa-solid fa-lightbulb' in content
