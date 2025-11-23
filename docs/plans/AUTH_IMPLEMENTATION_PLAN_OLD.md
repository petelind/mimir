# AUTH - User Authentication and Session Management
## Implementation Plan

**Feature**: Authentication system for FOB web interface  
**Feature File**: `docs/features/login.feature`  
**Scenarios**: 10 scenarios (6 @core, 4 @error)  
**Branch**: `feature/auth-login`

---

## Current State Assessment

### What Exists
- ✅ Django 5.2.8 project configured
- ✅ Bootstrap 5.3.8 + Font Awesome + HTMX in base template
- ✅ Base template with navbar (includes user auth display placeholders)
- ✅ Methodology index view (unprotected)
- ✅ URL routing configured

### What's Missing
- ❌ Custom User model
- ❌ Authentication views (login, logout)
- ❌ Login template
- ❌ Authentication middleware configuration
- ❌ Login required decorators on protected views
- ❌ Tests directory and test infrastructure
- ❌ E2E tests with Playwright

### Reusable Components
- ✅ `base.html` template - already has auth UI elements (`user.username`, logout link)
- ✅ `templates/methodology/index.html` - needs `@login_required` protection
- ⚠️ No existing authentication views to reuse - will build from scratch using Django's built-in auth

---

## Clarification Questions

### 1. Custom User Model
**Question**: Do we need a custom User model extending Django's User, or can we use Django's built-in User model?

**Context**: Feature spec says "Custom User model extends standard Django User" but doesn't specify what fields we need to add.

**Options**:
- **A)** Use Django's built-in User model (simpler, faster)
- **B)** Create custom User model with additional fields (email required, etc.)

**Recommendation**: Start with Django's built-in User (Option A). If we need custom fields later, we can migrate.

### 2. Remember Me Duration
**Question**: Scenario AUTH 4.2 specifies "30 days" for remember me. Is this the desired session duration?

**Context**: Django default is 2 weeks. 30 days is longer than typical.

**Recommendation**: Confirm 30 days or adjust to Django default (14 days).

### 3. Default Admin User
**Question**: Should we create a management command to create the default admin user automatically on first run?

**Context**: Feature spec says "default admin user with default admin password exists by default"

**Options**:
- **A)** Add to README with manual `createsuperuser` command
- **B)** Create custom management command for automated setup
- **C)** Use Django fixtures

**Recommendation**: Option B - custom management command for better UX.

### 4. Error Message Customization
**Question**: Should we use Django's default error messages or customize them?

**Context**: Scenarios specify exact error messages like "Please enter a correct username and password. Note that both fields may be case-sensitive."

**Recommendation**: This IS Django's default message, so we're good.

### 5. Test Strategy
**Question**: Should we implement E2E tests with Playwright now or defer to later?

**Context**: Feature has 10 scenarios with specific `data-testid` attributes defined. We have pytest-playwright in requirements.

**Options**:
- **A)** Implement unit + integration tests now, E2E tests later
- **B)** Implement all tests (unit + integration + E2E) now

**Recommendation**: Option B - implement all tests. Scenarios are well-defined with `data-testid` attributes.

---

## Implementation Plan

### Phase 0: Setup and Branch Management

- [ ] **Task 0.1**: Reset plan and create new branch
  - Check for work in progress per `.windsurf/rules/do-add-todos-for-incomplete-items.md`
  - Create and checkout branch: `git checkout -b feature/auth-login`
  
- [ ] **Task 0.2**: Create tests directory structure
  - Create `tests/` directory
  - Create `tests/__init__.py`
  - Create `tests/integration/` directory
  - Create `tests/integration/__init__.py`
  - Create `tests/unit/` directory
  - Create `tests/unit/__init__.py`
  - Create `tests/e2e/` directory
  - Create `tests/e2e/__init__.py`

- [ ] **Task 0.3**: Install Playwright browsers
  - Run: `source venv/bin/activate && playwright install`
  
- [ ] **Task 0.4**: Commit initial setup
  - Commit: `chore(tests): add test directory structure and install Playwright browsers`
  - Push to remote

---

### Phase 1: Backend - User Model and Authentication Setup

**Scenarios Covered**: Foundation for all scenarios

- [ ] **Task 1.1**: Review `.windsurf/rules/do-docstring-format.md` before implementing

