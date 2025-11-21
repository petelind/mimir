# Act 6: Sync Scenarios & Export - Screen ID Mapping

**Purpose**: Traceability matrix linking User Journey → Screen IDs → Wireframes → Feature Files

**Act**: Act 6 - Sharing Knowledge (Sync Scenarios + Download/Export)  
**User Journey Reference**: `docs/ux/user_journey.md` lines 818-1001

---

## Screen ID Convention

**Format**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

**Systems**:
- `FOB` = Forward Operating Base (Local Django GUI)

---

## Screen Inventory

### Scenario A: Clean Upload with PIP Generation

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-SYNC-ANALYSIS-1` | FOB Sync Analysis | Shows local vs remote versions, recommends PIP | Line 832-837 |
| `FOB-PIP-SUBMIT-1` | FOB PIP Submit to Homebase | Preview PIP before submitting to Homebase | Line 839-848 |

### Scenario B: Clean Download - No Conflicts

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-AVAILABLE-UPDATES-1` | FOB Available Updates | List of new playbooks available for download | Line 864-868 |

### Scenario C: Conflict Resolution

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-CONFLICT-RESOLUTION-1` | FOB Conflict Resolution Interface | Shows conflict between local and remote versions | Line 890-896 |
| `FOB-CONFLICT-MODAL-1` | FOB Conflict Resolution Options Modal | Choose Keep Remote or Keep Local | Line 898-908 |

### Scenario D: Download/Export Playbook

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-PLAYBOOK-DETAIL-AUTHOR-1` | FOB Playbook Detail (Author View) | Playbook detail with Export button (authors only) | Line 923-929 |
| `FOB-EXPORT-MODAL-1` | FOB Export Playbook Modal | Export options and filename configuration | Line 936-945 |
| `FOB-EXPORT-SUCCESS-1` | FOB Export Success Notification | Success message after JSON download | Line 947-951 |

---

## Flow Diagram Mapping

### Flow 1: Upload PIP to Homebase (Scenario A)

```
FOB-SYNC-DASHBOARD-1 (from Act 3)
  ↓
Click "Sync with Homebase"
  ↓
FOB analyzes local changes
  ↓
FOB-SYNC-ANALYSIS-1 (Detects difference)
  ↓
Shows:
  - Local: v1.1 (with Accessibility Audit)
  - Remote: v1.0
  - Recommendation: "Upload as PIP"
  ↓
Click "Generate PIP for Homebase"
  ↓
FOB-PIP-SUBMIT-1 (Preview PIP package)
  ↓
Shows: "PIP: Add Accessibility Audit..."
[Submit to Homebase]
  ↓
Click [Submit]
  ↓
Success: "PIP submitted for review"
Mike & admins notified
```

### Flow 2: Simple Download (Scenario B)

```
FOB-SYNC-DASHBOARD-1
  ↓
Click "Sync with Homebase"
  ↓
Checks entitled playbooks
  ↓
FOB-AVAILABLE-UPDATES-1
  ↓
Shows: "UX Research Methods v2.3 available"
No conflicts
[Download]
  ↓
Click [Download]
  ↓
Progress → Success
```

### Flow 3: Conflict Resolution (Scenario C)

```
FOB-SYNC-DASHBOARD-1
  ↓
Click "Sync with Homebase"
  ↓
Detects conflict
  ↓
FOB-CONFLICT-RESOLUTION-1
  ↓
Shows:
  - Local: v1.1 (Maria's changes)
  - Remote: v1.2 (Mike's update)
  - Changes highlighted
  ↓
FOB-CONFLICT-MODAL-1 (Choose resolution)
  ↓
Options:
  1. Keep Remote (recommended)
  2. Keep Local
  ↓
User selects "Keep Remote"
  ↓
Confirm modal → Confirmed
  ↓
Local updated to v1.2
Uncommitted changes saved as draft PIP
```

### Flow 4: Export Playbook as JSON (Scenario D)

