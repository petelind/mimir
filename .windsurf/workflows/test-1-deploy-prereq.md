---
description: 
auto_execution_mode: 1
---

# Playwright Test Setup 
This guide provides step-by-step instructions for the Playwright test setup

## Overview

The current Playwright setup includes:
- **E2E test configuration** with multi-browser support
- **Django integration** for backend testing
- **Automatic browser installation** and management
- **Test isolation** and database handling
- **Comprehensive reporting** and debugging features

## Prerequisites

- Python 3.8+ with virtual environment
- Django project (if transferring Django-specific features)

## Step 1: Install Dependencies

### 1.1 Core Playwright Dependencies

Add these packages to your `requirements.txt`:

```txt
# Playwright and testing
playwright==1.54.0
pytest==8.4.1
pytest-playwright==0.7.0
pytest-django==4.11.1  # Only if using Django
pytest-base-url==2.1.0
pytest-env==1.1.5
pytest-timeout==2.4.0

# Environment management
python-dotenv==1.1.1

# File watching (for continuous testing)
watchdog==6.0.0
```

### 1.2 Install Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate  # or your venv path

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
```

## Step 2: Copy Configuration Files

### 2.1 Main Playwright Configuration

Create `playwright.config.py`:

```python
"""
Playwright configuration for e2e tests.

Configures browser settings, test timeouts, and parallel execution
for comprehensive frontend acceptance testing.
"""
import os

# Playwright configuration
PLAYWRIGHT_CONFIG = {
    # Test directory
    "testdir": "tests/e2e",
    
    # Browser configuration
    "use": {
        "baseURL": "http://localhost:5174",  # Adjust for your frontend URL
        "trace": "on-first-retry",
        "screenshot": "only-on-failure",
        "video": "retain-on-failure",
        "viewport": {"width": 1280, "height": 720},
        "ignoreHTTPSErrors": True,
        "actionTimeout": 10000,
        "navigationTimeout": 30000,
    },
    
    # Test execution
    "timeout": 60000,  # 60 seconds per test
    "expect": {
        "timeout": 10000  # 10 seconds for assertions
    },
    
    # Parallel execution
    "workers": 1,  # Run tests sequentially for e2e stability
    "fullyParallel": False,
    
    # Retry configuration
    "retries": 2,  # Retry failed tests up to 2 times
    
    # Reporter configuration
    "reporter": [
        ["list"],
        ["html", {"open": "never", "outputFolder": "test-results/html"}],
        ["junit", {"outputFile": "test-results/junit.xml"}]
    ],
    
    # Output directories
    "outputDir": "test-results/artifacts",
    
    # Projects (different browser configurations)
    "projects": [
        {
            "name": "chromium",
            "use": {
                "channel": "chromium",
                "viewport": {"width": 1280, "height": 720}
            }
        },
        {
            "name": "firefox",
            "use": {
                "browserName": "firefox",
                "viewport": {"width": 1280, "height": 720}
            }
        },
        {
            "name": "webkit",
            "use": {
                "browserName": "webkit",
                "viewport": {"width": 1280, "height": 720}
            }
        },
        {
            "name": "mobile-chrome",
            "use": {
                "channel": "chromium",
                "viewport": {"width": 375, "height": 667},
                "deviceScaleFactor": 2,
                "isMobile": True,
                "hasTouch": True
            }
        }
    ]
}

def get_playwright_config():
    """Get Playwright configuration for pytest-playwright."""
    return PLAYWRIGHT_CONFIG

def setup_test_environment():
    """Set up environment variables and configuration for e2e tests."""
    # Set test environment variables
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")  # Update project name
    os.environ.setdefault("DJANGO_ENV", "test")
    
    # Ensure test database is used
    os.environ.setdefault("DATABASE_URL", "sqlite:///test_db.sqlite3")
    
    # Frontend/Backend URLs for testing
    os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")  # Adjust as needed
    os.environ.setdefault("BACKEND_URL", "http://localhost:8000")   # Adjust as needed

if __name__ == "__main__":
    setup_test_environment()
    print("Playwright configuration loaded successfully")
    print(f"Base URL: {PLAYWRIGHT_CONFIG['use']['baseURL']}")
    print(f"Test directory: {PLAYWRIGHT_CONFIG['testdir']}")
```

### 2.2 Pytest E2E Configuration

Create `pytest-e2e.ini`:

```ini
[tool:pytest]
# Pytest configuration for e2e acceptance tests
minversion = 7.0
addopts = 
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --maxfail=3
    --durations=10
    --browser chromium
    --headed
    --slowmo=100
    --video=retain-on-failure
    --screenshot=only-on-failure
    --tracing=retain-on-failure

# Test discovery
testpaths = tests/e2e
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers
markers =
    e2e: End-to-end tests using Playwright
    slow: Slow running tests
    auth: Authentication related tests
    ui: User interface tests
    mobile: Mobile responsive tests
    integration: Integration tests

