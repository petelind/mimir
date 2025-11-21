# Act 5: Creating PIPs - Screen ID Mapping

**Purpose**: Traceability matrix linking User Journey → Screen IDs → Wireframes → Feature Files

**Act**: Act 5 - Evolving Playbooks (Creating PIPs)  
**User Journey Reference**: `docs/ux/user_journey.md` lines 756-814

---

## Screen ID Convention

**Format**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

**Systems**:
- `WINDSURF` = Windsurf IDE Chat Interface
- `MCP` = Mimir MCP Server (background processing)
- `FOB` = Forward Operating Base (Local Django GUI)

---

## Screen Inventory

### Act 5: Evolving Playbooks - Creating PIPs

#### Windsurf/MCP Screens

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `WINDSURF-CHAT-PIP-1` | Windsurf Chat - Suggest PIP | Maria asks MCP to create PIP for improvement | Line 760-767 |
| `MCP-PIP-PROPOSAL-1` | MCP PIP Proposal Response | MCP generates PIP structure and proposal | Line 769-786 |
| `MCP-CREATE-PIP-1` | MCP Create PIP Action | MCP creates PIP in local FOB after confirmation | Line 788-793 |

#### FOB Screens

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-PIP-NOTIFY-1` | FOB PIP Created Notification | Toast/notification that PIP was created | Line 795-799 |
| `FOB-PIP-REVIEW-1` | FOB PIP Review Interface | Detailed PIP view with diff and approve/edit/reject | Line 801-806 |
| `FOB-PIP-APPROVE-MODAL-1` | FOB PIP Approve Modal | Confirmation modal when approving PIP locally | Line 808-813 |

---

## Flow Diagram Mapping

### Flow: User-Initiated PIP Creation via MCP

```
WINDSURF-CHAT-PIP-1 (User suggests improvement)
  ↓
"mimir: This playbook could use accessibility testing.
 Can you help me create a PIP?"
  ↓
MCP-PIP-PROPOSAL-1 (MCP analyzes and generates proposal)
  ↓
Shows proposed PIP:
  - Type: Extension
  - Activity Name: "Accessibility Audit"
  - Position: After "Set up testing environment"
  - Dependencies defined
  ↓
"Shall I create this PIP in your local FOB?"
  ↓
User confirms: "Yes, create the PIP"
  ↓
MCP-CREATE-PIP-1 (MCP calls FOB API to create PIP)
  ↓
FOB-PIP-NOTIFY-1 (Notification appears)
  ↓
"New PIP created: Add Accessibility Audit activity
 Status: Draft (local only)
 [View PIP]"
  ↓
User clicks [View PIP]
  ↓
FOB-PIP-REVIEW-1 (Detailed PIP interface)
  ↓
Shows:
  - Proposed changes (diff view)
  - Original vs. Proposed structure
  - Rationale field
  - [Approve] [Edit] [Reject]
  ↓
User clicks [Approve]
  ↓
FOB-PIP-APPROVE-MODAL-1 (Confirmation modal)
  ↓
"PIP approved locally. Your FOB now uses v1.1 (local).
 To contribute back, sync with Homebase."
  ↓
Playbook version updated to v1.1 (local)
```

---

## Key Concepts

### PIP Types

**Extension**:
- Add new Activity, Artifact, or Goal
- Example: Add "Accessibility Audit" activity

**Modification**:
- Change existing Activity, Artifact, or Goal
- Example: Update "Setup Project" description

**Removal**:
- Remove or deprecate existing element
- Example: Remove outdated "IE11 Support" activity

### PIP Status Flow

**Draft (local only)**:
- Created locally
- Not yet synced to Homebase
- Only visible to creator

**Approved (local)**:
- User approved locally
- Playbook version incremented (e.g., v1.0 → v1.1 local)
- Changes applied to local FOB copy
- Ready to sync/submit to Homebase

**Submitted**:
- Sent to Homebase for review
- Original author and family admins notified
- Awaiting approval

**Accepted**:
- Original author approved
- Merged into official playbook
- New version released on Homebase

**Rejected**:
- Original author or admin rejected
- Not merged
- Can be revised and resubmitted

### Local vs. Remote Versioning

**Local Version**:
- Example: `v1.1 (local)`
- Contains approved PIPs not yet synced
- Only exists in user's FOB

**Remote Version**:
- Example: `v1.0` (on Homebase)
- Official version
- Accessible to all family members

**Conflict Scenario**:
- Local: `v1.1` (with Maria's PIP)
- Remote: `v1.2` (Mike released update)
- Must resolve before syncing (see Act 6)

---

## Feature File Cross-Reference

**Planned Feature Files**:
- `docs/features/mcp-create-pip.feature` → WINDSURF-CHAT-PIP-1, MCP-PIP-PROPOSAL-1, MCP-CREATE-PIP-1
- `docs/features/fob-pip-review.feature` → FOB-PIP-REVIEW-1, FOB-PIP-APPROVE-MODAL-1

**Example Gherkin**:
```gherkin
Feature: Create PIP via MCP

  Scenario: User suggests improvement and MCP creates PIP
    Given user is working in Windsurf
    And Mimir MCP is connected
    And user has "React Frontend Development" playbook v1.0 downloaded
    When user sends message to MCP:
      """
      mimir: This playbook is great, but it doesn't mention accessibility testing. 
      I think we should add an Activity for "Accessibility Audit" after the testing setup. 
      Can you help me create a PIP for this?
      """
    Then MCP analyzes request
    And MCP shows "WINDSURF-CHAT-PIP-1"
    And MCP generates PIP proposal
    And MCP shows "MCP-PIP-PROPOSAL-1" with:
      | Field       | Value                                    |
      | Type        | Extension (new Activity)                 |
      | Name        | Accessibility Audit                      |
      | Position    | After "Set up testing environment"       |
      | Upstream    | Setup Project                            |
      | Downstream  | Create Components                        |
    And MCP asks "Shall I create this PIP in your local FOB?"
    When user confirms "Yes, create the PIP"
    Then MCP calls FOB API: POST /api/pips/
    And PIP is created with status "draft"
    And user sees "FOB-PIP-NOTIFY-1"
    And notification shows:
      """
      New PIP created: Add Accessibility Audit activity
      Status: Draft (local only)
      [View PIP]
      """