```
FOB-PLAYBOOK-DETAIL-AUTHOR-1
  ↓
Author viewing own playbook
[Export] button visible (permissions check)
  ↓
Click [Export]
  ↓
FOB-EXPORT-MODAL-1
  ↓
Shows export options:
  - ☑ Include version history
  - ☑ Include metadata
  - ☐ Include local PIPs
  - Filename: editable
  ↓
Click [Download JSON]
  ↓
Browser downloads file
  ↓
FOB-EXPORT-SUCCESS-1
  ↓
Success notification + file size
```

---

## Key Concepts

### Sync Scenarios

**Scenario A - Upload PIP**:
- Local version ahead of remote (v1.1 local > v1.0 remote)
- Changes are improvements to someone else's playbook
- Convert local changes to PIP for review
- Submit to Homebase for original author approval

**Scenario B - Clean Download**:
- New playbook available
- No local version exists
- Simple download, no conflicts

**Scenario C - Conflict**:
- Both local and remote changed (v1.1 local, v1.2 remote)
- User must choose which version to keep
- Uncommitted local changes saved as draft PIP
- No automatic merging

### Export Permissions

**[Export] button visible if**:
- User is the original author
- Playbook was created locally
- Playbook was imported from JSON (user becomes author)

**[Export] button NOT visible if**:
- Playbook synced from Homebase (authored by another user)
- User only has read access
- User is not the author

### Export Options

**Include version history**: Full change log
**Include metadata**: Author, timestamps, family
**Include local PIPs**: Approved local PIPs not yet submitted

---

## Feature File Cross-Reference

**Planned Feature Files**:
- `docs/features/fob-sync-upload-pip.feature` → FOB-SYNC-ANALYSIS-1, FOB-PIP-SUBMIT-1
- `docs/features/fob-conflict-resolution.feature` → FOB-CONFLICT-RESOLUTION-1, FOB-CONFLICT-MODAL-1
- `docs/features/fob-export-playbook.feature` → FOB-PLAYBOOK-DETAIL-AUTHOR-1, FOB-EXPORT-MODAL-1

**Example Gherkin**:
```gherkin
Feature: Upload PIP to Homebase

  Scenario: User uploads local changes as PIP
    Given user has playbook "React Frontend Dev" v1.1 (local)
    And remote version is v1.0
    And user has made local improvements
    When user clicks "Sync with Homebase"
    Then FOB analyzes local changes
    And user sees "FOB-SYNC-ANALYSIS-1"
    And system shows:
      | Field         | Value                                    |
      | Local version | v1.1 (with Accessibility Audit activity) |
      | Remote version| v1.0                                     |
      | Recommendation| Upload your improvements as a PIP        |
    When user clicks "Generate PIP for Homebase"
    Then user sees "FOB-PIP-SUBMIT-1"
    And PIP preview shows "PIP: Add Accessibility Audit to React Frontend Development"
    When user clicks "Submit to Homebase"
    Then PIP is uploaded to Homebase
    And Mike (original author) receives notification
    And Usability family admins receive notification
    And success message shows "Your PIP has been submitted for review"

Feature: Resolve Version Conflict

  Scenario: User resolves conflict by keeping remote version
    Given user has playbook "React Frontend Dev" v1.1 (local)
    And remote version is v1.2
    And user has uncommitted local changes
    When user clicks "Sync with Homebase"
    Then FOB detects conflict
    And user sees "FOB-CONFLICT-RESOLUTION-1"
    And system shows:
      | Version | Details                                          |
      | Local   | v1.1 with Performance Optimization activity      |
      | Remote  | v1.2 with Accessibility PIP + Error Boundaries   |
    When user clicks "Resolve Conflict"
    Then user sees "FOB-CONFLICT-MODAL-1"
    And options are:
      | Option        | Description                                    |
      | Keep Remote   | Overwrite local with v1.2, lose local changes  |
      | Keep Local    | Stay on v1.1, don't download updates           |
    When user selects "Keep Remote"
    And user clicks "Confirm"
    Then local playbook is updated to v1.2
    And uncommitted changes are saved as draft PIP
    And notification shows "You can review your draft PIP and submit it when ready"

Feature: Export Playbook as JSON

  Scenario: Author exports playbook for backup
    Given user is author of "UX Research Methodology" v2.1
    And user is viewing playbook detail
    When user sees "FOB-PLAYBOOK-DETAIL-AUTHOR-1"
    Then [Export] button is visible
    And button has icon "fa-download"
    And button has tooltip "Download this playbook as JSON file for backup or sharing"
    When user clicks [Export]
    Then user sees "FOB-EXPORT-MODAL-1"
    And modal shows:
      | Field         | Value                                  |
      | Playbook      | UX Research Methodology v2.1           |
      | Format        | JSON                                   |
      | Filename      | ux_research_methodology_v2.1.json      |
    And options show:
      | Option                | Selected |
      | Include version history| ☑       |
      | Include metadata       | ☑       |
      | Include local PIPs     | ☐       |
    When user clicks "Download JSON"
    Then browser downloads file "ux_research_methodology_v2.1.json"
    And user sees "FOB-EXPORT-SUCCESS-1"
    And success notification shows "Playbook exported successfully"
    And file size shows "~45 KB"

  Scenario: Non-author cannot export playbook
    Given user is viewing playbook "React Frontend Dev" v1.0
    And playbook is authored by Mike Chen
    And user is not Mike Chen
    When user views "FOB-PLAYBOOK-DETAIL-1"
    Then [Export] button is NOT visible
    And user only sees [View] [Edit (if permitted)] actions
```

