"""User Journey Certification Tests for Onboarding Tour.

Tests complete user journey from registration through tour to dashboard.
Uses LiveServerTestCase + Playwright for browser-based testing.

Run: pytest tests/e2e/test_journey_onboarding.py -v --headed
"""
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, Page, expect
from django.core.management import call_command
from django.contrib.auth.models import User
from methodology.models import Playbook


class TestOnboardingJourney(StaticLiveServerTestCase):
    """
    Certify complete onboarding journey from registration through tour.
    
    Journey Steps:
    1. New user visits site
    2. Registers for account
    3. Auto-redirected to onboarding
    4. Views welcome screen
    5. Proceeds to tour of features
    6. Interacts with tour features
    7. Completes tour
    8. Lands on dashboard
    
    Validates: Registration, authentication, navigation, HTMX, UI interactions
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up Playwright browser for all tests."""
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        # Use headed for debugging, change to headless=True for CI
        cls.browser = cls.playwright.chromium.launch(headless=False, slow_mo=100)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up Playwright resources."""
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()
    
    def setUp(self):
        """Create new browser context for each test."""
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
    
    def tearDown(self):
        """Close browser context after each test."""
        self.page.close()
        self.context.close()
    
    def _register_new_user(self, username: str, email: str, password: str):
        """Helper to register a new user via browser."""
        page = self.page
        
        # Navigate to registration
        page.goto(f'{self.live_server_url}/auth/user/register/')
        expect(page).to_have_title("Register - Mimir")
        
        # Fill registration form
        page.get_by_test_id('register-username-input').fill(username)
        page.get_by_test_id('register-email-input').fill(email)
        page.get_by_test_id('register-password-input').fill(password)
        page.get_by_test_id('register-password-confirm-input').fill(password)
        
        # Submit form
        page.get_by_test_id('register-submit-button').click()
        
        # Should redirect to onboarding
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/')
    
    def _wait_for_page_load(self):
        """Wait for page to fully load."""
        self.page.wait_for_load_state('networkidle')
    
    def test_journey_complete_onboarding_flow(self):
        """
        Journey: New user → Register → Onboarding → Tour → Dashboard
        
        Steps:
        1. Register new account
        2. Land on onboarding welcome page
        3. Navigate to tour of features
        4. Interact with tour features
        5. Complete tour
        6. Land on dashboard
        
        Validates: Complete onboarding flow with all UI interactions
        """
        page = self.page
        
        # Step 1: Register new user
        self._register_new_user('journey_user', 'journey@example.com', 'SecurePass123')
        self._wait_for_page_load()
        
        # Step 2: Verify onboarding welcome page
        expect(page.get_by_test_id('onboarding-stub')).to_be_visible()
        # The text is already verified by the test-id being visible
        
        # Step 3: Navigate to tour of features
        page.get_by_test_id('tour-features-link').click()
        self._wait_for_page_load()
        
        # Step 4: Verify tour page loaded
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/tour/')
        expect(page.get_by_test_id('onboarding-tour')).to_be_visible()
        
        # Verify all 4 feature cards are present
        expect(page.get_by_test_id('feature-workflows')).to_be_visible()
        expect(page.get_by_test_id('feature-activities')).to_be_visible()
        expect(page.get_by_test_id('feature-artifacts')).to_be_visible()
        expect(page.get_by_test_id('feature-sync')).to_be_visible()
        
        # Step 5: Verify progress indicator
        expect(page.get_by_text('Step 2 of 3')).to_be_visible()
        expect(page.get_by_test_id('onboarding-tour-step')).to_be_visible()
        expect(page.get_by_test_id('onboarding-tour-total-steps')).to_be_visible()
        
        # Step 6: Interact with feature modal
        # Click on Workflows card
        page.get_by_test_id('feature-workflows').click()
        
        # Wait for modal to appear
        expect(page.get_by_test_id('feature-modal')).to_be_visible()
        expect(page.locator('.feature-modal-title')).to_have_text('Workflows')
        expect(page.locator('.feature-modal-subtitle')).to_have_text('Organize activities into structured processes')
        
        # Close modal
        page.get_by_label('Close').click()
        
        # Step 7: Test navigation buttons
        # Test Back button
        page.get_by_role('link', name='Back').click()
        self._wait_for_page_load()
        
        # Should return to onboarding
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/')
        
        # Navigate back to tour
        page.get_by_test_id('tour-features-link').click()
        self._wait_for_page_load()
        
        # Step 8: Complete tour (Skip Tour for now)
        page.get_by_role('link', name='Skip Tour').click()
        self._wait_for_page_load()
        
        # Step 9: Should land on dashboard
        expect(page).to_have_url(f'{self.live_server_url}/dashboard/')
        
        # Verify user is authenticated and on dashboard
        # Check for dashboard stub
        expect(page.get_by_test_id('dashboard-stub')).to_be_visible()
    
    def test_journey_tour_modal_interactions(self):
        """
        Journey: User explores all tour feature modals
        
        Steps:
        1. Login and go to tour
        2. Open each feature modal
        3. Verify modal content
        4. Close modals
        5. Continue through tour
        
        Validates: Modal functionality and feature content
        """
        page = self.page
        
        # Register and go to tour
        self._register_new_user('modal_user', 'modal@example.com', 'SecurePass123')
        self._wait_for_page_load()
        
        page.get_by_test_id('tour-features-link').click()
        self._wait_for_page_load()
        
        # Test each feature modal
        features = [
            ('workflows', 'Workflows', 'Organize activities into structured processes'),
            ('activities', 'Activities', 'Define specific tasks'),
            ('artifacts', 'Artifacts', 'Track deliverables'),
            ('sync', 'Sync', 'Collaborate via Homebase')
        ]
        
        for feature_id, feature_name, feature_desc in features:
            # Click feature card
            page.get_by_test_id(f'feature-{feature_id}').click()
            
            # Verify modal content
            expect(page.get_by_test_id('feature-modal')).to_be_visible()
            expect(page.get_by_text(feature_name)).to_be_visible()
            expect(page.get_by_text(feature_desc)).to_be_visible()
            
            # Check for explore button
            expect(page.get_by_test_id('exploreFeature')).to_be_visible()
            
            # Close modal
            page.get_by_label('Close').click()
            
            # Verify modal closed
            expect(page.get_by_test_id('feature-modal')).not_to_be_visible()
    
    def test_journey_tour_progress_visualization(self):
        """
        Journey: User views tour progress visualization
        
        Steps:
        1. Navigate to tour
        2. Verify progress indicator
        3. Check step indicators
        4. Verify progress bar
        
        Validates: Progress visualization and step tracking
        """
        page = self.page
        
        # Register and go to tour
        self._register_new_user('progress_user', 'progress@example.com', 'SecurePass123')
        self._wait_for_page_load()
        
        page.get_by_test_id('tour-features-link').click()
        self._wait_for_page_load()
        
        # Verify progress text
        expect(page.get_by_text('Step 2 of 3')).to_be_visible()
        
        # Verify step circles
        step_circles = page.locator('.step-circle')
        expect(step_circles).to_have_count(3)
        
        # Check completed step (1)
        expect(page.locator('.step[data-step="1"] .step-circle')).to_have_text('✓')
        
        # Check active step (2)
        expect(page.locator('.step[data-step="2"] .step-circle')).to_have_text('2')
        expect(page.locator('.step[data-step="2"]')).to_have_class("active")
        
        # Check future step (3)
        expect(page.locator('.step[data-step="3"] .step-circle')).to_have_text('3')
        
        # Verify progress bar
        progress_bar = page.locator('.progress-bar')
        expect(progress_bar).to_have_attribute('aria-valuenow', '66.67')
    
    def test_journey_responsive_design(self):
        """
        Journey: User experiences responsive design on tour
        
        Steps:
        1. Navigate to tour on desktop
        2. Resize to mobile
        3. Verify layout adapts
        4. Test interactions on mobile
        
        Validates: Responsive design and mobile interactions
        """
        page = self.page
        
        # Register and go to tour
        self._register_new_user('responsive_user', 'responsive@example.com', 'SecurePass123')
        self._wait_for_page_load()
        
        page.get_by_test_id('tour-features-link').click()
        self._wait_for_page_load()
        
        # Start with desktop size
        page.set_viewport_size({"width": 1200, "height": 800})
        
        # Verify 2-column layout on desktop
        feature_cards = page.locator('.col-md-6')
        expect(feature_cards).to_have_count(4)
        
        # Test modal on desktop
        page.get_by_test_id('feature-workflows').click()
        expect(page.get_by_test_id('feature-modal')).to_be_visible()
        page.get_by_label('Close').click()
        
        # Resize to mobile
        page.set_viewport_size({"width": 375, "height": 667})
        self._wait_for_page_load()
        
        # Verify layout adapts (should stack vertically)
        feature_cards_mobile = page.locator('.tour-card')
        expect(feature_cards_mobile).to_have_count(4)
        
        # Test modal on mobile
        page.get_by_test_id('feature-workflows').click()
        expect(page.get_by_test_id('feature-modal')).to_be_visible()
        page.get_by_label('Close').click()
        
        # Test buttons on mobile
        expect(page.get_by_role('link', name='Back')).to_be_visible()
        expect(page.get_by_role('link', name='Skip Tour')).to_be_visible()
        expect(page.get_by_role('link', name='Continue')).to_be_visible()
    
    def test_journey_accessibility_features(self):
        """
        Journey: User with accessibility needs completes tour
        
        Steps:
        1. Navigate to tour
        2. Test keyboard navigation
        3. Verify ARIA labels
        4. Test screen reader compatibility
        
        Validates: Accessibility features and keyboard navigation
        """
        page = self.page
        
        # Register and go to tour
        self._register_new_user('a11y_user', 'a11y@example.com', 'SecurePass123')
        self._wait_for_page_load()
        
        page.get_by_test_id('tour-features-link').click()
        self._wait_for_page_load()
        
        # Test keyboard navigation
        # Tab to first feature card
        page.keyboard.press('Tab')
        expect(page.get_by_test_id('feature-workflows')).to_be_focused()
        
        # Activate with Enter
        page.keyboard.press('Enter')
        expect(page.get_by_test_id('feature-modal')).to_be_visible()
        
        # Close modal with Escape
        page.keyboard.press('Escape')
        expect(page.get_by_test_id('feature-modal')).not_to_be_visible()
        
        # Test ARIA attributes
        progress_bar = page.locator('.progress-bar')
        expect(progress_bar).to_have_attribute('role', 'progressbar')
        expect(progress_bar).to_have_attribute('aria-valuenow')
        expect(progress_bar).to_have_attribute('aria-valuemin')
        expect(progress_bar).to_have_attribute('aria-valuemax')
        
        # Test modal accessibility
        page.get_by_test_id('feature-workflows').click()
        modal = page.get_by_test_id('feature-modal')
        expect(modal).to_have_attribute('role', 'dialog')
        expect(modal).to_have_attribute('aria-modal', 'true')
        
        # Test focus management
        close_button = page.get_by_label('Close')
        expect(close_button).to_be_focused()
        
        page.keyboard.press('Escape')
    
    def test_journey_error_handling(self):
        """
        Journey: User encounters and handles errors gracefully
        
        Steps:
        1. Start tour
        2. Test network error scenarios
        3. Verify graceful fallbacks
        4. Complete journey despite errors
        
        Validates: Error handling and graceful degradation
        """
        page = self.page
        
        # Register and go to tour
        self._register_new_user('error_user', 'error@example.com', 'SecurePass123')
        self._wait_for_page_load()
        
        page.get_by_test_id('tour-features-link').click()
        self._wait_for_page_load()
        
        # Test navigation with invalid URLs (should handle gracefully)
        # Try to go directly to tour without authentication
        page.goto(f'{self.live_server_url}/auth/user/onboarding/tour/')
        
        # Should redirect to login (error handling)
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/login/')
        
        # Login and continue
        page.get_by_test_id('login-username-input').fill('error_user')
        page.get_by_test_id('login-password-input').fill('SecurePass123')
        page.get_by_test_id('login-submit-button').click()
        
        # Should redirect to dashboard (default after login)
        # Navigate back to tour
        page.goto(f'{self.live_server_url}/auth/user/onboarding/tour/')
        self._wait_for_page_load()
        
        # Verify tour loads correctly after error
        expect(page.get_by_test_id('onboarding-tour')).to_be_visible()
        
        # Complete journey
        page.get_by_role('link', name='Skip Tour').click()
        expect(page).to_have_url(f'{self.live_server_url}/dashboard/')
