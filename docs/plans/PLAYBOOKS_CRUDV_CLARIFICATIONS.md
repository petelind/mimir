# Playbooks CRUDV Implementation - Clarifications

## Overview
Implementing **89 scenarios** across 4 feature files:
- `playbooks-create.feature` (21 scenarios)
- `playbooks-view.feature` (24 scenarios)  
- `playbooks-edit.feature` (24 scenarios)
- `playbooks-delete.feature` (20 scenarios)

Excluded: `playbooks-list-find.feature` (will be implemented last per user request)

---

## Key Questions

### Q1: Models and NAV-06 Dependency
The NAV-06 (Global Search) implementation plan includes creating the Playbook model along with all 7 core entity models.

**Question**: Should we:
- **Option A**: Implement NAV-06 first (creates all models), then implement playbooks CRUDV (uses existing models)
- **Option B**: Implement playbooks CRUDV now (creates Playbook + minimal other models), then NAV-06 later
- **Option C**: Create models as part of playbooks implementation, accepting potential duplicate work with NAV-06

**Recommendation**: Option A - NAV-06 creates the foundation, playbooks CRUDV builds on top
A

---

### Q2: Existing Template Approach
Current templates (`templates/playbooks/`) use a **tabbed form approach**:
- `form.html` shows tabs: Basic Info | Classification | Metadata | Relationships
- `detail.html` shows basic detail view
- `list.html` shows card-based list

Feature files specify a **wizard approach** for creation:
- Step 1: Basic Information
- Step 2: Add Workflows  
- Step 3: Publishing Settings

**Question**: Should we:
- **Option A**: Replace existing templates entirely to match feature files exactly (wizard-based creation)
- **Option B**: Adapt existing templates to support wizard flow
- **Option C**: Keep existing templates as-is and adjust feature files

**Recommendation**: Option A - Match feature files exactly for consistency with specifications
A

---

### Q3: Workflow Integration
Multiple scenarios involve workflows (e.g., "Add first workflow" in PB-CREATE-10, viewing workflows in PB-VIEW-05). Workflows are separate entities managed in Act 3.

**Question**: For playbook creation/editing, should we:
- **Option A**: Implement minimal workflow stub (name + description only) for now
- **Option B**: Skip workflow-related scenarios entirely until Act 3 workflows are implemented
- **Option C**: Implement full workflow CRUD inline with playbooks

**Recommendation**: Option A - Minimal stub to unblock playbooks, full implementation in Act 3
A

---

### Q4: Family and Homebase Integration
Several scenarios reference "Family visibility" and "Homebase sync" (PB-CREATE-19, PB-EDIT-08, PB-DELETE-12).

**Question**: Should we:
- **Option A**: Implement stubs/placeholders for Family/Homebase features (not functional but UI present)
- **Option B**: Skip Family/Homebase scenarios entirely (mark as TODO for later)
- **Option C**: Implement full Family/Homebase integration now

**Recommendation**: Option B - Focus on core CRUDV, defer Family/Homebase to later milestone
B
---

### Q5: Export/Import Features
PB-VIEW-18 includes "Export playbook to JSON", and PB-CREATE includes import references.

**Question**: Should we:
- **Option A**: Implement full JSON export/import now
- **Option B**: Implement export only (simpler), defer import
- **Option C**: Defer both to separate feature

**Recommendation**: Option B - Export only using Django serializers, import deferred
B
---

### Q6: Version History and PIPs
PB-VIEW-08 through PB-VIEW-11 involve version history and PIPs (Process Improvement Proposals).

**Question**: Should we:
- **Option A**: Implement full version history + PIP system now
- **Option B**: Show single version (v1.0) only, defer versioning
- **Option C**: Implement version display only (no PIP workflow)

**Recommendation**: Option B - Single version for MVP, full versioning later
A - but I dont think we need PIP, as versions are not PIP-dependent.
Version are integers, not semantic-versioned.
---