# Django settings (adjust project name)
DJANGO_SETTINGS_MODULE = your_project.settings
django_find_project = false

# Playwright settings
playwright_browser = chromium
playwright_headless = false
playwright_slow_mo = 100

# Logging
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(name)s: %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# Warnings
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
    ignore:.*django.*:DeprecationWarning
```

### 2.3 Global Test Configuration

Create `conftest.py` in project root:

```python
"""
Global pytest configuration for Playwright tests.
"""
import pytest
from django.contrib.auth import get_user_model  # Only if using Django

User = get_user_model()  # Only if using Django

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for all tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch args."""
    return {
        **browser_type_launch_args,
        "headless": True,
        "slow_mo": 0,  # No slow motion for faster tests
    }

# Django-specific fixtures (remove if not using Django)
@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Set up the database for Django tests."""
    with django_db_blocker.unblock():
        # Create test users if needed
        if not User.objects.filter(username='testapi').exists():
            User.objects.create_superuser(
                username='testapi',
                email='testapi@example.com',
                password='testpass123'
            )
    return django_db_setup

@pytest.fixture(scope="function")
def live_server_url(live_server):
    """Provide the live server URL for e2e tests."""
    return live_server.url
```

### 2.4 Test-Specific Configuration

Create `tests/conftest.py`:

```python
"""
Configuration file for pytest.

This module contains fixtures and configuration for pytest to be used across tests.
"""
import os
import sys
import subprocess
import pytest
from dotenv import load_dotenv

def pytest_configure(config):
    """
    Configure pytest.
    
    This function is called once at the beginning of a test run.
    It loads environment variables from .env files.
    """
    # Load environment variables from .env files
    env_paths = [
        os.path.join(os.getcwd(), '.env'),  # Root .env file
        os.path.join(os.getcwd(), '.env.test'),  # Test-specific .env file
        os.path.join(os.getcwd(), '.env.local'),  # Local overrides
    ]

    for env_path in env_paths:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"Loaded environment variables from {env_path}")

@pytest.fixture(scope="session")
def base_url():
    """
    Get the base URL for tests.
    
    Returns:
        str: The base URL to use for tests.
    """
    return os.getenv("BASE_URL", "http://localhost:8001")  # Adjust default URL

def pytest_sessionstart(session):
    """
    Install Playwright browsers before tests start.
    
    This function is called once at the beginning of a test run.
    It ensures that Playwright browsers are installed if e2e tests are being run.
    """
    try:
        # Check if we need to install browsers
        has_e2e_tests = False
        for item in session.items:
            if 'e2e' in item.nodeid:
                has_e2e_tests = True
                break

        if has_e2e_tests:
            print("E2E tests detected - installing Playwright browsers...")
            subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                check=True
            )
            print("Playwright browser installation complete")
    except Exception as e:
        print(f"Warning: Failed to install Playwright browsers: {e}")
```

## Step 3: Create Directory Structure

### 3.1 Create Test Directories

```bash
mkdir -p tests/e2e
mkdir -p test-results/html
mkdir -p test-results/artifacts
```

### 3.2 Create Test Init Files

```bash
touch tests/__init__.py
touch tests/e2e/__init__.py
```

## Step 4: Browser Installation Script (Optional)

Create `.windsurf/playwright_setup.py` for IDE integration:

```python
#!/usr/bin/env python
"""
Playwright browser installation script for test environment.
"""
import os
import sys
import subprocess
from pathlib import Path

def install_playwright_browsers():
    """Install Playwright browser binaries."""
    try:
        print("Installing Playwright browsers...")
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Playwright browsers installed successfully.")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing Playwright browsers: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

if __name__ == "__main__":
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    
    success = install_playwright_browsers()
    
    cache_dir = Path.home() / "Library" / "Caches" / "ms-playwright"
    print(f"Playwright cache directory: {cache_dir}")
    print(f"Cache directory exists: {cache_dir.exists()}")
    
    if success:
        print("Playwright setup complete.")
        sys.exit(0)
    else:
        print("Playwright setup failed.")
        sys.exit(1)
```

## Step 5: Create Sample Test

Create `tests/e2e/test_sample.py`:

```python
"""
Sample Playwright E2E test to verify setup.
"""
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_sample_page_load(page: Page):
    """Test that the application loads successfully."""
    # Navigate to your application
    page.goto("/")  # Uses baseURL from config
    
    # Wait for page to load
    page.wait_for_load_state("networkidle")
    
    # Basic assertions
    expect(page).to_have_title(qr=r".*")  # Any title
    
    # Add your specific assertions here
    # expect(page.locator("h1")).to_contain_text("Welcome")

