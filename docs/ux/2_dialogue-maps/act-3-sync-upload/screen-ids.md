# Act 3: Sync & Upload - Screen ID Mapping

**Purpose**: Traceability matrix linking User Journey → Screen IDs → Wireframes → Feature Files

**Act**: Act 3 - First Sync + Act 3.1 - Upload Playbook from JSON  
**User Journey Reference**: `docs/ux/user_journey.md` lines 447-549

---

## Screen ID Convention

**Format**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

**Systems**:
- `FOB` = Forward Operating Base (Local Django GUI)

---

## Screen Inventory

### Act 3: First Sync - Discovering Mike's Playbook

#### FOB Screens (Sync & Download)

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-SYNC-DASHBOARD-1` | FOB Sync Dashboard | Initiate sync with Homebase, shows status | Line 451-457 |
| `FOB-AVAILABLE-PLAYBOOKS-1` | FOB Available Playbooks | List of playbooks from families after sync | Line 459-463 |
| `FOB-PLAYBOOK-PREVIEW-1` | FOB Playbook Preview | Preview playbook structure before download | Line 465-470 |
| `FOB-DOWNLOAD-PROGRESS-1` | FOB Download Progress | Progress indicator during playbook download | Line 472-477 |

---

### Act 3.1: Upload Playbook from JSON

#### FOB Screens (Upload/Import)

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-PLAYBOOKS-LIST-1` | FOB Playbooks List | Main playbooks page with Upload button | Line 486-490 |
| `FOB-UPLOAD-MODAL-1` | FOB Upload Playbook Modal | File upload dialog with drag-and-drop | Line 496-502 |
| `FOB-UPLOAD-VALIDATION-1` | FOB Upload Validation | Validation results with preview or error | Line 510-533 |
| `FOB-PLAYBOOKS-UPDATED-1` | FOB Playbooks List (Updated) | List showing newly imported playbook | Line 541-547 |

---

## Flow Diagram Mapping

### Flow 1: Sync and Download Playbook from Homebase

```
FOB-SYNC-DASHBOARD-1 (Click "Sync with Homebase")
  ↓
Connecting to Homebase (token auth)
  ↓
FOB-AVAILABLE-PLAYBOOKS-1 (List of entitled playbooks)
  ↓
Click "React Frontend Development"
  ↓
FOB-PLAYBOOK-PREVIEW-1 (Preview structure, author, version)
  ↓
Click "Download to FOB"
  ↓
FOB-DOWNLOAD-PROGRESS-1 (Progress indicator)
  ↓
Success: Playbook downloaded to local FOB
```

### Flow 2: Upload Playbook from JSON

```
FOB-PLAYBOOKS-LIST-1 (Click "Upload Playbook")
  ↓
FOB-UPLOAD-MODAL-1 (Drag-and-drop or browse for .json)
  ↓
Select file: ux_research_playbook_v2.1.json
  ↓
Click [Upload]
  ↓
FOB-UPLOAD-VALIDATION-1 (Validating schema...)
  ├─ Success Path:
  │   ↓
  │  Preview: Name, Version, Activities, Artifacts, Author
  │   ↓
  │  Click [Import Playbook]
  │   ↓
  │  FOB-PLAYBOOKS-UPDATED-1 (Imported playbook shown)
  │
  └─ Error Path:
      ↓
     Error message: "Invalid format: Missing field 'activities'"
      ↓
     Click [Try Another File] → Back to FOB-UPLOAD-MODAL-1
```

---

## Key Concepts

### Sync Requirements

**Prerequisites for Sync**:
- Active Homebase connection
- Valid authentication token
- FOB must be in "Connected Mode" (from Act 1)

**Sync Button State**:
- **Enabled**: If connected to Homebase
- **Disabled**: If not connected
  - Tooltip: "Connect to Homebase in Settings to enable sync"

### Upload/Import JSON

**File Requirements**:
- Format: `.json` only
- Schema: Must follow Mimir playbook schema
- Required fields: `id`, `name`, `description`, `activities`, `version`

**Validation Checks**:
1. JSON syntax valid
2. Schema version compatible
3. Required fields present
4. Version format correct (semantic versioning)
5. Dependencies structure valid

**Authorship**:
- Imported playbooks: User becomes the author
- Status: "Local (not synced to Homebase)"
- Can be edited, deleted, or exported

---

## Feature File Cross-Reference

**Planned Feature Files**:
- `docs/features/fob-sync-download.feature` → FOB-SYNC-DASHBOARD-1, FOB-AVAILABLE-PLAYBOOKS-1, FOB-PLAYBOOK-PREVIEW-1
- `docs/features/fob-upload-json.feature` → FOB-UPLOAD-MODAL-1, FOB-UPLOAD-VALIDATION-1

