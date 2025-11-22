Feature: FOB-ROLES-LIST+FIND-1 Roles List and Search
  As a methodology author (Maria)
  I want to view and search roles within a playbook
  So that I can manage team member responsibilities

  Background:
    Given Maria is authenticated in FOB
    And she is viewing playbook "React Frontend v1.2"
    And the playbook has 8 roles defined

  Scenario: ROLE-LIST-01 Navigate to roles list from playbook
    Given Maria is on FOB-PLAYBOOKS-VIEW_PLAYBOOK-1
    When she clicks the "Roles" tab
    Then she is redirected to FOB-ROLES-LIST+FIND-1
    And she sees "Roles in React Frontend v1.2" header

  Scenario: ROLE-LIST-02 View roles table
    Given Maria is on roles list
    Then she sees all 8 roles
    And each role shows: Name, Description, Activities, Actions

  Scenario: ROLE-LIST-03 Create new role
    Given Maria is on roles list
    When she clicks [Create New Role]
    Then she is redirected to FOB-ROLES-CREATE_ROLE-1

  Scenario: ROLE-LIST-04 Search roles by name
    Given Maria is on roles list
    When she enters "Developer" in search
    Then only roles matching "Developer" are shown

  Scenario: ROLE-LIST-05 Filter by activity usage
    Given some roles are used in activities
    When she filters by "Used in Activities"
    Then only roles assigned to activities are shown

  Scenario: ROLE-LIST-06 View role usage count
    Given Maria is on roles list
    Then each role shows activity count
    And she can click to see which activities use each role

  Scenario: ROLE-LIST-07 Navigate to view role
    Given Maria is on roles list
    When she clicks [View] for a role
    Then she is redirected to FOB-ROLES-VIEW_ROLE-1

  Scenario: ROLE-LIST-08 Empty state display
    Given the playbook has zero roles
    Then she sees "No roles yet"
    And she sees [Create First Role] button
