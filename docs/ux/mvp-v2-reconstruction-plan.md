# MVP Flow v2 Reconstruction Plan

## A. Current MVP Flow (v1) - Starting Point

### Current Acts Structure

#### ACT 0: LOCAL SETUP
**FOB Pages:**
- `FOB-STARTUP-1` - Pull container
- `FOB-LOCAL-USER-CREATE-1` - Create local user

#### ACT 1: MCP CONFIG
**FOB Pages:**
- `FOB-FIRST-RUN-1` - First run setup
- `FOB-MCP-CONFIG-1` - MCP configuration
- `FOB-DASHBOARD-1` - Main dashboard

#### ACT 7: CREATE PLAYBOOK
**FOB Pages:**
- `FOB-CREATE-PLAYBOOK-1` - Create playbook entry point
- `FOB-WIZARD-BASIC-1` - Basic wizard
- `FOB-EDITOR-1` - Playbook editor (Method 1)

**Windsurf Integration:**
- `WINDSURF-CREATE-1` - Create via Windsurf (Method 4)
- `MCP-CREATED-1` - MCP creation confirmation

**MCP Tools:**
- `@create_playbook`
- `@add_activity`
- `@list_activities`

#### ACT 4: USE WITH MCP
**FOB Pages:**
- `FOB-OPEN-PLAYBOOK-1` - Open playbook
- `FOB-DETAIL-1` - View details

**Windsurf Integration:**
- `WINDSURF-CHAT-1` - Chat interface
- `WINDSURF-COMMANDS-1` - Command palette
- `MCP-CONTEXT-1` - Context provider

**MCP Tools:**
- `@get_playbook_context`
- `@get_activity_howto`
- `@list_playbooks`
- `@open_in_gui`
- `@get_activity_details`

#### ACT 5: PIPS
**FOB Pages:**
- `FOB-PIP-REVIEW-1` - Review PIPs
- `FOB-PIP-APPROVED-1` - Approval confirmation

**Windsurf Integration:**
- `WINDSURF-PIP-SUGGEST-1` - Suggest PIP
- `MCP-PIP-GENERATE-1` - Generate PIP

**MCP Tools:**
- `@suggest_pip`
- `@submit_pip`
- `@list_pending_pips`
- `@approve_pip`

#### ACT 6: EXPORT/IMPORT
**FOB Pages:**
- `FOB-EXPORT-1` - Export playbook
- `FOB-IMPORT-UPLOAD-1` - Upload file
- `FOB-IMPORT-VALIDATE-1` - Validate import
- `FOB-IMPORT-COMPLETE-1` - Complete import

### Current Coverage Analysis

#### ✅ What's Covered:
- Playbook CRUDLF (Create, Read, Update, Delete, List, Find)
- Activity partial coverage (add, list, get details, get howto)
- PIP workflow (suggest, submit, list, approve)
- Export/Import functionality

#### ❌ What's Missing:
**No dedicated CRUDLF pages for:**
1. Workflow
2. Phase
3. Artifact
4. Goal
5. Howto
6. Role

**No dedicated MCP tools for these entities' full CRUDLF.**

---

## B. MVP v2 Reconstruction - Full CRUDLF Coverage

### Design Principles

1. **Entity-First Organization**: Each green entity gets dedicated CRUDLF pages
2. **Dual Access**: Every operation accessible via BOTH FOB pages AND MCP tools
3. **Consistent Naming**: `FOB-[ENTITY_PLURAL]-[ACTION]_[ENTITY_SINGULAR]`
4. **MCP Naming**: `@[action]_[entity]` format

### Green Entities from Domain Model

**MVP v2 SCOPE (7 entities):**
1. **Playbook** (already covered) - container
2. **Workflow** (missing) - top-level structure
3. **Phase** (missing) - workflow organization
4. **Activity** (partial) - actionable steps
5. **Artifact** (missing) - outputs/deliverables
6. **Howto** (missing) - detailed instructions
7. **Role** (missing) - performers

**DEFERRED TO v2.1:**
8. **Goal** - target outcomes (deferred - can be tracked informally in workflow/activity descriptions initially)

