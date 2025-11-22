Feature: FOB-HOWTOS-LIST+FIND-1 Howtos List and Search
  As a methodology author (Maria)
  I want to view and search howtos within a playbook
  So that I can manage guidance documentation

  Background:
    Given Maria is authenticated in FOB
    And she is viewing playbook "React Frontend v1.2"
    And the playbook has 12 howtos defined

  Scenario: HOWTO-LIST-01 Navigate to howtos list from playbook
    Given Maria is on FOB-PLAYBOOKS-VIEW_PLAYBOOK-1
    When she clicks the "Howtos" tab
    Then she is redirected to FOB-HOWTOS-LIST+FIND-1
    And she sees "Howtos in React Frontend v1.2" header

  Scenario: HOWTO-LIST-02 View howtos table
    Given Maria is on howtos list
    Then she sees all 12 howtos
    And each howto shows: Name, Description, Activities, Actions

  Scenario: HOWTO-LIST-03 Create new howto
    Given Maria is on howtos list
    When she clicks [Create New Howto]
    Then she is redirected to FOB-HOWTOS-CREATE_HOWTO-1

  Scenario: HOWTO-LIST-04 Search howtos by name
    Given Maria is on howtos list
    When she enters "Setup" in search
    Then only howtos matching "Setup" are shown

  Scenario: HOWTO-LIST-05 Filter by activity usage
    Given some howtos are linked to activities
    When she filters by "Used in Activities"
    Then only howtos linked to activities are shown

  Scenario: HOWTO-LIST-06 View howto usage count
    Given Maria is on howtos list
    Then each howto shows activity count
    And she can click to see which activities link each howto

  Scenario: HOWTO-LIST-07 Navigate to view howto
    Given Maria is on howtos list
    When she clicks [View] for a howto
    Then she is redirected to FOB-HOWTOS-VIEW_HOWTO-1

  Scenario: HOWTO-LIST-08 Empty state display
    Given the playbook has zero howtos
    Then she sees "No howtos yet"
    And she sees [Create First Howto] button
