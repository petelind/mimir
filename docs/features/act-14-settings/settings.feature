Feature: FOB-SETTINGS-1 Settings and Configuration
  As a methodology author (Maria)
  I want to configure FOB settings
  So that I can customize my experience

  Background:
    Given Maria is authenticated in FOB

  Scenario: SETTINGS-01 Navigate to settings
    Given Maria is anywhere in FOB
    When she clicks profile menu > [Settings]
    Then she sees FOB-SETTINGS-1
    And settings are organized in sections

  Scenario: SETTINGS-02 Account settings
    Given Maria is in settings
    When she navigates to Account section
    Then she can update: Name, Email, Password, Profile Photo

  Scenario: SETTINGS-03 Sync settings
    Given Maria is in settings
    When she navigates to Sync & Connection
    Then she can configure: Auto-sync frequency, Conflict resolution preference

  Scenario: SETTINGS-04 Storage settings
    Given Maria is in settings
    When she views Storage section
    Then she sees storage usage breakdown
    And she can clear cache or export data

  Scenario: SETTINGS-05 MCP configuration
    Given Maria is in settings
    When she navigates to MCP Configuration
    Then she can configure MCP server connection
    And enable/disable MCP features

  Scenario: SETTINGS-06 Notification preferences
    Given Maria is in settings
    When she navigates to Notifications
    Then she can toggle: Sync notifications, PIP alerts, Family invites

  Scenario: SETTINGS-07 Privacy settings
    Given Maria is in settings
    When she navigates to Privacy
    Then she can set playbook visibility defaults
    And manage data sharing preferences
