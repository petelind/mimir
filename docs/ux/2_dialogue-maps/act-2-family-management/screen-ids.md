# Act 2: Family Management - Screen ID Mapping

**Purpose**: Traceability matrix linking User Journey → Screen IDs → Wireframes → Feature Files

**Act**: Act 2 - Building Her Network + Act 2.5 - Family Admin Workflows  
**User Journey Reference**: `docs/ux/user_journey.md` lines 314-444

---

## ⚠️ Critical Architectural Note

**Playbooks Are STATIC Reference Material**

See main architectural note in `user_journey.md` for full details.

---

## Screen ID Convention

**Format**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

**Systems**:
- `FOB` = Forward Operating Base (Local Django GUI)

---

## Screen Inventory

### Act 2: Building Her Network

#### FOB Screens (Family Creation & Browsing)

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-DASHBOARD-FIRST-1` | FOB Dashboard (First Login) | Empty state with create/browse/sync buttons | Line 318-323 |
| `FOB-FAMILY-CREATE-1` | FOB Create Family | Form to create new family (public or hidden) | Line 325-344 |
| `FOB-FAMILY-BROWSER-1` | FOB Family Browser | Browse and search public families | Line 347-351 |
| `FOB-FAMILY-DETAILS-1` | FOB Family Details | View family info, members, playbooks before joining | Line 353-359 |
| `FOB-FAMILY-JOINED-1` | FOB Family Joined Notification | Toast/modal confirming family membership | Line 361-366 |

---

### Act 2.5: Family Admin Workflows

#### FOB Admin Screens

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-FAMILY-ADMIN-1` | FOB Family Admin Dashboard | Overview of family: members, pending requests, playbooks | Line 375-382 |
| `FOB-JOIN-REQUESTS-1` | FOB Join Requests Tab | List of pending join requests with approve/reject actions | Line 384-398 |
| `FOB-APPROVE-MODAL-1` | Confirm Join Approval Modal | Confirmation dialog for approving member | Line 405-410 |
| `FOB-REJECT-MODAL-1` | Reject Join Request Modal | Rejection dialog with optional reason and block option | Line 412-417 |
| `FOB-PLAYBOOK-SUBMISSIONS-1` | FOB Playbook Submissions Tab | List of pending playbook submissions to review | Line 421-427 |
| `FOB-PLAYBOOK-PREVIEW-1` | Playbook Preview Modal | Full playbook structure preview for review | Line 429-434 |
| `FOB-PLAYBOOK-APPROVE-MODAL-1` | Confirm Playbook Approval Modal | Confirmation to approve playbook for family | Line 436-441 |

---

## Flow Diagram Mapping

### Flow 1: Create Families (Public & Hidden)

```
FOB-DASHBOARD-FIRST-1 (Empty state)
  ↓
Click "Create Family"
  ↓
FOB-FAMILY-CREATE-1 (Form)
  ├─ Create #1: "UX" (Public, Requires Approval)
  └─ Create #2: "Acme, INC" (Hidden, Invite Only)
```

### Flow 2: Browse and Join Existing Family

```
FOB-DASHBOARD-FIRST-1
  ↓
Click "Browse Families"
  ↓
FOB-FAMILY-BROWSER-1 (Search/filter public families)
  ↓
Click on "Usability" family
  ↓
FOB-FAMILY-DETAILS-1 (View members, playbooks, join policy)
  ↓
Click "Join Family"
  ↓
Decision: Auto-approve or Requires Approval?
  ├─ Auto-approve: FOB-FAMILY-JOINED-1 (immediate)
  └─ Requires Approval: Request sent (wait for admin)
```

### Flow 3: Family Admin - Approve Join Request

```
FOB-FAMILY-ADMIN-1 (Overview with pending requests badge)
  ↓
Click "Members Tab → Join Requests (2)"
  ↓
FOB-JOIN-REQUESTS-1 (List of pending requests)
  ↓
Review request #1 (Alex Thompson)
  ↓
Click [Approve]
  ↓
FOB-APPROVE-MODAL-1 (Confirm approval)
  ↓
Click [Confirm]
  ↓
Alex added to family, notification sent
```

### Flow 4: Family Admin - Reject Spam Request