@pytest.mark.e2e
@pytest.mark.auth
def test_login_flow(page: Page):
    """Test login functionality (if applicable)."""
    page.goto("/login")
    
    # Fill login form
    page.fill('[data-testid="username"]', 'testuser')
    page.fill('[data-testid="password"]', 'testpass')
    
    # Submit form
    page.click('[data-testid="login-button"]')
    
    # Verify redirect or success
    page.wait_for_url("**/dashboard")  # Adjust URL pattern
    expect(page.locator('[data-testid="user-menu"]')).to_be_visible()
```

## Step 6: Django-Specific Integration (Optional)

### 6.1 Database Isolation for E2E Tests

If using Django, create test fixtures that work with persistent database:

```python
# In your test files
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def setup_test_user():
    """Create test user in persistent database for E2E tests."""
    user, created = User.objects.get_or_create(
        username='alex_chen',
        defaults={
            'email': 'alex@example.com',
            'first_name': 'Alex',
            'last_name': 'Chen'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
    return user
```

### 6.2 Authentication Headers

For API testing with Django Token Authentication:

```python
def test_api_with_auth(page: Page, setup_test_user):
    """Test API calls with authentication."""
    # Login first
    page.goto("/login")
    page.fill('[data-testid="username"]', 'alex_chen')
    page.fill('[data-testid="password"]', 'testpass123')
    page.click('[data-testid="login-button"]')
    
    # Get token from localStorage
    token = page.evaluate("() => localStorage.getItem('access_token')")
    
    # Make authenticated API request
    response = page.request.get("/api/data/", headers={
        "Authorization": f"Token {token}"  # Django TokenAuthentication format
    })
    
    assert response.status == 200
```

## Step 7: Running Tests

### 7.1 Basic Test Execution

```bash
# Run all E2E tests
pytest tests/e2e/ -c pytest-e2e.ini

# Run specific test
pytest tests/e2e/test_sample.py::test_sample_page_load -c pytest-e2e.ini

# Run with specific browser
pytest tests/e2e/ -c pytest-e2e.ini --browser firefox

# Run in headless mode
pytest tests/e2e/ -c pytest-e2e.ini --headed=false
```

### 7.2 Advanced Options

```bash
# Run with video recording
pytest tests/e2e/ -c pytest-e2e.ini --video=on

# Run with tracing for debugging
pytest tests/e2e/ -c pytest-e2e.ini --tracing=on

# Run mobile tests
pytest tests/e2e/ -c pytest-e2e.ini --browser-channel=mobile-chrome

# Generate HTML report
pytest tests/e2e/ -c pytest-e2e.ini --html=test-results/report.html
```

## Step 8: Project-Specific Customizations

### 8.1 Update URLs and Ports

1. **Frontend URL**: Update `baseURL` in `playwright.config.py`
2. **Backend URL**: Update `BACKEND_URL` in environment setup
3. **Database**: Adjust database settings for your project

### 8.2 Update Django Settings

1. **Project Name**: Replace `ripl.settings` with your Django project name
2. **User Model**: Adjust if using custom user model
3. **Authentication**: Modify auth patterns for your login system

### 8.3 Add Project-Specific Test IDs

Ensure your frontend components have `data-testid` attributes:

```tsx
// React example
<button data-testid="submit-button">Submit</button>
<div data-testid="user-profile">User Info</div>
```

## Step 9: CI/CD Integration

### 9.1 GitHub Actions Example

Create `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Install Playwright browsers
      run: python -m playwright install chromium
    
    - name: Run E2E tests
      run: pytest tests/e2e/ -c pytest-e2e.ini --browser chromium --headed=false
    
    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: test-results
        path: test-results/
```

## Step 10: Troubleshooting

### 10.1 Common Issues

1. **Browser Installation**: Run `python -m playwright install` if browsers missing
2. **Port Conflicts**: Ensure frontend/backend ports don't conflict
3. **Database Issues**: Use persistent database for E2E tests, not test database
4. **Authentication**: Use correct token format (`Token` not `Bearer` for Django)

### 10.2 Debug Mode

Enable debug mode for troubleshooting:

```bash
# Run with debug output
PWDEBUG=1 pytest tests/e2e/test_sample.py -c pytest-e2e.ini -s

# Run with slow motion
pytest tests/e2e/ -c pytest-e2e.ini --slowmo=1000
```

## Summary

This setup provides:
- ✅ **Multi-browser testing** (Chromium, Firefox, WebKit, Mobile)
- ✅ **Django integration** with proper database handling
- ✅ **Automatic browser installation** and management
- ✅ **Comprehensive reporting** with screenshots and videos
- ✅ **Test isolation** and parallel execution control
- ✅ **CI/CD ready** configuration
- ✅ **Debug capabilities** with tracing and slow motion

The transferred setup maintains all the robust testing capabilities while being adaptable to different project structures and requirements.
