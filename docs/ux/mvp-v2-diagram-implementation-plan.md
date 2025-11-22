# MVP Flow v2 - Diagram Implementation Plan

## Executive Summary

**Goal:** Create comprehensive MVP Flow v2 diagram showing full CRUDLF for 7 green domain entities (Playbook, Workflow, Phase, Activity, Artifact, Howto, Role) with dual access (FOB Pages + MCP Tools). Goal entity deferred to v2.1.

**Approach:** Systematic, act-by-act construction with validation checkpoints.

**Timeline:** 2-3 days for diagram creation + wireframe specifications.

---

## Step-by-Step Implementation

### STEP 1: Prepare Canvas and Structure (30 minutes)

#### 1.1 Create New Diagram Tab
- Open `screen-flow.drawio`
- Create new diagram tab: "MVP Flow v2 - Full CRUDLF"
- Set canvas properties:
  - Page width: 3600px
  - Page height: 2400px
  - Grid: 10px
  - Page scale: 1

#### 1.2 Create Master Legend
Position: Top-left (x=40, y=40)
```
LEGEND
├── 🟦 Blue Box = FOB Page (#4682B4)
├── 🟪 Purple Box = Windsurf Integration (#9370DB)
├── ⚫ Grey Box = MCP Tool (#666666, dashed)
├── 🟧 Orange Box = MCP Service (#FF8C00)
├── → Bold Black Arrow = Primary Flow
├── → Thin Blue Arrow = Alternative Flow
└── → Dashed Grey Arrow = Tool Connection
```

#### 1.3 Define Layout Grid
```
Column 1: x=40-840    (Acts 0, 1, 10)
Column 2: x=880-1680  (Acts 2, 3, 4)
Column 3: x=1720-2520 (Acts 5, 6, 7)
Column 4: x=2560-3360 (Acts 8, 9)

Row 1: y=140-540   (Setup acts)
Row 2: y=580-1020  (Entity acts 2-4: Playbook, Workflow, Phase)
Row 3: y=1060-1500 (Entity acts 5-7: Activity, Artifact, Howto)
Row 4: y=1540-1980 (Entity acts 8-9: Role, PIPs)
Row 5: y=2020-2300 (Export/Import, Summary)

Note: Goal (ACT 7 in original plan) deferred to v2.1
```

---

### STEP 2: Build Foundation Acts (1 hour)

#### 2.1 ACT 0: LOCAL SETUP
**Position:** Column 1, Row 1 (x=40, y=140)

**Elements:**
```xml
<mxCell id="v2-act0-label" value="ACT 0: LOCAL SETUP" 
        style="...fillColor=#e3f2fd;strokeColor=#1565c0..." 
        geometry x="40" y="140" width="180" height="30"/>

<mxCell id="v2-start" value="START\nPull FOB Container" 
        style="ellipse...fillColor=#e1d5e7;strokeColor=#9673a6..." 
        geometry x="40" y="180" width="120" height="80"/>

<mxCell id="v2-fob-startup" value="FOB-STARTUP-1" 
        style="...fillColor=#4682B4;strokeColor=#1565c0..." 
        geometry x="200" y="180" width="100" height="50"/>

<mxCell id="v2-fob-user-create" value="FOB-LOCAL-\nUSER-CREATE-1" 
        style="...fillColor=#4682B4;strokeColor=#1565c0..." 
        geometry x="200" y="250" width="100" height="50"/>
```

#### 2.2 ACT 1: MCP CONFIG
**Position:** Column 1, Row 1 (x=360, y=140)

**Elements:**
```xml
<mxCell id="v2-act1-label" value="ACT 1: MCP CONFIG" 
        style="...fillColor=#e8f5e9;strokeColor=#2e7d32..." 
        geometry x="360" y="140" width="180" height="30"/>

<mxCell id="v2-fob-first-run" value="FOB-FIRST-RUN-1" 
        style="...fillColor=#4682B4..." 
        geometry x="360" y="180" width="90" height="50"/>

<mxCell id="v2-fob-mcp-config" value="FOB-MCP-CONFIG-1" 
        style="...fillColor=#4682B4..." 
        geometry x="360" y="250" width="90" height="50"/>

<mxCell id="v2-fob-dashboard" value="FOB-DASHBOARD-1" 
        style="...fillColor=#4682B4;strokeWidth=2..." 
        geometry x="360" y="320" width="90" height="50"/>
```

