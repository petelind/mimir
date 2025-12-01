Feature: FOB-PLAYBOOKS-DELETE_PLAYBOOK-1 Delete Playbook ✅
  As a methodology author (Maria)
  I want to safely delete playbooks I own
  So that I can remove obsolete or unwanted methodologies

  Background:
    Given Maria is authenticated in FOB
    And Maria owns the playbook "Old Design Patterns" with:
      | field     | value    |
      | version   | v1.0     |
      | status    | Disabled |
      | workflows |        2 |

  Scenario: PB-DELETE-01 ✅ Open delete confirmation from list
    Given Maria is on FOB-PLAYBOOKS-LIST+FIND-1
    And "Old Design Patterns" is in the list
    When she clicks [Delete] in the Actions menu
    Then the FOB-PLAYBOOKS-DELETE_PLAYBOOK-1 modal appears
    And the modal shows "Delete Playbook?"

  Scenario: PB-DELETE-02 ✅ Open delete confirmation from detail page
    Given Maria is on FOB-PLAYBOOKS-VIEW_PLAYBOOK-1 for "Old Design Patterns"
    When she clicks the [Delete] button
    Then the FOB-PLAYBOOKS-DELETE_PLAYBOOK-1 modal appears
    And she sees the deletion confirmation

  Scenario: PB-DELETE-03 ✅ Modal shows playbook details
    Given the delete confirmation modal is open
    Then the modal displays playbook information:
      | field         | value               |
      | Name          | Old Design Patterns |
      | Version       | v1.0                |
      | Workflows     |                   2 |
      | Activities    |                   8 |
      | Last modified |        6 months ago |

  Scenario: PB-DELETE-04 ✅ Modal shows warning message
    Given the delete confirmation modal is open
    Then she sees warning message "This action cannot be undone"
    And she sees explanation "All workflows, activities, artifacts, and associated data will be permanently deleted"
    And she sees [Cancel] and [Delete Playbook] buttons
    And the [Delete Playbook] button is styled as danger (red)

  Scenario: PB-DELETE-05 ✅ Confirm deletion
    Given the delete confirmation modal is open
    When she clicks [Delete Playbook]
    Then the playbook is permanently deleted from FOB
    And she sees success notification "Playbook 'Old Design Patterns' deleted successfully"
    And she is redirected to FOB-PLAYBOOKS-LIST+FIND-1
    And "Old Design Patterns" no longer appears in the list

  Scenario: PB-DELETE-06 ✅ Cancel deletion from modal
    Given the delete confirmation modal is open
    When she clicks [Cancel]
    Then the modal closes
    And the playbook is not deleted
    And she remains on the current page
    And "Old Design Patterns" still exists

  Scenario: PB-DELETE-07 ✅ Close modal with X button
    Given the delete confirmation modal is open
    When she clicks the X close button
    Then the modal closes
    And the playbook is not deleted

  Scenario: PB-DELETE-08 ✅ Close modal by clicking outside
    Given the delete confirmation modal is open
    When she clicks outside the modal (on backdrop)
    Then the modal closes
    And the playbook is not deleted

  Scenario: PB-DELETE-09 ✅ Cannot delete downloaded playbooks
    Given Maria is viewing downloaded playbook "React Frontend Development"
    Then the [Delete] button is not visible in the detail page
    And the [Delete] action is not available in the list Actions menu
    And hovering shows tooltip "Only owned playbooks can be deleted"

  Scenario: PB-DELETE-10 ✅ Delete playbook with dependencies warning
    Given Maria owns playbook "Main Methodology"
    And "Main Methodology" has 5 workflows and 50 activities
    When she opens the delete confirmation modal
    Then she sees enhanced warning "This playbook contains:"
    And the warning lists:
      | item       | count |
      | Workflows  |     5 |
      | Activities |    50 |
      | Artifacts  |    25 |
      | Roles      |     8 |
      | Howtos     |    50 |
    And she sees "All of this data will be permanently lost"

  Scenario: PB-DELETE-11 ✅ Delete confirmation requires explicit action
    Given the delete confirmation modal is open
    Then the [Delete Playbook] button requires a click
    And pressing Enter does not trigger deletion
    And the modal does not auto-submit

  Scenario: PB-DELETE-12 ⏭️ Delete playbook from family affects members
    Given Maria owns playbook "Shared UX Methodology"
    And the playbook visibility is "Family (UX)"
    And the playbook is published to Homebase
    When she opens the delete confirmation modal
    Then she sees additional warning "This playbook is shared with UX family"
    And she sees "Family members will lose access after next sync"

  Scenario: PB-DELETE-13 ✅ Delete active vs disabled playbook
    Given Maria owns an Active playbook "Current Methodology"
    When she attempts to delete it
    Then she sees warning "This playbook is currently Active"
    And she sees suggestion "Consider Disabling it first if you're unsure"
    But deletion is still allowed after confirmation

  Scenario: PB-DELETE-14 ✅ Bulk delete not supported
    Given Maria has selected multiple playbooks in the list
    Then bulk delete option is not available
    And she must delete playbooks one at a time
    And each deletion requires individual confirmation

  Scenario: PB-DELETE-15 ✅ Delete with keyboard accessibility
    Given the delete confirmation modal is open
    And she is using keyboard navigation
    When she presses Tab
    Then focus moves between [Cancel] and [Delete Playbook] buttons
    When she focuses [Cancel] and presses Enter
    Then the modal closes without deleting
    When she reopens modal and focuses [Delete Playbook] and presses Enter
    Then the playbook is deleted

  Scenario: PB-DELETE-16 ✅ Deletion removes from all views
    Given Maria deletes playbook "Old Patterns"
    Then "Old Patterns" is removed from:
      | view                    |
      | Playbooks list          |
      | Search results          |
      | Recent playbooks        |
      | Dashboard widgets       |
      | MCP available playbooks |

  Scenario: PB-DELETE-17 ✅ Deletion cannot be undone
    Given Maria has deleted playbook "Mistake Delete"
    Then there is no [Undo] option
    And there is no way to recover the deleted playbook
    And she sees notification "Deletion is permanent and cannot be undone"

  Scenario: PB-DELETE-18 ⏭️ Delete local-only playbook
    Given Maria owns local-only playbook "Draft Methodology"
    And it is not synced to Homebase
    When she deletes it
    Then it is removed only from local FOB
    And no Homebase sync operation occurs

  Scenario: PB-DELETE-19 ✅ Delete error handling
    Given the delete confirmation modal is open
    And a database error occurs during deletion
    When she clicks [Delete Playbook]
    Then she sees error notification "Failed to delete playbook: [error details]"
    And the playbook is not deleted
    And the modal remains open
    And she can [Retry] or [Cancel]

  Scenario: PB-DELETE-20 ✅ Delete with export backup suggestion
    Given Maria owns playbook "Important Methodology"
    And it has significant content
    When she opens the delete confirmation modal
    Then she sees suggestion "Consider exporting before deleting"
    And she sees [Export JSON First] link
    When she clicks [Export JSON First]
    Then the export download is triggered
    And the modal remains open for her to proceed with deletion
