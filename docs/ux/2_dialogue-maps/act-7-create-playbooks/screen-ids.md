# Act 7: Creating Original Content - Screen ID Mapping

**Purpose**: Traceability matrix linking User Journey → Screen IDs → Wireframes → Feature Files

**Act**: Act 7 - Creating Original Content (Multiple Playbooks)  
**User Journey Reference**: `docs/ux/user_journey.md` lines 1005-1159

---

## Screen ID Convention

**Format**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

**Systems**:
- `FOB` = Forward Operating Base (Local Django GUI)
- `WINDSURF` = Windsurf IDE Chat Interface
- `MCP` = Mimir MCP Server

---

## Screen Inventory

### Playbook 1: Private Personal Playbook

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-CREATE-PLAYBOOK-1` | FOB Create Playbook Dashboard | Entry point with "Create New Playbook" button | Line 1013-1014 |
| `FOB-PLAYBOOK-WIZARD-BASIC-1` | FOB Playbook Wizard - Basic Info | Name, description, category form | Line 1016-1021 |
| `FOB-PLAYBOOK-EDITOR-1` | FOB Playbook Editor | Add/edit activities, artifacts, goals with dependencies | Line 1023-1027 |
| `FOB-PLAYBOOK-WIZARD-PUBLISH-1` | FOB Playbook Wizard - Publishing | Visibility and location settings | Line 1029-1033 |

### Playbook 2: Family Playbook from Notes

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-IMPORT-NOTES-1` | FOB Import from Notes Interface | Paste markdown notes for AI analysis | Line 1043-1051 |
| `FOB-AI-STRUCTURE-1` | FOB AI-Assisted Structure | Shows AI-extracted activities, artifacts, goals | Line 1053-1059 |
| `FOB-UPLOAD-HOMEBASE-1` | FOB Upload to Homebase Progress | Upload progress and success notification | Line 1075-1079 |

### Playbook 3: Hidden Family - Client Playbook

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-TEMPLATE-SELECT-1` | FOB Template Selection | Choose from pre-built templates | Line 1089-1093 |
| `FOB-MEMBER-MANAGEMENT-1` | FOB Manual Member Management | Add team members to hidden family | Line 1109-1116 |

### Playbook 4: MCP-Driven Creation

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `WINDSURF-CREATE-PLAYBOOK-1` | Windsurf MCP Playbook Creation | Create playbook via chat commands | Line 1126-1135 |
| `MCP-PLAYBOOK-CREATED-1` | MCP Playbook Created Response | Confirmation with playbook ID and status | Line 1138-1149 |

---

## Flow Diagram Mapping

### Flow 1: Create Private Personal Playbook

```
FOB-CREATE-PLAYBOOK-1 (Dashboard)
  ↓
Click "Create New Playbook"
  ↓
FOB-PLAYBOOK-WIZARD-BASIC-1
  ↓
Enter:
  - Name: "My Goals"
  - Description: "Personal development goals"
  - Category: Personal
  ↓
Click "Next"
  ↓
FOB-PLAYBOOK-EDITOR-1
  ↓
Add Goals, Activities, Dependencies
  ↓
Click "Next"
  ↓
FOB-PLAYBOOK-WIZARD-PUBLISH-1
  ↓
Select:
  - Visibility: Private
  - Location: Local FOB only
  ↓
Click "Create Playbook"
  ↓
Success: Private playbook created
```

### Flow 2: Create Family Playbook from Notes (AI-Assisted)

```
FOB-CREATE-PLAYBOOK-1
  ↓
Click "Import from Notes"
  ↓
FOB-IMPORT-NOTES-1
  ↓
Paste markdown notes
  ↓
FOB-AI-STRUCTURE-1 (AI analyzes and suggests)
  ↓
Shows detected:
  - Activities: 12
  - Artifacts: 8
  - Goals: 5
  ↓
Click "Review and Edit"
  ↓
FOB-PLAYBOOK-EDITOR-1
  ↓
Adjust dependencies, enrich descriptions
  ↓
FOB-PLAYBOOK-WIZARD-PUBLISH-1
  ↓