**Arrow:** ACT 0 → ACT 1
```xml
<mxCell id="v2-arrow-act0-act1" value="Next" 
        source="v2-fob-user-create" target="v2-fob-first-run" 
        style="...strokeWidth=3;strokeColor=#000000..."/>
```

---

### STEP 3: Create Entity Act Template (2 hours)

#### 3.1 Define Standard Entity Act Structure

**Template for each entity act:**
```
ACT [N]: [ENTITY_PLURAL]
├── Act Label (colored header)
├── Navigation from Dashboard
├── FOB-[ENTITY_PLURAL]-LIST+FIND (entry point)
├── FOB-[ENTITY_PLURAL]-CREATE_[ENTITY]
├── FOB-[ENTITY_PLURAL]-VIEW_[ENTITY]
├── FOB-[ENTITY_PLURAL]-EDIT_[ENTITY]
├── FOB-[ENTITY_PLURAL]-DELETE_[ENTITY] (modal)
├── WINDSURF-[ENTITY]-CHAT
├── MCP-[ENTITY]-CONTEXT
└── @tools section:
    ├── @create_[entity]
    ├── @get_[entity]
    ├── @update_[entity]
    ├── @delete_[entity]
    ├── @list_[entities]
    └── @find_[entities]
```

#### 3.2 Standard Element Dimensions
```
FOB Page:     width=140, height=60
Windsurf:     width=100, height=50
MCP Tool:     width=110, height=30
MCP Service:  width=100, height=50
Act Label:    width=220, height=30
```

#### 3.3 Standard Spacing
```
Between pages:     40px horizontal, 20px vertical
Page to tools:     60px vertical
Tools horizontal:  10px gap
Act to act:        200px
```

---

### STEP 4: Build ACT 2 - PLAYBOOKS (45 minutes)

**Position:** Column 2, Row 2 (x=880, y=580)

#### 4.1 Act Label
```xml
<mxCell id="v2-act2-label" value="ACT 2: PLAYBOOKS" 
        style="...fillColor=#fff3e0;strokeColor=#ff8f00..." 
        geometry x="880" y="580" width="220" height="30"/>
```

#### 4.2 FOB Pages
```xml
<!-- From Dashboard -->
<mxCell id="v2-fob-playbooks-list" 
        value="FOB-PLAYBOOKS-\nLIST+FIND" 
        style="...fillColor=#4682B4;strokeColor=#1565c0;strokeWidth=2..." 
        geometry x="880" y="620" width="140" height="60"/>

<!-- CRUD Pages -->
<mxCell id="v2-fob-playbooks-create" 
        value="FOB-PLAYBOOKS-\nCREATE_PLAYBOOK" 
        style="...fillColor=#4682B4..." 
        geometry x="1030" y="620" width="140" height="60"/>

<mxCell id="v2-fob-playbooks-view" 
        value="FOB-PLAYBOOKS-\nVIEW_PLAYBOOK" 
        style="...fillColor=#4682B4..." 
        geometry x="880" y="700" width="140" height="60"/>

<mxCell id="v2-fob-playbooks-edit" 
        value="FOB-PLAYBOOKS-\nEDIT_PLAYBOOK" 
        style="...fillColor=#4682B4..." 
        geometry x="1030" y="700" width="140" height="60"/>

<mxCell id="v2-fob-playbooks-delete" 
        value="FOB-PLAYBOOKS-\nDELETE_PLAYBOOK\n(modal)" 
        style="...fillColor=#f8cecc;strokeColor=#b85450..." 
        geometry x="1180" y="700" width="140" height="60"/>
```

#### 4.3 Windsurf Integration
```xml
<mxCell id="v2-windsurf-playbook" 
        value="WINDSURF-\nPLAYBOOK-CHAT" 
        style="...fillColor=#9370DB;strokeColor=#6a5acd..." 
        geometry x="1180" y="620" width="100" height="50"/>

<mxCell id="v2-mcp-playbook-context" 
        value="MCP-PLAYBOOK-\nCONTEXT" 
        style="...fillColor=#FF8C00;strokeColor=#d68000..." 
        geometry x="1290" y="620" width="100" height="50"/>
```

