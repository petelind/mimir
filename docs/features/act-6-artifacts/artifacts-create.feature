Feature: FOB-ARTIFACTS-CREATE_ARTIFACT-1 Create Artifact
  As a methodology author (Maria)
  I want to create artifacts for activities
  So that I can define required deliverables

  Background:
    Given Maria is authenticated in FOB
    And she is viewing playbook "React Frontend v1.2"

  Scenario: ART-CREATE-01 Open create artifact form
    Given Maria is on artifacts list
    When she clicks [Create New Artifact]
    Then she is redirected to FOB-ARTIFACTS-CREATE_ARTIFACT-1
    And the Parent Playbook field shows "React Frontend v1.2" (read-only)

  Scenario: ART-CREATE-02 Create artifact successfully
    Given Maria is on the create artifact form
    When she enters "Component Design Document" in Name
    And she enters "Detailed component architecture and patterns" in Description
    And she selects "Document" as Type
    And she clicks [Create Artifact]
    Then the artifact is created
    And she sees success notification

  Scenario: ART-CREATE-03 Validate required fields
    Given Maria is on the create artifact form
    When she leaves Name empty
    And she clicks [Create Artifact]
    Then she sees validation error "Name is required"

  Scenario: ART-CREATE-04 Select artifact type
    Given Maria is on the create artifact form
    Then she sees type options: Document, Template, Code, Diagram, Data, Other

  Scenario: ART-CREATE-05 Associate with activity
    Given Maria is on the create artifact form
    When she selects activity "Setup Component Structure"
    And she creates the artifact
    Then the artifact is linked to the activity

  Scenario: ART-CREATE-06 Mark as required
    Given Maria is on the create artifact form
    When she checks "Required" checkbox
    And she creates the artifact
    Then the artifact is marked as required

  Scenario: ART-CREATE-07 Add file template
    Given Maria is creating a "Template" artifact
    When she uploads a template file
    And she creates the artifact
    Then the template is stored with the artifact

  Scenario: ART-CREATE-08 Cancel artifact creation
    Given Maria has entered artifact data
    When she clicks [Cancel]
    Then she sees "Discard changes?" confirmation
    When she confirms
    Then no artifact is created