```
FOB-JOIN-REQUESTS-1 (Pending requests list)
  ↓
Review request #2 (Spam Bot)
  ↓
Click [Reject]
  ↓
FOB-REJECT-MODAL-1 (Rejection reason, block option)
  ↓
Click [Reject]
  ↓
Request rejected, user optionally blocked
```

### Flow 5: Family Admin - Approve Playbook Submission

```
FOB-FAMILY-ADMIN-1 (Overview)
  ↓
Click "Playbooks Tab → Pending Submissions (1)"
  ↓
FOB-PLAYBOOK-SUBMISSIONS-1 (List of pending playbooks)
  ↓
Click [Preview Full]
  ↓
FOB-PLAYBOOK-PREVIEW-1 (Full playbook structure modal)
  ↓
Click [Approve]
  ↓
FOB-PLAYBOOK-APPROVE-MODAL-1 (Confirm approval)
  ↓
Click [Confirm]
  ↓
Playbook available to all family members
```

---

## Key Concepts

### Family Visibility Types

**Public Families**:
- Appear in `FOB-FAMILY-BROWSER-1`
- Anyone can discover and request to join
- Example: "UX" family

**Hidden Families**:
- Do NOT appear in browse
- Only visible to invited members
- Example: "Acme, INC" (client work)

### Join Policies

**Auto-Approve**:
- User clicks "Join Family"
- Immediate membership (no admin review)
- Example: "Usability" family

**Requires Approval**:
- User clicks "Join Family" → Request sent
- Admin reviews in `FOB-JOIN-REQUESTS-1`
- Admin approves/rejects
- Example: "UX" family

**Invite Only**:
- Users cannot request to join
- Admin must manually invite members
- Example: "Acme, INC" family

---

## Feature File Cross-Reference

**Planned Feature Files**:
- `docs/features/fob-family-creation.feature` → FOB-FAMILY-CREATE-1
- `docs/features/fob-family-browsing.feature` → FOB-FAMILY-BROWSER-1, FOB-FAMILY-DETAILS-1
- `docs/features/fob-family-admin-join-requests.feature` → FOB-JOIN-REQUESTS-1, FOB-APPROVE-MODAL-1, FOB-REJECT-MODAL-1
- `docs/features/fob-family-admin-playbook-review.feature` → FOB-PLAYBOOK-SUBMISSIONS-1, FOB-PLAYBOOK-PREVIEW-1, FOB-PLAYBOOK-APPROVE-MODAL-1