#### 4.4 MCP Tools Section
```xml
<mxCell id="v2-tool-playbooks-label" 
        value="@tools" 
        style="...fillColor=#f5f5f5;strokeColor=#666666..." 
        geometry x="880" y="780" width="50" height="20"/>

<!-- CRUDLF Tools -->
<mxCell id="v2-tool-create-playbook" 
        value="@create_playbook" 
        style="...fillColor=#f5f5f5;strokeColor=#666666;dashed=1..." 
        geometry x="940" y="780" width="110" height="30"/>

<mxCell id="v2-tool-get-playbook" 
        value="@get_playbook" 
        style="...fillColor=#f5f5f5;strokeColor=#666666;dashed=1..." 
        geometry x="1060" y="780" width="110" height="30"/>

<mxCell id="v2-tool-update-playbook" 
        value="@update_playbook" 
        style="...fillColor=#f5f5f5;strokeColor=#666666;dashed=1..." 
        geometry x="1180" y="780" width="110" height="30"/>

<mxCell id="v2-tool-delete-playbook" 
        value="@delete_playbook" 
        style="...fillColor=#f5f5f5;strokeColor=#666666;dashed=1..." 
        geometry x="1300" y="780" width="110" height="30"/>

<mxCell id="v2-tool-list-playbooks" 
        value="@list_playbooks" 
        style="...fillColor=#f5f5f5;strokeColor=#666666;dashed=1..." 
        geometry x="940" y="820" width="110" height="30"/>

<mxCell id="v2-tool-find-playbooks" 
        value="@find_playbooks" 
        style="...fillColor=#f5f5f5;strokeColor=#666666;dashed=1..." 
        geometry x="1060" y="820" width="110" height="30"/>
```

#### 4.5 Flow Arrows
```xml
<!-- From Dashboard -->
<mxCell id="v2-arrow-dash-playbooks" 
        value="[Playbooks]" 
        source="v2-fob-dashboard" target="v2-fob-playbooks-list" 
        style="...strokeWidth=3;strokeColor=#000000..."/>

<!-- List to CRUD -->
<mxCell id="v2-arrow-list-create" 
        value="[New]" 
        source="v2-fob-playbooks-list" target="v2-fob-playbooks-create" 
        style="...strokeWidth=2;strokeColor=#4682B4..."/>

<mxCell id="v2-arrow-list-view" 
        value="[Select]" 
        source="v2-fob-playbooks-list" target="v2-fob-playbooks-view" 
        style="...strokeWidth=2;strokeColor=#4682B4..."/>

<mxCell id="v2-arrow-view-edit" 
        value="[Edit]" 
        source="v2-fob-playbooks-view" target="v2-fob-playbooks-edit" 
        style="...strokeWidth=2;strokeColor=#4682B4..."/>

<mxCell id="v2-arrow-view-delete" 
        value="[Delete]" 
        source="v2-fob-playbooks-view" target="v2-fob-playbooks-delete" 
        style="...strokeWidth=1;strokeColor=#b85450;dashed=1..."/>

<!-- Tool connections -->
<mxCell id="v2-arrow-tool-create-pb" 
        source="v2-fob-playbooks-create" target="v2-tool-create-playbook" 
        style="...strokeWidth=1;strokeColor=#666666;dashed=1..."/>

<mxCell id="v2-arrow-tool-get-pb" 
        source="v2-fob-playbooks-view" target="v2-tool-get-playbook" 
        style="...strokeWidth=1;strokeColor=#666666;dashed=1..."/>

<mxCell id="v2-arrow-tool-update-pb" 
        source="v2-fob-playbooks-edit" target="v2-tool-update-playbook" 
        style="...strokeWidth=1;strokeColor=#666666;dashed=1..."/>

<mxCell id="v2-arrow-tool-delete-pb" 
        source="v2-fob-playbooks-delete" target="v2-tool-delete-playbook" 
        style="...strokeWidth=1;strokeColor=#666666;dashed=1..."/>

<mxCell id="v2-arrow-tool-list-pb" 
        source="v2-fob-playbooks-list" target="v2-tool-list-playbooks" 
        style="...strokeWidth=1;strokeColor=#666666;dashed=1..."/>

<mxCell id="v2-arrow-tool-find-pb" 
        source="v2-fob-playbooks-list" target="v2-tool-find-playbooks" 
        style="...strokeWidth=1;strokeColor=#666666;dashed=1..."/>
```

**Validation Checkpoint:**
- [ ] All 5 FOB pages present
- [ ] All 6 MCP tools present
- [ ] 2 Windsurf integrations
- [ ] All arrows connected
- [ ] Naming convention correct

