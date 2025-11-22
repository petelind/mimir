Feature: FOB-ROLES-VIEW_ROLE-1 View Role Details
  As a methodology author (Maria)
  I want to view role details
  So that I can understand responsibilities

  Background:
    Given Maria is authenticated in FOB
    And she is viewing role "Frontend Developer"
    And the role belongs to playbook "React Frontend v1.2"

  Scenario: ROLE-VIEW-01 Open role detail page
    Given Maria is on roles list
    When she clicks [View] for "Frontend Developer"
    Then she is redirected to FOB-ROLES-VIEW_ROLE-1
    And she sees breadcrumb with playbook and role name

  Scenario: ROLE-VIEW-02 View role header
    Given Maria is on the role detail page
    Then she sees role name "Frontend Developer"
    And she sees parent playbook badge

  Scenario: ROLE-VIEW-03 View role description
    Given Maria is on the role detail page
    Then she sees the full description
    And she sees creation and modification timestamps

  Scenario: ROLE-VIEW-04 View activities using this role
    Given the role is assigned to 5 activities
    Then she sees "Used in Activities" section
    And she sees list of activities with this role
    And each activity link is clickable

  Scenario: ROLE-VIEW-05 Edit role button
    Given Maria is viewing the role
    When she clicks [Edit Role]
    Then she is redirected to FOB-ROLES-EDIT_ROLE-1

  Scenario: ROLE-VIEW-06 Delete role button
    Given Maria is viewing the role
    When she clicks [Delete Role]
    Then the FOB-ROLES-DELETE_ROLE-1 modal appears
