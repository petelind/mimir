Feature: FOB-HOWTOS-VIEW_HOWTO-1 View Howto Details
  As a methodology author (Maria)
  I want to view howto details
  So that I can read guidance documentation

  Background:
    Given Maria is authenticated in FOB
    And she is viewing howto "Setup React Component"
    And the howto belongs to playbook "React Frontend v1.2"

  Scenario: HOWTO-VIEW-01 Open howto detail page
    Given Maria is on howtos list
    When she clicks [View] for "Setup React Component"
    Then she is redirected to FOB-HOWTOS-VIEW_HOWTO-1
    And she sees breadcrumb with playbook and howto name

  Scenario: HOWTO-VIEW-02 View howto header
    Given Maria is on the howto detail page
    Then she sees howto name "Setup React Component"
    And she sees parent playbook badge

  Scenario: HOWTO-VIEW-03 View howto content
    Given Maria is on the howto detail page
    Then she sees the formatted content
    And formatting is preserved (bold, italic, lists, code)

  Scenario: HOWTO-VIEW-04 View activities using this howto
    Given the howto is linked to 3 activities
    Then she sees "Used in Activities" section
    And she sees list of activities with this howto
    And each activity link is clickable

  Scenario: HOWTO-VIEW-05 Edit howto button
    Given Maria is viewing the howto
    When she clicks [Edit Howto]
    Then she is redirected to FOB-HOWTOS-EDIT_HOWTO-1

  Scenario: HOWTO-VIEW-06 Delete howto button
    Given Maria is viewing the howto
    When she clicks [Delete Howto]
    Then the FOB-HOWTOS-DELETE_HOWTO-1 modal appears
