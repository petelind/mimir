"""E2E test configuration with Playwright and Django live server.

IMPORTANT: Playwright's sync API creates an event loop internally, which conflicts
with Django's requirement for synchronous context. To work around this, we use
lazy initialization - Playwright is only started when first accessed in a test,
after Django setup is complete.
"""

import pytest
import os
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


# Allow Django to run in async context for E2E tests only
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Load E2E test fixtures at session start.
    
    This fixture extends the base django_db_setup to load
    test data needed for E2E scenarios.
    """
    from django.core.management import call_command
    import os
    
    # Get absolute path to fixture file
    fixture_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures/e2e_seed.json'))
    
    with django_db_blocker.unblock():
        # Load E2E test fixtures (includes test users)
        call_command('loaddata', fixture_path)


class LazyPlaywright:
    """Lazy wrapper for Playwright to delay event loop creation."""
    def __init__(self):
        self._playwright = None
        self._context_manager = None
    
    def __enter__(self):
        self._context_manager = sync_playwright()
        self._playwright = self._context_manager.__enter__()
        return self._playwright
    
    def __exit__(self, *args):
        if self._context_manager:
            return self._context_manager.__exit__(*args)


@pytest.fixture(scope="module")
def playwright():
    """
    Create Playwright instance for the test module.
    
    Uses lazy initialization to avoid creating event loop during Django setup.
    """
    lazy_pw = LazyPlaywright()
    with lazy_pw as p:
        yield p


@pytest.fixture(scope="module")
def browser(playwright):
    """
    Launch browser for the test module.
    
    Uses Chromium in headless mode for CI/CD compatibility.
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