- [ ] **Task 1.2**: Configure authentication settings
  - Update `mimir/settings.py`:
    - Add `LOGIN_URL = '/accounts/login/'`
    - Add `LOGIN_REDIRECT_URL = '/'`
    - Add `LOGOUT_REDIRECT_URL = '/accounts/login/'`
    - Configure session settings for remember me (30 days if checkbox checked)
  - Create docstrings following the format rule

- [ ] **Task 1.3**: Create authentication app structure
  - Run: `python manage.py startapp accounts`
  - Add `accounts` to `INSTALLED_APPS` in settings
  - Update `accounts/apps.py` with proper app config

- [ ] **Task 1.4**: Write unit tests for auth configuration
  - File: `tests/unit/test_auth_config.py`
  - Test LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
  - Test session configuration

- [ ] **Task 1.5**: Run tests and verify
  - Run: `pytest tests/unit/test_auth_config.py -v`

- [ ] **Task 1.6**: Commit auth configuration
  - Commit: `feat(auth): configure authentication settings and create accounts app`
  - Push to remote

---

### Phase 2: Backend - Authentication Views

**Scenarios Covered**: AUTH 1.1, 1.2, 2.1, 2.2, 2.3, 4.2

- [ ] **Task 2.1**: Review `.windsurf/rules/do-docstring-format.md` before implementing

- [ ] **Task 2.2**: Create login view
  - File: `accounts/views.py`
  - Class: `CustomLoginView(LoginView)`
  - Override to handle "remember me" checkbox
  - Handle session duration based on remember me
  - Add proper docstrings with examples
  - All methods 20-30 lines max (`.windsurf/rules/do-write-concise-methods.md`)

- [ ] **Task 2.3**: Create logout view
  - File: `accounts/views.py`
  - Function: `custom_logout_view(request)`
  - Add success message "You have been logged out successfully"
  - Add proper docstrings with examples

- [ ] **Task 2.4**: Create URL patterns
  - File: `accounts/urls.py`
  - Pattern: `/accounts/login/` → CustomLoginView
  - Pattern: `/accounts/logout/` → custom_logout_view
  - Include in main `mimir/urls.py`

- [ ] **Task 2.5**: Write unit tests for authentication views
  - File: `tests/unit/test_auth_views.py`
  - Test login view GET (displays form)
  - Test login view POST with valid credentials
  - Test login view POST with invalid credentials (wrong password)
  - Test login view POST with non-existent user
  - Test login view POST with empty form
  - Test remember me functionality
  - Test logout view

- [ ] **Task 2.6**: Run tests and verify
  - Run: `pytest tests/unit/test_auth_views.py -v`

- [ ] **Task 2.7**: Commit authentication views
  - Commit: `feat(auth): implement login and logout views with remember me`
  - Push to remote

---

### Phase 3: Frontend - Login Template

**Scenarios Covered**: AUTH 1.1, 2.1, 2.2, 2.3

- [ ] **Task 3.1**: Review `.windsurf/rules/do-semantic-versioning-on-ui-elements.md` before implementing

- [ ] **Task 3.2**: Create login template
  - File: `templates/accounts/login.html`
  - Extend `base.html`
  - Bootstrap 5 form styling
  - Include all `data-testid` attributes from scenarios:
    - `login-form`
    - `login-username-input`
    - `login-password-input`
    - `login-remember-checkbox`
    - `login-submit-button`
    - `login-error-message`
    - `username-field-error`
    - `password-field-error`
  - Display Django form errors
  - CSRF token included

- [ ] **Task 3.3**: Update base template navbar
  - File: `templates/base.html`
  - Ensure `{% if user.is_authenticated %}` block shows username
  - Ensure logout link has `data-testid="logout-link"`
  - Ensure login link has `data-testid="login-link"` (for logged out state)

- [ ] **Task 3.4**: Write template rendering tests
  - File: `tests/integration/test_login_template.py`
  - Test login template renders correctly
  - Test all form fields present
  - Test all `data-testid` attributes present
  - Test error message display

- [ ] **Task 3.5**: Run tests and verify
  - Run: `pytest tests/integration/test_login_template.py -v`

- [ ] **Task 3.6**: Commit login template
  - Commit: `feat(auth): create login template with Bootstrap styling and test IDs`
  - Push to remote

