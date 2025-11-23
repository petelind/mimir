# Authentication Feature - Implementation Plan

**Feature**: FOB-AUTH-LOGIN-1 Authentication and Login  
**Feature File**: `docs/features/act-0-auth/authentication.feature`  
**GitHub Issues**: #7, #8, #9, #10, #11 (AUTH-01 through AUTH-05)  
**Branch**: `feature/auth-scenarios`

---

## Current State Assessment

### ✅ What Exists (Reusable)

1. **Login View (Partial)** - `accounts/views.py::CustomLoginView`
   - Uses Django's `AuthenticationForm` ⚠️ (violates SAO.md "no Django Forms" rule)
   - Session management with remember me (30 days / 2 weeks)
   - Proper logging
   - **Decision**: Rebuild to use custom template validation

2. **Login Template** - `templates/accounts/login.html`
   - Bootstrap 5 styled
   - Has `data-testid` attributes
   - **Decision**: Keep structure, remove Django Form dependencies

3. **Logout View** - `accounts/views.py::custom_logout_view`
   - ✅ Fully implemented and correct
   - **Decision**: Keep as-is

4. **Settings Configuration**
   - LOGIN_URL, LOGIN_REDIRECT_URL configured
   - Session settings configured
   - **Decision**: Update URLs to match convention

5. **Base Template** - `templates/base.html`
   - Bootstrap 5.3.8 + Font Awesome + HTMX
   - **Decision**: Reuse for all auth templates

### ❌ What's Missing

1. **Custom User Model** - Using Django's default User
2. **Registration Views/Templates** - AUTH-03
3. **Password Reset Flow** - AUTH-04  
4. **Dashboard Stub** - FOB-DASHBOARD-1
5. **Onboarding Stub** - FOB-ONBOARDING-1
6. **Integration Tests** - All scenarios
7. **URL Convention Compliance** - `/auth/user/` pattern

### ⚠️ Issues to Fix

1. **URL Pattern**: `/accounts/` → `/auth/` (violates convention)
2. **Django Forms**: Remove `AuthenticationForm`, use manual validation
3. **Missing Stubs**: Dashboard and onboarding pages needed

---

## Clarification Questions

### Q1: User Model
**Question**: SAO.md says "extends Django's standard User model" but no custom fields specified. Start with built-in User?  
**Answer**: YES - Use Django's built-in User. Email field already exists. Can extend later if needed.

### Q2: Email-based Login
**Question**: Login form shows "Username" but docs mention email. Use username or email?  
**Answer**: KEEP USERNAME - Django's default. Email-based login is future enhancement.

### Q3: Password Reset Email
**Question**: AUTH-04 requires "receives a reset link". Use console email backend for MVP?  
**Answer**: YES - Console backend for now. SMTP later.

---

## Implementation Plan

### Phase 0: Preparation

- [ ] **0.1** Create feature branch
  ```bash
  git checkout -b feature/auth-scenarios
  ```

- [ ] **0.2** Read workflow files
  - Read `.windsurf/workflows/dev-2-implement-backend.md`
  - Read `.windsurf/workflows/dev-3-implement-frontend.md`
  - Read `.windsurf/rules/do-github-issues.md`

---

### Phase 1: Fix URL Convention & Django Forms (AUTH-01, AUTH-02)

**Scenario**: AUTH-01 Login with valid credentials, AUTH-02 Login with invalid credentials  
**GitHub Issue**: #7, #8

#### Backend Changes

- [ ] **1.1** Update URL routing
  - **File**: `mimir/urls.py`
  - Change: `path("accounts/", include("accounts.urls"))` → `path("auth/", include("accounts.urls"))`
  
- [ ] **1.2** Update accounts URLs to match convention
  - **File**: `accounts/urls.py`
  - Change: `login/` → `user/login/`
  - Change: `logout/` → `user/logout/`
  - Result: `/auth/user/login/`, `/auth/user/logout/`

- [ ] **1.3** Rebuild login view without Django Forms
  - **File**: `accounts/views.py`
  - Remove: `from django.contrib.auth.views import LoginView`
  - Remove: `class CustomLoginView(LoginView)`
  - Create: `def login_view(request)` with manual validation
  - Implement: POST handler with `authenticate()` and `login()`
  - Implement: Remember me checkbox handling
  - Add: Server-side validation errors
  - Add: Logging for auth attempts
  - Re-read: `.windsurf/rules/do-docstring-format.md` before implementing
  - Re-read: `.windsurf/rules/informative-logging.md` before implementing

- [ ] **1.4** Update settings.py
  - **File**: `mimir/settings.py`
  - Change: `LOGIN_URL = "/auth/user/login/"`
  - Change: `LOGIN_REDIRECT_URL` (see Phase 2 for dashboard)
  - Change: `LOGOUT_REDIRECT_URL = "/auth/user/login/"`

