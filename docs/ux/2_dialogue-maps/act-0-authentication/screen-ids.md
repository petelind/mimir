# Act 0: System Entry & Authentication - Screen ID Mapping

**Purpose**: Traceability matrix linking User Journey → Screen IDs → Wireframes → Feature Files

**Act**: Act 0 - System Entry & Authentication + Act 0.1 - The Foundation (Mike's Setup)  
**User Journey Reference**: `docs/ux/user_journey.md` lines 70-167

---

## ⚠️ Critical Architectural Note

**Playbooks Are STATIC Reference Material**

See `act-4-mcp-usage/screen-ids.md` for full architectural note.
- Playbooks = Static documentation (like a book)
- Work tracking = External systems only (GitHub/Jira)
- AI/MCP = Cross-references between the two

---

## Screen ID Convention

**Format**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

**Systems**:
- `HB` = Homebase (Django Admin + Web Interface)
- `FOB` = Forward Operating Base (Local Django GUI)
- `HB-ADMIN` = Homebase Django Admin Interface (system administrator)

---

## Screen Inventory

### Act 0: System Entry & Authentication

#### HB Screens

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `HB-LOGIN-1` | HB Login Page | User login to Homebase web interface | Line 76-85 |
| `HB-ADMIN-DASHBOARD-1` | HB Django Admin Dashboard | System admin view (Django's built-in admin) | Line 87-98 |

#### FOB Screens

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-STARTUP-1` | FOB Login/Startup | Container initialization and authentication | Line 100-107 |
| `FOB-ERROR-CONNECTION-1` | FOB Connection Failed (Error Modal) | Error when FOB can't reach Homebase | Line 109-115 |

---

### Act 0.1: The Foundation (Mike's Setup)

#### HB Admin Screens (Mike - Playbook Author)

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `HB-ADMIN-DASHBOARD-2` | HB Admin Dashboard | Main dashboard for playbook management | Line 123-124 |
| `HB-PLAYBOOK-CREATE-1` | HB Create Playbook Wizard | Form to create new playbook | Line 126-130 |
| `HB-PLAYBOOK-EDITOR-1` | HB Playbook Editor | Visual editor for playbook structure | Line 132-136 |
| `HB-PLAYBOOK-ASSIGN-1` | HB Family Assignment | Assign playbook to family, set visibility | Line 138-142 |
| `HB-PLAYBOOK-PENDING-1` | HB Pending Approval | Confirmation of submission | Line 144-147 |

#### HB Admin Screens (Sarah - System Administrator)

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `HB-ADMIN-APPROVAL-1` | Django Admin: Playbook Approval | System admin reviews and approves playbook | Line 149-159 |
| `HB-PLAYBOOK-ACTIVATED-1` | HB Playbook Activated | Notification of approval to author | Line 161-165 |

---

## Flow Diagram Mapping

### Act 0: Authentication Flows

**Mike's Flow (HB Admin)**:
1. `HB-LOGIN-1` → Login as admin
2. `HB-ADMIN-DASHBOARD-1` → Django Admin interface

**Maria's Flow (FOB User)**:
1. `FOB-STARTUP-1` → Container starts
2. Decision: Connected to HB?
   - Yes → Dashboard
   - No → `FOB-ERROR-CONNECTION-1` → Retry/Offline options

### Act 0.1: Playbook Creation & Approval

**Mike's Playbook Creation Flow**:
1. `HB-ADMIN-DASHBOARD-2` → Start
2. `HB-PLAYBOOK-CREATE-1` → Enter basic info
3. `HB-PLAYBOOK-EDITOR-1` → Structure playbook (activities, artifacts)
4. `HB-PLAYBOOK-ASSIGN-1` → Assign to family
5. `HB-PLAYBOOK-PENDING-1` → Await approval

**Sarah's Approval Flow**:
6. `HB-ADMIN-APPROVAL-1` → Review in Django Admin
7. Approve → `HB-PLAYBOOK-ACTIVATED-1` → Mike receives notification

**Result**: Playbook available to Usability family members

---

## Feature File Cross-Reference

**Planned Feature Files**:
- `docs/features/hb-authentication.feature` → HB-LOGIN-1
- `docs/features/fob-startup.feature` → FOB-STARTUP-1, FOB-ERROR-CONNECTION-1
- `docs/features/hb-playbook-creation.feature` → HB-PLAYBOOK-CREATE-1, HB-PLAYBOOK-EDITOR-1
- `docs/features/hb-playbook-approval.feature` → HB-ADMIN-APPROVAL-1

**Screen ID Usage in Feature Files**:
```gherkin
Scenario: Admin logs into Homebase
  Given user is on "HB-LOGIN-1"
  When user enters valid credentials
  Then user is redirected to "HB-ADMIN-DASHBOARD-1"
  And user sees Django Admin interface

Scenario: FOB starts without Homebase connection
  Given FOB container is starting on "FOB-STARTUP-1"
  When connection to Homebase fails
  Then user sees "FOB-ERROR-CONNECTION-1"
  And user can choose "Work Offline" or "Retry Connection"
```

---

## Next Steps

1. ✅ Screen IDs defined (11 screens)
2. ⏳ Add Act 0 diagram to `screen-flow.drawio` (new page/tab)
3. ⏳ Create wireframes for HB and FOB screens
4. ⏳ Write feature files referencing these IDs
5. ⏳ Implement Django views/templates

---

**Version**: 1.0  
**Created**: 2024-11-20  
**Status**: Draft - Building diagram