### Q7: Auto-save Feature
PB-EDIT-24 mentions optional auto-save draft feature.

**Question**: Should we:
- **Option A**: Implement auto-save now
- **Option B**: Skip entirely (marked as optional in scenario)
- **Option C**: Implement but disabled by default

**Recommendation**: Option B - Skip optional feature for MVP
B
---

### Q8: Duplicate Playbook Feature
PB-VIEW-19 includes duplicating playbooks.

**Question**: Should we:
- **Option A**: Implement full duplication now
- **Option B**: Defer to separate enhancement
- **Option C**: Implement basic copy (without deep cloning workflows/activities)

**Recommendation**: Option C - Basic copy (metadata only), deep clone later
C. Mark the feature that we have "shallow copy only" now
---

### Q9: GitHub Issues Strategy
No existing GitHub issues for playbook CRUDV exist.

**Question**: Should we:
- **Option A**: Create one umbrella issue for entire playbooks CRUDV implementation
- **Option B**: Create separate issues for Create, View, Edit, Delete (4 issues)
- **Option C**: Create issues per feature file scenario (89 issues!)

**Recommendation**: Option B - 4 issues (one per operation), easier to track and close
B

---

### Q10: Implementation Order
Given the dependencies and scope:

**Question**: What order should we implement?
- **Option A**: Create → View → Edit → Delete (natural CRUD flow)
- **Option B**: View → Create → Edit → Delete (view first for testing)
- **Option C**: All models → All views → All templates → All tests (layer-by-layer)

**Recommendation**: Option A - CRUD flow, but with "View" early for testing created playbooks
A

**Refined Order**:
1. Models + Admin (foundation)
2. Create (can create test data)
3. View (can see what we created)
4. Edit (can modify)  
5. Delete (cleanup)

---

### Q11: Test Coverage Strategy
89 scenarios require significant test coverage.

**Question**: Should we:
- **Option A**: Implement all scenarios with full test coverage from start
- **Option B**: Implement core scenarios first (happy paths), edge cases later
- **Option C**: Implement features first, backfill tests after

**Recommendation**: Option B - Core scenarios first (~40-50 tests), edge cases in refinement pass
A.
WE ARE TEST DRIVEN, CANNOT SKIP.

**Core Scenarios to Prioritize**:
- CREATE: Steps 1-3 happy path, basic validation
- VIEW: Header, overview tab, basic navigation
- EDIT: Basic field updates, validation
- DELETE: Confirmation modal, successful deletion

---

### Q12: Scope Reduction Proposal
To make this more manageable, consider phased approach:

**Phase 1 (MVP - This Implementation)**:
- ✅ Playbook model + migrations
- ✅ Admin registration
- ✅ Create: Wizard steps 1-3 (without workflow integration)
- ✅ View: Overview tab only (defer History, Settings tabs)
- ✅ Edit: Basic metadata editing
- ✅ Delete: Confirmation modal

**Phase 2 (Enhancement - Separate PR)**:
- Workflow integration in create/edit
- Full view tabs (History, Settings)
- Family/Homebase integration
- Version history + PIPs
- Export/Import
- Advanced features

**Question**: Accept this phased approach?
NO.
DO:
- Playbook model + migrations
- Admin registration
- Create: Wizard steps 1-3 (without workflow integration)
- View: Overview tab only (defer History, Settings tabs)
- Edit: Basic metadata editing
- Delete: Confirmation modal
- Versions, but not PIPs
- Full view tabs (History, Settings)
- Export/Import


## Next Steps

Please review and answer:
1. Do you accept the phased approach (Phase 1 MVP scope)?
2. Any questions where you prefer a different option?
3. Should I proceed with implementing NAV-06 first, or start directly on playbooks?
4. Any additional clarifications needed before I create the full implementation plan?

Once clarified, I'll create the comprehensive implementation plan with atomic, test-first steps.
