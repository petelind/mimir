# Screen Flow Diagram Update Instructions

**File**: `docs/ux/2_dialogue-maps/screen-flow.drawio`  
**Tool**: Draw.io (diagrams.net)  
**Task**: Mark completed pages with visual indicators

---

## Color Coding System

### ✅ Bold Green Border (100% Complete)
**Meaning**: All scenarios for this page are fully implemented and tested

**Apply to these pages**:

#### Playbooks
- ✅ **Playbooks List** - List, search, filters all implemented
- ✅ **Create Playbook Wizard Step 1** - Basic information form complete
- ✅ **Create Playbook Wizard Step 2** - Add workflows inline complete
- ✅ **Create Playbook Wizard Step 3** - Publishing settings complete  
- ✅ **Playbook Detail** - Full detail view with workflows implemented
- ✅ **Edit Playbook** - Edit form complete

#### Workflows
- ✅ **Workflows List** (scoped to playbook) - List view complete
- ✅ **Create Workflow** - Create form complete
- ✅ **Workflow Detail** - Detail view with Graphviz diagram complete
- ✅ **Edit Workflow** - Edit form complete
- ✅ **Delete Workflow** - Delete confirmation page complete

#### Activities
- ✅ **Activities List** (scoped to workflow) - List with phase grouping complete
- ✅ **Create Activity** - Create form with Markdown guidance complete
- ✅ **Activity Detail** - Detail view with rendered Markdown + Mermaid complete
- ✅ **Edit Activity** - Edit form complete
- ✅ **Delete Activity** - Delete confirmation page complete

---

### 🟢 Dashed Bold Green Border (Partial Implementation)
**Meaning**: Core functionality exists but missing some features

**Apply to these pages**:

#### Authentication
- 🟢 **Login** - Basic login works, missing "Remember me", OAuth
- 🟢 **Register** - Basic registration works, missing email verification flow
- 🟢 **Password Reset** - Basic reset works, missing advanced features

#### Dashboard  
- 🟢 **Dashboard/Home** - Basic dashboard exists but minimal functionality
  - Shows: Recent playbooks, quick actions
  - Missing: Activity feed, recent edits, statistics

---

### ⚪ Gray/Uncolored (Not Started)
**Meaning**: No implementation yet, page exists only in design

**Leave as-is for these pages**:

#### Not Implemented Entities
- ⚪ All Phase pages (Act 4) - **Phase implemented as string field, not separate entity**
- ⚪ All Artifact pages (Act 6)
- ⚪ All Role pages (Act 7)
- ⚪ All Howto pages (Act 8)

#### Not Implemented Features
- ⚪ PIPs (Playbook Improvement Proposals) - Act 9
- ⚪ Import/Export pages - Act 10 (only basic export exists)
- ⚪ Family Management - Act 11
- ⚪ Sync with Homebase - Act 12
- ⚪ Settings - Act 14
- ⚪ Error Recovery - Act 15
- ⚪ Onboarding flow - Act 0

---

## How to Apply in Draw.io

### Step 1: Open the File
```bash
# Navigate to the file
cd /Users/denispetelin/GitHub/mimir/docs/ux/2_dialogue-maps/
# Open with Draw.io desktop app or diagrams.net
open screen-flow.drawio
```

### Step 2: Select Pages/Shapes

For each page listed above, select the shape (rectangle/box) representing that page

### Step 3: Apply Formatting

#### For ✅ Bold Green Border (100% Complete):
1. Select the shape
2. Click "Format" panel (right sidebar)
3. Under "Style":
   - **Line color**: `#22c55e` (green)
   - **Line width**: `3` (bold)
   - **Line style**: Solid
4. (Optional) Add checkmark emoji "✅" to the label

#### For 🟢 Dashed Bold Green Border (Partial):
1. Select the shape
2. Click "Format" panel
3. Under "Style":
   - **Line color**: `#22c55e` (green)
   - **Line width**: `3` (bold)
   - **Line style**: Dashed
4. (Optional) Add gear emoji "⚙️" to the label

#### For ⚪ Not Started (keep as-is):
- Leave existing gray/default formatting
- No changes needed

---

## Example Before/After

### Before
```
[Playbook Detail]  ← Gray border, normal weight
```

### After (Complete)
```
[✅ Playbook Detail]  ← Bold green border, 3px width
```

### After (Partial)
```
[⚙️ Dashboard]  ← Dashed bold green border, 3px width
```

---

## Notes

### Why Manual Update?
- Draw.io files are XML-based but complex to edit programmatically
- Visual formatting is best done in the Draw.io GUI
- Preserves diagram layout and connections

### Alternative: Export and Recreate
If the diagram is simple, you could:
1. Export current diagram as PNG/SVG for reference
2. Create new diagram with proper color coding
3. Replace old file with new one

### Version Control
- Draw.io files are XML and git-friendly
- Changes will show in git diff
- Commit with message: `docs(ux): update screen flow with implementation status`

---

## Checklist

- [ ] Open `screen-flow.drawio` in Draw.io
- [ ] Apply ✅ bold green borders to 15 complete pages (Playbooks: 6, Workflows: 5, Activities: 5)  
- [ ] Apply 🟢 dashed green borders to 4 partial pages (Login, Register, Password Reset, Dashboard)
- [ ] Verify gray/uncolored pages remain unchanged (Phases, Artifacts, Roles, Howtos, PIPs, etc.)
- [ ] Save file
- [ ] Commit: `git add docs/ux/2_dialogue-maps/screen-flow.drawio`
- [ ] Commit message: `docs(ux): update screen flow with implementation status (15 complete, 4 partial)`

---

## Quick Reference Table

| Status | Border Color | Border Width | Border Style | Emoji | Count |
|--------|--------------|--------------|--------------|-------|-------|
| Complete | Green (#22c55e) | 3px | Solid | ✅ | 15 pages |
| Partial | Green (#22c55e) | 3px | Dashed | ⚙️ | 4 pages |
| Not Started | Gray (default) | 1px | Solid | - | Remaining |

---

## Questions?

If any pages are unclear or you need help identifying them in the diagram:
1. Check `docs/features/RECONCILIATION_REPORT.md` for full implementation details
2. Review URL patterns in `methodology/*_urls.py` files
3. Ask for clarification on specific pages