---

### Phase 4: Backend - Access Control (Protected Views)

**Scenarios Covered**: AUTH 3.1, 3.2, 3.3, 4.1

- [ ] **Task 4.1**: Review `.windsurf/rules/do-docstring-format.md` before implementing

- [ ] **Task 4.2**: Add login required decorator to methodology index
  - File: `methodology/views.py`
  - Add `@login_required` decorator to `index` view
  - Update docstring with authentication requirement

- [ ] **Task 4.3**: Create placeholder PIP views (for testing)
  - File: `methodology/views.py`
  - Function: `pip_list(request)` - protected
  - Function: `pip_review(request, pip_id)` - protected
  - Add proper docstrings
  - These are stubs for testing auth; full PIP feature comes later

- [ ] **Task 4.4**: Add PIP URL patterns
  - File: `methodology/urls.py` (create if doesn't exist)
  - Pattern: `/pip/list/` → pip_list
  - Pattern: `/pip/review/<uuid:pip_id>/` → pip_review
  - Include in main `mimir/urls.py`

- [ ] **Task 4.5**: Create placeholder PIP templates (for testing)
  - File: `templates/methodology/pip_list.html`
  - File: `templates/methodology/pip_review.html`
  - Include `data-testid="pip-review-form"` in review template
  - Minimal content - just for auth testing

- [ ] **Task 4.6**: Write integration tests for access control
  - File: `tests/integration/test_access_control.py`
  - Test unauthenticated access to `/` redirects to login
  - Test unauthenticated access to `/pip/review/...` redirects to login
  - Test authenticated access to `/` succeeds
  - Test authenticated access to `/pip/review/...` succeeds
  - Test `?next=` parameter preserved in redirects

- [ ] **Task 4.7**: Run tests and verify
  - Run: `pytest tests/integration/test_access_control.py -v`

- [ ] **Task 4.8**: Commit access control
  - Commit: `feat(auth): protect views with login_required decorator`
  - Push to remote

---

### Phase 5: Backend - Session Management

**Scenarios Covered**: AUTH 4.1, 4.2

- [ ] **Task 5.1**: Review `.windsurf/rules/do-docstring-format.md` before implementing

- [ ] **Task 5.2**: Configure session middleware settings
  - File: `mimir/settings.py`
  - Set `SESSION_COOKIE_AGE` defaults
  - Set `SESSION_SAVE_EVERY_REQUEST = True` for session refresh

- [ ] **Task 5.3**: Update login view for session duration
  - File: `accounts/views.py`
  - Override `form_valid()` in CustomLoginView
  - Set `request.session.set_expiry()` based on remember me:
    - If remember me: 30 days (2592000 seconds)
    - If not: Django default (2 weeks)

- [ ] **Task 5.4**: Write integration tests for session management
  - File: `tests/integration/test_session_management.py`
  - Test session persists across page navigations
  - Test session expiry with remember me (30 days)
  - Test session expiry without remember me (default)
  - Test session cookie set on login
  - Test session cookie deleted on logout

- [ ] **Task 5.5**: Run tests and verify
  - Run: `pytest tests/integration/test_session_management.py -v`

- [ ] **Task 5.6**: Commit session management
  - Commit: `feat(auth): implement session management with remember me`
  - Push to remote

---

### Phase 6: Management Commands

**Scenarios Covered**: Setup for all scenarios (default admin user)

- [ ] **Task 6.1**: Review `.windsurf/rules/do-docstring-format.md` before implementing

- [ ] **Task 6.2**: Create management command for default user
  - File: `accounts/management/commands/create_default_admin.py`
  - Create admin user if doesn't exist
  - Username: `admin`, Password: `admin`
  - Add proper docstrings

- [ ] **Task 6.3**: Write unit tests for management command
  - File: `tests/unit/test_management_commands.py`
  - Test command creates user
  - Test command is idempotent (doesn't fail if user exists)

- [ ] **Task 6.4**: Update README or setup documentation
  - Add section on running `python manage.py create_default_admin`

- [ ] **Task 6.5**: Run tests and verify
  - Run: `pytest tests/unit/test_management_commands.py -v`
  - Run command manually: `python manage.py create_default_admin`

- [ ] **Task 6.6**: Commit management command
  - Commit: `feat(auth): add management command for default admin user`
  - Push to remote

---

### Phase 7: E2E Tests with Playwright

**Scenarios Covered**: ALL scenarios (AUTH 1.1 through AUTH 4.2)

- [ ] **Task 7.1**: Review `.windsurf/workflows/dev-4-e2e-tests.md` before implementing

- [ ] **Task 7.2**: Create pytest configuration for Playwright
  - File: `pytest.ini` or update existing
  - Configure Django LiveServerTestCase + Playwright
  - Set up test database

- [ ] **Task 7.3**: Create E2E test base class
  - File: `tests/e2e/conftest.py`
  - Configure Playwright fixtures
  - LiveServerTestCase integration
  - Helper methods for common actions (login, logout)

- [ ] **Task 7.4**: Implement E2E test: AUTH 1.1 (Valid login)
  - File: `tests/e2e/test_auth_login.py`
  - Test class: `TestValidLogin`
  - Navigate to login page
  - Enter valid credentials
  - Click submit
  - Assert redirect to `/`
  - Assert methodology-explorer visible
  - Assert "Logged in as: admin" displayed
  - Assert session cookie set

- [ ] **Task 7.5**: Implement E2E test: AUTH 1.2 (Logout)
  - File: `tests/e2e/test_auth_login.py`
  - Test class: `TestLogout`
  - Login first (helper method)
  - Click logout link
  - Assert redirect to login page
  - Assert success message
  - Assert session cookie deleted
  - Attempt to access `/`, assert redirect to login with `?next=/`

- [ ] **Task 7.6**: Implement E2E tests: AUTH 2.x (Error scenarios)
  - File: `tests/e2e/test_auth_errors.py`
  - Test AUTH 2.1: Incorrect password
  - Test AUTH 2.2: Non-existent user
  - Test AUTH 2.3: Empty form

- [ ] **Task 7.7**: Implement E2E tests: AUTH 3.x (Access control)
  - File: `tests/e2e/test_auth_access_control.py`
  - Test AUTH 3.1: Unauthenticated redirect
  - Test AUTH 3.2: Authenticated PIP access
  - Test AUTH 3.3: Unauthenticated PIP redirect

- [ ] **Task 7.8**: Implement E2E tests: AUTH 4.x (Session management)
  - File: `tests/e2e/test_auth_sessions.py`
  - Test AUTH 4.1: Session persistence
  - Test AUTH 4.2: Remember me checkbox

- [ ] **Task 7.9**: Run all E2E tests
  - Run: `pytest tests/e2e/ -v --headed` (for visual debugging)
  - Run: `pytest tests/e2e/ -v` (headless for CI)

- [ ] **Task 7.10**: Commit E2E tests
  - Commit: `test(auth): add comprehensive E2E tests with Playwright`
  - Push to remote

---

### Phase 8: Integration Testing and Final Verification

**Scenarios Covered**: ALL

- [ ] **Task 8.1**: Run complete test suite
  - Run: `pytest tests/ -v --tb=short`
  - Ensure all tests pass

- [ ] **Task 8.2**: Manual testing checklist
  - [ ] Login with valid credentials
  - [ ] Login with invalid credentials (wrong password)
  - [ ] Login with non-existent user
  - [ ] Login with empty form
  - [ ] Logout successfully
  - [ ] Access protected page without login (redirects)
  - [ ] Access protected page with login (succeeds)
  - [ ] Remember me checkbox works
  - [ ] Session persists across pages
  - [ ] Navbar shows username when logged in

- [ ] **Task 8.3**: Code review checklist
  - [ ] All docstrings follow `.windsurf/rules/do-docstring-format.md`
  - [ ] All methods follow `.windsurf/rules/do-write-concise-methods.md`
  - [ ] All UI elements have semantic `data-testid` attributes
  - [ ] No hardcoded strings - use Django settings
  - [ ] Logging added per `.windsurf/rules/add-logging.md`

- [ ] **Task 8.4**: Update documentation
  - File: `README.md`
  - Add authentication section
  - Document default admin user
  - Document login URL

- [ ] **Task 8.5**: Run Definition of Done checklist
  - Follow `.windsurf/workflows/dev-5-check-dod.md`

- [ ] **Task 8.6**: Final commit and push
  - Commit: `docs(auth): update README with authentication documentation`
  - Push to remote

---

### Phase 9: Pull Request and GitHub Issue Management

**Scenarios Covered**: ALL

- [ ] **Task 9.1**: Review `.windsurf/rules/do-github-issues.md` before proceeding

- [ ] **Task 9.2**: Create or update GitHub issue
  - Issue title: `feat(auth): Implement user authentication and session management`
  - Link to feature file: `docs/features/login.feature`
  - List all 10 scenarios
  - Add labels: `enhancement`, `auth`, `core`

- [ ] **Task 9.3**: Create pull request
  - Base branch: `main`
  - Compare branch: `feature/auth-login`
  - PR title: `feat(auth): Implement user authentication and session management`
  - PR description:
    - Link to GitHub issue
    - Summary of changes
    - Testing performed
    - Checklist of completed scenarios

- [ ] **Task 9.4**: Link PR to issue
  - Add "Closes #X" or "Fixes #X" in PR description

- [ ] **Task 9.5**: Update implementation plan status
  - Mark all tasks as complete in this file
  - Commit: `docs(auth): mark implementation plan as complete`

---

## Test Coverage Summary

### Unit Tests (Pure Logic)
- `tests/unit/test_auth_config.py` - Settings validation
- `tests/unit/test_auth_views.py` - View logic
- `tests/unit/test_management_commands.py` - Command logic

### Integration Tests (Database + Views)
- `tests/integration/test_login_template.py` - Template rendering
- `tests/integration/test_access_control.py` - Authorization
- `tests/integration/test_session_management.py` - Session behavior

### E2E Tests (Full Browser)
- `tests/e2e/test_auth_login.py` - AUTH 1.1, 1.2
- `tests/e2e/test_auth_errors.py` - AUTH 2.1, 2.2, 2.3
- `tests/e2e/test_auth_access_control.py` - AUTH 3.1, 3.2, 3.3
- `tests/e2e/test_auth_sessions.py` - AUTH 4.1, 4.2

**Total Test Files**: 10  
**Estimated Test Count**: 35-40 tests

---

## Dependencies Required

Already in `requirements.txt`:
- ✅ Django >= 5.0
- ✅ pytest >= 8.0
- ✅ pytest-django >= 4.0
- ✅ playwright >= 1.40.0
- ✅ pytest-playwright >= 0.4.0

No additional dependencies needed.

---

## Key Design Decisions

1. **Use Django's Built-in Auth**: No custom User model initially. Keeps things simple.

2. **Remember Me Duration**: 30 days as specified in scenarios (can be adjusted).

3. **Session Management**: Use Django's session framework with custom expiry handling.

4. **Testing Strategy**: Unit → Integration → E2E progression. All tests implemented.

5. **Template Approach**: Extend `base.html`, use Bootstrap 5 styling, include all `data-testid` attributes.

6. **Error Handling**: Use Django's default error messages (they match scenario requirements).

7. **Logging**: Add extensive logging per `.windsurf/rules/add-logging.md`:
   - Log all login attempts (success/failure)
   - Log logout actions
   - Log access control redirects
   - Use logs/app.log for troubleshooting

---

## Estimated Complexity

**Total Tasks**: 63 tasks across 9 phases  
**Complexity**: Medium  
**Risk Areas**:
- E2E test setup with Playwright + Django LiveServerTestCase (new territory)
- Session expiry testing (time-sensitive)
- Remember me checkbox behavior across browser restarts

**Mitigation**:
- Follow `.windsurf/workflows/dev-4-e2e-tests.md` carefully
- Use pytest fixtures for E2E test setup
- Test session behavior with explicit cookie inspection

---

## Success Criteria

- [ ] All 10 scenarios from `login.feature` pass E2E tests
- [ ] All unit and integration tests pass
- [ ] Code follows all `.windsurf/rules/` guidelines
- [ ] Documentation updated
- [ ] GitHub issue created/updated
- [ ] Pull request created and linked to issue
- [ ] Definition of Done checklist complete

---

## Notes

- This is the first feature implementation for the FOB web UI
- Sets the pattern for future feature development
- Authentication is foundational - all other features will depend on it
- MCP interface intentionally excluded (process isolation = no auth needed)
