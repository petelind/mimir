from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestTourView(TestCase):
    """Test cases for TourView (ONBOARD-03)."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.tour_url = reverse('onboarding_tour')
    
    def test_tour_view_requires_authentication(self):
        """Test that tour view requires user to be logged in."""
        response = self.client.get(self.tour_url)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/user/login/', response.url)
    
    def test_tour_view_authenticated(self):
        """Test that authenticated user can access tour view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.tour_url)
        
        # Should return 200 and use correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/onboarding_tour.html')
    
    def test_tour_view_context_data(self):
        """Test that tour view provides correct context data."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.tour_url)
        
        # Check context contains expected data
        self.assertIn('features', response.context)
        self.assertIn('current_step', response.context)
        self.assertIn('total_steps', response.context)
        
        # Check step numbers
        self.assertEqual(response.context['current_step'], 2)
        self.assertEqual(response.context['total_steps'], 3)
    
    def test_tour_view_displays_all_feature_cards(self):
        """Test that all 4 feature cards are displayed."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.tour_url)
        
        # Check that response contains all feature highlights
        self.assertContains(response, 'Workflows')
        self.assertContains(response, 'Activities')
        self.assertContains(response, 'Artifacts')
        self.assertContains(response, 'Sync')
        
        # Check feature descriptions
        self.assertContains(response, 'Organize activities into structured processes')
        self.assertContains(response, 'Define specific tasks')
        self.assertContains(response, 'Track deliverables')
        self.assertContains(response, 'Collaborate via Homebase')
    
    def test_tour_view_progress_indicator(self):
        """Test that progress indicator shows correct step."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.tour_url)
        
        # Check progress indicator
        self.assertContains(response, 'Step 2 of 3')
    
    def test_tour_view_continue_button(self):
        """Test that continue button is present with correct attributes."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.tour_url)
        
        # Check continue button
        self.assertContains(response, 'Continue')
        self.assertContains(response, 'fa-solid fa-arrow-right')
        self.assertContains(response, 'data-bs-toggle="tooltip"')
        self.assertContains(response, 'title="Proceed to next step"')
    
    def test_tour_view_test_identifier(self):
        """Test that test identifier is present for automated testing."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.tour_url)
        
        # Check test identifier
        self.assertContains(response, 'data-testid="onboarding-tour"')
    
    def test_onboarding_links_to_tour(self):
        """Test that onboarding page contains link to tour."""
        self.client.login(username='testuser', password='testpass123')
        onboarding_url = reverse('onboarding')
        response = self.client.get(onboarding_url)
        
        # Check that onboarding page links to tour
        self.assertContains(response, reverse('onboarding_tour'))
        self.assertContains(response, 'Tour Features')