---

## C. MVP Flow v2 - Detailed Act Structure

### ACT 0: LOCAL SETUP (unchanged)
- `FOB-STARTUP-1`
- `FOB-LOCAL-USER-CREATE-1`

### ACT 1: MCP CONFIG (unchanged)
- `FOB-FIRST-RUN-1`
- `FOB-MCP-CONFIG-1`
- `FOB-DASHBOARD-1`

### ACT 2: PLAYBOOKS (expanded)

#### FOB Pages:
- `FOB-PLAYBOOKS-LIST+FIND` - List all playbooks with search/filter
- `FOB-PLAYBOOKS-CREATE_PLAYBOOK` - Create new playbook
- `FOB-PLAYBOOKS-VIEW_PLAYBOOK` - View playbook details
- `FOB-PLAYBOOKS-EDIT_PLAYBOOK` - Edit playbook
- `FOB-PLAYBOOKS-DELETE_PLAYBOOK` - Delete confirmation modal

#### MCP Tools:
- `@create_playbook`
- `@get_playbook`
- `@update_playbook`
- `@delete_playbook`
- `@list_playbooks`
- `@find_playbooks`

#### Windsurf:
- `WINDSURF-PLAYBOOK-CHAT`
- `MCP-PLAYBOOK-CONTEXT`

### ACT 3: WORKFLOWS

#### FOB Pages:
- `FOB-WORKFLOWS-LIST+FIND` - List all workflows with search
- `FOB-WORKFLOWS-CREATE_WORKFLOW` - Create workflow
- `FOB-WORKFLOWS-VIEW_WORKFLOW` - View workflow details
- `FOB-WORKFLOWS-EDIT_WORKFLOW` - Edit workflow
- `FOB-WORKFLOWS-DELETE_WORKFLOW` - Delete confirmation

#### MCP Tools:
- `@create_workflow`
- `@get_workflow`
- `@update_workflow`
- `@delete_workflow`
- `@list_workflows`
- `@find_workflows`

#### Windsurf:
- `WINDSURF-WORKFLOW-CHAT`
- `MCP-WORKFLOW-CONTEXT`

### ACT 4: PHASES

#### FOB Pages:
- `FOB-PHASES-LIST+FIND` - List phases with filter by workflow
- `FOB-PHASES-CREATE_PHASE` - Create phase
- `FOB-PHASES-VIEW_PHASE` - View phase details
- `FOB-PHASES-EDIT_PHASE` - Edit phase
- `FOB-PHASES-DELETE_PHASE` - Delete confirmation

#### MCP Tools:
- `@create_phase`
- `@get_phase`
- `@update_phase`
- `@delete_phase`
- `@list_phases`
- `@find_phases`

#### Windsurf:
- `WINDSURF-PHASE-CHAT`
- `MCP-PHASE-CONTEXT`

### ACT 5: ACTIVITIES

#### FOB Pages:
- `FOB-ACTIVITIES-LIST+FIND` - List activities with filter by workflow/phase
- `FOB-ACTIVITIES-CREATE_ACTIVITY` - Create activity
- `FOB-ACTIVITIES-VIEW_ACTIVITY` - View activity details
- `FOB-ACTIVITIES-EDIT_ACTIVITY` - Edit activity
- `FOB-ACTIVITIES-DELETE_ACTIVITY` - Delete confirmation

#### MCP Tools:
- `@create_activity`
- `@get_activity`
- `@update_activity`
- `@delete_activity`
- `@list_activities`
- `@find_activities`

#### Windsurf:
- `WINDSURF-ACTIVITY-CHAT`
- `MCP-ACTIVITY-CONTEXT`

### ACT 6: ARTIFACTS

#### FOB Pages:
- `FOB-ARTIFACTS-LIST+FIND` - List artifacts with filter by activity
- `FOB-ARTIFACTS-CREATE_ARTIFACT` - Create artifact
- `FOB-ARTIFACTS-VIEW_ARTIFACT` - View artifact details
- `FOB-ARTIFACTS-EDIT_ARTIFACT` - Edit artifact
- `FOB-ARTIFACTS-DELETE_ARTIFACT` - Delete confirmation

