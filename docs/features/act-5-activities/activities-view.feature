Feature: FOB-ACTIVITIES-VIEW_ACTIVITY-1 View Activity Details
  As a methodology author (Maria)
  I want to view activity details
  So that I can understand work tasks completely

  Background:
    Given Maria is authenticated in FOB
    And she is viewing activity "Setup component structure"
    And the activity belongs to workflow "Component Development"

  Scenario: ACT-VIEW-01 Open activity detail page
    Given Maria is on activities list
    When she clicks [View] for "Setup component structure"
    Then she is redirected to FOB-ACTIVITIES-VIEW_ACTIVITY-1
    And she sees breadcrumb with workflow and activity name

  Scenario: ACT-VIEW-02 View activity header
    Given Maria is on the activity detail page
    Then she sees activity name "Setup component structure"
    And she sees parent workflow badge
    And she sees phase badge (if assigned)
    And she sees order badge

  Scenario: ACT-VIEW-03 View activity description
    Given Maria is on the activity detail page
    Then she sees the full description
    And she sees creation and modification timestamps

  Scenario: ACT-VIEW-04 View dependencies
    Given the activity has 2 dependencies
    Then she sees "Dependencies" section
    And she sees list of prerequisite activities
    And each dependency is clickable to view its details

  Scenario: ACT-VIEW-05 View artifacts
    Given the activity has 3 associated artifacts
    Then she sees "Artifacts" section
    And each artifact shows: Name, Type, Required status

  Scenario: ACT-VIEW-06 View roles involved
    Given the activity has assigned roles
    Then she sees "Roles" section
    And each role shows: Name, Responsibility

  Scenario: ACT-VIEW-07 View howtos
    Given the activity has linked howtos
    Then she sees "Howtos" section
    And each howto is clickable for guidance

  Scenario: ACT-VIEW-08 Edit activity button
    Given Maria is viewing the activity
    When she clicks [Edit Activity]
    Then she is redirected to FOB-ACTIVITIES-EDIT_ACTIVITY-1

  Scenario: ACT-VIEW-09 Delete activity button
    Given Maria is viewing the activity
    When she clicks [Delete Activity]
    Then the FOB-ACTIVITIES-DELETE_ACTIVITY-1 modal appears
