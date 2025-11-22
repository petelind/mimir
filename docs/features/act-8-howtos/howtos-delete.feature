Feature: FOB-HOWTOS-DELETE_HOWTO-1 Delete Howto
  As a methodology author (Maria)
  I want to delete howtos
  So that I can remove obsolete guidance

  Background:
    Given Maria is authenticated in FOB
    And she owns playbook "React Frontend v1.2"
    And the playbook has howto "Old Guide"

  Scenario: HOWTO-DELETE-01 Open delete confirmation
    Given Maria is on howtos list
    When she clicks [Delete] for "Old Guide"
    Then the FOB-HOWTOS-DELETE_HOWTO-1 modal appears
    And it shows "Delete Howto?"

  Scenario: HOWTO-DELETE-02 Modal shows howto details
    Given the delete modal is open
    Then it displays howto name
    And it shows warning about activity links

  Scenario: HOWTO-DELETE-03 Warning about linked activities
    Given the howto is linked to 5 activities
    Then the modal shows "Linked to 5 activities"
    And it lists the activities
    And it shows "Activity links will be removed"

  Scenario: HOWTO-DELETE-04 Confirm deletion
    Given the delete modal is open
    When she clicks [Delete Howto]
    Then the howto is deleted
    And activity links are removed
    And she sees success notification

  Scenario: HOWTO-DELETE-05 Cancel deletion
    Given the delete modal is open
    When she clicks [Cancel]
    Then the modal closes
    And the howto is not deleted