#### MCP Tools:
- `@create_artifact`
- `@get_artifact`
- `@update_artifact`
- `@delete_artifact`
- `@list_artifacts`
- `@find_artifacts`

#### Windsurf:
- `WINDSURF-ARTIFACT-CHAT`
- `MCP-ARTIFACT-CONTEXT`

### ACT 7: HOWTOS

#### FOB Pages:
- `FOB-HOWTOS-LIST+FIND` - List howtos with filter by activity
- `FOB-HOWTOS-CREATE_HOWTO` - Create howto
- `FOB-HOWTOS-VIEW_HOWTO` - View howto details
- `FOB-HOWTOS-EDIT_HOWTO` - Edit howto
- `FOB-HOWTOS-DELETE_HOWTO` - Delete confirmation

#### MCP Tools:
- `@create_howto`
- `@get_howto`
- `@update_howto`
- `@delete_howto`
- `@list_howtos`
- `@find_howtos`

#### Windsurf:
- `WINDSURF-HOWTO-CHAT`
- `MCP-HOWTO-CONTEXT`

### ACT 8: ROLES

#### FOB Pages:
- `FOB-ROLES-LIST+FIND` - List roles with filter by activity
- `FOB-ROLES-CREATE_ROLE` - Create role
- `FOB-ROLES-VIEW_ROLE` - View role details
- `FOB-ROLES-EDIT_ROLE` - Edit role
- `FOB-ROLES-DELETE_ROLE` - Delete confirmation

#### MCP Tools:
- `@create_role`
- `@get_role`
- `@update_role`
- `@delete_role`
- `@list_roles`
- `@find_roles`

#### Windsurf:
- `WINDSURF-ROLE-CHAT`
- `MCP-ROLE-CONTEXT`

### ACT 9: PIPS (expanded from v1)

#### FOB Pages:
- `FOB-PIPS-LIST+FIND` - List PIPs with filter/search
- `FOB-PIPS-CREATE_PIP` - Create PIP manually
- `FOB-PIPS-VIEW_PIP` - View PIP details
- `FOB-PIPS-EDIT_PIP` - Edit PIP before submission
- `FOB-PIPS-REVIEW_PIP` - Review PIP (approval flow)
- `FOB-PIPS-APPROVED_PIP` - Approval confirmation
- `FOB-PIPITEMS-LIST+FIND` - List PIP items
- `FOB-PIPITEMS-VIEW_PIPITEM` - View individual PIP item

#### MCP Tools:
- `@create_pip`
- `@get_pip`
- `@update_pip`
- `@delete_pip`
- `@list_pips`
- `@find_pips`
- `@suggest_pip` (AI-generated)
- `@submit_pip`
- `@approve_pip`
- `@reject_pip`
- `@list_pip_items`
- `@get_pip_item`

#### Windsurf:
- `WINDSURF-PIP-SUGGEST`
- `MCP-PIP-GENERATE`

### ACT 10: EXPORT/IMPORT (unchanged)
- `FOB-EXPORT-1`
- `FOB-IMPORT-UPLOAD-1`
- `FOB-IMPORT-VALIDATE-1`
- `FOB-IMPORT-COMPLETE-1`

---

## D. Implementation Plan

### Phase 1: Document Structure (This Document)
✅ Analyze current MVP
✅ Define v2 structure
✅ List all pages and tools

