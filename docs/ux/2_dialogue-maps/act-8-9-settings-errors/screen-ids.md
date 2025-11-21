# Acts 8 & 9: Settings & Error Recovery - Screen ID Mapping

**Purpose**: Traceability matrix linking User Journey → Screen IDs → Wireframes → Feature Files

**Acts**: Act 8 - Settings & Preferences + Act 9 - Error Recovery & Edge Cases  
**User Journey Reference**: `docs/ux/user_journey.md` lines 1339-1561

---

## Screen ID Convention

**Format**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

**Systems**:
- `FOB` = Forward Operating Base (Local Django GUI)

---

## Screen Inventory

### Act 8: Settings & Preferences

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-SETTINGS-MAIN-1` | FOB Settings Main | Settings hub with sidebar navigation | Line 1343-1359 |
| `FOB-SETTINGS-SYNC-1` | FOB Settings - Sync & Connection | Homebase connection, sync prefs, conflict resolution | Line 1361-1400 |
| `FOB-SETTINGS-STORAGE-1` | FOB Settings - Storage | Database location, cache, cleanup | Line 1401-1413 |
| `FOB-SETTINGS-MCP-1` | FOB Settings - MCP Configuration | MCP server status, features, external MCPs | Line 1415-1431 |
| `FOB-SETTINGS-NOTIFICATIONS-1` | FOB Settings - Notifications | Notification preferences and quiet hours | Line 1433-1449 |

---

### Act 9: Error Recovery & Edge Cases

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-SYNC-ERROR-1` | FOB Sync Dashboard - Error | Sync failure with recovery actions | Line 1460-1481 |
| `FOB-PERMISSION-ERROR-1` | FOB Permission Denied Modal | Edit permission error with recovery options | Line 1486-1500 |
| `FOB-UPLOAD-ERROR-1` | FOB Upload Failed | Upload failure with optimization suggestions | Line 1505-1517 |
| `FOB-CORRUPTION-ERROR-1` | FOB Playbook Corruption | Data corruption with recovery options | Line 1522-1535 |
| `FOB-EMPTY-PLAYBOOKS-1` | FOB Dashboard - Empty State | No playbooks yet, onboarding guidance | Line 1540-1549 |
| `FOB-EMPTY-SEARCH-1` | FOB Family Browser - No Results | No search results with suggestions | Line 1551-1560 |

---

## Flow Diagram Mapping

### Act 8: Settings Navigation

```
FOB-SETTINGS-MAIN-1 (Entry point)
  ↓
Sidebar Navigation:
  ├─ Account (default)
  ├─ FOB-SETTINGS-SYNC-1 (Sync & Connection)
  ├─ FOB-SETTINGS-STORAGE-1 (Storage)
  ├─ FOB-SETTINGS-MCP-1 (MCP Configuration)
  ├─ FOB-SETTINGS-NOTIFICATIONS-1 (Notifications)
  ├─ Privacy
  └─ Advanced
```

### Act 9: Error Recovery Paths

**Sync Failure**:
```
FOB-SYNC-ERROR-1
  ↓
Options:
  ├─ [Retry Sync] → Attempt sync again
  ├─ [Check Connection Settings] → FOB-SETTINGS-SYNC-1
  ├─ [Work Offline] → Continue with local playbooks
  └─ [View Error Log] → Error log viewer
```

**Permission Error**:
```
FOB-PERMISSION-ERROR-1
  ↓
Options:
  ├─ [Create Local Copy] → Creates editable copy
  ├─ [Submit PIP] → Opens PIP creation flow
  └─ [Cancel] → Returns to previous screen
```

**Upload Failure**:
```
FOB-UPLOAD-ERROR-1
  ↓
Options:
  ├─ [Compress Images] → Auto-optimize media
  ├─ [Remove Large Artifacts] → Manual selection
  ├─ [Split into Multiple Playbooks] → Guidance
  └─ [Contact Support] → Support form
```

---

## Key Concepts

### Settings Organization

**Sidebar Sections**:
- **Account**: Profile, password, 2FA, delete account
- **Sync & Connection**: Homebase URL, token, sync preferences
- **Storage**: Database location, cache, cleanup
- **MCP Configuration**: Server status, features, API keys
- **Notifications**: Preferences, methods, quiet hours
- **Privacy**: Data sharing, analytics
- **Advanced**: Debug mode, experimental features

### Connection States

**Connected to Homebase**:
- Shows connection status, last sync time
- Sync preferences enabled
- Can upload/download playbooks

**Not Connected** (Local-Only Mode):
- Cannot sync with families
- Can use local playbooks and MCP
- Clear guidance on limitations

### Error Categories

**Network Errors**:
- Connection timeout
- Homebase unreachable
- Recovery: Retry, work offline

**Permission Errors**:
- Cannot edit others' playbooks
- Recovery: Create copy, submit PIP

**Resource Errors**:
- File size exceeded
- Storage full
- Recovery: Compress, cleanup, split

**Data Errors**:
- Corruption detected
- Invalid format
- Recovery: Restore from backup, HB, or delete

### Empty States

**No Playbooks**:
- Onboarding guidance
- Primary actions highlighted
- Tutorial links