**Example Gherkin**:
```gherkin
Feature: Create Public and Hidden Families

  Scenario: User creates public family
    Given user is on "FOB-DASHBOARD-FIRST-1"
    When user clicks "Create Family"
    Then user sees "FOB-FAMILY-CREATE-1"
    When user fills form:
      | Field        | Value                                  |
      | Name         | UX                                     |
      | Description  | User Experience methodologies          |
      | Visibility   | Public                                 |
      | Join Policy  | Requires Approval                      |
      | Category     | Design                                 |
    And user clicks "Create Family"
    Then family "UX" is created
    And user is admin of "UX" family

  Scenario: User creates hidden family
    Given user is on "FOB-FAMILY-CREATE-1"
    When user fills form:
      | Field        | Value                                  |
      | Name         | Acme, INC                              |
      | Visibility   | Hidden                                 |
      | Join Policy  | Invite Only                            |
    And user clicks "Create Family"
    Then family "Acme, INC" is created
    And family does NOT appear in "FOB-FAMILY-BROWSER-1"

Feature: Browse and Join Families

  Scenario: User joins auto-approve family
    Given user is on "FOB-FAMILY-BROWSER-1"
    When user clicks on "Usability" family
    Then user sees "FOB-FAMILY-DETAILS-1"
    And join policy shows "Auto-approve"
    When user clicks "Join Family"
    Then user is immediately added to family
    And user sees "FOB-FAMILY-JOINED-1" notification
    And family playbooks are now visible

  Scenario: User requests to join approval-required family
    Given user is on "FOB-FAMILY-DETAILS-1" for "UX" family
    And join policy shows "Requires Approval"
    When user clicks "Join Family"
    Then join request is sent to family admin
    And user sees "Request sent" message
    And user is NOT yet a member

Feature: Family Admin Reviews Join Requests

  Scenario: Admin approves legitimate join request
    Given user is admin of "UX" family
    And user is on "FOB-FAMILY-ADMIN-1"
    And there are 2 pending join requests
    When user clicks "Members Tab → Join Requests (2)"
    Then user sees "FOB-JOIN-REQUESTS-1"
    And request from "Alex Thompson" is shown
    When user clicks [Approve] for Alex
    Then user sees "FOB-APPROVE-MODAL-1"
    When user clicks [Confirm]
    Then Alex is added to "UX" family
    And Alex receives notification
    And pending requests count decreases to 1

  Scenario: Admin rejects and blocks spam request
    Given user is on "FOB-JOIN-REQUESTS-1"
    When user clicks [Reject] for "Spam Bot"
    Then user sees "FOB-REJECT-MODAL-1"
    When user checks "Block user from future requests"
    And user clicks [Reject]
    Then request is rejected
    And "Spam Bot" is blocked from "UX" family
    And pending requests count decreases

Feature: Family Admin Reviews Playbook Submissions

  Scenario: Admin approves playbook submission
    Given user is admin of "UX" family
    And user is on "FOB-FAMILY-ADMIN-1"
    And there is 1 pending playbook submission
    When user clicks "Playbooks Tab → Pending Submissions (1)"
    Then user sees "FOB-PLAYBOOK-SUBMISSIONS-1"
    And playbook "Information Architecture Patterns" by Tom is shown
    When user clicks [Preview Full]
    Then user sees "FOB-PLAYBOOK-PREVIEW-1"
    And full playbook structure is displayed
    When user clicks [Approve]
    Then user sees "FOB-PLAYBOOK-APPROVE-MODAL-1"
    When user clicks [Confirm]
    Then playbook is activated in "UX" family
    And Tom receives approval notification
    And all family members can now access playbook
```

---

## Django Implementation Notes

### FOB Screens

**Family Creation**:
- `FOB-FAMILY-CREATE-1` → New: `templates/families/create.html`
  - Form fields: name, description, visibility, join_policy, category
  - Visibility choices: Public, Hidden
  - Join policy choices: Auto-approve, Requires Approval, Invite Only
  - Creates Family model instance with user as admin

**Family Browsing**:
- `FOB-FAMILY-BROWSER-1` → New: `templates/families/browser.html`
  - List view with search and filters
  - Only shows Public families
  - Displays member count, playbook count
  
- `FOB-FAMILY-DETAILS-1` → New: `templates/families/detail.html`
  - Shows family info, members, playbooks
  - "Join Family" button logic depends on join_policy
  - Auto-approve: Immediate membership
  - Requires Approval: Create JoinRequest instance

**Family Admin**:
- `FOB-FAMILY-ADMIN-1` → New: `templates/families/admin_dashboard.html`
  - Tabs: Overview, Members, Playbooks, Settings
  - Badge notifications for pending counts
  - Only accessible to family admins

- `FOB-JOIN-REQUESTS-1` → New: `templates/families/join_requests.html`
  - List of JoinRequest instances where status='pending'
  - Approve action: Update JoinRequest.status='approved', add user to family
  - Reject action: Update JoinRequest.status='rejected', optionally block

- `FOB-PLAYBOOK-SUBMISSIONS-1` → New: `templates/families/playbook_submissions.html`
  - List of PlaybookSubmission instances where status='pending'
  - Preview modal shows full playbook structure
  - Approve action: Update status='approved', make playbook visible to family

**Modals**:
- All modals use Bootstrap 5 modal components
- AJAX submit for approve/reject actions
- Success/error notifications via toast

---

## Next Steps

1. ✅ Screen IDs defined (12 screens)
2. ⏳ Add Act 2 diagram to `screen-flow.drawio` (page 4)
3. ⏳ Create wireframes
4. ⏳ Write feature files
5. ⏳ Implement Django models (Family, JoinRequest, PlaybookSubmission)
6. ⏳ Implement views and templates

---

**Version**: 1.0  
**Created**: 2024-11-20  
**Status**: Draft - Building diagram
