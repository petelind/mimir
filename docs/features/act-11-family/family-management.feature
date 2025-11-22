Feature: FOB-FAMILY-MANAGE-1 Family Management
  As a methodology author (Maria)
  I want to manage my family group
  So that I can collaborate with Mike

  Background:
    Given Maria is authenticated in FOB

  Scenario: FAMILY-01 Create family
    Given Maria has no family
    When she clicks [Create Family]
    And she enters family name "Rodriguez Family"
    Then the family is created
    And Maria is the admin

  Scenario: FAMILY-02 Invite member
    Given Maria is family admin
    When she clicks [Invite Member]
    And she enters Mike's email
    Then invitation is sent

  Scenario: FAMILY-03 Accept invitation
    Given Mike receives invitation
    When he clicks invitation link
    And he accepts
    Then Mike joins the family

  Scenario: FAMILY-04 View family members
    Given Maria's family has 2 members
    When she views Family page
    Then she sees both members with roles

  Scenario: FAMILY-05 Transfer playbook ownership
    Given Maria owns a playbook
    When she transfers ownership to Mike
    Then Mike becomes owner
    And Maria becomes viewer

  Scenario: FAMILY-06 Remove member
    Given Maria is admin
    When she removes a member
    Then member loses access to family playbooks
    And their owned playbooks remain with them
