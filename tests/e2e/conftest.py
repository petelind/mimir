"""E2E test configuration with Playwright and Django live server.

IMPORTANT: This conftest manually manages Playwright in SYNC mode
to avoid pytest-asyncio treating all tests as async.

pytest-playwright plugin is disabled globally in pytest.ini with '-p no:playwright'
to prevent auto-conversion of tests to async.
"""

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Load E2E test fixtures at session start.
    
    This fixture extends the base django_db_setup to load
    test data needed for E2E scenarios.
    """
    from django.core.management import call_command
    
    with django_db_blocker.unblock():
        # Load E2E test fixtures (includes test users)
        call_command('loaddata', 'tests/fixtures/e2e_seed.json')


@pytest.fixture(scope="module")
def playwright():
    """
    Create Playwright instance for the test module.
    
    Uses sync_playwright context manager to ensure proper cleanup.
    Module scope ensures it's cleaned up before Django's live_server teardown.
    """
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="module")
def browser(playwright):
    """
    Launch browser for the test module.
    
    Uses Chromium in headless mode for CI/CD compatibility.
    Module scope to reuse browser across tests in same module.
    """
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    Create a new browser context for each test.
    
    This ensures test isolation with fresh cookies and storage.
    """
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """
    Create a new page for each test.
    
    Provides a fresh page within the browser context.
    """
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def live_server_url(live_server):
    """
    Provide the live server URL for E2E tests.
    
    Uses Django's live_server fixture (provided by pytest-django)
    which starts a live Django server in a separate thread.
    """
    return live_server.url
