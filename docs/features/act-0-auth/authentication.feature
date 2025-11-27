Feature: ✅ FOB-AUTH-LOGIN-1 Authentication and Login
  As a methodology author (Maria)
  I want to securely log into FOB
  So that I can access my playbooks

  Scenario: ✅ AUTH-01 Login with valid credentials
    Given Maria is on the FOB login page
    When she enters valid email and password
    And she clicks [Login]
    Then she is authenticated
    And she is redirected to FOB-DASHBOARD-1

  Scenario: ✅ AUTH-02 Login with invalid credentials
    Given Maria is on the FOB login page
    When she enters invalid credentials
    And she clicks [Login]
    Then she sees "Invalid email or password" error

  Scenario: ✅ AUTH-03 First-time user registration
    Given Maria is a new user
    When she clicks [Sign Up]
    Then she sees the registration form
    When she completes registration
    Then her account is created
    And she is redirected to FOB-ONBOARDING-1

  Scenario: ✅ AUTH-04 Password reset flow
    Given Maria forgot her password
    When she clicks [Forgot Password]
    And she enters her email
    Then she receives a reset link
    When she clicks the link and sets new password
    Then she can login with new password

  Scenario: ✅ AUTH-05 Logout
    Given Maria is logged in
    When she clicks [Logout]
    Then she is logged out
    And she is redirected to login page