Select:
  - Visibility: Family - "UX"
  - Location: Upload to Homebase
  ↓
FOB-UPLOAD-HOMEBASE-1
  ↓
Progress → Success
  ↓
All family members notified
```

### Flow 3: Create Hidden Family Playbook from Template

```
FOB-CREATE-PLAYBOOK-1
  ↓
FOB-TEMPLATE-SELECT-1
  ↓
Choose "Consulting Project" template
  ↓
FOB-PLAYBOOK-EDITOR-1
  ↓
Customize for client needs
  ↓
FOB-PLAYBOOK-WIZARD-PUBLISH-1
  ↓
Select:
  - Visibility: Family - "Acme, INC" (hidden)
  - Access: Invite only
  ↓
Click "Create and Publish"
  ↓
FOB-MEMBER-MANAGEMENT-1
  ↓
Manually add team members
  ↓
Email invitations sent
```

### Flow 4: MCP-Driven Playbook Creation

```
WINDSURF-CREATE-PLAYBOOK-1
  ↓
User: "mimir: Create playbook 'Design System Management'
       with activities 1-4, private, local only"
  ↓
MCP processes command
  ↓
MCP-PLAYBOOK-CREATED-1
  ↓
Response:
  - ✓ Created playbook
  - ✓ Added 4 activities
  - ✓ Visibility: Private
  - Playbook ID: ds-mgmt-001
  ↓
User continues adding content via MCP
```

---

## Key Concepts

### Playbook Types

**Private Playbook**:
- Visibility: Only creator
- Location: Local FOB only
- Never synced to Homebase
- Use case: Personal goals, private notes

**Family Playbook**:
- Visibility: All family members
- Location: Upload to Homebase
- Accessible after family membership
- Use case: Community sharing, team collaboration

**Hidden Family Playbook**:
- Visibility: Hidden family members only
- Location: Upload to Homebase
- Invite-only access
- Use case: Client work, confidential projects

### Creation Methods

**Manual Creation**:
- Step-by-step wizard
- Manual entry of all components
- Full control over structure

**Import from Notes** (AI-Assisted):
- Paste markdown or text notes
- AI analyzes and extracts structure
- User reviews and adjusts
- Faster initial creation

**Template-Based**:
- Start with pre-built structure
- Customize for specific needs
- Saves time for common patterns

**MCP-Driven**:
- Create via chat commands
- No GUI interaction needed
- Quick for experienced users
- Can add content iteratively

---

## Feature File Cross-Reference

**Planned Feature Files**:
- `docs/features/fob-create-playbook.feature` → FOB-CREATE-PLAYBOOK-1, FOB-PLAYBOOK-WIZARD-*
- `docs/features/fob-import-notes-ai.feature` → FOB-IMPORT-NOTES-1, FOB-AI-STRUCTURE-1
- `docs/features/mcp-create-playbook.feature` → WINDSURF-CREATE-PLAYBOOK-1, MCP-PLAYBOOK-CREATED-1

**Example Gherkin**:
```gherkin
Feature: Create Private Playbook

  Scenario: User creates private personal playbook
    Given user is on "FOB-CREATE-PLAYBOOK-1"
    When user clicks "Create New Playbook"
    Then user sees "FOB-PLAYBOOK-WIZARD-BASIC-1"
    When user fills form:
      | Field       | Value                                     |
      | Name        | My Goals                                  |
      | Description | Personal development goals for 2024       |
      | Category    | Personal                                  |
    And user clicks "Next"
    Then user sees "FOB-PLAYBOOK-EDITOR-1"
    When user adds goals:
      | Goal                          |
      | Learn Three.js                |
      | Speak at UX conference        |
      | Publish case study            |
    And user adds activities with dependencies
    And user clicks "Next"
    Then user sees "FOB-PLAYBOOK-WIZARD-PUBLISH-1"
    When user selects visibility "Private (only me)"
    And user selects location "Local FOB only"
    And user clicks "Create Playbook"
    Then playbook is created successfully
    And playbook is visible only to user
    And playbook is NOT synced to Homebase

