Feature: FOB-DASHBOARD-1 Dashboard and Navigation
  As a methodology author (Maria)
  I want to navigate FOB efficiently
  So that I can access my work quickly

  Background:
    Given Maria is authenticated in FOB
    And she is on FOB-DASHBOARD-1

  Scenario: NAV-01 View dashboard overview
    Given Maria is on the dashboard
    Then she sees "My Playbooks" section with recent playbooks
    And she sees "Recent Activity" feed
    And she sees quick action buttons

  Scenario: NAV-02 Navigate to Playbooks
    Given Maria is on the dashboard
    When she clicks "Playbooks" in main navigation
    Then she is redirected to FOB-PLAYBOOKS-LIST+FIND-1

  Scenario: NAV-03 Quick create playbook
    Given Maria is on the dashboard
    When she clicks [+ New Playbook] quick action
    Then she is redirected to FOB-PLAYBOOKS-CREATE_PLAYBOOK-1

  Scenario: NAV-04 View recent playbook
    Given Maria sees recent playbooks on dashboard
    When she clicks a recent playbook
    Then she is redirected to that playbook's view page

  Scenario: NAV-05 Access settings
    Given Maria is on the dashboard
    When she clicks her profile menu
    And she clicks [Settings]
    Then she is redirected to FOB-SETTINGS-1

  Scenario: NAV-06 Global search
    Given Maria is anywhere in FOB
    When she uses global search for "Component"
    Then she sees results across: Playbooks, Workflows, Activities
    And she can navigate to any result