---

### STEP 5: Replicate for Remaining Entities (3-4 hours)

#### 5.1 ACT 3: WORKFLOWS
**Position:** Column 2, Row 2 (x=1420, y=580)
- Copy ACT 2 structure
- Replace "PLAYBOOKS" → "WORKFLOWS"
- Replace "playbook" → "workflow" in all IDs and labels
- Update colors if needed (keep consistent)

#### 5.2 ACT 4: PHASES
**Position:** Column 2, Row 2 (x=1960, y=580)
- Replicate structure
- Update entity name

#### 5.3 ACT 5: ACTIVITIES
**Position:** Column 3, Row 3 (x=880, y=1060)
- Replicate structure
- Update entity name

#### 5.4 ACT 6: ARTIFACTS
**Position:** Column 3, Row 3 (x=1420, y=1060)
- Replicate structure
- Update entity name

#### 5.5 ACT 7: HOWTOS
**Position:** Column 3, Row 3 (x=1960, y=1060)
- Replicate structure
- Update entity name

#### 5.6 ACT 8: ROLES
**Position:** Column 4, Row 4 (x=880, y=1540)
- Replicate structure
- Update entity name

**Batch Validation:**
- [ ] All 7 entity acts created (Playbook, Workflow, Phase, Activity, Artifact, Howto, Role)
- [ ] Goal entity explicitly NOT included (deferred to v2.1)
- [ ] Naming consistent across all
- [ ] Each has 5 pages + 6 tools + 2 Windsurf
- [ ] Colors match legend

---

### STEP 6: Build ACT 9 - PIPS (1 hour)

**Position:** Column 4, Row 4 (x=1420, y=1540)

**Special Structure** (expanded from v1):
```
FOB Pages:
- FOB-PIPS-LIST+FIND
- FOB-PIPS-CREATE_PIP
- FOB-PIPS-VIEW_PIP
- FOB-PIPS-EDIT_PIP
- FOB-PIPS-REVIEW_PIP (approval workflow)
- FOB-PIPS-APPROVED_PIP (confirmation)
- FOB-PIPITEMS-LIST+FIND (sub-entity)
- FOB-PIPITEMS-VIEW_PIPITEM

MCP Tools:
- @create_pip
- @get_pip
- @update_pip
- @delete_pip
- @list_pips
- @find_pips
- @suggest_pip (AI)
- @submit_pip
- @approve_pip
- @reject_pip
- @list_pip_items
- @get_pip_item

Windsurf:
- WINDSURF-PIP-SUGGEST
- MCP-PIP-GENERATE
```

---

### STEP 7: Build ACT 10 - EXPORT/IMPORT (30 minutes)

**Position:** Column 1, Row 5 (x=40, y=2020)

**Reuse from v1:**
- `FOB-EXPORT-1`
- `FOB-IMPORT-UPLOAD-1`
- `FOB-IMPORT-VALIDATE-1`
- `FOB-IMPORT-COMPLETE-1`

**Add MCP Tools:**
- `@export_playbook`
- `@import_playbook`
- `@validate_import`

---

### STEP 8: Add Cross-Act Navigation (1 hour)

#### 8.1 Dashboard Hub Arrows
```
Dashboard → ACT 2 (Playbooks)
Dashboard → ACT 3 (Workflows)
Dashboard → ACT 4 (Phases)
Dashboard → ACT 5 (Activities)
Dashboard → ACT 6 (Artifacts)
Dashboard → ACT 7 (Howtos)
Dashboard → ACT 8 (Roles)
Dashboard → ACT 9 (PIPs)
Dashboard → ACT 10 (Export/Import)
```

#### 8.2 Inter-Entity Navigation
```
Workflows → Phases (contains)
Workflows → Activities (contains)
Activities → Artifacts (produces)
Activities → Goals (achieves) [deferred to v2.1]
Activities → Howtos (guided by)
Activities → Roles (performed by)
```

---

### STEP 9: Add Summary Boxes (30 minutes)

**Position:** Bottom (y=2100)

#### 9.1 Included in MVP v2
```xml
<mxCell id="v2-summary-included" 
        value="INCLUDED IN MVP v2:\n
        • Full CRUDLF for 8 entities\n
        • Dual access: FOB + MCP\n
        • Windsurf integration\n
        • PIP workflow (expanded)\n
        • Export/Import\n
        • Local-only operation" 
        style="...fillColor=#e8f5e9;strokeColor=#2e7d32..." 
        geometry x="40" y="2100" width="400" height="160"/>
```

