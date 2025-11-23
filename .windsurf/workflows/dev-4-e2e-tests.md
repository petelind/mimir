---
description: E2E Testing with Django LiveServerTestCase + Playwright
auto_execution_mode: 3
---

# E2E Test Implementation Workflow

This workflow guides you through implementing E2E tests for Django + HTMX applications using **Django Test Client**.

**Approach:** Use Django's Test Client to simulate complete user journeys. Faster, more reliable, and better Django integration than browser-based tests.

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

## Step 5: Implement E2E Tests with Django Test Client

### 5.1 Test Structure with Django Test Client

```python
# tests/e2e/test_workflow_e2e.py
import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.django_db
class TestWorkflowE2E:
    """E2E tests for complete workflow user journeys"""
    
    def test_create_activity_complete_flow(self):
        """
        E2E: User creates a new activity.
        
        Journey:
        1. Login
        2. Navigate to workflow
        3. Click create activity
        4. Fill form
        5. Submit
        6. Verify activity appears in list
        """
        # Arrange - Setup test data
        client = Client()
        user = User.objects.create_user(username='maria', password='test123')
        workflow = Workflow.objects.create(name='Test Workflow', created_by=user)
        
        # Step 1: Login
        login_response = client.post(reverse('login'), {
            'username': 'maria',
            'password': 'test123',
        })
        assert login_response.status_code == 302  # Redirect on success
        
        # Step 2: Navigate to workflow
        workflow_url = reverse('workflow_detail', args=[workflow.id])
        response = client.get(workflow_url)
        assert response.status_code == 200
        assert 'Test Workflow' in response.content.decode('utf-8')
        
        # Step 3 & 4 & 5: Create activity (simulate form POST)
        create_response = client.post(
            reverse('activity_create', args=[workflow.id]),
            {
                'name': 'New Activity',
                'description': 'Test description',
                'phase': 'planning',
            },
            follow=True  # Follow redirects
        )
        
        # Step 6: Verify activity in response
        assert create_response.status_code == 200
        content = create_response.content.decode('utf-8')
        assert 'New Activity' in content
        assert 'data-testid="activity-list"' in content or 'New Activity' in content
        
        # Verify in database
        assert Activity.objects.filter(name='New Activity', workflow=workflow).exists()
        activity = Activity.objects.get(name='New Activity')
        assert activity.description == 'Test description'
```

### 5.2 Helper Functions (Optional)

```python
# tests/e2e/helpers.py
from django.test import Client
from django.urls import reverse

def login_user(client: Client, username: str, password: str):
    """Helper to login user via Test Client"""
    response = client.post(reverse('login'), {
        'username': username,
        'password': password,
    })
    assert response.status_code == 302, "Login should redirect"
    return client

def create_activity(client: Client, workflow_id: int, name: str, description: str = ''):
    """Helper to create activity via POST"""
    response = client.post(
        reverse('activity_create', args=[workflow_id]),
        {
            'name': name,
            'description': description,
            'phase': 'planning',
        },
        follow=True
    )
    assert response.status_code == 200
    return response

def verify_content_in_response(response, expected_text: str):
    """Helper to verify text appears in response"""
    content = response.content.decode('utf-8')
    assert expected_text in content, f"Expected '{expected_text}' in response"
```

### 5.3 Testing HTMX Endpoints

```python
def test_htmx_partial_update(self):
    """Test HTMX endpoint returns partial HTML"""
    client = Client()
    client.login(username='maria', password='test123')
    
    # Make HTMX request (usually has HX-Request header)
    response = client.get(
        reverse('activity_partial', args=[activity.id]),
        HTTP_HX_REQUEST='true'  # Simulate HTMX request
    )
    
    assert response.status_code == 200
    content = response.content.decode('utf-8')
    
    # Should return partial HTML, not full page
    assert '<html' not in content  # No full page
    assert '<div data-testid="activity-item"' in content  # Partial content
    assert activity.name in content
```

---

## Step 6: Run and Debug Tests

```bash
# Run specific test
pytest tests/e2e/test_workflow_e2e.py::TestWorkflowE2E::test_create_activity_complete_flow -v

# Run all E2E tests
pytest tests/e2e/ -v

# Run with verbose output
pytest tests/e2e/ -vv

# Run with print statements visible
pytest tests/e2e/ -v -s
```

**Debugging:**
- Use `print(response.content.decode())` to see HTML
- Use `-s` flag to see print output  
- Check response.status_code for redirects/errors
- Verify database state with queries

---

## Step 7: Document Test Coverage

```python
class TestWorkflowE2E:
    """
    ✅ E2E Tests for Workflow Management
    
    Coverage:
    ✅ Create workflow complete flow
    ✅ Create activity via form POST
    ✅ Edit activity
    ✅ View workflow detail page
    ✅ HTMX partial endpoint responses
    
    Test Strategy:
    - Uses Django Test Client (pytest)
    - Tests complete user journeys
    - Validates HTML responses and redirects
    - Verifies database state after operations
    - No mocking - real database
    - No browser needed - faster and more reliable
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
│         - Redirects work
        
└─ Need live server? → Use pytest + Django Test Client (E2E tests)
          - Complete user journeys
          - Multi-step workflows  
          - Form submissions with redirects
          - HTMX endpoint validation
          - Database state verification
          - Faster than browser-based tests
          - No Playwright/browser setup needed
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