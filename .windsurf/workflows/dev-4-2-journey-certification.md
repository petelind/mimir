---
description: User Journey Certification with LiveServerTestCase + Playwright
---

# User Journey Certification Test Implementation

**Tier 2 Testing:** Browser-based validation of complete user journeys across multiple features.

**Purpose:** Certify that complete user experiences work end-to-end with real browser, HTMX, and JavaScript.

**When to use:** For critical user journeys spanning multiple features. Run on PR merge / nightly / pre-release.

---

## Step 1: Identify Critical User Journeys

**Ask:** What are the most important paths users take through the application?

**Examples:**
- New user: Register → Onboarding → Create first playbook → Add workflow
- Existing user: Login → Navigate dashboard → Edit workflow → View activities
- Power user: Create methodology → Version it → Share with team

**Criteria for journey tests:**
- ✅ Spans multiple features (cross-cutting)
- ✅ Represents common user workflow
- ✅ Involves HTMX interactions
- ✅ Has visual/UI components
- ✅ Critical to business value

**Limit:** 5-10 journey tests total (they're slow, keep focused)

---

## Step 2: Design Test Data Fixtures

**See rule:** `.windsurf/rules/do-test-fixture-data-management.md`

### 2.1 Create Fixture JSON

```bash
# Create fixture file
mkdir -p tests/fixtures
touch tests/fixtures/journey_seed.json
```

### 2.2 Export Sample Data

```bash
# Create sample data in dev database
python manage.py runserver
# (Create users, methodologies, workflows via UI)

# Export to fixture
python manage.py dumpdata auth.User methodology.Methodology methodology.Workflow \
    --natural-foreign --natural-primary \
    --indent 2 \
    -o tests/fixtures/journey_seed.json
```

### 2.3 Fixture Contents

Include:
- **Test users** with different roles/permissions
- **Sample methodologies** with realistic data
- **Workflows** with activities and relationships
- **Any dependencies** (e.g., phases, statuses)

**Example structure:**
```json
[
  {
    "model": "auth.user",
    "pk": 1,
    "fields": {
      "username": "maria",
      "email": "maria@example.com",
      "password": "pbkdf2_sha256$..."
    }
  },
  {
    "model": "methodology.methodology",
    "pk": 1,
    "fields": {
      "name": "Agile Development",
      "created_by": 1,
      "version": "1.0"
    }
  }
]
```

---

## Step 3: Implement Journey Test with Playwright

### 3.1 Test File Structure

```python
"""User Journey Certification Tests with Playwright.

Tests complete user journeys across multiple features.
Uses LiveServerTestCase + Playwright for browser-based testing.

Run: pytest tests/e2e/test_journey_<name>.py -v --headed
"""
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, Page, expect
from django.core.management import call_command


class TestNewUserJourney(StaticLiveServerTestCase):
    """Certify complete new user journey from registration to first playbook."""
    
    fixtures = ['tests/fixtures/journey_seed.json']  # Auto-load fixtures
    
    @classmethod
    def setUpClass(cls):
        """Set up Playwright browser for all tests."""
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=False)  # headed for debugging
    
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
    
    def test_new_user_complete_journey(self):
        """
        Journey: New user → Register → Onboarding → Create first playbook
        
        Steps:
        1. Visit site (not logged in)
        2. Click "Sign Up"
        3. Fill registration form
        4. Auto-redirected to onboarding
        5. Skip onboarding → Dashboard
        6. Create new playbook
        7. Verify playbook appears
        
        Validates: Registration, authentication, navigation, HTMX, UI
        """
        page = self.page
        
        # Step 1: Visit site
        page.goto(f'{self.live_server_url}/')
        expect(page).to_have_title(/FOB Dashboard/)
        
        # Step 2: Navigate to registration
        page.get_by_test_id('signup-link').click()
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/register/')
        
        # Step 3: Fill registration form
        page.get_by_test_id('register-username-input').fill('newuser')
        page.get_by_test_id('register-email-input').fill('new@example.com')
        page.get_by_test_id('register-password-input').fill('SecurePass123')
        page.get_by_test_id('register-password-confirm-input').fill('SecurePass123')
        page.get_by_test_id('register-submit-button').click()
        
        # Step 4: Should be on onboarding
        expect(page).to_have_url(f'{self.live_server_url}/auth/user/onboarding/')
        expect(page.get_by_test_id('onboarding-stub')).to_be_visible()
        
        # Step 5: Skip to dashboard
        page.get_by_text('Skip to Dashboard').click()
        expect(page).to_have_url(f'{self.live_server_url}/dashboard/')
        
        # Step 6: Create playbook (HTMX interaction)
        page.get_by_test_id('create-playbook-button').click()
        
        # Wait for HTMX form to appear
        expect(page.get_by_test_id('playbook-form')).to_be_visible()
        
        page.get_by_test_id('playbook-name-input').fill('My First Playbook')
        page.get_by_test_id('playbook-save-button').click()
        
        # Step 7: Verify playbook created (HTMX content swap)
        expect(page.get_by_test_id('playbook-list')).to_contain_text('My First Playbook')
        
        # Verify in database (can access Django ORM)
        from methodology.models import Methodology
        assert Methodology.objects.filter(name='My First Playbook').exists()
```

### 3.2 Helper Methods for Common Actions

```python
def _login(self, page: Page, username: str, password: str):
    """Helper to login via browser."""
    page.goto(f'{self.live_server_url}/auth/user/login/')
    page.get_by_test_id('login-username-input').fill(username)
    page.get_by_test_id('login-password-input').fill(password)
    page.get_by_test_id('login-submit-button').click()
    expect(page).to_have_url(f'{self.live_server_url}/dashboard/')

def _wait_for_htmx_update(self, page: Page):
    """Wait for HTMX request to complete."""
    page.wait_for_load_state('networkidle')
    # Or wait for specific element
    page.wait_for_selector('[hx-indicator].htmx-settled')
```

### 3.3 HTMX Testing Patterns

```python
def test_htmx_navigation(self):
    """Test HTMX updates content without full page reload."""
    page = self.page
    self._login(page, 'maria', 'testpass')
    
    # Get initial URL
    initial_url = page.url
    
    # Click HTMX link
    page.get_by_test_id('workflow-tab').click()
    
    # Wait for content change
    expect(page.get_by_test_id('workflow-list')).to_be_visible()
    
    # Verify URL didn't change (HTMX swap, not navigation)
    assert page.url == initial_url
    
    # Verify new content loaded
    expect(page.get_by_test_id('workflow-list')).to_contain_text('Workflows')
```

---

## Step 4: Run and Debug Journey Tests

```bash
# Run with visible browser (for development)
pytest tests/e2e/test_journey_new_user.py -v --headed

# Run headless (for CI/CD)
pytest tests/e2e/test_journey_new_user.py -v

# Run with slow motion (see actions)
pytest tests/e2e/test_journey_new_user.py -v --headed --slowmo 500

# Run specific test
pytest tests/e2e/test_journey_new_user.py::TestNewUserJourney::test_new_user_complete_journey -v --headed

# Debug with traces (Playwright Inspector)
PWDEBUG=1 pytest tests/e2e/test_journey_new_user.py -v
```

**Debugging tips:**
- Use `--headed` to see browser
- Use `page.pause()` for breakpoints
- Check `test-results/` for screenshots on failure
- Use Playwright Inspector with `PWDEBUG=1`

---

## Step 5: Organize Journey Tests

```
tests/e2e/
├── conftest.py              # Shared fixtures
├── test_journey_new_user.py        # Registration → first playbook
├── test_journey_workflow_mgmt.py   # Create → edit → execute workflow
├── test_journey_navigation.py      # Dashboard navigation with HTMX
└── test_journey_collaboration.py   # Share → comment → version
```

**Keep it focused:** 5-10 total journey tests covering critical paths.

---

## Step 6: Document Journey Coverage

```python
class TestNewUserJourney(StaticLiveServerTestCase):
    """
    ✅ User Journey Certification: New User Onboarding
    
    Journey: Anonymous → Register → Onboarding → Create First Playbook
    
    What this tests:
    ✅ Registration form (AUTH-03)
    ✅ Auto-login after registration
    ✅ Onboarding flow (FOB-ONBOARDING-1)
    ✅ Dashboard navigation (FOB-DASHBOARD-1)
    ✅ HTMX playbook creation (FOB-PLAYBOOKS-CREATE-1)
    ✅ UI rendering and visual correctness
    ✅ JavaScript interactions
    ✅ Bootstrap components
    
    Technology Validated:
    - Django authentication
    - HTMX content swaps
    - Bootstrap tooltips/modals
    - Font Awesome icons
    - Graphviz rendering (if applicable)
    
    Run: pytest tests/e2e/test_journey_new_user.py -v --headed
    Time: ~15-20 seconds
    """
```

---

## Key Differences from Feature ATs

| Aspect | Feature AT (4-1) | Journey Certification (4-2) |
|--------|------------------|----------------------------|
| **Tool** | Django Test Client | Playwright + LiveServer |
| **Speed** | Fast (1-5s) | Slow (10-30s) |
| **Scope** | Single feature | Multiple features |
| **Coverage** | All scenarios | Happy path only |
| **What it tests** | Logic, redirects, DB | UI, HTMX, JavaScript, UX |
| **When to run** | Every commit | PR merge / nightly |
| **Fixtures** | Create inline | Load from JSON |

---

## When to Add Journey Test

Add a journey test when:
- ✅ Feature involves HTMX interactions
- ✅ Feature has visual/UI complexity
- ✅ Feature is part of critical user path
- ✅ Feature involves JavaScript
- ✅ Feature ATs alone don't give enough confidence

Don't add if:
- ❌ Simple CRUD with no HTMX
- ❌ Backend-heavy feature
- ❌ Already covered by existing journey test

---

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  feature-tests:
    # Fast - run on every commit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Feature ATs
        run: pytest tests/integration/ -v
  
  journey-tests:
    # Slow - run on PR merge only
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    steps:
      - uses: actions/checkout@v2
      - name: Install Playwright
        run: python -m playwright install chromium
      - name: Run Journey Tests
        run: pytest tests/e2e/ -v
```

---

## Maintenance Tips

1. **Keep journeys stable** - Don't change fixtures frequently
2. **Use data-testid** - Makes tests resilient to UI changes
3. **Avoid brittle selectors** - Don't use CSS classes for testing
4. **Handle timing** - Use Playwright's auto-waiting, avoid manual sleeps
5. **Screenshot on failure** - Helps debug flaky tests

---

## Summary

**Journey Certification Tests:**
- ✅ Use Playwright + LiveServerTestCase
- ✅ Load fixtures from JSON
- ✅ Test complete user flows
- ✅ Validate HTMX, JavaScript, UI
- ✅ Run slower, provide high confidence
- ✅ Keep focused on critical paths (5-10 tests)

**Next Steps:**
1. Identify 3-5 critical user journeys
2. Create fixture data (journey_seed.json)
3. Implement journey tests with Playwright
4. Run: `pytest tests/e2e/ -v --headed`
5. Integrate into PR merge pipeline