**Example Gherkin**:
```gherkin
Feature: Sync with Homebase and Download Playbooks

  Scenario: User syncs and downloads available playbook
    Given user is on "FOB-SYNC-DASHBOARD-1"
    And user is connected to Homebase
    When user clicks "Sync with Homebase"
    Then FOB connects using authentication token
    And system shows "Checking for updates..."
    When sync completes successfully
    Then user sees "FOB-AVAILABLE-PLAYBOOKS-1"
    And list shows "React Frontend Development" (Usability family)
    And status shows "Not downloaded"
    When user clicks on "React Frontend Development"
    Then user sees "FOB-PLAYBOOK-PREVIEW-1"
    And preview shows:
      | Field       | Value                        |
      | Name        | React Frontend Development   |
      | Version     | v1.0                         |
      | Author      | Mike Chen                    |
      | Family      | Usability                    |
    When user clicks "Download to FOB"
    Then user sees "FOB-DOWNLOAD-PROGRESS-1"
    And progress indicator shows download
    When download completes
    Then success message shows "React Frontend Development v1.0 downloaded"
    And playbook is added to local FOB

Feature: Upload Playbook from JSON

  Scenario: User successfully uploads valid JSON playbook
    Given user is on "FOB-PLAYBOOKS-LIST-1"
    When user clicks "Upload Playbook"
    Then user sees "FOB-UPLOAD-MODAL-1"
    And modal shows file upload area
    And modal shows "Drop JSON file here or click to browse"
    And [Upload] button is disabled
    When user selects file "ux_research_playbook_v2.1.json"
    Then file name appears in modal
    And [Upload] button becomes active
    When user clicks [Upload]
    Then user sees "FOB-UPLOAD-VALIDATION-1"
    And system shows "Validating playbook structure..."
    When validation succeeds
    Then preview shows:
      | Field      | Value                    |
      | Name       | UX Research Methodology  |
      | Version    | 2.1                      |
      | Activities | 12                       |
      | Artifacts  | 8                        |
      | Author     | Maria Rodriguez          |
    And message shows "This playbook will be added to your local FOB"
    When user clicks [Import Playbook]
    Then system shows "Importing playbook..."
    And playbook is added to local graph
    And success notification shows "UX Research Methodology v2.1 imported successfully"
    Then user sees "FOB-PLAYBOOKS-UPDATED-1"
    And imported playbook appears in list
    And status shows "Local (not synced to Homebase)"
    And source shows "Imported from JSON"

  Scenario: User uploads invalid JSON playbook
    Given user is on "FOB-UPLOAD-MODAL-1"
    And user has selected file "invalid_playbook.json"
    When user clicks [Upload]
    Then user sees "FOB-UPLOAD-VALIDATION-1"
    And system shows "Validating playbook structure..."
    When validation fails
    Then error message shows "Invalid playbook format: Missing required field 'activities'"
    And [Try Another File] button is visible
    When user clicks [Try Another File]
    Then user returns to "FOB-UPLOAD-MODAL-1"
```

---

## Django Implementation Notes

### FOB Screens

**Sync Dashboard**:
- `FOB-SYNC-DASHBOARD-1` → Update: `templates/dashboard.html`
  - Add "Sync with Homebase" button
  - Button enabled only if `user.is_connected_to_homebase`
  - Disabled tooltip: "Connect to Homebase in Settings to enable sync"
  - AJAX call to `/api/sync/` endpoint

**Available Playbooks**:
- `FOB-AVAILABLE-PLAYBOOKS-1` → New: `templates/sync/available_playbooks.html`
  - List of playbooks from user's families
  - Filter: Only show playbooks not yet downloaded
  - Each card shows: name, family, author, version, status
  - Click card → Navigate to FOB-PLAYBOOK-PREVIEW-1

**Playbook Preview**:
- `FOB-PLAYBOOK-PREVIEW-1` → New: `templates/sync/playbook_preview.html`
  - Show full playbook structure (read-only)
  - Activities, Artifacts, Goals tabs
  - Version history
  - "Download to FOB" button (enabled)
  - AJAX call to `/api/sync/download/<playbook_id>/`

**Upload Modal**:
- `FOB-UPLOAD-MODAL-1` → New: `templates/playbooks/upload_modal.html`
  - Bootstrap modal component
  - File upload with drag-and-drop (use dropzone.js or similar)
  - Accept only `.json` files
  - AJAX submit to `/api/playbooks/upload/`

**Upload Validation**:
- `FOB-UPLOAD-VALIDATION-1` → New: `templates/playbooks/upload_validation.html`
  - Server-side JSON validation
  - Check schema compliance using jsonschema library
  - Success: Show preview with playbook metadata
  - Error: Show error message with specific field missing
  - POST to `/api/playbooks/import/` on confirm

**Backend Logic**:
- Sync: `/api/sync/` calls Homebase API, retrieves entitled playbooks
- Download: `/api/sync/download/<id>/` fetches playbook JSON from HB, creates local Playbook instance
- Upload: `/api/playbooks/upload/` validates JSON against schema
- Import: `/api/playbooks/import/` creates Playbook instance with user as author, status="local"

---

## Next Steps

1. ✅ Screen IDs defined (8 screens)
2. ⏳ Add Act 3 diagram to `screen-flow.drawio` (page 5)
3. ⏳ Create wireframes
4. ⏳ Write feature files
5. ⏳ Implement Django views and templates
6. ⏳ Implement API endpoints

---

**Version**: 1.0  
**Created**: 2024-11-20  
**Status**: Draft - Building diagram