Feature: Import Playbook from Notes with AI

  Scenario: User imports markdown notes and AI structures playbook
    Given user is on "FOB-CREATE-PLAYBOOK-1"
    When user clicks "Import from Notes"
    Then user sees "FOB-IMPORT-NOTES-1"
    When user pastes markdown notes containing:
      """
      # User Research
      - Interview stakeholders
      - Create personas
      
      # Wireframing
      - Sketch lo-fi wireframes
      - Create hi-fi mockups
      """
    And user clicks "Analyze"
    Then AI processes notes
    And user sees "FOB-AI-STRUCTURE-1"
    And AI suggests:
      | Type       | Count | Examples                                |
      | Activities | 12    | Interview stakeholders, Create personas |
      | Artifacts  | 8     | Interview notes, Persona documents      |
      | Goals      | 5     | Understand user needs                   |
    When user clicks "Review and Edit"
    Then user sees "FOB-PLAYBOOK-EDITOR-1"
    And user can adjust extracted structure
    When user configures publishing:
      | Field      | Value                 |
      | Visibility | Family - UX           |
      | Location   | Upload to Homebase    |
    And user clicks "Create and Publish"
    Then user sees "FOB-UPLOAD-HOMEBASE-1"
    And playbook uploads to Homebase
    And all UX family members receive notification

Feature: Create Playbook via MCP

  Scenario: User creates playbook using MCP commands
    Given user is in Windsurf with MCP connected
    When user sends command:
      """
      mimir: Create a new playbook called "Design System Management" with these activities:
      1. Establish design tokens
      2. Create component library
      3. Document usage guidelines
      4. Maintain versioning
      Make it private, keep it local only.
      """
    Then MCP processes command
    And user sees "MCP-PLAYBOOK-CREATED-1"
    And response shows:
      """
      ✓ Created playbook: "Design System Management"
      ✓ Added 4 activities with dependencies
      ✓ Visibility: Private (local only)
      ✓ Status: Active on your FOB
      
      Playbook ID: ds-mgmt-001
      """
    When user sends command:
      """
      mimir: Add artifact "Token Library" to activity 1
      """
    Then artifact is added to playbook
    And user can view playbook in FOB GUI
```

---

## Django Implementation Notes

### Playbook Creation Wizard
- `FOB-PLAYBOOK-WIZARD-BASIC-1` → New: `templates/playbooks/wizard/step1_basic.html`
  - Form for name, description, category
  - Validation: Name required, unique within user's playbooks

- `FOB-PLAYBOOK-EDITOR-1` → Update: `templates/playbooks/editor.html`
  - Drag-and-drop interface for activities/artifacts/goals
  - Dependency graph visualization
  - Save as draft functionality

- `FOB-PLAYBOOK-WIZARD-PUBLISH-1` → New: `templates/playbooks/wizard/step3_publish.html`
  - Visibility radio buttons: Private, Family, Hidden Family
  - Location: Local only or Upload to Homebase
  - Family selector (if Family visibility chosen)

### AI Note Import
- `FOB-IMPORT-NOTES-1` → New: `templates/playbooks/import_notes.html`
  - Textarea for markdown/text paste
  - Call AI service: POST `/api/playbooks/analyze-notes/`
  
- `FOB-AI-STRUCTURE-1` → New: `templates/playbooks/ai_structure.html`
  - Shows extracted structure in preview
  - Edit/accept buttons
  - Backend uses NLP to extract:
    - Activities (action verbs)
    - Artifacts (noun phrases)
    - Goals (objective statements)

### MCP Integration
- MCP command: `create_playbook(name, activities, visibility, location)`
- Returns playbook ID and summary
- User can continue editing via GUI or MCP

---

## Next Steps

1. ✅ Screen IDs defined (11 screens)
2. ⏳ Add Act 7 diagram
3. ⏳ Implement playbook wizard
4. ⏳ Implement AI note import
5. ⏳ Implement MCP playbook creation

---

**Version**: 1.0  
**Created**: 2024-11-20  
**Status**: Draft - Building diagram
