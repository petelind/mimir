# Act 1: Maria's Onboarding - Screen ID Mapping

**Purpose**: Traceability matrix linking User Journey → Screen IDs → Wireframes → Feature Files

**Act**: Act 1 - Maria's Onboarding  
**User Journey Reference**: `docs/ux/user_journey.md` lines 170-235

---

## ⚠️ Critical Architectural Note

**Playbooks Are STATIC Reference Material**

See main architectural note in `user_journey.md` for full details.

---

## Screen ID Convention

**Format**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

**Systems**:
- `HB` = Homebase (Web Interface)
- `FOB` = Forward Operating Base (Local Django GUI)

---

## Screen Inventory

### HB Screens (Registration Flow)

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `HB-REGISTER-1` | HB Registration Page | User fills registration form (email, password, name) | Line 174-179 |
| `HB-EMAIL-VERIFY-1` | HB Email Verification | Email confirmation screen/link | Line 181-182 |
| `HB-TOKEN-SUCCESS-1` | HB Registration Success - Token Display | Shows Django DRF token, HB URL, setup options | Line 184-198 |

### FOB Screens (Setup & Configuration)

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-CONNECT-HB-1` | FOB First Launch - HB Connection | Configure HB URL and token, or skip for local-only | Line 210-223 |
| `FOB-SYNC-PREFS-1` | FOB Sync Preferences | Configure auto-sync, frequency, conflict resolution | Line 225-228 |
| `FOB-MCP-CONFIG-1` | FOB External MCP Configuration | Configure external MCPs (GitHub, Jira) in Windsurf | Line 230-233 |
| `FOB-DASHBOARD-1` | FOB Dashboard | First view of FOB main interface | Line 235 + Act 1.5 |

### External/Guide Screens (Non-UI)

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `GUIDE-FOB-SETUP-1` | FOB Setup Guide | PDF/documentation for downloading container | Line 194, 200-208 |

---

## Flow Diagram Mapping

### Primary Flow: Maria's Registration & Setup

```
START
  ↓
HB-REGISTER-1 (Fill form)
  ↓
HB-EMAIL-VERIFY-1 (Click confirmation link)
  ↓
HB-TOKEN-SUCCESS-1 (Save token, see HB URL)
  ↓
[External: Download FOB container, configure in Windsurf]
  ↓
FOB-CONNECT-HB-1 (Paste token, test connection)
  ↓
Decision: Skip or Connect?
  → Skip: FOB-DASHBOARD-1 (local-only mode)
  → Connect: FOB-SYNC-PREFS-1
      ↓
    FOB-MCP-CONFIG-1 (Configure external MCPs)
      ↓
    FOB-DASHBOARD-1 (connected mode)
      ↓
    END
```

### Alternative Path: Local-Only Mode

```
FOB-CONNECT-HB-1
  ↓
User clicks "Skip - Work Locally"
  ↓
FOB-DASHBOARD-1 (local-only, no sync)
  ↓
END (can add HB connection later in Settings)
```

---

## Key Integration Points

### Token-Based Authentication

**Critical Flow**:
1. `HB-REGISTER-1` → User registers
2. `HB-EMAIL-VERIFY-1` → Email confirmed
3. `HB-TOKEN-SUCCESS-1` → Django DRF token generated and displayed
4. `FOB-CONNECT-HB-1` → User pastes token to connect FOB to HB

**Token Properties**:
- Format: `mimir_[random_hash]`
- Purpose: Authenticates FOB to HB for sync operations
- Can be regenerated from HB account page
- Only one HB connection per FOB

### External MCP Configuration

**Important Note**: This happens in Windsurf settings, NOT in FOB GUI
- `FOB-MCP-CONFIG-1` is informational/guide screen in FOB
- Actual configuration: Windsurf → MCP Settings → Add servers
- GitHub MCP, Jira MCP, etc. are 3rd party servers
- Separate from Mimir MCP (which is part of FOB container)

---

## Feature File Cross-Reference

**Planned Feature Files**:
- `docs/features/hb-registration.feature` → HB-REGISTER-1, HB-EMAIL-VERIFY-1, HB-TOKEN-SUCCESS-1
- `docs/features/fob-setup.feature` → FOB-CONNECT-HB-1, FOB-SYNC-PREFS-1
- `docs/features/fob-dashboard.feature` → FOB-DASHBOARD-1

**Example Gherkin**:
```gherkin
Scenario: User registers on Homebase and receives token
  Given user navigates to "HB-REGISTER-1"
  When user fills registration form with valid data
  And user clicks "Register" button
  Then user receives verification email
  When user clicks confirmation link
  Then user is redirected to "HB-TOKEN-SUCCESS-1"
  And user sees Django DRF authentication token
  And user sees Homebase URL
  
Scenario: User connects FOB to Homebase with token
  Given user has authentication token from HB
  And FOB container is starting
  When FOB shows "FOB-CONNECT-HB-1"
  And user pastes HB URL and token
  And user clicks "Test Connection"
  Then connection is successful
  And user sees their account email
  When user clicks "Continue"
  Then user sees "FOB-SYNC-PREFS-1"

Scenario: User skips HB connection for local-only mode
  Given FOB is showing "FOB-CONNECT-HB-1"
  When user clicks "Skip - Work Locally"
  Then user sees "FOB-DASHBOARD-1"
  And connection status shows "Local FOB"
  And sync features are disabled
  And user can add HB connection later in Settings
```

---

## Django Implementation Notes

### HB Screens
- `HB-REGISTER-1` → New: `templates/accounts/register.html`
- `HB-EMAIL-VERIFY-1` → Django built-in email verification
- `HB-TOKEN-SUCCESS-1` → New: `templates/accounts/token_success.html`
  - Generate token using Django REST Framework TokenAuthentication
  - Display token with copy button
  - Link to FOB setup guide

### FOB Screens
- `FOB-CONNECT-HB-1` → New: `templates/setup/connect_hb.html`
  - First-run wizard screen
  - Form with HB URL and token inputs
  - "Test Connection" AJAX call to verify token
  - "Skip" button for local-only mode
- `FOB-SYNC-PREFS-1` → New: `templates/setup/sync_preferences.html`
- `FOB-MCP-CONFIG-1` → New: `templates/setup/mcp_guide.html` (informational)
- `FOB-DASHBOARD-1` → Extends existing or new `templates/dashboard.html`
  - Shows connection status in navbar
  - Different views for connected vs. local-only mode

---

## Next Steps

1. ✅ Screen IDs defined (7 screens + 1 guide)
2. ⏳ Add Act 1 diagram to `screen-flow.drawio` (page 3)
3. ⏳ Create wireframes for HB and FOB screens
4. ⏳ Write feature files
5. ⏳ Implement Django views/templates

---

**Version**: 1.0  
**Created**: 2024-11-20  
**Status**: Draft - Building diagram