#### Frontend Changes

- [ ] **1.5** Update login template
  - **File**: `templates/accounts/login.html`
  - Remove: Django Form rendering (`{{ form.username }}`)
  - Add: Manual input fields with Bootstrap classes
  - Add: Server-side error display using `{% if errors %}`
  - Keep: `data-testid` attributes
  - Add: Font Awesome icons per IA guidelines
  - Add: Bootstrap tooltips on buttons
  - Ensure: Follows validation pattern from IA_guidelines.md (red errors under fields)
  - Re-read: `.windsurf/rules/tooltips.md` before implementing
  - Re-read: `.windsurf/rules/do-semantic-versioning-on-ui-elements.md`

#### Tests

- [ ] **1.6** Create integration test for AUTH-01
  - **File**: `tests/integration/test_auth_login.py`
  - Test: `test_login_with_valid_credentials()`
    - Create test user
    - POST to `/auth/user/login/`
    - Assert: 302 redirect to dashboard
    - Assert: User is authenticated
    - Assert: Session created
  - Re-read: `.windsurf/rules/do-not-mock-in-integration-tests.md` before implementing

- [ ] **1.7** Create integration test for AUTH-02
  - **File**: `tests/integration/test_auth_login.py`
  - Test: `test_login_with_invalid_credentials()`
    - POST invalid credentials to `/auth/user/login/`
    - Assert: 200 status (stays on page)
    - Assert: Error message in response
    - Assert: User not authenticated

- [ ] **1.8** Commit & Update Issue #7 #8
  - Re-read: `.windsurf/rules/do-follow-commit-convention.md`
  - Commit message: `feat(auth): implement login with custom validation (AUTH-01, AUTH-02)`
  - Body: List changes, mention no Django Forms per SAO.md
  - Update GitHub issues #7 and #8 with progress

---

### Phase 2: Create Dashboard & Onboarding Stubs

**Purpose**: Provide redirect targets for authentication flows

#### Backend - Dashboard Stub

- [ ] **2.1** Create dashboard view
  - **File**: `methodology/views.py` (or new `accounts/views.py`)
  - Function: `def dashboard(request)`
  - Decorator: `@login_required`
  - Return: `render(request, 'dashboard.html')`
  - Re-read: `.windsurf/rules/do-docstring-format.md`

- [ ] **2.2** Add dashboard URL
  - **File**: `mimir/urls.py`
  - Add: `path('dashboard/', views.dashboard, name='dashboard')`

#### Frontend - Dashboard Stub

- [ ] **2.3** Create dashboard template
  - **File**: `templates/dashboard.html`
  - Extends: `base.html`
  - Content: Simple card with "FOB-DASHBOARD-1 - This will be the dashboard"
  - Add: `data-testid="dashboard-stub"`
  - Note: "Dashboard implementation tracked in navigation.feature issues #17-22"

#### Backend - Onboarding Stub

- [ ] **2.4** Create onboarding view
  - **File**: `accounts/views.py`
  - Function: `def onboarding(request)`
  - Decorator: `@login_required`
  - Return: `render(request, 'accounts/onboarding.html')`

- [ ] **2.5** Add onboarding URL
  - **File**: `accounts/urls.py`
  - Add: `path('user/onboarding/', views.onboarding, name='onboarding')`
  - Result: `/auth/user/onboarding/`

#### Frontend - Onboarding Stub

- [ ] **2.6** Create onboarding template
  - **File**: `templates/accounts/onboarding.html`
  - Extends: `base.html`
  - Content: Simple card with "FOB-ONBOARDING-1 - This will be onboarding"
  - Add: `data-testid="onboarding-stub"`
  - Note: "Onboarding implementation tracked in onboarding.feature issues #12-16"

#### Update Settings

- [ ] **2.7** Update LOGIN_REDIRECT_URL
  - **File**: `mimir/settings.py`
  - Change: `LOGIN_REDIRECT_URL = "/dashboard/"`

#### Tests

- [ ] **2.8** Test dashboard stub
  - **File**: `tests/integration/test_dashboard_stub.py`
  - Test: `test_dashboard_requires_login()`
  - Test: `test_dashboard_displays_stub()`

- [ ] **2.9** Test onboarding stub
  - **File**: `tests/integration/test_onboarding_stub.py`  
  - Test: `test_onboarding_requires_login()`
  - Test: `test_onboarding_displays_stub()`

- [ ] **2.10** Commit stubs
  - Commit: `feat(stubs): add dashboard and onboarding placeholder pages`
  - Body: "Stub pages for FOB-DASHBOARD-1 and FOB-ONBOARDING-1. Full implementation tracked separately."