#### 9.2 Excluded from MVP v2
```xml
<mxCell id="v2-summary-excluded" 
        value="EXCLUDED FROM MVP v2:\n
        • Homebase sync\n
        • Family management\n
        • Token auth\n
        • Conflict resolution\n
        • External MCPs (GitHub/Jira)" 
        style="...fillColor=#ffebee;strokeColor=#c62828..." 
        geometry x="460" y="2100" width="400" height="160"/>
```

#### 9.3 What's Next
```xml
<mxCell id="v2-summary-next" 
        value="WHAT'S NEXT:\n
        Phase 2: Add Homebase sync\n
        Phase 3: Community features\n
        Phase 4: Advanced settings\n
        \nSee MVP_SPECIFICATION.md" 
        style="...fillColor=#fff3e0;strokeColor=#ff8f00..." 
        geometry x="880" y="2100" width="400" height="160"/>
```

---

### STEP 10: Final Validation (30 minutes)

#### 10.1 Completeness Check
- [ ] All 10 acts present (ACT 0-10)
- [ ] All 7 entities have 5 pages each = 35 pages
- [ ] All 7 entities have 6 tools each = 42 tools
- [ ] PIP act has 8 pages + 12 tools
- [ ] Export/Import has 4 pages + 3 tools
- [ ] Setup acts (0, 1) present
- [ ] Goal entity explicitly NOT included (deferred to v2.1)
- [ ] Total: **50 FOB pages, 57 MCP tools, 14 Windsurf integrations**

#### 10.2 Visual Check
- [ ] No overlapping elements
- [ ] All arrows point to valid targets
- [ ] Colors match legend
- [ ] Text readable at 100% zoom
- [ ] Layout balanced across canvas
- [ ] Spacing consistent

#### 10.3 Naming Convention Check
Run find/replace validation:
```
FOB-[ENTITY_PLURAL]-LIST+FIND
FOB-[ENTITY_PLURAL]-CREATE_[ENTITY]
FOB-[ENTITY_PLURAL]-VIEW_[ENTITY]
FOB-[ENTITY_PLURAL]-EDIT_[ENTITY]
FOB-[ENTITY_PLURAL]-DELETE_[ENTITY]
@create_[entity]
@get_[entity]
@update_[entity]
@delete_[entity]
@list_[entities]
@find_[entities]
```

#### 10.4 Export
1. Save `screen-flow.drawio`
2. Export "MVP Flow v2" tab as PNG (150% scale)
3. Export as SVG for documentation
4. Commit to git

---

## Timeline Summary

| Task | Duration | Dependencies |
|------|----------|--------------|
| 1. Canvas setup | 30 min | None |
| 2. Foundation acts | 1 hour | Step 1 |
| 3. Entity template | 2 hours | Step 2 |
| 4. ACT 2 (Playbooks) | 45 min | Step 3 |
| 5. ACTs 3-8 (6 entities) | 3-4 hours | Step 4 |
| 6. ACT 9 (PIPs) | 1 hour | Step 5 |
| 7. ACT 10 (Export/Import) | 30 min | Step 6 |
| 8. Cross-act navigation | 1 hour | Steps 4-7 |
| 9. Summary boxes | 30 min | All above |
| 10. Validation | 30 min | All above |
| **TOTAL** | **10-11 hours** | |

**Realistic estimate with breaks:** 2 working days

**Note:** Goal entity (originally ACT 7) deferred to v2.1, reducing scope from 11 to 10 acts.

---

## Success Criteria

✅ **Diagram is complete when:**
1. All 7 green entities have full CRUDLF (5 pages + 6 tools each)
2. Goal entity explicitly marked as deferred to v2.1
3. Every FOB page has MCP tool equivalent
4. All navigation paths clearly shown
5. Naming conventions 100% consistent
6. Visual layout clean and readable
7. Can trace path from dashboard to any entity operation
8. Legend and summary accurate
9. Export PNG at 150% is readable

✅ **Ready for implementation when:**
1. Stakeholders approve diagram
2. Page inventory document created
3. MCP tool specifications written
4. Wireframes for representative pages done
5. Technical feasibility confirmed
