Feature: FOB-ROLES-DELETE_ROLE-1 Delete Role
  As a methodology author (Maria)
  I want to delete roles
  So that I can remove obsolete team definitions

  Background:
    Given Maria is authenticated in FOB
    And she owns playbook "React Frontend v1.2"
    And the playbook has role "Old Role"

  Scenario: ROLE-DELETE-01 Open delete confirmation
    Given Maria is on roles list
    When she clicks [Delete] for "Old Role"
    Then the FOB-ROLES-DELETE_ROLE-1 modal appears
    And it shows "Delete Role?"

  Scenario: ROLE-DELETE-02 Modal shows role details
    Given the delete modal is open
    Then it displays role name
    And it shows warning about activity assignments

  Scenario: ROLE-DELETE-03 Warning about assigned activities
    Given the role is assigned to 4 activities
    Then the modal shows "Used in 4 activities"
    And it lists the activities
    And it shows "Role assignments will be removed"

  Scenario: ROLE-DELETE-04 Confirm deletion
    Given the delete modal is open
    When she clicks [Delete Role]
    Then the role is deleted
    And activity assignments are removed
    And she sees success notification

  Scenario: ROLE-DELETE-05 Cancel deletion
    Given the delete modal is open
    When she clicks [Cancel]
    Then the modal closes
    And the role is not deleted
