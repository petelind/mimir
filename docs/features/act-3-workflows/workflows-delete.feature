Feature: FOB-WORKFLOWS-DELETE_WORKFLOW-1 Delete Workflow
  As a methodology author (Maria)
  I want to delete workflows
  So that I can remove obsolete execution sequences

  Background:
    Given Maria is authenticated in FOB
    And she owns playbook "React Frontend Development"
    And the playbook has workflow "Old Workflow" with 5 activities

  Scenario: WF-DELETE-01 Open delete confirmation
    Given Maria is on workflows list
    When she clicks [Delete] for "Old Workflow"
    Then the FOB-WORKFLOWS-DELETE_WORKFLOW-1 modal appears
    And it shows "Delete Workflow?"

  Scenario: WF-DELETE-02 Modal shows workflow details
    Given the delete modal is open
    Then it displays workflow name, activity count, and warning
    And it shows "This will permanently delete 5 activities"

  Scenario: WF-DELETE-03 Confirm deletion
    Given the delete modal is open
    When she clicks [Delete Workflow]
    Then the workflow is deleted
    And she sees success notification
    And the workflow no longer appears in the list

  Scenario: WF-DELETE-04 Cancel deletion
    Given the delete modal is open
    When she clicks [Cancel]
    Then the modal closes
    And the workflow is not deleted

  Scenario: WF-DELETE-05 Delete workflow with phases
    Given the workflow has 3 phases and 10 activities
    When she opens delete confirmation
    Then she sees enhanced warning about phases and activities

  Scenario: WF-DELETE-06 Reorder remaining workflows after deletion
    Given playbook has 3 workflows in order
    When she deletes workflow #2
    Then remaining workflows are renumbered to 1, 2

  Scenario: WF-DELETE-07 Cannot undo deletion
    Given Maria has deleted a workflow
    Then there is no undo option
    And deletion is permanent