---

### Phase 3: User Registration (AUTH-03)

**Scenario**: AUTH-03 First-time user registration  
**GitHub Issue**: #9

#### Backend

- [ ] **3.1** Create registration view
  - **File**: `accounts/views.py`
  - Function: `def register(request)`
  - GET: Show registration form
  - POST: 
    - Validate: username, email, password, password_confirm
    - Check: username/email uniqueness
    - Create: User with `User.objects.create_user()`
    - Login: Auto-login new user
    - Redirect: `/auth/user/onboarding/`
  - Add: Extensive logging per rules
  - Re-read: `.windsurf/rules/informative-logging.md`
  - Re-read: `.windsurf/rules/do-docstring-format.md`

- [ ] **3.2** Add registration URL
  - **File**: `accounts/urls.py`
  - Add: `path('user/register/', views.register, name='register')`

#### Frontend

- [ ] **3.3** Create registration template
  - **File**: `templates/accounts/register.html`
  - Extends: `base.html`
  - Form fields:
    - Username (required)
    - Email (required, with email validation)
    - Password (required, min 8 chars)
    - Confirm Password (must match)
  - Add: Field-level validation errors (red text under fields)
  - Add: Font Awesome icons
  - Add: Bootstrap tooltips
  - Add: Link to login page
  - Add: `data-testid` attributes
  - Re-read: `.windsurf/rules/tooltips.md`

- [ ] **3.4** Add registration link to login template
  - **File**: `templates/accounts/login.html`
  - Add: "Don't have an account? [Sign Up]" link below form

#### Tests

- [ ] **3.5** Create registration integration tests
  - **File**: `tests/integration/test_auth_registration.py`
  - Test: `test_register_new_user()`
    - POST valid registration data
    - Assert: User created in database
    - Assert: User auto-logged in
    - Assert: Redirected to `/auth/user/onboarding/`
  - Test: `test_register_duplicate_username()`
    - Create user
    - Attempt register with same username
    - Assert: Error message displayed
  - Test: `test_register_password_mismatch()`
    - POST with mismatched passwords
    - Assert: Error message
  - Test: `test_register_invalid_email()`
  - Re-read: `.windsurf/rules/do-not-mock-in-integration-tests.md`

- [ ] **3.6** Commit & Update Issue #9
  - Commit: `feat(auth): implement user registration (AUTH-03)`
  - Update: GitHub issue #9 with completion status

---

### Phase 4: Password Reset Flow (AUTH-04)

**Scenario**: AUTH-04 Password reset flow  
**GitHub Issue**: #10

#### Backend

- [ ] **4.1** Configure email backend
  - **File**: `mimir/settings.py`
  - Add: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
  - Note: Console backend for MVP, SMTP for production

- [ ] **4.2** Create password reset request view
  - **File**: `accounts/views.py`
  - Function: `def password_reset_request(request)`
  - POST: Generate reset token, send email
  - Use: Django's `PasswordResetTokenGenerator`
  - Re-read: `.windsurf/rules/do-docstring-format.md`

- [ ] **4.3** Create password reset confirm view
  - **File**: `accounts/views.py`
  - Function: `def password_reset_confirm(request, uidb64, token)`
  - Validate: Token and user ID
  - POST: Set new password
  - Redirect: Login with success message

- [ ] **4.4** Add password reset URLs
  - **File**: `accounts/urls.py`
  - Add: `path('user/password-reset/', views.password_reset_request, name='password_reset')`
  - Add: `path('user/password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm')`

#### Frontend

- [ ] **4.5** Create password reset request template
  - **File**: `templates/accounts/password_reset.html`
  - Form: Email input
  - Message: "Enter your email to receive a reset link"
  - Add: `data-testid` attributes

- [ ] **4.6** Create password reset confirm template
  - **File**: `templates/accounts/password_reset_confirm.html`
  - Form: New password, confirm password
  - Add: Password strength indicator (optional)
  - Add: `data-testid` attributes

- [ ] **4.7** Create password reset email template
  - **File**: `templates/accounts/password_reset_email.txt`
  - Content: Plain text with reset link

- [ ] **4.8** Add "Forgot Password" link to login
  - **File**: `templates/accounts/login.html`
  - Add: Link below form

#### Tests

- [ ] **4.9** Create password reset integration tests
  - **File**: `tests/integration/test_auth_password_reset.py`
  - Test: `test_password_reset_request()`
    - POST email to reset view
    - Assert: Email sent (check mail.outbox)
    - Assert: Reset link generated
  - Test: `test_password_reset_confirm_valid_token()`
    - Generate token
    - POST new password
    - Assert: Password changed
    - Assert: Can login with new password
  - Test: `test_password_reset_confirm_invalid_token()`
  - Re-read: `.windsurf/rules/do-not-mock-in-integration-tests.md`

