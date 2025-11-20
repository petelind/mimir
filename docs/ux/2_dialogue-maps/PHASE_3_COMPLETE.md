# Phase 3 Complete: Act 1 - Maria's Onboarding Dialogue Map

**Status**: ✅ Complete  
**Date**: 2024-11-20  
**Commit**: d700ff2

---

## Deliverables

### 1. Screen ID Mapping
**File**: `act-1-onboarding/screen-ids.md`

**Screen IDs Defined**: 7 screens + 1 guide document

| Type | Count | Examples |
|------|-------|----------|
| HB Screens | 3 | `HB-REGISTER-1`, `HB-EMAIL-VERIFY-1`, `HB-TOKEN-SUCCESS-1` |
| FOB Screens | 4 | `FOB-CONNECT-HB-1`, `FOB-SYNC-PREFS-1`, `FOB-MCP-CONFIG-1`, `FOB-DASHBOARD-1` |
| Guides | 1 | `GUIDE-FOB-SETUP-1` (PDF documentation) |

---

### 2. Screen Flow Diagram (Page 3)
**File**: `screen-flow.drawio` (Page 3: "Act 1 - Onboarding")

**Elements**: 12+ components including:
- 3 HB screens (green) - Registration flow
- 4 FOB screens (blue) - Setup and configuration
- 1 decision diamond (yellow) - Skip or Connect
- 2 dashboard endpoints (connected vs local-only)
- Complete legend
- START and END nodes

---

## Key Flows Mapped

### Flow 1: HB Registration & Token Generation

```
START
  ↓
HB-REGISTER-1 (Fill form: email, password, name)
  ↓
HB-EMAIL-VERIFY-1 (Click confirmation link in email)
  ↓
HB-TOKEN-SUCCESS-1 (Django DRF token displayed)
  ↓
Download FOB container, configure in Windsurf
```

**Critical: Token-Based Authentication**
- Django REST Framework generates token upon email verification
- Token format: `mimir_[random_hash]`
- User must save token for FOB setup
- Can regenerate token from HB account page

### Flow 2: FOB Setup - Connected Mode (Primary Path)

```
FOB-CONNECT-HB-1 (First launch)
  ↓
User pastes HB URL + token
  ↓
Clicks "Test Connection" → ✓ Success
  ↓
Decision: Skip or Connect?
  ↓
Connect (token verified)
  ↓
FOB-SYNC-PREFS-1 (Configure auto-sync, frequency)
  ↓
FOB-MCP-CONFIG-1 (Guide for external MCPs)
  ↓
FOB-DASHBOARD-1 (Connected Mode)
  ✓ Connected to Homebase
  Sync enabled
  ↓
END
```

### Flow 3: FOB Setup - Local-Only Mode (Alternative Path)

```
FOB-CONNECT-HB-1 (First launch)
  ↓
Decision: Skip or Connect?
  ↓
Skip - Work Locally
  ↓
FOB-DASHBOARD-1 (Local-Only Mode)
  ⊝ Local FOB
  Sync disabled
  Can add HB connection later in Settings
  ↓
END
```

---

## Critical Architecture Points

### Token-Based Authentication

**Flow**:
1. User registers on HB → Email sent
2. User clicks verification link → Account activated
3. **Django DRF token generated** → Displayed on `HB-TOKEN-SUCCESS-1`
4. User saves token (copy or download guide)
5. User pastes token in `FOB-CONNECT-HB-1`
6. FOB verifies token with HB API
7. Connection established (or user skips for local-only)

**Properties**:
- One token per user
- Can be regenerated (invalidates old token)
- Used for all FOB→HB API calls
- Limitation: Only one HB connection per FOB

### External MCP Configuration

**Important Distinction**:
- `FOB-MCP-CONFIG-1` is a **guide/info screen** in FOB
- Actual configuration happens in **Windsurf settings** (not FOB GUI)
- External MCPs (GitHub, Jira) are **3rd party servers**
- Separate from **Mimir MCP** (part of FOB container)

**Flow**:
1. FOB shows guide screen with instructions
2. User opens Windsurf → Settings → MCP Servers
3. User adds GitHub MCP server configuration
4. User adds Jira MCP (optional)
5. Windsurf connects to these external servers
6. Mimir MCP (playbook context) + External MCPs (work items) = Full integration

---

## Integration Points

### With User Journey
- **Source**: `docs/ux/user_journey.md` lines 170-235
- **Coverage**: 100% of Act 1