Feature: Review and Approve PIP Locally

  Scenario: User reviews and approves PIP
    Given PIP "Add Accessibility Audit activity" exists with status "draft"
    And user sees "FOB-PIP-NOTIFY-1"
    When user clicks [View PIP]
    Then user sees "FOB-PIP-REVIEW-1"
    And diff view shows:
      | Section          | Original       | Proposed             |
      | Activities count | 10             | 11                   |
      | New activity     | (none)         | Accessibility Audit  |
      | Position         | N/A            | After activity #5    |
    And rationale field is populated
    And [Approve] button is enabled
    When user clicks [Approve]
    Then user sees "FOB-PIP-APPROVE-MODAL-1"
    And modal shows:
      """
      This PIP is approved locally. Your FOB now uses version 1.1 (local). 
      To contribute back to the original playbook, sync with Homebase.
      """
    When user clicks [Confirm]
    Then PIP status changes to "approved_local"
    And playbook version updates to "v1.1 (local)"
    And changes are applied to local playbook
    And user can continue using updated playbook
```

---

## Django Implementation Notes

### MCP Integration

**MCP PIP Creation Flow**:
1. User sends message to Mimir MCP in Windsurf
2. MCP uses NLU to extract:
   - PIP type (extension, modification, removal)
   - Target playbook
   - Proposed changes
   - Dependencies
3. MCP generates structured PIP proposal
4. User confirms
5. MCP calls FOB API: `POST /api/pips/`
   - Creates PIP instance with status="draft"
   - Associates with playbook and user

### FOB Screens

**PIP Notification**:
- `FOB-PIP-NOTIFY-1` → Use: Bootstrap toast component
  - Triggered by websocket or polling
  - Shows PIP summary
  - Link to FOB-PIP-REVIEW-1

**PIP Review Interface**:
- `FOB-PIP-REVIEW-1` → New: `templates/pips/review.html`
  - Diff view: Use diff2html.js or similar
  - Show original playbook structure vs. proposed
  - Highlight additions (green), removals (red), modifications (yellow)
  - Rationale textarea (pre-filled by MCP)
  - Actions: [Approve] [Edit] [Reject]

**PIP Approve Modal**:
- `FOB-PIP-APPROVE-MODAL-1` → Bootstrap modal
  - Explanation of local approval
  - Mention version increment
  - Suggest next step: Sync with Homebase to submit
  - Confirm button applies changes

**Backend Logic**:
- PIP Model:
  ```python
  class PIP(models.Model):
      playbook = models.ForeignKey(Playbook)
      creator = models.ForeignKey(User)
      type = models.CharField(choices=['extension', 'modification', 'removal'])
      title = models.CharField()
      description = models.TextField()
      proposed_changes = models.JSONField()  # Structured diff
      rationale = models.TextField()
      status = models.CharField(choices=['draft', 'approved_local', 'submitted', 'accepted', 'rejected'])
      created_at = models.DateTimeField(auto_now_add=True)
  ```

- Approve action:
  - Update PIP status to "approved_local"
  - Apply changes to local Playbook instance
  - Increment playbook version (1.0 → 1.1)
  - Add "(local)" suffix to version

---

## Next Steps

1. ✅ Screen IDs defined (6 screens)
2. ⏳ Add Act 5 diagram to `screen-flow.drawio` (page 6)
3. ⏳ Implement PIP model
4. ⏳ Create PIP review interface
5. ⏳ Implement MCP PIP creation logic

---

**Version**: 1.0  
**Created**: 2024-11-20  
**Status**: Draft - Building diagram
