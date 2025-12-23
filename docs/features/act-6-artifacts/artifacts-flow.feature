Feature: FOB-ARTIFACTS-FLOW-1 Artifact Input/Output Flow
  As a methodology author (Maria)
  I want to define artifacts as outputs and inputs across activities
  So that I can track deliverable flow through workflows

  Background:
    Given Maria is authenticated in FOB
    And she is viewing playbook "React Frontend v1.2"
    And the playbook has workflow "Component Development"
    And the workflow has activities:
      | Activity Name          | Order |
      | Design Component API   | 1     |
      | Implement Component    | 2     |
      | Test Component         | 3     |
      | Document Component     | 4     |

  # ============================================================
  # PRODUCER/CONSUMER RELATIONSHIPS
  # ============================================================

  Scenario: ART-FLOW-01 Define artifact as output of activity
    Given Maria is creating artifact "Component API Specification"
    When she sets "Design Component API" as the producing activity
    And she clicks [Create Artifact]
    Then the artifact is created
    And the artifact is marked as output of "Design Component API"
    And she sees "Produced by: Design Component API" on artifact detail page

  Scenario: ART-FLOW-02 Define artifact as input to downstream activity
    Given artifact "Component API Specification" exists as output of "Design Component API"
    When Maria is on activity "Implement Component" detail page
    And she clicks [Manage Input Artifacts]
    And she selects "Component API Specification" from available artifacts
    And she marks it as "Required"
    And she clicks [Add Input]
    Then "Component API Specification" appears in "Implement Component" inputs list
    And the artifact detail page shows "Consumed by: Implement Component"

  Scenario: ART-FLOW-03 Add multiple consumers for single artifact
    Given artifact "Component API Specification" is output of "Design Component API"
    And it is already input to "Implement Component"
    When Maria adds it as input to "Test Component"
    And she adds it as input to "Document Component"
    Then the artifact detail page shows:
      | Consumed by              |
      | Implement Component      |
      | Test Component           |
      | Document Component       |

  Scenario: ART-FLOW-04 View artifact flow through workflow
    Given "Component API Specification" is output of "Design Component API"
    And it is input to "Implement Component", "Test Component", and "Document Component"
    When Maria views the artifact detail page
    Then she sees "Artifact Flow" section
    And she sees "Produced by: Design Component API (Activity #1)"
    And she sees "Consumed by: 3 activities"
    And she sees list:
      | Activity               | Required | Status   |
      | Implement Component    | Yes      | Pending  |
      | Test Component         | Yes      | Pending  |
      | Document Component     | No       | Pending  |

  Scenario: ART-FLOW-05 View workflow with artifact flow visualization
    Given workflow "Component Development" has multiple artifacts flowing between activities
    When Maria clicks [View Artifact Flow] on workflow detail page
    Then she sees a flow diagram showing:
      | Activity               | Outputs                      | Inputs                       |
      | Design Component API   | Component API Specification  | -                            |
      | Implement Component    | Component Code               | Component API Specification  |
      | Test Component         | Test Suite                   | Component Code, API Spec     |
      | Document Component     | Documentation                | Component Code, API Spec     |

  # ============================================================
  # VALIDATION & CONSTRAINTS
  # ============================================================

  Scenario: ART-FLOW-06 Prevent circular artifact dependencies
    Given "Component Code" is output of "Implement Component"
    And "Component Code" is input to "Test Component"
    When Maria tries to add "Component Code" as input to "Implement Component"
    Then she sees error "Circular dependency detected: An artifact cannot be input to its producing activity"
    And the input is not added

  Scenario: ART-FLOW-07 Prevent artifact from being input before it's produced
    Given activity "Design Component API" is order 1
    And activity "Implement Component" is order 2
    And artifact "Component Code" is output of "Implement Component" (order 2)
    When Maria tries to add "Component Code" as input to "Design Component API" (order 1)
    Then she sees warning "Dependency issue: This artifact is produced by a later activity (order 2). Consider reordering activities or using a different artifact."
    And she can choose:
      | Option                          |
      | Cancel                          |
      | Add anyway (override warning)   |

  Scenario: ART-FLOW-08 Warn about missing required inputs
    Given activity "Implement Component" requires input "Component API Specification"
    And "Component API Specification" does not exist yet
    When Maria views "Implement Component" detail page
    Then she sees warning banner "Missing required input: Component API Specification"
    And she sees [Create Missing Artifact] button

  Scenario: ART-FLOW-09 Validate artifact type compatibility
    Given artifact "Component Code" has type "Code"
    And activity "Document Component" expects input type "Document" or "Code"
    When Maria adds "Component Code" as input to "Document Component"
    Then the input is accepted
    And no type mismatch warning appears

  Scenario: ART-FLOW-10 Warn about artifact type mismatch
    Given artifact "Test Results Data" has type "Data"
    And activity "Write Documentation" typically expects input type "Document" or "Code"
    When Maria tries to add "Test Results Data" as input to "Write Documentation"
    Then she sees warning "Type mismatch: This activity typically uses Document or Code artifacts, but you're adding a Data artifact"
    And she can choose:
      | Option                          |
      | Cancel                          |
      | Add anyway (I know what I'm doing) |

  # ============================================================
  # ARTIFACT INPUT MANAGEMENT
  # ============================================================

  Scenario: ART-FLOW-11 Mark artifact input as required vs optional
    Given Maria is adding "Component API Specification" as input to "Implement Component"
    When she checks "Required" checkbox
    And she clicks [Add Input]
    Then the artifact is marked as required input
    And activity detail page shows "Component API Specification (Required)"

  Scenario: ART-FLOW-12 Mark artifact input as optional
    Given Maria is adding "Design Mockups" as input to "Implement Component"
    When she leaves "Required" checkbox unchecked
    And she clicks [Add Input]
    Then the artifact is marked as optional input
    And activity detail page shows "Design Mockups (Optional)"

  Scenario: ART-FLOW-13 Change artifact input from required to optional
    Given "Component API Specification" is required input to "Implement Component"
    When Maria clicks [Edit Input] for that artifact
    And she unchecks "Required" checkbox
    And she clicks [Save Changes]
    Then the artifact becomes optional input
    And activity detail page shows "Component API Specification (Optional)"

  Scenario: ART-FLOW-14 Remove artifact as input from activity
    Given "Design Mockups" is optional input to "Implement Component"
    When Maria clicks [Remove Input] for that artifact
    Then confirmation modal appears "Remove input artifact?"
    When she confirms
    Then "Design Mockups" is removed from "Implement Component" inputs
    And artifact detail page no longer shows "Implement Component" as consumer

  Scenario: ART-FLOW-15 Warn when removing required input
    Given "Component API Specification" is required input to "Implement Component"
    When Maria clicks [Remove Input]
    Then she sees warning "This is a required input. Removing it may impact activity execution."
    And she can choose:
      | Option                          |
      | Cancel                          |
      | Remove anyway                   |

  # ============================================================
  # ACTIVITY OUTPUT MANAGEMENT
  # ============================================================

  Scenario: ART-FLOW-16 View activity outputs on activity detail page
    Given activity "Implement Component" produces artifacts:
      | Artifact Name          | Type     | Required |
      | Component Code         | Code     | Yes      |
      | Unit Tests             | Code     | Yes      |
      | Component Styles       | Code     | No       |
    When Maria views "Implement Component" detail page
    Then she sees "Output Artifacts" section
    And she sees all 3 artifacts listed
    And each shows type and required status

  Scenario: ART-FLOW-17 View activity inputs on activity detail page
    Given activity "Implement Component" consumes artifacts:
      | Artifact Name                  | Type      | Required | Produced By          |
      | Component API Specification    | Document  | Yes      | Design Component API |
      | Design Mockups                 | Diagram   | No       | Design UI            |
    When Maria views "Implement Component" detail page
    Then she sees "Input Artifacts" section
    And she sees both artifacts listed
    And each shows producer activity and required status

  Scenario: ART-FLOW-18 Navigate from activity to input artifact
    Given activity "Implement Component" has input "Component API Specification"
    When Maria clicks on "Component API Specification" in inputs list
    Then she is redirected to FOB-ARTIFACTS-VIEW_ARTIFACT-1 for that artifact
    And she sees full artifact details

  Scenario: ART-FLOW-19 Navigate from activity to output artifact
    Given activity "Implement Component" produces "Component Code"
    When Maria clicks on "Component Code" in outputs list
    Then she is redirected to FOB-ARTIFACTS-VIEW_ARTIFACT-1 for that artifact
    And she sees full artifact details

  # ============================================================
  # BULK OPERATIONS
  # ============================================================

  Scenario: ART-FLOW-20 Add multiple artifacts as inputs at once
    Given Maria is on activity "Test Component" detail page
    When she clicks [Manage Input Artifacts]
    And she selects multiple artifacts:
      | Artifact Name                  | Required |
      | Component Code                 | Yes      |
      | Component API Specification    | Yes      |
      | Test Data                      | No       |
    And she clicks [Add Selected Inputs]
    Then all 3 artifacts are added as inputs
    And she sees success notification "3 input artifacts added"

  Scenario: ART-FLOW-21 Copy artifact inputs from another activity
    Given activity "Test Component" has inputs:
      | Component Code                 |
      | Component API Specification    |
    And Maria is on activity "Document Component" detail page
    When she clicks [Copy Inputs From...]
    And she selects "Test Component"
    And she clicks [Copy Inputs]
    Then both artifacts are added as inputs to "Document Component"
    And she sees "2 inputs copied from Test Component"

  # ============================================================
  # REPORTING & VISUALIZATION
  # ============================================================

  Scenario: ART-FLOW-22 View playbook artifact dependency graph
    Given playbook "React Frontend v1.2" has multiple workflows with artifact flows
    When Maria clicks [View Artifact Dependencies] on playbook detail page
    Then she sees a graph visualization showing:
      | All artifacts as nodes                              |
      | Producer activities as source nodes                 |
      | Consumer activities as target nodes                 |
      | Arrows showing artifact flow direction              |
      | Color coding for artifact types                     |

  Scenario: ART-FLOW-23 Filter artifact flow by type
    Given Maria is viewing artifact dependency graph
    When she filters by artifact type "Document"
    Then only Document artifacts and their flows are shown
    And other artifact types are hidden

  Scenario: ART-FLOW-24 Identify orphaned artifacts
    Given playbook has artifact "Old Design Doc" with no consumers
    When Maria views artifact list with filter "Orphaned artifacts"
    Then she sees "Old Design Doc" in the list
    And she sees warning "No activities consume this artifact"
    And she can choose:
      | Option                          |
      | Add consumers                   |
      | Archive artifact                |
      | Delete artifact                 |

  Scenario: ART-FLOW-25 Identify missing artifact producers
    Given activity "Implement Component" requires input "Component API Specification"
    And no activity produces "Component API Specification"
    When Maria views workflow validation report
    Then she sees error "Missing producer: Component API Specification has no producing activity"
    And she sees [Create Producer Activity] button

  # ============================================================
  # INTEGRATION WITH EXISTING FEATURES
  # ============================================================

  Scenario: ART-FLOW-26 Create artifact with producer from activity detail page
    Given Maria is on activity "Design Component API" detail page
    When she clicks [Create Output Artifact]
    Then she is redirected to FOB-ARTIFACTS-CREATE_ARTIFACT-1
    And the "Produced by" field is pre-filled with "Design Component API"
    And the "Parent Playbook" field shows "React Frontend v1.2" (read-only)

  Scenario: ART-FLOW-27 View artifact flow from artifact detail page
    Given artifact "Component Code" is output of "Implement Component"
    And it is input to "Test Component" and "Document Component"
    When Maria views artifact detail page
    Then she sees "Artifact Flow" card showing:
      | Producer: Implement Component (Activity #2)         |
      | Consumers: 2 activities                             |
      | - Test Component (Required)                         |
      | - Document Component (Optional)                     |

  Scenario: ART-FLOW-28 Delete artifact with consumers shows warning
    Given artifact "Component Code" is input to 3 activities
    When Maria clicks [Delete Artifact]
    Then she sees warning "This artifact is used as input by 3 activities:"
    And she sees list of consumer activities
    And she sees "Deleting will break these dependencies"
    And she can choose:
      | Option                                    |
      | Cancel                                    |
      | Delete and remove from all consumers      |
