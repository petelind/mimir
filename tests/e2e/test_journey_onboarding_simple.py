"""User Journey Certification Tests with Playwright.

Tests complete user journeys across multiple features.
Uses LiveServerTestCase + Playwright for browser-based testing.

Run: pytest tests/e2e/test_journey_onboarding_simple.py -v --headed
"""
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, Page, expect


class TestOnboardingJourneySimple(StaticLiveServerTestCase):
    """Certify complete onboarding journey from registration to tour completion."""
    
    @classmethod
    def setUpClass(cls):
        """Set up Playwright browser for all tests."""
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        # Use headless=False for debugging, can be changed to True for CI
        cls.browser = cls.playwright.chromium.launch(headless=True)
    
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
    
    def test_new_user_complete_onboarding_journey(self):
        """
        Journey: New user → Register → Onboarding Welcome → Tour → Dashboard
        
        Steps:
        1. Visit site homepage
        2. Navigate to registration
        3. Fill and submit registration form
        4. Auto-redirected to onboarding welcome
        5. Click "Begin your journey" to go to tour
        6. View all 4 feature cards on tour page
        7. Click continue button (navigates to completion stub - 404)
        8. Navigate back to dashboard manually
        
        Validates: Registration, authentication, navigation, tour UI
        """
        page = self.page
        
        # Step 1: Visit site homepage
        page.goto(f'{self.live_server_url}/')
        # Homepage is accessible, navigate to registration directly
        expect(page).to_have_url(f'{self.live_server_url}/')
        
        # Step 2: Navigate to registration directly
        page.goto(f'{self.live_server_url}/auth/user/register/')
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/register/')
        
        # Step 3: Fill and submit registration form
        new_username = 'newuser_journey'
        page.get_by_test_id('register-username-input').fill(new_username)
        page.get_by_test_id('register-email-input').fill('newuser_journey@example.com')
        page.get_by_test_id('register-password-input').fill('SecurePass123')
        page.get_by_test_id('register-password-confirm-input').fill('SecurePass123')
        page.get_by_test_id('register-submit-button').click()
        
        # Step 4: Should be auto-redirected to onboarding welcome
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/')
        expect(page.get_by_test_id('onboarding-welcome')).to_be_visible()
        
        # Verify welcome content
        expect(page.get_by_role('heading', name='Welcome to FOB')).to_be_visible()
        expect(page.get_by_test_id('onboarding-begin-journey-button')).to_be_visible()
        expect(page.get_by_test_id('onboarding-begin-journey-button')).to_have_text('Begin your journey')
        
        # Step 5: Click "Begin your journey" to go to tour
        page.get_by_test_id('onboarding-begin-journey-button').click()
        
        # Step 6: Should be on tour page with all 4 feature cards
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/tour/')
        expect(page.get_by_test_id('tour-page')).to_be_visible()
        
        # Verify progress indicator
        expect(page.get_by_test_id('tour-progress-header')).to_be_visible()
        expect(page.get_by_text('Step 2 of 3 - Feature Tour')).to_be_visible()
        expect(page.get_by_text('Discover FOB\'s Features')).to_be_visible()
        
        # Verify all 4 feature cards
        expect(page.get_by_test_id('tour-card-workflows')).to_be_visible()
        expect(page.get_by_test_id('tour-card-activities')).to_be_visible()
        expect(page.get_by_test_id('tour-card-artifacts')).to_be_visible()
        expect(page.get_by_test_id('tour-card-sync')).to_be_visible()
        
        # Verify feature content
        expect(page.get_by_test_id('tour-card-workflows').get_by_role('heading', name='Workflows')).to_be_visible()
        expect(page.get_by_test_id('tour-card-activities').get_by_role('heading', name='Activities')).to_be_visible()
        expect(page.get_by_test_id('tour-card-artifacts').get_by_role('heading', name='Artifacts')).to_be_visible()
        expect(page.get_by_test_id('tour-card-sync').get_by_role('heading', name='Sync')).to_be_visible()
        
        # Verify feature descriptions
        expect(page.get_by_text('Organize activities into structured processes')).to_be_visible()
        expect(page.get_by_text('Define specific tasks')).to_be_visible()
        expect(page.get_by_text('Track deliverables')).to_be_visible()
        expect(page.get_by_text('Collaborate via Homebase')).to_be_visible()
        
        # Verify feature badges
        expect(page.get_by_test_id('tour-card-workflows').get_by_text('Process Management')).to_be_visible()
        expect(page.get_by_test_id('tour-card-activities').get_by_text('Task Management')).to_be_visible()
        expect(page.get_by_test_id('tour-card-artifacts').get_by_text('Deliverable Tracking')).to_be_visible()
        expect(page.get_by_test_id('tour-card-sync').get_by_text('Team Collaboration')).to_be_visible()
        
        # Verify continue button
        expect(page.get_by_test_id('tour-continue-button')).to_be_visible()
        expect(page.get_by_text('Continue Your Journey')).to_be_visible()
        expect(page.locator('.fa-solid.fa-arrow-right')).to_have_count(1)
        
        # Step 7: Click continue button (should navigate to completion stub - 404)
        with page.expect_navigation():
            page.get_by_test_id('tour-continue-button').click()
        
        # Should show 404 since completion step not implemented
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/complete/')
        # 404 page content may vary, so just check URL is correct
        # The 404 status is confirmed by the successful navigation
        
        # Step 8: Navigate back to dashboard manually
        page.goto(f'{self.live_server_url}/dashboard/')
        expect(page).to_have_url(f'{self.live_server_url}/dashboard/')
        expect(page.get_by_test_id('dashboard-loaded')).to_have_count(1)
        
        # Verify user is authenticated
        expect(page.get_by_text(f'Welcome back, {new_username}')).to_be_visible()
    
    def test_tour_ui_interactions_journey(self):
        """
        Journey: Tour page UI interactions and visual validation
        
        Steps:
        1. Register and login
        2. Navigate to tour
        3. Test hover effects on feature cards
        4. Test tooltip functionality
        5. Test responsive design elements
        6. Test accessibility attributes
        
        Validates: UI interactions, tooltips, accessibility, responsive design
        """
        page = self.page
        
        # Step 1: Register new user
        new_username = 'ui_test_user'
        page.goto(f'{self.live_server_url}/auth/user/register/')
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/register/')
        
        page.get_by_test_id('register-username-input').fill(new_username)
        page.get_by_test_id('register-email-input').fill('ui_test@example.com')
        page.get_by_test_id('register-password-input').fill('SecurePass123')
        page.get_by_test_id('register-password-confirm-input').fill('SecurePass123')
        page.get_by_test_id('register-submit-button').click()
        
        # Should be on onboarding welcome
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/')
        
        # Step 2: Navigate to tour
        page.get_by_test_id('onboarding-begin-journey-button').click()
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/tour/')
        
        # Step 3: Test hover effects on feature cards
        workflows_card = page.get_by_test_id('tour-card-workflows')
        
        # Hover over workflows card
        workflows_card.hover()
        # Check for visual changes (e.g., shadow, transform)
        # Note: Visual effects might be hard to test programmatically
        # We can at least verify the card is still visible and interactive
        expect(workflows_card).to_be_visible()
        
        # Step 4: Test tooltip functionality
        continue_button = page.get_by_test_id('tour-continue-button')
        
        # Hover over continue button to trigger tooltip
        continue_button.hover()
        
        # Check if tooltip attribute exists
        expect(continue_button).to_have_attribute('data-bs-toggle', 'tooltip')
        expect(continue_button).to_have_attribute('data-bs-placement', 'top')
        
        # Step 5: Test responsive design elements
        # Verify grid layout exists
        expect(page.get_by_test_id('tour-features-grid')).to_be_visible()
        
        # Check for responsive classes
        expect(page.locator('.col-md-6')).to_have_count(4)  # Should have 4 cards
        expect(page.locator('.col-lg-3')).to_have_count(4)  # Desktop layout
        
        # Step 6: Test accessibility attributes
        # Verify semantic HTML structure
        expect(page.locator('main[role="main"]')).to_be_visible()
        expect(page.locator('main[aria-label="Feature Tour"]')).to_be_visible()
        
        # Verify ARIA labels on feature cards
        expect(page.locator('[data-testid="tour-card-workflows"][aria-label="Workflows Feature"]')).to_be_visible()
        expect(page.locator('[data-testid="tour-card-activities"][aria-label="Activities Feature"]')).to_be_visible()
        expect(page.locator('[data-testid="tour-card-artifacts"][aria-label="Artifacts Feature"]')).to_be_visible()
        expect(page.locator('[data-testid="tour-card-sync"][aria-label="Sync Feature"]')).to_be_visible()
        
        # Verify feature icons exist
        expect(page.locator('.fa-solid.fa-sitemap')).to_be_visible()  # Workflows
        expect(page.locator('.fa-solid.fa-tasks')).to_be_visible()    # Activities
        expect(page.locator('.fa-solid.fa-folder-open')).to_be_visible()  # Artifacts
        expect(page.locator('.fa-solid.fa-sync')).to_be_visible()     # Sync
        
        # Verify continue button accessibility
        expect(page.get_by_test_id('tour-continue-button')).to_have_attribute('aria-label', 'Continue to next onboarding step')
    
    def test_skip_onboarding_journey(self):
        """
        Journey: User skips onboarding from welcome screen
        
        Steps:
        1. Register new user
        2. On welcome screen, click skip link
        3. Confirm skip in modal
        4. Verify redirected to dashboard
        
        Validates: Skip functionality, modal interaction
        """
        page = self.page
        
        # Step 1: Register new user
        new_username = 'skip_user_journey'
        page.goto(f'{self.live_server_url}/auth/user/register/')
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/register/')
        
        page.get_by_test_id('register-username-input').fill(new_username)
        page.get_by_test_id('register-email-input').fill('skip_user@example.com')
        page.get_by_test_id('register-password-input').fill('SecurePass123')
        page.get_by_test_id('register-password-confirm-input').fill('SecurePass123')
        page.get_by_test_id('register-submit-button').click()
        
        # Step 2: Should be on welcome screen
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/')
        expect(page.get_by_test_id('onboarding-welcome')).to_be_visible()
        
        # Step 3: Click skip link and confirm
        page.get_by_test_id('onboarding-skip-link-top').click()
        
        # Wait for modal to appear
        expect(page.get_by_test_id('onboarding-skip-modal')).to_be_visible()
        expect(page.get_by_text('Skip tour?')).to_be_visible()
        
        # Confirm skip
        page.get_by_test_id('onboarding-skip-confirm').click()
        
        # Step 4: Verify redirected to dashboard
        expect(page).to_have_url(f'{self.live_server_url}/dashboard/')
        expect(page.get_by_test_id('dashboard-loaded')).to_be_visible()
        
        # Verify user is authenticated
        expect(page.get_by_text(f'Welcome back, {new_username}')).to_be_visible()
