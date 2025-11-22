Feature: FOB-HOWTOS-EDIT_HOWTO-1 Edit Howto
  As a methodology author (Maria)
  I want to edit howto details
  So that I can update guidance documentation

  Background:
    Given Maria is authenticated in FOB
    And she owns playbook "React Frontend v1.2"
    And the playbook has howto "Setup React Component"

  Scenario: HOWTO-EDIT-01 Open edit form
    Given Maria is viewing the howto
    When she clicks [Edit Howto]
    Then she is redirected to FOB-HOWTOS-EDIT_HOWTO-1
    And all fields are pre-populated

  Scenario: HOWTO-EDIT-02 Edit howto name
    Given Maria is on the edit form
    When she changes Name to "Advanced React Component Setup"
    And she clicks [Save Changes]
    Then the howto is updated

  Scenario: HOWTO-EDIT-03 Edit howto content
    Given Maria is on the edit form
    When she updates the content in rich text editor
    And she saves
    Then the content is updated

  Scenario: HOWTO-EDIT-04 Cancel editing
    Given Maria has made changes
    When she clicks [Cancel]
    Then changes are discarded
