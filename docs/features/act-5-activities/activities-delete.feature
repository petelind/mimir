Feature: FOB-ACTIVITIES-DELETE_ACTIVITY-1 Delete Activity
  As a methodology author (Maria)
  I want to delete activities
  So that I can remove obsolete work tasks

  Background:
    Given Maria is authenticated in FOB
    And she owns workflow "Component Development"
    And the workflow has activity "Old Setup Task"

  Scenario: ACT-DELETE-01 Open delete confirmation
    Given Maria is on activities list
    When she clicks [Delete] for "Old Setup Task"
    Then the FOB-ACTIVITIES-DELETE_ACTIVITY-1 modal appears
    And it shows "Delete Activity?"

  Scenario: ACT-DELETE-02 Modal shows activity details
    Given the delete modal is open
    Then it displays activity name and phase
    And it shows warning about dependencies

  Scenario: ACT-DELETE-03 Warning about dependent activities
    Given other activities depend on this activity
    Then the modal shows "2 activities depend on this one"
    And it lists dependent activities
    And it shows "Dependencies will be broken"

  Scenario: ACT-DELETE-04 Confirm deletion
    Given the delete modal is open
    When she clicks [Delete Activity]
    Then the activity is deleted
    And dependent activities have dependencies removed
    And she sees success notification

  Scenario: ACT-DELETE-05 Cancel deletion
    Given the delete modal is open
    When she clicks [Cancel]
    Then the modal closes
    And the activity is not deleted

  Scenario: ACT-DELETE-06 Delete activity with artifacts
    Given the activity has 3 associated artifacts
    Then the modal shows "3 artifacts are linked"
    And it shows "Artifact links will be removed"

  Scenario: ACT-DELETE-07 Reorder remaining activities after deletion
    Given the phase has 5 activities in order
    When she deletes activity #3
    Then remaining activities are renumbered
