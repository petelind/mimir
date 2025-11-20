# Act 4: MCP Usage - Screen ID Mapping

**Purpose**: Traceability matrix linking User Journey → Screen IDs → Wireframes → Feature Files

**Act**: Act 4 - Working with MCP - Using the Playbook  
**User Journey Reference**: `docs/ux/user_journey.md` lines 524-650

---

## Screen ID Convention

**Format**: `{SYSTEM}-{SECTION}-{SEQUENCE}`

**Systems**:
- `FOB` = Forward Operating Base (Local Django GUI)
- `MCP` = Mimir MCP Server (Tool/Command flows)
- `EXT-MCP` = External MCP Servers (GitHub, Jira, etc.)

---

## Screen Inventory

### FOB Screens

| Screen ID | Screen Name | Description | Journey Reference |
|-----------|------------|-------------|-------------------|
| `FOB-PLAYBOOK-ACTIVATE-1` | FOB Playbook Activation | User activates a playbook from dashboard | Line 528-534 |
| `FOB-PLAYBOOK-DETAIL-1` | FOB Playbook Detail (Auto-Opened) | Browser opens to workflow view, shows activity status | Line 611-617 |
| `FOB-PIP-NOTIFY-1` | FOB PIP Created Notification | Notification toast showing AI-created PIP | Line 644-648 |

### MCP Tool Flows (Grey)

| Flow ID | Tool/Command | Description | Journey Reference |
|---------|-------------|-------------|-------------------|
| `MCP-GET-CONTEXT-1` | `@tool get_playbook_context` | AI retrieves active playbook context | Line 544-562 |
| `MCP-GET-ACTIVITY-1` | `@tool get_activity_details` | AI retrieves specific activity guidance | Line 588-602 |
| `MCP-SUGGEST-PIP-1` | `@tool suggest_pip` | AI analyzes work patterns and suggests PIP | Line 619-635 |
| `MCP-OPEN-BROWSER-1` | `@tool open_playbook_browser` | MCP opens FOB web GUI in browser | Line 604-617 |
| `MCP-CREATE-PIP-1` | `@tool create_pip` | MCP creates PIP draft in local FOB | Line 637-648 |

### External MCP Flows (Grey Dotted)

| Flow ID | External MCP | Description | Journey Reference |
|---------|-------------|-------------|-------------------|
| `EXT-MCP-GITHUB-CREATE-1` | GitHub MCP `create_issue` | Creates GitHub issue via external MCP | Line 564-579 |
| `EXT-MCP-GITHUB-QUERY-1` | GitHub MCP `get_issue` | Queries GitHub issue status | Line 584-590 |

### Interface Screens (Windsurf)

| Screen ID | Interface | Description | Journey Reference |
|-----------|----------|-------------|-------------------|
| `WINDSURF-CHAT-1` | Windsurf MCP Chat | User interacts with AI via Windsurf Cascade | Line 537-541 |
| `WINDSURF-CHAT-2` | Windsurf MCP Chat (Work Item) | User requests work item creation | Line 565-568 |
| `WINDSURF-CHAT-3` | Windsurf MCP Chat (Continue) | User picks up existing work item | Line 582-602 |
| `WINDSURF-CHAT-4` | Windsurf MCP Chat (AI PIP) | AI proactively suggests PIP | Line 619-635 |
| `WINDSURF-CHAT-5` | Windsurf MCP Chat (Approve PIP) | User approves AI-initiated PIP | Line 637-642 |

---

## Flow Diagram Mapping

**Primary User Path (Bold Green Arrows)**:
1. `FOB-PLAYBOOK-ACTIVATE-1` → Activate playbook
2. `WINDSURF-CHAT-1` → Ask MCP for guidance
3. `MCP-GET-CONTEXT-1` → MCP retrieves playbook context
4. `WINDSURF-CHAT-2` → Request work item creation
5. `EXT-MCP-GITHUB-CREATE-1` → GitHub MCP creates issue
6. `WINDSURF-CHAT-3` → Continue with work
7. `MCP-GET-ACTIVITY-1` → MCP provides next activity
8. `WINDSURF-CHAT-4` → AI suggests PIP
9. `MCP-SUGGEST-PIP-1` → MCP analyzes patterns
10. `WINDSURF-CHAT-5` → User approves
11. `MCP-CREATE-PIP-1` → MCP creates PIP
12. `FOB-PIP-NOTIFY-1` → Notification shown

**MCP-to-MCP Internal Flows (Grey Dotted)**:
- `MCP-GET-CONTEXT-1` ⤏ `MCP-GET-ACTIVITY-1` (context sharing)
- `MCP-SUGGEST-PIP-1` ⤏ `MCP-CREATE-PIP-1` (PIP creation flow)

**UI-to-MCP Triggers (Solid Grey Arrows)**:
- User question in Windsurf → `MCP-GET-CONTEXT-1`
- User request → `EXT-MCP-GITHUB-CREATE-1`
- AI observation → `MCP-SUGGEST-PIP-1`

---

## Feature File Cross-Reference

**Planned Feature Files**:
- `docs/features/mcp-playbook-guidance.feature` → Scenarios for MCP context retrieval
- `docs/features/mcp-work-items.feature` → Scenarios for external MCP integration
- `docs/features/mcp-pip-suggestions.feature` → Scenarios for AI-initiated PIPs

**Screen ID Usage in Feature Files**:
```gherkin
Scenario: AI provides playbook guidance
  Given user has activated playbook on "FOB-PLAYBOOK-ACTIVATE-1"
  When user asks question in "WINDSURF-CHAT-1"
  Then MCP executes "MCP-GET-CONTEXT-1"
  And guidance is displayed in "WINDSURF-CHAT-1"
```

---

## Next Steps

1. ✅ Screen IDs defined
2. ⏳ Create `screen-flow.drawio` with these IDs
3. ⏳ Create wireframes for each FOB screen
4. ⏳ Write feature files referencing these IDs
5. ⏳ Implement Django views/templates for FOB screens
6. ⏳ Implement MCP tools with FastMCP decorators

---

**Version**: 1.0  
**Created**: 2024-11-20  
**Status**: Draft - Pending diagram creation