- [ ] **4.10** Commit & Update Issue #10
  - Commit: `feat(auth): implement password reset flow (AUTH-04)`
  - Update: GitHub issue #10

---

### Phase 5: Logout Tests (AUTH-05)

**Scenario**: AUTH-05 Logout  
**GitHub Issue**: #11  
**Note**: Logout view already implemented, only tests needed

#### Tests

- [ ] **5.1** Create logout integration tests
  - **File**: `tests/integration/test_auth_logout.py`
  - Test: `test_logout_authenticated_user()`
    - Login user
    - GET `/auth/user/logout/`
    - Assert: User logged out
    - Assert: Redirected to `/auth/user/login/`
    - Assert: Success message displayed
  - Test: `test_logout_unauthenticated_user()`
    - GET logout without login
    - Assert: Redirected to login (no error)

- [ ] **5.2** Commit & Update Issue #11
  - Commit: `test(auth): add logout integration tests (AUTH-05)`
  - Update: GitHub issue #11 (mark complete)

---

### Phase 6: E2E Testing

**Purpose**: Test complete user journeys

- [ ] **6.1** Create E2E test for complete auth flow
  - **File**: `tests/e2e/test_auth_complete_flow.py`
  - Use: Django LiveServerTestCase + pytest
  - Flow:
    1. Visit login page
    2. Click "Sign Up"
    3. Complete registration
    4. Redirected to onboarding
    5. Return to dashboard
    6. Logout
  - Re-read: `.windsurf/rules/do-runner.md`

- [ ] **6.2** Commit E2E tests
  - Commit: `test(auth): add E2E tests for complete authentication flow`

---

### Phase 7: Documentation & Cleanup

- [ ] **7.1** Update README if needed
  - Add: Default user creation command
  - Add: Testing instructions

- [ ] **7.2** Run all tests
  ```bash
  pytest tests/ -v
  ```

- [ ] **7.3** Check test coverage
  ```bash
  pytest --cov=accounts --cov-report=html
  ```

- [ ] **7.4** Final commit
  - Commit: `docs(auth): update documentation for authentication implementation`

- [ ] **7.5** Push branch
  ```bash
  git push origin feature/auth-scenarios
  ```

- [ ] **7.6** Create Pull Request
  - Title: "feat(auth): Implement authentication scenarios (AUTH-01 to AUTH-05)"
  - Body: Link to issues #7-11, describe changes
  - Request review per `.windsurf/rules/cp-2-review-copilot-work.md`

---

## Test Summary

### Unit Tests
- `tests/unit/test_auth_config.py` - ✅ Already exists

### Integration Tests (NEW)
- `tests/integration/test_auth_login.py` - AUTH-01, AUTH-02
- `tests/integration/test_auth_registration.py` - AUTH-03
- `tests/integration/test_auth_password_reset.py` - AUTH-04
- `tests/integration/test_auth_logout.py` - AUTH-05
- `tests/integration/test_dashboard_stub.py` - Dashboard stub
- `tests/integration/test_onboarding_stub.py` - Onboarding stub

### E2E Tests (NEW)
- `tests/e2e/test_auth_complete_flow.py` - Full user journey

**Total New Tests**: ~20 test functions

---

## Success Criteria

- ✅ All 5 authentication scenarios pass integration tests
- ✅ No Django Forms used (per SAO.md)
- ✅ URL conventions followed (`/auth/user/*`)
- ✅ Dashboard and onboarding stubs in place
- ✅ Bootstrap toasts for success messages
- ✅ Field-level validation errors per IA guidelines
- ✅ Font Awesome icons and tooltips on all buttons
- ✅ All `data-testid` attributes present for testing
- ✅ Extensive logging per project rules
- ✅ Test coverage > 90% for accounts app
- ✅ Issues #7-11 marked complete

---

## Dependencies

**Python Packages** (already in requirements.txt):
- Django 5.2.8
- pytest-django
- No additional packages needed

**Documentation References**:
- `docs/architecture/SAO.md` - Architecture patterns
- `docs/ux/IA_guidelines.md` - UI/UX patterns
- `.windsurf/rules/*.md` - Development rules

---

## Estimated Scope

- **5 Scenarios**: AUTH-01 through AUTH-05
- **2 Stub Pages**: Dashboard, Onboarding
- **6 Views**: Login, logout, register, password_reset (2 views), dashboard, onboarding
- **6 Templates**: Login, register, password_reset (2), email, dashboard, onboarding  
- **7 Test Files**: ~20 test functions total
- **URL Updates**: Restructure to `/auth/user/` pattern

**Complexity**: Medium (login already exists, need to rebuild without Forms)
