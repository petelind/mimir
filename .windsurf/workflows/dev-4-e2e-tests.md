---
description: E2E Testing with Django LiveServerTestCase + Playwright
auto_execution_mode: 3
---

# E2E Test Implementation Workflow

This workflow guides you through implementing E2E tests for Django + HTMX applications using Playwright.

**When implementing tests** - assume app is already working, so if there are discrepancies between feature files and implementation - implementation takes precedence.

---

## Step 1: Define Test Scope

**Identify the user journey:**
```bash
# Review feature files
ls docs/features/*.feature

# Map out the sequential journey
for file in docs/features/*.feature; do
    echo "\n=== $file ==="
    grep -n "Scenario:" "$file"
done
```

**Ask user:** "Which scenarios should be covered in E2E tests? Default: happy path + critical error cases"

---

## Step 2: Analyze Django Templates

### 2.1 Review Template Implementation
```bash
# Find relevant templates
find methodology/templates -name "*.html"

# Check for data-testid attributes
grep -r "data-testid" methodology/templates/
```

### 2.2 Identify Selectors
**Selector Priority:**
1. **`data-testid`** - Primary choice (use `get_by_test_id()`)
2. **`id`** - Secondary for unique elements
3. **`name`** - For form inputs
4. **Semantic HTML** - For stable content

**See rule:** `.windsurf/rules/do-semantic-versioning-on-ui-elements.md`

### 2.3 Check HTMX Interactions
```bash
# Find HTMX usage
grep -r "hx-get\|hx-post\|hx-target" methodology/templates/
```

Note dynamic content areas that need wait strategies.

---

## Step 3: Compare Feature vs Implementation

**Check for inconsistencies:**
- Missing UI elements mentioned in scenarios
- Different terminology between feature and implementation
- Incomplete flows or validation points

**Ask user if discrepancies found:**
"Found inconsistency: [DESCRIPTION]. Implementation takes precedence for testing purposes. Should we update feature file?"

---

## Step 4: Design Test Data Setup

**See rule:** `.windsurf/rules/do-test-fixture-data-management.md`

**Test data in `tests/fixtures/e2e_seed.json`:**
```python
# Load once at test class setup
@pytest.fixture(scope="class", autouse=True)
def setup_test_data(self):
    import subprocess
    subprocess.run(["python", "manage.py", "loaddata", "tests/fixtures/e2e_seed.json"])
    yield
    subprocess.run(["python", "manage.py", "flush", "--noinput"])
```

**Include:**
- Test user with permissions
- Sample methodologies, workflows, activities
- Relationships between entities

---

## Step 5: Implement E2E Tests

### 5.1 Test Structure with Playwright

```python
# tests/e2e/test_workflow.py
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect

class WorkflowE2ETest(StaticLiveServerTestCase):
    """E2E tests for workflow management"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
    
    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()
    
    def test_create_activity(self):
        """Test activity creation via HTMX form"""
        page = self.context.new_page()
        page.goto(f'{self.live_server_url}/workflow/{self.workflow.id}/')
        
        # Wait for page load
        expect(page.get_by_test_id('workflow-detail')).to_be_visible()
        
        # Click create button
        page.get_by_test_id('create-activity-button').click()
        
        # Wait for HTMX form to load
        expect(page.get_by_test_id('activity-form')).to_be_visible()
        
        # Fill form
        page.get_by_test_id('activity-name-input').fill('New Activity')
        
        # Submit
        page.get_by_test_id('save-activity-button').click()
        
        # Wait for HTMX update
        expect(page.get_by_test_id('activity-list')).to_contain_text('New Activity')
        
        # Verify in database
        self.assertTrue(Activity.objects.filter(name='New Activity').exists())
        
        page.close()
```

### 5.2 Page Object Pattern (Optional)

