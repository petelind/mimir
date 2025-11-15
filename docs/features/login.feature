Feature: AUTH - User Authentication and Session Management
# Icon: 🔐
# ID Prefix: AUTH

## Feature Specification

**User**: Software Engineer / Methodology Manager  
**Goal**: Access the FOB web interface to view methodologies, review PIPs, and manage local methodology customizations  
**Context**: FOB is a single-user desktop application that requires authentication to prevent unauthorized access to methodology data and work orders. While the MCP interface runs without auth (process isolation), the web UI requires login to ensure only the authorized user can approve PIPs and modify methodologies.

**Assumptions**:
- User management is done via Django admin console (`python manage.py createsuperuser`)
- Custom User model extends standard Django User
- Default admin user (username: `admin`, password: `admin`) exists after initial setup
- Sessions use Django's default session middleware
- Login page is at `/accounts/login/`
- After successful login, user is redirected to methodology explorer at `/`
- Logout redirects to login page

**Affected Pages/Views**:
- **Existing**: None (new implementation)
- **To Build**:
  - Login page (`/accounts/login/`) - Django template with HTMX form
  - Logout endpoint (`/accounts/logout/`) - Django view
  - Protected views (methodology explorer, PIP review)

---

@core
Scenario: AUTH 1.1 Engineer logs in with valid credentials
  Given the FOB application is running on "http://localhost:8000"
  And the user "admin" with password "admin" exists in the database
  And the user navigates to "http://localhost:8000/accounts/login/"
  When the user enters "admin" into the field with data-testid "login-username-input"
  And the user enters "admin" into the field with data-testid "login-password-input"
  And the user clicks the button with data-testid "login-submit-button"
  Then the user should be redirected to "http://localhost:8000/"
  And the page should display the element with data-testid "methodology-explorer"
  And the navigation bar should display "Logged in as: admin"
  And the session cookie "sessionid" should be set

@core
Scenario: AUTH 1.2 Engineer logs out successfully
  Given the user "admin" is logged in at "http://localhost:8000/"
  And the user is on the page "http://localhost:8000/"
  When the user clicks the link with data-testid "logout-link"
  Then the user should be redirected to "http://localhost:8000/accounts/login/"
  And the page should display the message "You have been logged out successfully"
  And the session cookie "sessionid" should be deleted
  And attempting to access "http://localhost:8000/" should redirect to "http://localhost:8000/accounts/login/?next=/"

@error
Scenario: AUTH 2.1 Engineer enters incorrect password
  Given the user "admin" with password "admin" exists in the database
  And the user navigates to "http://localhost:8000/accounts/login/"
  When the user enters "admin" into the field with data-testid "login-username-input"
  And the user enters "wrongpassword" into the field with data-testid "login-password-input"
  And the user clicks the button with data-testid "login-submit-button"
  Then the page should remain at "http://localhost:8000/accounts/login/"
  And the element with data-testid "login-error-message" should display "Please enter a correct username and password. Note that both fields may be case-sensitive."
  And the field with data-testid "login-username-input" should retain the value "admin"
  And the field with data-testid "login-password-input" should be empty
  And no session cookie should be set

@error
Scenario: AUTH 2.2 Engineer attempts login with non-existent user
  Given no user with username "nonexistent" exists in the database
  And the user navigates to "http://localhost:8000/accounts/login/"
  When the user enters "nonexistent" into the field with data-testid "login-username-input"
  And the user enters "anypassword" into the field with data-testid "login-password-input"
  And the user clicks the button with data-testid "login-submit-button"
  Then the page should remain at "http://localhost:8000/accounts/login/"
  And the element with data-testid "login-error-message" should display "Please enter a correct username and password. Note that both fields may be case-sensitive."
  And no session cookie should be set

@error
Scenario: AUTH 2.3 Engineer submits empty login form
  Given the user navigates to "http://localhost:8000/accounts/login/"
  When the user clicks the button with data-testid "login-submit-button"
  Then the page should remain at "http://localhost:8000/accounts/login/"
  And the element with data-testid "username-field-error" should display "This field is required."
  And the element with data-testid "password-field-error" should display "This field is required."
  And no session cookie should be set

@core
Scenario: AUTH 3.1 Unauthenticated user is redirected to login
  Given no user is logged in
  When the user attempts to access "http://localhost:8000/"
  Then the user should be redirected to "http://localhost:8000/accounts/login/?next=/"
  And the page should display the element with data-testid "login-form"

@core
Scenario: AUTH 3.2 Authenticated user accesses protected PIP review page
  Given the user "admin" is logged in at "http://localhost:8000/"
  When the user navigates to "http://localhost:8000/pip/review/a1b2c3d4-e5f6-7890-abcd-ef1234567890/"
  Then the page should display the element with data-testid "pip-review-form"
  And the user should be able to approve or reject the PIP

@core
Scenario: AUTH 3.3 Unauthenticated user cannot access PIP review
  Given no user is logged in
  When the user attempts to access "http://localhost:8000/pip/review/a1b2c3d4-e5f6-7890-abcd-ef1234567890/"
  Then the user should be redirected to "http://localhost:8000/accounts/login/?next=/pip/review/a1b2c3d4-e5f6-7890-abcd-ef1234567890/"

@core
Scenario: AUTH 4.1 Session persists across page navigations
  Given the user "admin" is logged in at "http://localhost:8000/"
  When the user navigates to "http://localhost:8000/methodology/fdd/"
  And the user navigates to "http://localhost:8000/workflow/build-feature/"
  And the user navigates to "http://localhost:8000/pip/list/"
  Then each page should display "Logged in as: admin"
  And the user should not be prompted to log in again
  And the session cookie "sessionid" should remain valid

@core  
Scenario: AUTH 4.2 Remember me checkbox extends session duration
  Given the user navigates to "http://localhost:8000/accounts/login/"
  When the user enters "admin" into the field with data-testid "login-username-input"
  And the user enters "admin" into the field with data-testid "login-password-input"
  And the user checks the checkbox with data-testid "login-remember-checkbox"
  And the user clicks the button with data-testid "login-submit-button"
  Then the session cookie "sessionid" should be set with expiry of 30 days
  And the user should remain logged in across browser restarts