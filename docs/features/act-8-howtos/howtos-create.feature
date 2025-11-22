Feature: FOB-HOWTOS-CREATE_HOWTO-1 Create Howto
  As a methodology author (Maria)
  I want to create howtos within a playbook
  So that I can provide guidance documentation

  Background:
    Given Maria is authenticated in FOB
    And she is viewing playbook "React Frontend v1.2"

  Scenario: HOWTO-CREATE-01 Open create howto form
    Given Maria is on howtos list
    When she clicks [Create New Howto]
    Then she is redirected to FOB-HOWTOS-CREATE_HOWTO-1

  Scenario: HOWTO-CREATE-02 Create howto successfully
    Given Maria is on the create howto form
    When she enters "Setup React Component" in Name
    And she enters "Step-by-step guide to create a new React component" in Description
    And she enters howto content in rich text editor
    And she clicks [Create Howto]
    Then the howto is created
    And she sees success notification

  Scenario: HOWTO-CREATE-03 Validate required fields
    Given Maria is on the create howto form
    When she leaves Name empty
    And she clicks [Create Howto]
    Then she sees validation error "Name is required"

  Scenario: HOWTO-CREATE-04 Rich text formatting
    Given Maria is on the create howto form
    Then she can format text with bold, italic, lists
    And she can add code blocks
    And she can add links

  Scenario: HOWTO-CREATE-05 Cancel howto creation
    Given Maria has entered howto data
    When she clicks [Cancel]
    Then she sees "Discard changes?" confirmation
    When she confirms
    Then no howto is created
