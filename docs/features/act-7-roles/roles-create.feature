Feature: FOB-ROLES-CREATE_ROLE-1 Create Role
  As a methodology author (Maria)
  I want to create roles within a playbook
  So that I can define team member responsibilities

  Background:
    Given Maria is authenticated in FOB
    And she is viewing playbook "React Frontend v1.2"

  Scenario: ROLE-CREATE-01 Open create role form
    Given Maria is on roles list
    When she clicks [Create New Role]
    Then she is redirected to FOB-ROLES-CREATE_ROLE-1

  Scenario: ROLE-CREATE-02 Create role successfully
    Given Maria is on the create role form
    When she enters "Frontend Developer" in Name
    And she enters "Responsible for UI implementation and testing" in Description
    And she clicks [Create Role]
    Then the role is created
    And she sees success notification

  Scenario: ROLE-CREATE-03 Validate required fields
    Given Maria is on the create role form
    When she leaves Name empty
    And she clicks [Create Role]
    Then she sees validation error "Name is required"

  Scenario: ROLE-CREATE-04 Cancel role creation
    Given Maria has entered role data
    When she clicks [Cancel]
    Then she sees "Discard changes?" confirmation
    When she confirms
    Then no role is created
