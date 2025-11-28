"""User Journey Certification Tests for ONBOARD-01 + ONBOARD-03.

Tier 2: Browser-based validation of the onboarding welcome → tour journey.

Run (dev):
    pytest tests/e2e/test_journey_onboarding.py::test_new_user_welcome_to_tour_journey -v --headed

Run (CI/headless):
    pytest tests/e2e/test_journey_onboarding.py -v
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
@pytest.mark.django_db
def test_new_user_welcome_to_tour_journey(live_server, page: Page) -> None:
    """Journey: New user → Register → ONBOARD-01 welcome → ONBOARD-03 tour.

    Steps:
    1. Open registration page
    2. Submit valid registration form
    3. Auto-redirected to onboarding welcome (ONBOARD-01)
    4. Verify welcome content and CTA
    5. Click "Begin your journey" CTA
    6. Land on tour page (ONBOARD-03) and verify key UI and content

    Notes:
    - Uses pytest-django's ``live_server`` fixture for the base URL
    - Uses pytest-playwright's ``page`` fixture for browser automation
    - Avoids Django TestCase classes to prevent async DB teardown issues
    """

    base_url = live_server.url

    # Step 1: Open registration page directly
    page.goto(f"{base_url}/auth/user/register/")
    expect(page).to_have_url(f"{base_url}/auth/user/register/")

    # Step 2: Submit valid registration form
    username = "journey_user"
    page.get_by_test_id("register-username-input").fill(username)
    page.get_by_test_id("register-email-input").fill("journey_user@example.com")
    page.get_by_test_id("register-password-input").fill("SecurePass123")
    page.get_by_test_id("register-password-confirm-input").fill("SecurePass123")
    page.get_by_test_id("register-submit-button").click()

    # Step 3: Expect onboarding welcome screen (ONBOARD-01)
    expect(page).to_have_url(f"{base_url}/auth/user/onboarding/")
    expect(page.get_by_test_id("onboarding-welcome")).to_be_visible()

    # Verify key welcome content and structure
    expect(page.get_by_role("heading", name="Welcome to FOB")).to_be_visible()
    expect(page.get_by_test_id("onboarding-step-1")).to_be_visible()
    expect(page.get_by_test_id("onboarding-step-2")).to_be_visible()
    expect(page.get_by_test_id("onboarding-step-3")).to_be_visible()
    expect(page.get_by_test_id("onboarding-begin-journey-button")).to_be_visible()

    # Step 4: Click "Begin your journey" CTA
    page.get_by_test_id("onboarding-begin-journey-button").click()

    # Step 5: Expect ONBOARD-03 tour page
    expect(page).to_have_url(f"{base_url}/auth/user/onboarding/tour/")
    expect(page.get_by_test_id("tour-page")).to_be_visible()

    # Verify progress header per plan: "Step 2 of 3 - Feature Tour"
    expect(page.get_by_test_id("tour-progress-header")).to_be_visible()
    expect(page.get_by_text("Step 2 of 3 - Feature Tour")).to_be_visible()

    # Verify header text "Discover FOB's Features"
    expect(page.get_by_test_id("tour-header")).to_be_visible()
    expect(page.get_by_text("Discover FOB's Features")).to_be_visible()

    # Verify 4 feature cards exist with correct testids
    features_grid = page.get_by_test_id("tour-features-grid")
    expect(features_grid).to_be_visible()
    expect(page.get_by_test_id("tour-card-workflows")).to_be_visible()
    expect(page.get_by_test_id("tour-card-activities")).to_be_visible()
    expect(page.get_by_test_id("tour-card-artifacts")).to_be_visible()
    expect(page.get_by_test_id("tour-card-sync")).to_be_visible()

    # Verify feature titles inside respective cards
    expect(
        page.get_by_test_id("tour-card-workflows").get_by_role("heading", name="Workflows")
    ).to_be_visible()
    expect(
        page.get_by_test_id("tour-card-activities").get_by_role("heading", name="Activities")
    ).to_be_visible()
    expect(
        page.get_by_test_id("tour-card-artifacts").get_by_role("heading", name="Artifacts")
    ).to_be_visible()
    expect(
        page.get_by_test_id("tour-card-sync").get_by_role("heading", name="Sync")
    ).to_be_visible()

    # Verify key description snippets from the plan
    expect(page.get_by_text("Organize activities into structured processes")).to_be_visible()
    expect(page.get_by_text("Define specific tasks")).to_be_visible()
    expect(page.get_by_text("Track deliverables")).to_be_visible()
    expect(page.get_by_text("Collaborate via Homebase")).to_be_visible()

    # Verify badges in context of their cards
    expect(
        page.get_by_test_id("tour-card-workflows").get_by_text("Process Management")
    ).to_be_visible()
    expect(
        page.get_by_test_id("tour-card-activities").get_by_text("Task Management")
    ).to_be_visible()
    expect(
        page.get_by_test_id("tour-card-artifacts").get_by_text("Deliverable Tracking")
    ).to_be_visible()
    expect(
        page.get_by_test_id("tour-card-sync").get_by_text("Team Collaboration")
    ).to_be_visible()

    # Verify continue button presence (navigation itself is tested at integration level)
    expect(page.get_by_test_id("tour-continue-button")).to_be_visible()
    expect(page.get_by_text("Continue Your Journey")).to_be_visible()

