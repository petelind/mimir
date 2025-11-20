# Phase 2 Complete: Act 0 - Authentication & Setup Dialogue Map

**Status**: ✅ Complete  
**Date**: 2024-11-20  
**Commit**: 8732f81

---

## Deliverables

### 1. Screen ID Mapping
**File**: `act-0-authentication/screen-ids.md`

**Screen IDs Defined**: 11 unique identifiers

| Type | Count | Examples |
|------|-------|----------|
| HB Screens | 5 | `HB-LOGIN-1`, `HB-PLAYBOOK-CREATE-1`, `HB-PLAYBOOK-EDITOR-1` |
| HB Django Admin | 3 | `HB-ADMIN-DASHBOARD-1`, `HB-ADMIN-DASHBOARD-2`, `HB-ADMIN-APPROVAL-1` |
| FOB Screens | 2 | `FOB-STARTUP-1`, `FOB-ERROR-CONNECTION-1` |
| Final Screens | 1 | `HB-PLAYBOOK-ACTIVATED-1` |

**Naming Convention**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

---

### 2. Screen Flow Diagram (Page 2)
**File**: `act-4-mcp-usage/screen-flow.drawio` (Page 2: "Act 0 - Authentication & Setup")

**Elements**: 15+ components including:
- 5 HB screens (green)
- 3 HB Django Admin screens (yellow)
- 2 FOB screens (blue)
- 1 FOB error screen (red)
- 2 decision diamonds (user type, HB connection)
- Complete legend
- START and END nodes

**Visual Design**:
- ✅ Color-coded by system (Green=HB, Blue=FOB, Yellow=Admin, Red=Error)
- ✅ Two-branch flow (Mike's HB path, Maria's FOB path)
- ✅ Decision points clearly marked
- ✅ Error path with dashed red arrows
- ✅ Proper spacing and layout

---

## Key Flows Mapped

### Flow 1: Mike's Authentication (HB Admin)
```
START → User Type Decision → "Mike (HB Admin)"
  → HB-LOGIN-1 (login page)
  → HB-ADMIN-DASHBOARD-1 (Django Admin)
```

### Flow 2: Maria's Authentication (FOB User)
```
START → User Type Decision → "Maria (FOB User)"
  → FOB-STARTUP-1 (container initialization)
  → HB Connection Decision
    → Yes: FOB Dashboard (Act 1)
    → No: FOB-ERROR-CONNECTION-1 (error modal with retry/offline options)
```

### Flow 3: Mike Creates Playbook (Act 0.1)
```
HB-ADMIN-DASHBOARD-1 (Mike continues)
  → HB-ADMIN-DASHBOARD-2 (playbook management view)
  → HB-PLAYBOOK-CREATE-1 (wizard: name, description, category)
  → HB-PLAYBOOK-EDITOR-1 (structure: activities, artifacts, dependencies)
  → HB-PLAYBOOK-ASSIGN-1 (family: Usability, visibility: Public)
  → HB-PLAYBOOK-PENDING-1 (awaiting approval)
```

### Flow 4: Sarah Approves Playbook
```
HB-PLAYBOOK-PENDING-1 (notification sent)
  → HB-ADMIN-APPROVAL-1 (Sarah in Django Admin reviews)
  → Approves
  → HB-PLAYBOOK-ACTIVATED-1 (Mike receives notification)
  → END (Playbook available to Usability family)
```

---

## Integration Points

### With User Journey
- **Source**: `docs/ux/user_journey.md` lines 70-167
- **Coverage**: 100% of Act 0 and Act 0.1

### With Django Templates
**Screens to implement**:
- `HB-LOGIN-1` → Already exists: `templates/accounts/login.html`
- `HB-ADMIN-DASHBOARD-1` → Django Admin (built-in)
- `FOB-STARTUP-1` → New: Container startup screen
- `FOB-ERROR-CONNECTION-1` → New: Error modal component
- `HB-PLAYBOOK-CREATE-1` → New: `templates/playbooks/create_wizard.html`
- `HB-PLAYBOOK-EDITOR-1` → New: `templates/playbooks/editor.html`
- `HB-PLAYBOOK-ASSIGN-1` → New: `templates/playbooks/assign_family.html`

---

## Multi-Page Diagram Structure

The diagram file now contains **2 pages**:

### Page 1: Act 4 - MCP Usage Flow
- 20+ elements
- MCP tool calls (grey boxes)
- External MCP integration (GitHub)
- Windsurf interface flows

### Page 2: Act 0 - Authentication & Setup
- 15+ elements
- Two-branch authentication (Mike/Maria)
- Playbook creation workflow
- Error handling paths

**To view**:
1. Open https://app.diagrams.net/
2. Open `docs/ux/2_dialogue-maps/act-4-mcp-usage/screen-flow.drawio`
3. Click tabs at bottom: "Act 4 - MCP Usage Flow" or "Act 0 - Authentication & Setup"

---

## Feature File Cross-Reference

**Planned**:
- `docs/features/hb-authentication.feature` → HB-LOGIN-1, HB-ADMIN-DASHBOARD-1
- `docs/features/fob-startup.feature` → FOB-STARTUP-1, FOB-ERROR-CONNECTION-1
- `docs/features/hb-playbook-creation.feature` → HB-PLAYBOOK-CREATE-1 through HB-PLAYBOOK-PENDING-1
- `docs/features/hb-playbook-approval.feature` → HB-ADMIN-APPROVAL-1, HB-PLAYBOOK-ACTIVATED-1

**Example Gherkin**:
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

Scenario: Playbook author creates and publishes playbook
  Given Mike is on "HB-ADMIN-DASHBOARD-2"
  When Mike creates playbook on "HB-PLAYBOOK-CREATE-1"
  And structures it on "HB-PLAYBOOK-EDITOR-1"
  And assigns to family on "HB-PLAYBOOK-ASSIGN-1"
  Then playbook status is "Pending" on "HB-PLAYBOOK-PENDING-1"
  When system admin approves on "HB-ADMIN-APPROVAL-1"
  Then Mike sees "HB-PLAYBOOK-ACTIVATED-1"
  And playbook is available to family members
```

---

## Summary

**Total Screens Mapped Across Both Acts**:
- **Act 0**: 11 screens
- **Act 4**: 12 screens
- **Total**: 23 unique screen IDs

**Diagram Pages**: 2 (Act 4, Act 0)

**Systems Covered**:
- ✅ HB Web Interface (authentication, playbook creation)
- ✅ HB Django Admin (system administration, approvals)
- ✅ FOB Container (startup, error handling)
- ✅ MCP Server (Act 4 - playbook context)
- ✅ External MCPs (Act 4 - GitHub integration)

---

## Next Phase Options

**Remaining Acts**:
- Act 1: Maria's Onboarding (HB registration, FOB setup, token configuration)
- Act 2: Family Management (create, join, admin workflows)
- Act 3: Sync & Discovery (download playbooks, explore details)
- Act 5: PIP Creation & Approval (user-initiated improvements)
- Act 6: Sync Scenarios (upload, conflicts)
- Act 7: Playbook Creation (3 different types)
- Act 8: Settings & Preferences
- Act 9: Error Recovery

**Recommendation**: Act 1 next (completes authentication foundation with registration & token flow)

---

**Phase 2 Status**: ✅ **COMPLETE**  
**Awaiting**: User review and next phase selection
