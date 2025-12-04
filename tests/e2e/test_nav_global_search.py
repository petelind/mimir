import re

import pytest
from playwright.sync_api import Page


@pytest.mark.e2e
@pytest.mark.xfail(reason="Django async DB teardown with pytest-playwright on Django 5 (infrastructure issue)")
class TestNavGlobalSearchE2E:
    """E2E test for NAV-06 Global search user journey using Playwright."""

    def test_nav06_global_search_allows_navigation_across_entities(
        self,
        page: Page,
        live_server,
    ):
        """NAV-06: User can invoke global search from navbar and reach results page."""
        base_url = live_server.url

        # Step 1: Login via UI
        page.goto(f"{base_url}/auth/user/login/")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin")
        page.click('button[type="submit"]')

        # Expect redirect to dashboard
        page.wait_for_url(re.compile(rf"{re.escape(base_url)}/dashboard/.*"))

        # Step 2: Use global search from navbar
        page.fill('[data-testid="global-search-input"]', "Component")
        # Press Enter to submit the form
        page.keyboard.press("Enter")

        # Expect to land on search results page
        page.wait_for_url(re.compile(r".*/search/.*"))

        # Step 3: Verify results page UI elements are present
        page.wait_for_selector('[data-testid="global-search-results-page"]')
        page.wait_for_selector('[data-testid="global-search-playbooks"]')
        page.wait_for_selector('[data-testid="global-search-workflows"]')
        page.wait_for_selector('[data-testid="global-search-activities"]')