```python
# tests/e2e/pages/workflow_page.py
from playwright.sync_api import Page, expect

class WorkflowPage:
    def __init__(self, page: Page, live_server_url: str):
        self.page = page
        self.live_server_url = live_server_url
    
    def navigate_to(self, workflow_id):
        self.page.goto(f'{self.live_server_url}/workflow/{workflow_id}/')
        expect(self.page.get_by_test_id('workflow-detail')).to_be_visible()
    
    def create_activity(self, name: str):
        self.page.get_by_test_id('create-activity-button').click()
        expect(self.page.get_by_test_id('activity-form')).to_be_visible()
        self.page.get_by_test_id('activity-name-input').fill(name)
        self.page.get_by_test_id('save-activity-button').click()
        expect(self.page.get_by_test_id('activity-form')).not_to_be_visible()
    
    def verify_activity_exists(self, name: str):
        expect(self.page.get_by_test_id('activity-list')).to_contain_text(name)
```

### 5.3 Testing HTMX Interactions

```python
def test_htmx_content_swap(self):
    """Test HTMX swaps content without page reload"""
    page = self.context.new_page()
    page.goto(f'{self.live_server_url}/methodology/{self.methodology.id}/')
    
    initial_text = page.get_by_test_id('main-content').text_content()
    
    # Trigger HTMX navigation
    page.get_by_test_id('version-link').click()
    
    # Wait for content change
    page.wait_for_function(
        f'document.querySelector(\'[data-testid="main-content"]\').textContent !== "{initial_text}"'
    )
    
    # Verify URL didn't change (HTMX update, not navigation)
    self.assertIn('/methodology/', page.url)
    
    page.close()
```

---

## Step 6: Run and Debug Tests

**See rule:** `.windsurf/rules/do-django-live-server-tests.md`

```bash
# Run specific test
pytest tests/e2e/test_workflow.py::WorkflowE2ETest::test_create_activity -v

# Run with visible browser
pytest tests/e2e/test_workflow.py --headed

# Run all E2E tests
pytest tests/e2e/ -v
```

**Debugging:**
- Use `--headed` to see browser
- Use `page.pause()` for breakpoint
- Check `test-results/` for screenshots on failure

---

## Step 7: Document Test Coverage

```python
class WorkflowE2ETest(StaticLiveServerTestCase):
    """
    ✅ E2E Tests for Workflow Management
    
    Coverage:
    ✅ Create workflow
    ✅ Create activity via HTMX
    ✅ Edit activity
    ✅ View workflow graph
    ✅ HTMX dynamic updates
    
    Test Strategy:
    - Uses LiveServerTestCase + Playwright
    - Tests Django templates + HTMX interactions
    - Validates Graphviz SVG rendering
    - No mocking - real database and server
    """
```

---

## Decision Tree: TestCase vs LiveServerTestCase

```
Can you test without browser?
├─ Yes → Use Django TestCase (90% of tests)
│         - View returns correct status
│         - Template context is correct
│         - Forms submit properly
│         - HTMX endpoints return HTML
│
└─ No → Use LiveServerTestCase + Playwright
          When you need:
          - HTMX DOM updates
          - SVG interactions
          - JavaScript behavior
          - Multi-step workflows
```

---

## Key Testing Principles

1. **Prefer Django TestCase** - 10x faster than browser tests
2. **Use `data-testid`** - Primary selector with `get_by_test_id()`
3. **Use Playwright's `expect()`** - Built-in auto-waiting
4. **Test business logic separately** - Don't test services in E2E
5. **Keep E2E minimal** - Happy path + critical errors only
6. **Close pages** - Always call `page.close()` after test

---

## Workflow Summary

1. ✅ Define test scope → Map user journey
2. ✅ Analyze templates → Extract selectors
3. ✅ Compare vs features → Resolve inconsistencies
4. ✅ Design test data → Create fixtures
5. ✅ Implement tests → Use Playwright + LiveServerTestCase
6. ✅ Run & debug → Use --headed for debugging
7. ✅ Document coverage → Mark tested scenarios