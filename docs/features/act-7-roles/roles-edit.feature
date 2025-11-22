Feature: FOB-ROLES-EDIT_ROLE-1 Edit Role
  As a methodology author (Maria)
  I want to edit role details
  So that I can update responsibilities

  Background:
    Given Maria is authenticated in FOB
    And she owns playbook "React Frontend v1.2"
    And the playbook has role "Frontend Developer"

  Scenario: ROLE-EDIT-01 Open edit form
    Given Maria is viewing the role
    When she clicks [Edit Role]
    Then she is redirected to FOB-ROLES-EDIT_ROLE-1
    And all fields are pre-populated

  Scenario: ROLE-EDIT-02 Edit role name
    Given Maria is on the edit form
    When she changes Name to "Senior Frontend Developer"
    And she clicks [Save Changes]
    Then the role is updated

  Scenario: ROLE-EDIT-03 Edit role description
    Given Maria is on the edit form
    When she updates the Description
    And she saves
    Then the description is updated

  Scenario: ROLE-EDIT-04 Cancel editing
    Given Maria has made changes
    When she clicks [Cancel]
    Then changes are discarded
