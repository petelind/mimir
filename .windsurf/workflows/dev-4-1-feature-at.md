---
description: Feature Acceptance Tests with Django Test Client
---

# Feature-Level Acceptance Test (AT) Implementation

**Tier 1 Testing:** Fast, comprehensive feature validation using Django Test Client.

**Purpose:** Test all scenarios from a `.feature` file to ensure feature works correctly at the logic level.

**When to use:** For every feature implementation. Run on every commit.

---

## Step 1: Identify Feature Scenarios

```bash
# Review the feature file
cat docs/features/act-X-<feature>/<feature-name>.feature

# List all scenarios
grep "Scenario:" docs/features/act-X-<feature>/<feature-name>.feature
```

**Goal:** Create one test method per scenario (or logical group).

---

## Step 2: Create Test File

```bash
# File naming convention
tests/integration/test_<feature>_<aspect>.py

# Examples:
tests/integration/test_auth_login.py
tests/integration/test_auth_registration.py
tests/integration/test_workflow_create.py
tests/integration/test_activity_crud.py
```

---

## Step 3: Implement Tests with Django Test Client

### 3.1 Test Structure

```python
"""Feature Acceptance Tests for <FEATURE>.

Tests all scenarios from docs/features/act-X-<feature>/<feature>.feature

Uses Django Test Client for fast, reliable testing.
NO browser needed. NO mocking (per project rules).
"""
import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
class Test<FeatureName>:
    """Test <FEATURE-ID>: <Feature description>"""
    
    def test_scenario_happy_path(self):
        """
        Test <SCENARIO-ID>: <Scenario name>
        
        Given: <preconditions>
        When: <action>
        Then: <expected result>
        """
        # Arrange
        client = Client()
        user = User.objects.create_user(username='testuser', password='testpass')
        
        # Act
        response = client.post(reverse('some_view'), {
            'field': 'value',
        })
        
        # Assert
        assert response.status_code == 200
        assert 'expected content' in response.content.decode('utf-8')
    
    def test_scenario_validation_error(self):
        """
        Test <SCENARIO-ID>: <Scenario name>
        
        Given: <preconditions>
        When: <invalid action>
        Then: <error displayed>
        """
        # Arrange
        client = Client()
        
        # Act
        response = client.post(reverse('some_view'), {
            'field': '',  # Invalid
        })
        
        # Assert
        assert response.status_code == 200  # Stays on page
        content = response.content.decode('utf-8')
        assert 'data-testid="field-error"' in content
        assert 'required' in content.lower()
```

### 3.2 Test All Paths

For each feature, test:
- ✅ Happy path (valid input → success)
- ✅ Validation errors (invalid input → error messages)
- ✅ Edge cases (boundary conditions)
- ✅ Authentication/authorization checks
- ✅ Database state changes
- ✅ Redirects and messages

### 3.3 Verification Checklist

For each test, verify:
```python
# HTTP response
assert response.status_code == 200  # or 302 for redirect

# Content verification
content = response.content.decode('utf-8')
assert 'expected text' in content
assert 'data-testid="element"' in content

# Database state
assert Model.objects.filter(field=value).exists()
obj = Model.objects.get(id=obj_id)
assert obj.field == expected_value

# Session/authentication
assert response.wsgi_request.user.is_authenticated
assert response.wsgi_request.user.username == 'testuser'

# Messages
messages = list(response.context['messages'])
assert len(messages) == 1
assert 'success' in str(messages[0]).lower()

# Redirects
assert response.redirect_chain[-1][0] == '/expected/url/'
```

---

## Step 4: Run Tests

```bash
# Run specific feature tests
pytest tests/integration/test_<feature>.py -v

# Run with coverage
pytest tests/integration/test_<feature>.py --cov=<app> -v

# Debug with output
pytest tests/integration/test_<feature>.py -v -s

# Fast feedback - just one test
pytest tests/integration/test_<feature>.py::TestClass::test_method -v
```

---

## Step 5: Document Coverage

Add docstring to test class:

```python
@pytest.mark.django_db
class TestAuthLogin:
    """
    Feature Acceptance Tests for User Login (AUTH-01, AUTH-02)
    
    Coverage from authentication.feature:
    ✅ AUTH-01: Login with valid credentials
       - Redirects to dashboard
       - User is authenticated
       - Remember me sets long session
    
    ✅ AUTH-02: Login with invalid credentials
       - Wrong password → error message
       - Non-existent user → error message
       - Empty fields → validation errors
       - Username preserved on error
    
    Test Strategy:
    - Uses Django Test Client (fast, reliable)
    - Tests all scenarios from feature file
    - Validates HTML responses, redirects, database state
    - No mocking - real database operations
    
    Run: pytest tests/integration/test_auth_login.py -v
    """
```

---

## Key Principles

1. **Fast** - Should run in 1-5 seconds
2. **Comprehensive** - Cover ALL scenarios from .feature file
3. **No Mocking** - Use real database (per project rules)
4. **Clear** - One test per scenario, clear docstrings
5. **Reliable** - No flaky tests, deterministic results

---

## Example: Complete Test File

```python
"""Feature Acceptance Tests for User Registration (AUTH-03).

Tests all scenarios from docs/features/act-0-auth/authentication.feature
"""
import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
class TestUserRegistration:
    """Test AUTH-03: First-time user registration"""
    
    def test_register_new_user_redirects_to_onboarding(self):
        """
        Happy path: New user registers successfully.
        
        Given: User is on registration page
        When: Valid registration data submitted
        Then: User created, auto-logged in, redirected to onboarding
        """
        client = Client()
        
        response = client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
        }, follow=True)
        
        # Assert redirect to onboarding
        assert response.redirect_chain[-1][0] == '/auth/user/onboarding/'
        
        # Assert user created
        assert User.objects.filter(username='newuser').exists()
        user = User.objects.get(username='newuser')
        assert user.email == 'new@example.com'
        
        # Assert auto-logged in
        assert response.wsgi_request.user.is_authenticated
        assert response.wsgi_request.user.username == 'newuser'
    
    def test_register_with_duplicate_username_shows_error(self):
        """
        Error case: Username already exists.
        
        Given: User with username 'existinguser' exists
        When: Registration with same username
        Then: Error message, user not created
        """
        # Arrange
        User.objects.create_user(username='existinguser', password='pass')
        client = Client()
        
        # Act
        response = client.post(reverse('register'), {
            'username': 'existinguser',
            'email': 'different@example.com',
            'password': 'Pass123',
            'password_confirm': 'Pass123',
        })
        
        # Assert stays on page
        assert response.status_code == 200
        
        # Assert error shown
        content = response.content.decode('utf-8')
        assert 'data-testid="username-field-error"' in content
        assert 'already exists' in content.lower() or 'taken' in content.lower()
        
        # Assert no new user created
        assert User.objects.filter(email='different@example.com').count() == 0
    
    # ... more tests for other scenarios
```

---

## When Tests Fail

1. **Read the assertion** - What specifically failed?
2. **Check response.content** - Print HTML to see what was returned
3. **Check database** - Query to see actual state
4. **Check logs** - Review Django logs for errors
5. **Debug with pdb** - Add `import pdb; pdb.set_trace()`

---

## Next Steps

After implementing Feature ATs:
1. Run tests: `pytest tests/integration/test_<feature>.py -v`
2. Verify coverage: All scenarios from .feature file tested
3. Commit with message: `test(<feature>): add feature acceptance tests`
4. Consider if feature needs Journey Certification test (dev-4-2)
