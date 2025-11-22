Feature: FOB-ACTIVITIES-LIST+FIND-1 Activities List and Search
  As a methodology author (Maria)
  I want to view and search activities within a workflow
  So that I can manage individual work tasks

  Background:
    Given Maria is authenticated in FOB
    And she is viewing workflow "Component Development" in playbook "React Frontend v1.2"
    And the workflow has 8 activities across 2 phases

  Scenario: ACT-LIST-01 Navigate to activities list from workflow
    Given Maria is on FOB-WORKFLOWS-VIEW_WORKFLOW-1
    When she clicks the "Activities" tab
    Then she is redirected to FOB-ACTIVITIES-LIST+FIND-1
    And she sees "Activities in Component Development" header

  Scenario: ACT-LIST-02 View activities table
    Given Maria is on activities list
    Then she sees all 8 activities
    And each activity shows: Name, Description, Phase, Dependencies, Status, Order, Actions

  Scenario: ACT-LIST-03 Create new activity
    Given Maria is on activities list
    When she clicks [Create New Activity]
    Then she is redirected to FOB-ACTIVITIES-CREATE_ACTIVITY-1

  Scenario: ACT-LIST-04 View by phase grouping
    Given the workflow has phases
    When Maria views activities list
    Then activities are grouped by phase
    And she sees phase headers with activity counts

  Scenario: ACT-LIST-05 View flat list (no phases)
    Given the workflow has no phases
    Then activities are shown in a flat list
    And ordered by sequence number

  Scenario: ACT-LIST-06 Search activities by name
    Given Maria is on activities list
    When she enters "Setup" in search
    Then only activities matching "Setup" are shown

  Scenario: ACT-LIST-07 Filter by phase
    Given the workflow has 2 phases
    When she filters by "Planning" phase
    Then only activities in Planning phase are shown

  Scenario: ACT-LIST-08 Filter by dependency status
    Given some activities have dependencies
    When she filters by "Has Dependencies"
    Then only activities with dependencies are shown

  Scenario: ACT-LIST-09 Reorder activities
    Given Maria is on activities list
    When she clicks [Reorder Activities]
    Then drag-and-drop mode is enabled
    And she can reorder within phases

  Scenario: ACT-LIST-10 Navigate to view activity
    Given Maria is on activities list
    When she clicks [View] for an activity
    Then she is redirected to FOB-ACTIVITIES-VIEW_ACTIVITY-1

  Scenario: ACT-LIST-11 Navigate to edit activity
    Given Maria is on activities list
    When she clicks [Edit] for an activity
    Then she is redirected to FOB-ACTIVITIES-EDIT_ACTIVITY-1

  Scenario: ACT-LIST-12 Delete activity
    Given Maria is on activities list
    When she clicks [Delete] for an activity
    Then the FOB-ACTIVITIES-DELETE_ACTIVITY-1 modal appears

  Scenario: ACT-LIST-13 Empty state display
    Given the workflow has zero activities
    Then she sees "No activities yet"
    And she sees [Create First Activity] button