### Phase 2: Create Visual Layout Plan
**Tasks:**
1. Define canvas size (suggested: 3600px wide × 2400px high)
2. Define act layout (3 columns × 4 rows for acts 2-9)
3. Define spacing (200px between acts, 150px between pages)
4. Define color coding:
   - FOB pages: Blue (#4682B4)
   - Windsurf: Purple (#9370DB)
   - MCP tools: Grey (#666666)
   - MCP services: Orange (#FF8C00)

### Phase 3: Create Entity Groups
**For each of 7 entities (Playbook, Workflow, Phase, Activity, Artifact, Howto, Role):**

Create group structure:
```
ACT [N]: [ENTITY_PLURAL]
├── FOB-[ENTITY_PLURAL]-LIST+FIND
├── FOB-[ENTITY_PLURAL]-CREATE_[ENTITY]
├── FOB-[ENTITY_PLURAL]-VIEW_[ENTITY]
├── FOB-[ENTITY_PLURAL]-EDIT_[ENTITY]
├── FOB-[ENTITY_PLURAL]-DELETE_[ENTITY]
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

### Phase 4: Create Flow Arrows
**Arrow Types:**
1. **Primary flow** (Black, solid, width=3) - Main user path
2. **Alternative flow** (Blue, solid, width=2) - Secondary paths
3. **Tool connections** (Grey, dashed, width=1) - FOB ↔ MCP
4. **Act transitions** (Black, solid, width=3) - Between acts

### Phase 5: Add Navigation Elements
**Add to each act:**
- Act label (color-coded header)
- @tools section label
- Tool connection arrows
- Navigation hints ("from dashboard", "back to list", etc.)

### Phase 6: Add Legend and Summary
**Add at bottom:**
1. **Color Legend:**
   - 🟦 FOB Page
   - 🟪 Windsurf Integration
   - ⚫ MCP Tool
   - 🟧 MCP Service

2. **Summary Boxes:**
   - "INCLUDED IN MVP v2"
   - "EXCLUDED FROM MVP v2"
   - "WHAT'S NEXT"

### Phase 7: Validate Completeness
**Checklist:**
- [ ] All 7 green entities have full CRUDLF
- [ ] Every FOB page has corresponding MCP tools
- [ ] All arrows properly connected
- [ ] No orphaned elements
- [ ] Naming conventions consistent
- [ ] Colors consistent with legend
- [ ] Layout readable at 100% zoom
- [ ] Goal entity deferred to v2.1 (documented in plan)

### Phase 8: Export and Document
**Deliverables:**
1. `screen-flow.drawio` updated with "MVP Flow v2 - Full CRUDLF" tab
2. Export PNG at 150% for review
3. Update `MVP_SPECIFICATION.md` with v2 details
4. Create `mvp-v2-page-inventory.md` (all pages + tools)

---

## E. Statistics

### MVP v1 (Current):
- **Acts:** 7 (ACT 0, 1, 4, 5, 6, 7, plus fragments)
- **FOB Pages:** 15
- **MCP Tools:** 12
- **Windsurf Integrations:** 4
- **Entities Covered:** 2 (Playbook full, Activity partial)

### MVP v2 (Proposed - 7 Entities):
- **Acts:** 10 (ACT 0-10)
- **FOB Pages:** 50 (5 pages × 7 entities + 7 PIP pages + 4 system pages + 4 import/export)
- **MCP Tools:** 48 (6 tools × 7 entities + 6 PIP tools)
- **Windsurf Integrations:** 14 (2 per entity)
- **Entities Covered:** 7 (Playbook, Workflow, Phase, Activity, Artifact, Howto, Role)
- **Deferred:** 1 (Goal → v2.1)

### Effort Estimate:
- **Diagram creation:** 8-10 hours
- **Page wireframes:** 35-50 hours (50 pages × ~1 hour each)
- **MCP tool specs:** 20-25 hours (48 tools)
- **Implementation:** 180-250 hours (engineering)

---

## F. Next Steps

### Immediate Actions:
1. **Review this plan** with stakeholders
2. **Adjust scope** if needed (MVP v2 might be too large)
3. **Prioritize entities** (which CRUDLF to implement first?)
4. **Create diagram layout** (empty structure)
5. **Populate act by act** (ACT 2 → ACT 3 → ... → ACT 11)

### ✅ APPROVED SCOPE: MVP v2 (7 Entities)

**Included:**
- Playbook ✅
- Workflow ✅
- Phase ✅
- Activity ✅
- Artifact ✅
- Howto ✅
- Role ✅

**Result:** 50 pages, 48 tools, 8-10 weeks

**Deferred to v2.1:**
- Goal (can be tracked informally in descriptions until then)
