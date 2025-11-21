# Integrated End-to-End Workflow - Design Plan

**Purpose**: Single master diagram showing complete user journey through all acts with swimlanes

---

## Layout Design

### Swimlane Structure (Horizontal Containers)

```
┌─────────────────────────────────────────────────────────────────┐
│ ACT 0: Authentication & Setup                                    │
│ [HB Register] → [Email Verify] → [Token Gen] → [FOB Connect]   │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ ACT 1: Onboarding                                                │
│ [First Run] → [Sync Prefs] → [MCP Config] → [Dashboard]        │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ ACT 2: Family Management                                         │
│ [Browse] → [Join Family] ⟷ [Create Family] → [Admin Tasks]    │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ ACT 3: First Sync & Download                                     │
│ [Sync] → [Available] → [Preview] → [Download] + [Import JSON]  │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ ACT 4: MCP Usage (Parallel - can happen anytime)                │
│ [Windsurf] → [Playbook Context] → [Create Work Items]          │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ ACT 5: Creating PIPs                                             │
│ [Windsurf Chat] → [MCP Suggests] → [Generate PIP] → [Review]   │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ ACT 6: Sync Scenarios                                            │
│ [Upload PIP] | [Download] | [Conflict] | [Export JSON]         │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ ACT 7: Create New Playbooks (Optional branch)                   │
│ [Manual] | [AI from Notes] | [Template] | [MCP]                │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ ACTS 8-9: Settings & Error Recovery (Side branches throughout)  │
│ [Settings] | [Errors] | [Empty States]                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Main Success Scenario Path

**Maria's Complete Journey**:

1. **Act 0**: Register on HB → Verify email → Get token → Connect FOB
2. **Act 1**: First FOB run → Configure sync → Setup MCP → Reach dashboard
3. **Act 2**: Browse families → Join "Usability" family (Mike's)
4. **Act 3**: First sync → See Mike's playbook → Preview → Download
5. **Act 4**: Open Windsurf → Load playbook context → Use MCP commands
6. **Act 5**: Work in Windsurf → MCP suggests PIP → Generate → Review in FOB → Approve
7. **Act 6**: Sync with HB → Upload PIP → Clean download of others' playbooks

**Optional Branches**:
- **Act 2**: Create own family (parallel to join)
- **Act 3**: Import playbook from JSON (alternative to download)
- **Act 6**: Conflict resolution (alternative to clean upload/download)
- **Act 6**: Export playbook as JSON (if author)
- **Act 7**: Create new playbook (anytime after Act 3)
- **Acts 8-9**: Access settings (anytime), handle errors (as needed)

---

## Screen Count by Act

| Act | Screens | Key Screens for Main Path |
|-----|---------|---------------------------|
| 0 | 11 | 6 (main auth flow) |
| 1 | 8 | 5 (core onboarding) |
| 2 | 12 | 4 (join family path) |
| 3 | 8 | 4 (first sync & download) |
| 4 | 12 | 3 (basic MCP usage) |
| 5 | 6 | 4 (PIP creation flow) |
| 6 | 8 | 2 (upload PIP scenario) |
| 7 | 11 | 0 (optional) |
| 8-9 | 11 | 0 (side paths) |

**Total for main path**: ~28 screens  
**Total available**: 87 screens

---

## Visual Design

### Swimlane Styling
- **Height**: 200-300px per swimlane (depending on content)
- **Width**: 2400px (wide canvas for full flow)
- **Color**: Alternating light backgrounds for readability
  - Act 0: Light blue (#e3f2fd)
  - Act 1: Light green (#e8f5e9)
  - Act 2: Light yellow (#fff9c4)
  - Act 3: Light cyan (#e0f7fa)
  - Act 4: Light purple (#f3e5f5)
  - Act 5: Light orange (#fff3e0)
  - Act 6: Light teal (#e0f2f1)
  - Act 7: Light pink (#fce4ec)
  - Acts 8-9: Light grey (#f5f5f5)

### Screen Boxes
- **Main path screens**: Bold border (3px), colored by system
  - Blue (#4682B4): FOB
  - Green (#82b366): HB
  - Purple (#9370DB): Windsurf/MCP
- **Alternative paths**: Dashed border (2px)
- **Error/recovery**: Red border (#f44336)

### Arrows
- **Main success path**: Bold 3px solid black arrows
- **Alternative paths**: 2px dashed grey
- **Error detours**: 2px dashed red
- **Return paths**: 2px dotted green

### Labels
- **Swimlane titles**: 16px bold, left-aligned
- **Screen names**: 10px, inside boxes
- **Decision points**: Diamond shapes
- **Notes**: Yellow sticky note shapes

---

## Implementation Strategy

### Phase 1: Structure
1. Create new diagram page "Integrated Flow"
2. Add 8-9 horizontal swimlane containers
3. Set swimlane heights and colors
4. Add swimlane title labels

### Phase 2: Act 0 (Authentication)
1. Add HB screens (Register, Verify, Token)
2. Add FOB screens (Connect, Token Setup)
3. Connect with main path arrows
4. Add decision points if needed

### Phase 3: Act 1 (Onboarding)
1. Add FOB screens (First Run, Sync Prefs, MCP Config, Dashboard)
2. Connect from Act 0
3. Add configuration options

### Phase 4: Act 2 (Family Management)
1. Add main path: Browse → Join Family
2. Add alternative: Create Family (dashed path)
3. Add admin approval flow
4. Connect to Act 3

### Phase 5: Act 3 (First Sync)
1. Add Sync → Available → Preview → Download
2. Add alternative: Import JSON (dashed path)
3. Connect to Act 4

### Phase 6: Act 4 (MCP Usage)
1. Add Windsurf → Context → Commands
2. Show parallel usage (can happen anytime)
3. Connect to Act 5

### Phase 7: Act 5 (PIPs)
1. Add Chat → Suggest → Generate → Review → Approve
2. Show MCP ↔ FOB interaction
3. Connect to Act 6

### Phase 8: Act 6 (Sync Scenarios)
1. Add main path: Upload PIP
2. Add alternatives: Download, Conflict, Export (dashed)
3. Show decision points

### Phase 9: Act 7 (Create Playbooks)
1. Add as optional branch from Act 3+
2. Show 4 creation methods
3. Reconnect to Act 6 (sync new playbook)

### Phase 10: Acts 8-9 (Settings & Errors)
1. Add settings as side branch (accessible anytime)
2. Add error recovery detours from relevant acts
3. Show return paths

### Phase 11: Polish
1. Add legend
2. Add START and END markers
3. Add annotations for key decisions
4. Verify all connections
5. Balance layout

---

## Canvas Size

- **Width**: 2800px (to accommodate full flow left-to-right)
- **Height**: 2400px (8-9 swimlanes × ~250px each + spacing)
- **Page**: Custom size for wide format

---

## Decision Points to Show

1. **Act 2**: Join existing family OR Create new family?
2. **Act 3**: Download from HB OR Import from JSON?
3. **Act 5**: User-initiated PIP OR AI-suggested PIP?
4. **Act 6**: Clean upload/download OR Conflict resolution?
5. **Act 7**: When to create new playbook?

---

## Key Annotations

- "First-time user path" label on main flow
- "Optional: Create your own content" on Act 7 branch
- "Accessible anytime" on Act 4 (MCP)
- "Error recovery" on Acts 8-9 detours
- "Parallel activity" on Act 4

---

## Success Criteria

✅ All 87 screens represented (main + alternatives)  
✅ Main success path clearly visible (bold arrows)  
✅ Alternative paths shown (dashed)  
✅ Error recovery detours included  
✅ Clear act separation with swimlanes  
✅ Logical left-to-right, top-to-bottom flow  
✅ Color-coded by system (HB, FOB, Windsurf)  
✅ Decision points highlighted  
✅ Legend explains visual language  

---

## File Details

**File**: `screen-flow.drawio`  
**New Page**: Page 10 - "Integrated End-to-End Flow"  
**Root Cell ID**: `integrated-root-0` and `integrated-root-1`

---

**Status**: Ready to build  
**Next**: Start with Phase 1 (Structure)