---

## Django Implementation Notes

### Sync Analysis
- `FOB-SYNC-ANALYSIS-1` → New: `templates/sync/analysis.html`
  - Compare local and remote versions
  - Highlight differences
  - Recommend action: Download, Upload PIP, or Resolve Conflict

### PIP Submission
- `FOB-PIP-SUBMIT-1` → New: `templates/pips/submit.html`
  - Package local changes as PIP
  - Show preview
  - Submit to Homebase API: `POST /api/homebase/pips/`

### Conflict Resolution
- `FOB-CONFLICT-RESOLUTION-1` → New: `templates/sync/conflict.html`
  - Diff view showing local vs remote
  - Highlight conflicting changes
  - Button to open resolution modal

- `FOB-CONFLICT-MODAL-1` → Bootstrap modal
  - Radio buttons: Keep Remote / Keep Local
  - Explanation of consequences
  - Confirm button

### Export Playbook
- `FOB-PLAYBOOK-DETAIL-AUTHOR-1` → Update: `templates/playbooks/detail.html`
  - Add [Export] button with permission check:
    ```python
    {% if playbook.author == request.user or playbook.source == 'local' %}
        <button class="btn btn-outline-secondary" 
                data-bs-toggle="tooltip"
                title="Download this playbook as JSON file for backup or sharing"
                onclick="openExportModal()">
            <i class="fa-solid fa-download"></i> Export
        </button>
    {% endif %}
    ```

- `FOB-EXPORT-MODAL-1` → Bootstrap modal
  - Checkboxes for export options
  - Editable filename input
  - Download button triggers: `GET /api/playbooks/<id>/export/?options=...`

- `FOB-EXPORT-SUCCESS-1` → Toast notification
  - Show after successful download
  - Display file size

**Backend Logic**:
- Export endpoint:
  ```python
  def export_playbook(request, playbook_id):
      playbook = get_object_or_404(Playbook, id=playbook_id)
      # Permission check
      if playbook.author != request.user and playbook.source != 'local':
          return HttpResponseForbidden()
      
      # Build JSON
      data = {
          'schema_version': '1.0',
          'playbook': {
              'id': playbook.id,
              'name': playbook.name,
              'version': playbook.version,
              # ... include activities, artifacts, goals
          }
      }
      
      response = JsonResponse(data)
      response['Content-Disposition'] = f'attachment; filename="{playbook.slug}_v{playbook.version}.json"'
      return response
  ```

---

## Next Steps

1. ✅ Screen IDs defined (8 screens)
2. ⏳ Add Act 6 diagram (will be complex with 4 scenarios)
3. ⏳ Implement sync analysis logic
4. ⏳ Implement conflict resolution
5. ⏳ Implement export functionality

---

**Version**: 1.0  
**Created**: 2024-11-20  
**Status**: Draft - Building diagram
