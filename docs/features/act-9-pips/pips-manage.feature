Feature: FOB-PIPS-LIST-1 Manage PIPs
  As a methodology author (Maria)
  I want to view and manage PIPs
  So that I can implement improvements systematically

  Background:
    Given Maria is authenticated in FOB
    And she is viewing playbook "React Frontend v1.2"
    And the playbook has 5 PIPs with various statuses

  Scenario: PIP-MANAGE-01 View PIPs list
    Given Maria is on playbook view
    When she clicks "PIPs" tab
    Then she sees FOB-PIPS-LIST-1
    And she sees all 5 PIPs

  Scenario: PIP-MANAGE-02 Filter PIPs by status
    Given Maria is on PIPs list
    When she filters by "Proposed"
    Then only proposed PIPs are shown

  Scenario: PIP-MANAGE-03 Approve PIP
    Given Maria views a proposed PIP
    When she clicks [Approve]
    Then PIP status changes to "Approved"
    And it moves to implementation queue

  Scenario: PIP-MANAGE-04 Reject PIP
    Given Maria views a proposed PIP
    When she clicks [Reject]
    And she enters rejection reason
    Then PIP status changes to "Rejected"

  Scenario: PIP-MANAGE-05 Implement PIP
    Given Maria has an approved PIP
    When she clicks [Implement]
    Then she is guided through implementation
    And changes are applied to playbook
    And PIP status changes to "Implemented"

  Scenario: PIP-MANAGE-06 Track PIP history
    Given Maria views a PIP
    Then she sees status history with timestamps
    And she sees who approved/rejected/implemented it
  # ============================================================
  # NAVBAR INTEGRATION - Wire when PIPs block is complete
  # ============================================================

  Scenario: PIP-NAVBAR-01 PIPs link appears in main navigation
    Given the PIPs feature is fully implemented
    And Maria is authenticated in FOB
    When she views any page in FOB
    Then she sees "PIPs" link in the main navbar
    And the link has icon "fa-lightbulb"
    And the link has tooltip "Review Playbook Improvement Proposals"

  Scenario: PIP-NAVBAR-02 Navigate to PIPs list from any page
    Given Maria is authenticated in FOB
    And she is on any page in FOB
    When she clicks "PIPs" in the main navbar
    Then she is redirected to FOB-PIPS-LIST-1
    And she sees all PIPs across all playbooks
    And the PIPs nav link is highlighted as active