### With Django Implementation

**HB Screens**:
- `HB-REGISTER-1` → New: `templates/accounts/register.html`
  - Standard Django form
  - Fields: email, password, full_name
  - CSRF protection
  
- `HB-EMAIL-VERIFY-1` → Django built-in email verification
  - Uses django-allauth or custom implementation
  - Sends confirmation email
  
- `HB-TOKEN-SUCCESS-1` → New: `templates/accounts/token_success.html`
  - Generate token: `Token.objects.create(user=user)`
  - Display with copy button
  - Link to FOB setup guide

**FOB Screens**:
- `FOB-CONNECT-HB-1` → New: `templates/setup/connect_hb.html`
  - First-run wizard
  - Form: HB URL, Token
  - AJAX "Test Connection" call
  - Skip button for local-only
  
- `FOB-SYNC-PREFS-1` → New: `templates/setup/sync_preferences.html`
  - Sync frequency settings
  - Auto-sync toggle
  - Conflict resolution preferences
  
- `FOB-MCP-CONFIG-1` → New: `templates/setup/mcp_guide.html`
  - Instructions for Windsurf MCP config
  - Links to external MCP documentation
  
- `FOB-DASHBOARD-1` → Update: `templates/dashboard.html`
  - Navbar shows connection status
  - Different views for connected vs local-only

---

## Feature File Examples

```gherkin
Feature: User Registration and Token Generation

  Scenario: User successfully registers and receives token
    Given user navigates to "HB-REGISTER-1"
    When user fills form with valid data
    And user clicks "Register" button
    Then user receives verification email
    When user clicks confirmation link
    Then user is redirected to "HB-TOKEN-SUCCESS-1"
    And Django DRF token is displayed
    And user sees Homebase URL
    And user can copy token
    And user can download setup guide

Feature: FOB Setup with Homebase Connection

  Scenario: User connects FOB to Homebase with token
    Given user has authentication token from HB
    And FOB container is starting
    When FOB displays "FOB-CONNECT-HB-1"
    And user enters HB URL "https://homebase.mimir.io"
    And user pastes authentication token
    And user clicks "Test Connection"
    Then connection is verified
    And user sees their email displayed
    When user clicks "Continue"
    Then user sees "FOB-SYNC-PREFS-1"
    When user configures sync preferences
    Then user sees "FOB-DASHBOARD-1" in connected mode
    And navbar shows "✓ Connected to Homebase"
    And sync features are enabled

  Scenario: User skips Homebase connection for local-only mode
    Given FOB is displaying "FOB-CONNECT-HB-1"
    When user clicks "Skip - Work Locally"
    Then user sees "FOB-DASHBOARD-1" in local-only mode
    And navbar shows "⊝ Local FOB"
    And sync features are disabled
    And user can add HB connection later in Settings menu
```

---

## Multi-Page Diagram Structure

The diagram file now has **3 pages**:

| Page | Name | Screens | Description |
|------|------|---------|-------------|
| **1** | Act 0 - Authentication and Setup | 11 | Mike's HB login, playbook creation, Sarah's approval |
| **2** | Act 4 - MCP Usage Flow | 12 | MCP tools, GitHub integration, AI PIP suggestions |
| **3** | Act 1 - Onboarding | 8 | Maria's registration, token generation, FOB setup |

**Total**: **31 unique screen IDs** mapped!

---

## File Reorganization

**Previous structure**:
```
docs/ux/2_dialogue-maps/
└── act-4-mcp-usage/
    └── screen-flow.drawio  ← Was here
```

**New structure**:
```
docs/ux/2_dialogue-maps/
├── screen-flow.drawio      ← Moved here (top-level)
├── act-0-authentication/
│   └── screen-ids.md
├── act-1-onboarding/
│   └── screen-ids.md
└── act-4-mcp-usage/
    └── screen-ids.md
```

**Benefit**: Single multi-page diagram file for all Acts at top level

---

## Summary

**Acts Completed**: 0, 1, 4  
**Screens Mapped**: 31 total
- Act 0: 11 screens (authentication, playbook creation)
- Act 1: 8 screens (registration, FOB setup)
- Act 4: 12 screens (MCP usage, work items, PIPs)

**Remaining Acts**: 2, 3, 5, 6, 7, 8, 9

**Next Recommended**: Act 2 (Family Management) or Act 3 (Sync & Discovery)

---

**Phase 3 Status**: ✅ **COMPLETE**  
**Awaiting**: User review and next phase selection