**No Search Results**:
- Suggestions provided
- Clear filters option
- Alternative actions

---

## Feature File Cross-Reference

**Planned Feature Files**:
- `docs/features/fob-settings.feature` → All FOB-SETTINGS-* screens
- `docs/features/fob-error-recovery.feature` → All error screens
- `docs/features/fob-empty-states.feature` → Empty state screens

**Example Gherkin**:
```gherkin
Feature: FOB Settings

  Scenario: User configures sync preferences
    Given user is on "FOB-SETTINGS-MAIN-1"
    When user clicks "Sync & Connection" in sidebar
    Then user sees "FOB-SETTINGS-SYNC-1"
    And connection status shows "✓ Connected to homebase.mimir.io"
    And last sync shows timestamp
    When user toggles "Auto-sync" to ON
    And user selects sync frequency "Every 15min"
    And user saves settings
    Then FOB will auto-sync every 15 minutes

  Scenario: User connects to Homebase from local-only mode
    Given user is on "FOB-SETTINGS-SYNC-1"
    And connection status shows "⊝ Not connected"
    When user enters Homebase URL "https://homebase.mimir.io"
    And user pastes authentication token
    And user clicks "Test Connection"
    Then connection test succeeds
    When user clicks "Save Connection"
    Then status changes to "✓ Connected"
    And sync preferences become available

Feature: Error Recovery

  Scenario: User handles sync failure
    Given user clicks "Sync with Homebase"
    And network connection is down
    Then user sees "FOB-SYNC-ERROR-1"
    And error shows "Sync failed: Cannot connect to Homebase"
    And error details show:
      | Field      | Value              |
      | Error type | Network error      |
      | Error code | CONNECTION_TIMEOUT |
    When user clicks "Work Offline"
    Then modal shows "Working offline - limited functionality"
    When user confirms
    Then FOB continues in offline mode
    And sync button shows "Offline" indicator

  Scenario: User handles permission denied error
    Given user is viewing "React Frontend Development" playbook
    And playbook is owned by Mike Chen
    When user clicks "Edit"
    Then user sees "FOB-PERMISSION-ERROR-1"
    And error shows "You don't have permission to edit this playbook"
    And options show:
      | Option            | Description                        |
      | Create Local Copy | Creates editable copy              |
      | Submit PIP        | Suggests changes to original       |
    When user clicks "Submit PIP"
    Then PIP creation flow opens

  Scenario: User handles upload size limit error
    Given user is uploading "UX Comprehensive Guide" playbook
    And playbook size is 125 MB
    And size limit is 100 MB
    Then user sees "FOB-UPLOAD-ERROR-1"
    And error shows "File size exceeds limit"
    And error details show embedded images are too large
    When user clicks "Compress Images"
    Then images are optimized automatically
    And new size is shown
    And user can retry upload

Feature: Empty States

  Scenario: First-time user sees empty playbooks dashboard
    Given user has no playbooks
    When user opens FOB dashboard
    Then user sees "FOB-EMPTY-PLAYBOOKS-1"
    And empty state shows illustration
    And heading shows "No playbooks yet"
    And actions show:
      | Action                     | Type    |
      | Create Your First Playbook | Primary |
      | Browse Families            | Secondary|
      | Import from File           | Secondary|
    When user clicks "Create Your First Playbook"
    Then playbook creation wizard opens

  Scenario: User searches for non-existent family
    Given user is on family browser
    When user searches for "blockchain"
    And no families match
    Then user sees "FOB-EMPTY-SEARCH-1"
    And message shows "No families found matching 'blockchain'"
    And suggestions show similar families
    And user can clear filters or create new family
```

---

## Django Implementation Notes

### Settings Screens

All settings screens use a consistent layout:
- Left sidebar navigation (sticky)
- Right content area (scrollable)
- Save/Cancel buttons at bottom

**Base Template**: `templates/settings/base.html`
- Shared sidebar
- Active section highlighting
- Auto-save indicators

**Individual Sections**:
- `FOB-SETTINGS-SYNC-1` → `templates/settings/sync.html`
  - Form for HB URL and token
  - Test connection AJAX call
  - Sync preference toggles

- `FOB-SETTINGS-MCP-1` → `templates/settings/mcp.html`
  - MCP server status check
  - Feature toggles
  - API key management

### Error Screens

**Error Display Pattern**:
- Toast for transient errors
- Modal for blocking errors
- Inline for validation errors

**Common Error Component**: `components/error_message.html`
- Icon based on severity
- Error title and description
- Error details (expandable)
- Recovery actions (buttons)
- Error code and timestamp

**Error Logging**:
- All errors logged to `logs/errors.log`
- User can view recent errors in settings

### Empty States

**Empty State Component**: `components/empty_state.html`
- Illustration (SVG)
- Heading and subtext
- Primary and secondary actions
- Optional tutorial/help links

---

## Next Steps

1. ✅ Screen IDs defined (11 screens total: 5 settings + 6 errors/empty)
2. ⏳ Add Acts 8 & 9 diagram (combined page)
3. ⏳ Implement settings screens
4. ⏳ Implement error handling
5. ⏳ Create empty state components

---

**Version**: 1.0  
**Created**: 2024-11-20  
**Status**: Draft - Building diagram
