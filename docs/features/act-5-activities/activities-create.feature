Feature: FOB-ACTIVITIES-CREATE_ACTIVITY-1 Create Activity
  As a methodology author (Maria)
  I want to create activities within workflows
  So that I can define specific work tasks

  Background:
    Given Maria is authenticated in FOB
    And she is viewing workflow "Component Development"

  Scenario: ACT-CREATE-01 Open create activity form
    Given Maria is on activities list
    When she clicks [Create New Activity]
    Then she is redirected to FOB-ACTIVITIES-CREATE_ACTIVITY-1
    And the Parent Workflow field shows "Component Development" (read-only)

  Scenario: ACT-CREATE-02 Create activity successfully
    Given Maria is on the create activity form
    When she enters "Setup component structure" in Name
    And she enters "Create folder structure and base files" in Description
    And she clicks [Create Activity]
    Then the activity is created
    And she sees success notification

  Scenario: ACT-CREATE-03 Validate required fields
    Given Maria is on the create activity form
    When she leaves Name empty
    And she clicks [Create Activity]
    Then she sees validation error "Name is required"

  Scenario: ACT-CREATE-04 Assign to phase
    Given the workflow has phases
    When she selects "Planning" phase
    And she creates the activity
    Then the activity is assigned to Planning phase

  Scenario: ACT-CREATE-05 Create without phase assignment
    Given the workflow has phases
    When she leaves phase unassigned
    And she creates the activity
    Then the activity is created in "Unassigned" state

  Scenario: ACT-CREATE-06 Set activity order
    Given the phase has 3 existing activities
    When she sets order to "2"
    And she creates the activity
    Then the activity is inserted at position 2

  Scenario: ACT-CREATE-07 Add dependencies during creation
    Given other activities exist in the workflow
    When she selects "Define requirements" as a dependency
    And she creates the activity
    Then the dependency is saved

  Scenario: ACT-CREATE-08 Add artifacts during creation
    Given Maria is on the create activity form
    When she clicks [Add Artifact]
    And she enters artifact details
    Then the artifact is associated with the activity

  Scenario: ACT-CREATE-09 Cancel activity creation
    Given Maria has entered activity data
    When she clicks [Cancel]
    Then she sees "Discard changes?" confirmation
    When she confirms
    Then no activity is created
