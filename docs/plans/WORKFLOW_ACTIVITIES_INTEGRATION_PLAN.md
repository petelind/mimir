# Workflow-Activities Integration Implementation Plan

## Overview
Integrate activities display and management into the Workflow detail page, completing the workflow → activities user flow.

**Branch**: `feature/activities-list` (current)  
**Feature Files**: 
- `docs/features/act-3-workflows/workflows-view.feature` (WF-VIEW-03, 04, 05, 10)
- `docs/features/act-5-activities/activities-list-find.feature` (already implemented)

**Status**: Activities CRUDV is fully implemented (44/44 tests passing). Need to wire activities into workflow detail view.

---

## Current State Assessment

### ✅ **Already Implemented**

**Backend:**
- Activity model with all fields (name, description, phase, order, status, has_dependencies)
- ActivityService with full CRUD operations
- Activity views: list, create, detail, edit, delete
- Activity URLs scoped to workflow: `/playbooks/<pk>/workflows/<pk>/activities/`
- Global activities list view
- Workflow model with helper methods

**Frontend:**
- All activity templates (list, create, detail, edit, delete, global_list)
- Activities wired to navbar
- Workflow detail template exists but has **placeholder** for activities (line 59-67)

**Tests:**
- 44 integration tests for activities (100% passing)
  - LIST: 9/9 ✓
  - CREATE: 8/8 ✓
  - VIEW: 8/8 ✓
  - EDIT: 11/11 ✓
  - DELETE: 8/8 ✓

### ❌ **Missing Implementation**

**From `workflows-view.feature`:**
- **WF-VIEW-03**: Display activities list in workflow detail (currently placeholder)
- **WF-VIEW-04**: Group activities by phase if phases exist
- **WF-VIEW-05**: Navigate to activity detail from workflow page
- **WF-VIEW-10**: "Add Activity" button for editable workflows

**Reusable Components:**
- Activity list display logic exists in `templates/activities/list.html`
- Phase grouping logic exists in ActivityService
- Permission checks exist in workflow and activity views

---

## Missing Scenarios Analysis

### Scenario WF-VIEW-03: View activities list
```gherkin
Given Maria is on the workflow detail page
Then she sees "Activities" section
And she sees all 8 activities in order
And each activity shows: Name, Description, Dependencies, Status
```
**User Requirement**: Display as **Graphviz flow diagram** (not table/cards)
- **Phase 1 (Now)**: Activity flow with clickable nodes and arrows showing sequence
- **Phase 2 (Later)**: Enhanced graph with:
  - Goals at top (activities contribute to)
  - Input artifacts on left
  - Output artifacts on right
  - Activities in center flow

**Needs:**
- Create `ActivityGraphService` with `generate_activities_graph()` method
- Fetch activities in `workflow_detail` view
- Generate SVG using Graphviz
- Replace placeholder in template with SVG graph
- Make activity nodes clickable (link to detail)
- Show sequence with arrows (based on `order` field)
- Empty state when no activities

### Scenario WF-VIEW-04: View phases
```gherkin
Given the workflow has 2 phases
When Maria views the workflow
Then she sees "Phases" section showing 2 phases
And activities are grouped under their respective phases
```
**Visual Approach:**
- Use Graphviz **subgraphs** for phase grouping
- Each phase = cluster with distinct background color
- Activities within phase flow left-to-right or top-to-bottom
- Cross-phase dependencies shown with inter-cluster edges

**Needs:**
- Check if workflow has phases
- If yes: use `cluster_<phase_name>` subgraphs
- If no: simple linear flow
- Phase styling: border, background color, phase name label

### Scenario WF-VIEW-05: Navigate to activity detail
```gherkin
Given Maria is viewing the workflow
When she clicks on an activity
Then she navigates to FOB-ACTIVITIES-VIEW_ACTIVITY-1
```
**Graphviz Approach:**
- Use `href` attribute on Graphviz nodes for clickability
- SVG nodes become HTML links automatically
- Link to `activity_detail` with correct PKs
- Nodes show visual hover effect (CSS)

**Needs:**
- Set `href` on each node: `/playbooks/{playbook_pk}/workflows/{workflow_pk}/activities/{activity_pk}/`
- Set `target='_top'` for full page navigation
- Add cursor pointer CSS for SVG links

### Scenario WF-VIEW-10: Add activity button
```gherkin
Given Maria is viewing her own playbook's workflow
Then she sees [Add Activity] button
When she clicks it
Then activity creation form appears
```
**Needs:**
- Position "Add Activity" button above/below graph
- Check `can_edit` permission in template
- Show button if true
- Link to `activity_create` with workflow context
- Button with Font Awesome icon and tooltip

---

## Implementation Plan

### Step 1: Create ActivityGraphService
**File**: `methodology/services/activity_graph_service.py` (NEW)

- [ ] Read `.windsurf/rules/do-short-concise-methods.md` before implementing
- [ ] Read SAO.md Pattern 2: Graph Visualization with Graphviz (lines 647-746)
- [ ] Create `ActivityGraphService` class
- [ ] Implement `generate_activities_graph(workflow, playbook)` method:
  - Create `graphviz.Digraph` instance
  - Set graph attributes: `rankdir='TB'` (top to bottom)
  - Check if activities have phases
  - **If phases exist**: Use `subgraph` with `cluster_<phase>` names
    - Set cluster attributes: label, style, color
    - Add activity nodes within clusters
  - **If no phases**: Add activity nodes directly
  - Add node for each activity:
    - `node_id` = `f"activity_{activity.pk}"`
    - `label` = `f"{activity.name}\n{activity.get_status_display()}"`
    - `href` = reverse URL to activity_detail with all PKs
    - `target` = `'_top'`
    - Node styling based on status (colors)
    - Add dependency indicator if `has_dependencies`
  - Add edges between activities (based on `order` field)
  - Generate SVG: `dot.pipe(format='svg').decode('utf-8')`
  - Return SVG string
- [ ] Handle empty activities (return placeholder SVG or None)
- [ ] Add comprehensive logging
- [ ] Document all parameters with examples

**Expected Signature:**
```python
def generate_activities_graph(self, workflow, playbook):
    """
    Generate Graphviz flow diagram of activities.
    
    :param workflow: Workflow instance
    :param playbook: Playbook instance (for URL generation)
    :return: SVG markup as string or None if no activities
    :raises: GraphvizError if graph generation fails
    """
```

### Step 2: Update Backend - Workflow Detail View
**File**: `methodology/workflow_views.py`

- [ ] Read `.windsurf/rules/do-short-concise-methods.md` before implementing
- [ ] Import `ActivityGraphService`
- [ ] Update `workflow_detail()` view:
  - Fetch activities: `ActivityService.get_activities_for_workflow(workflow.pk)`
  - Get activity count
  - Generate SVG graph:
    ```python
    graph_service = ActivityGraphService()
    activities_svg = graph_service.generate_activities_graph(workflow, playbook)
    ```
  - Add to context: `activities_svg`, `activity_count`, `has_activities`
- [ ] Add logging for graph generation
- [ ] Handle graph generation errors gracefully
- [ ] Document parameters and return values

**Expected Context:**
```python
context = {
    'playbook': playbook,
    'workflow': workflow,
    'can_edit': workflow.can_edit(request.user),
    'activities_svg': activities_svg,  # SVG string or None
    'activity_count': activity_count,  # Integer
    'has_activities': activity_count > 0,  # Boolean
}
```

### Step 3: Update Frontend - Workflow Detail Template
**File**: `templates/workflows/detail.html`

- [ ] Read `.windsurf/rules/tooltips.md` before implementing
- [ ] Read `.windsurf/rules/do-semantic-versioning-on-ui-elements.md`
- [ ] Replace activities placeholder (lines 59-67) with:
  - **Activities Section Header**
    - Title: "Activities Flow ({{ activity_count }})"
    - "Add Activity" button if `can_edit` (with tooltip)
    - Link to `activity_create` with `playbook_pk` and `workflow_pk`
    - Positioned above graph
  - **Graphviz SVG Display** (if `has_activities`)
    - Container div: `<div class="graph-container" data-testid="activities-graph">`
    - Render SVG: `{{ activities_svg|safe }}`
    - Add CSS for responsive SVG
  - **Empty State** (if `activity_count == 0`)
    - "No activities yet" message with icon
    - "Create First Activity" button (if `can_edit`)
    - data-testid="empty-activities-state"
- [ ] Add CSS styles:
  ```css
  .graph-container svg {
      max-width: 100%;
      height: auto;
      border: 1px solid #dee2e6;
      border-radius: 4px;
      background: white;
  }
  .graph-container svg a {
      cursor: pointer;
  }
  .graph-container svg a:hover {
      opacity: 0.8;
  }
  ```
- [ ] Add semantic `data-testid` attributes:
  - `activities-section`
  - `add-activity-btn`
  - `activities-graph`
  - `empty-activities-state`
  - `create-first-activity-btn`
- [ ] Use Bootstrap 5 styling for header/buttons
- [ ] Font Awesome Pro icon for "Add Activity" button
- [ ] Tooltip on "Add Activity" button

### Step 4: Unit Tests - ActivityGraphService
**File**: `tests/unit/test_activity_graph_service.py` (NEW)

- [ ] Read `.windsurf/rules/do-test-first.md` before implementing
- [ ] Read `.windsurf/rules/pytest.md`
- [ ] Create test class `TestActivityGraphService`
- [ ] Setup fixtures: workflow, playbook, activities
- [ ] **Test**: Generate graph with no activities
  - Should return None or empty state message
- [ ] **Test**: Generate graph with simple linear flow (no phases)
  - Verify SVG contains activity nodes
  - Check edges connect activities in order
  - Verify href attributes present
- [ ] **Test**: Generate graph with phases
  - Verify subgraph clusters created
  - Check activities grouped by phase
  - Verify cluster labels
- [ ] **Test**: Node styling based on status
  - completed = green
  - in_progress = blue
  - blocked = red
  - not_started = gray
- [ ] **Test**: Clickable nodes (href attributes)
  - Verify href points to activity_detail
  - Check target='_top' present
- [ ] **Test**: Dependencies visualization
  - Activities with has_dependencies=True show indicator

**Expected: 6-8 unit tests**

### Step 5: Integration Tests - Workflow Detail with Activities
**File**: `tests/integration/test_workflow_detail_activities.py` (NEW)

- [ ] Read `.windsurf/rules/do-test-first.md` before implementing
- [ ] Read `.windsurf/rules/pytest.md`
- [ ] Read `.windsurf/rules/do-not-mock-in-integration-tests.md`
- [ ] Create test class `TestWorkflowDetailActivities`
- [ ] Setup fixture: user, playbook, workflow, activities
- [ ] **Test WF-VIEW-03**: Display activities list
  - Navigate to workflow detail
  - Verify activities section exists
  - Check all activities displayed
  - Verify name, description, status, dependencies shown
- [ ] **Test WF-VIEW-04-A**: Phase grouping (with phases)
  - Create activities with phases
  - Navigate to workflow detail
  - Verify phase groups displayed
  - Check activities under correct phases
  - Verify phase count badges
- [ ] **Test WF-VIEW-04-B**: Flat list (no phases)
  - Create activities without phases
  - Navigate to workflow detail
  - Verify flat list displayed
  - Check ordering by sequence
- [ ] **Test WF-VIEW-05**: Navigate to activity detail
  - Create activity
  - Navigate to workflow detail
  - Click activity view button
  - Verify redirected to activity detail
  - Check URL contains correct PKs
- [ ] **Test WF-VIEW-10-A**: Add activity button (owner)
  - Owner viewing own workflow
  - Verify "Add Activity" button exists
  - Check button links to activity_create
  - Verify tooltip present
- [ ] **Test WF-VIEW-10-B**: No add button (non-owner)
  - Different user viewing workflow
  - Verify "Add Activity" button not shown
- [ ] **Test WF-VIEW-XX**: Empty state
  - Workflow with zero activities
  - Verify empty state message
  - Check "Add First Activity" button (if owner)
- [ ] **Test WF-VIEW-XX**: Activity actions buttons
  - Verify View/Edit buttons present
  - Check correct URLs
  - Verify tooltips
  
**Expected: 8-10 new integration tests, all passing**

### Step 6: Commit and Update
- [ ] Read `.windsurf/rules/do-follow-commit-convention.md`
- [ ] Run all tests to verify nothing broken:
  ```bash
  pytest tests/integration/test_workflow_detail_activities.py -v
  pytest tests/integration/test_activity_*.py -v
  ```
- [ ] Commit with message following Angular convention:
  ```
  feat(workflows): add Graphviz activities flow diagram to workflow detail (WF-VIEW-03,04,05,10)
  
  Services (activity_graph_service.py):
  - NEW: ActivityGraphService for Graphviz SVG generation
  - generate_activities_graph() creates flow diagram
  - Phase grouping using Graphviz subgraph clusters
  - Clickable nodes linking to activity detail
  - Status-based node coloring
  - Sequential arrows between activities
  
  Backend (workflow_views.py):
  - Updated workflow_detail view to generate SVG graph
  - Fetch activities and pass to graph service
  - Handle graph generation errors gracefully
  - Added activity count to context
  
  Frontend (detail.html):
  - Replaced activities placeholder with Graphviz SVG
  - Responsive SVG container with styling
  - Add Activity button for owners above graph
  - Empty state with "Create First Activity" button
  - CSS for SVG hover effects and clickability
  - All semantic data-testid attributes
  
  Tests:
  - Unit tests (test_activity_graph_service.py): 6-8 tests
    * Graph generation with/without phases
    * Node styling by status
    * Clickable href attributes
    * Empty activities handling
  - Integration tests (test_workflow_detail_activities.py): 8-10 tests
    * SVG display in workflow detail
    * Phase grouping visualization
    * Clickable nodes navigation
    * Add activity button permissions
    * Empty state display
  
  Visual flow diagram replaces table/card display
  Phase 2 (future): Goals, input/output artifacts layout
  
  All tests passing: XX/XX ✓
  
  Refs: workflows-view.feature WF-VIEW-03, WF-VIEW-04, WF-VIEW-05, WF-VIEW-10
  ```
- [ ] Update this implementation plan status
- [ ] Push to branch

### Step 5: Final Validation
- [ ] Read `.windsurf/rules/do-continuous-testing.md`
- [ ] Run full test suite:
  ```bash
  pytest tests/ -v --tb=short
  ```
- [ ] Verify all activity tests still pass (44/44)
- [ ] Verify new workflow-activities tests pass (8-10/8-10)
- [ ] Manual smoke test:
  - Start dev server: `python manage.py runserver`
  - Navigate to a workflow detail page
  - Verify activities displayed correctly
  - Test "Add Activity" button
  - Test phase grouping
  - Test activity navigation
- [ ] Check logs for any errors

### Step 6: Update Feature Files and Documentation
- [ ] Mark scenarios as implemented in `workflows-view.feature`:
  - WF-VIEW-03: ✓ Implemented
  - WF-VIEW-04: ✓ Implemented
  - WF-VIEW-05: ✓ Implemented
  - WF-VIEW-10: ✓ Implemented
- [ ] Update `WORKFLOW_ACTIVITIES_INTEGRATION_PLAN.md` with completion status
- [ ] Add notes about any deferred items (if any)

### Step 7: GitHub Issue Management
- [ ] Read `.windsurf/rules/do-github-issues.md`
- [ ] Check for existing GitHub issue for workflow-activities integration
- [ ] If exists: Update with implementation status and test results
- [ ] If not exists: Create issue documenting what was implemented
- [ ] Link commits to issue
- [ ] Add labels: `feature`, `workflows`, `activities`, `integration`

---

## Architecture Alignment

### Repository Pattern (from SAO.md)
- ✓ Using ActivityService for data access (storage-agnostic)
- ✓ No direct ORM queries in views
- ✓ Services handle business logic

### Django + HTMX UI (from SAO.md)
- ✓ Server-rendered templates (no client-side framework)
- ✓ Bootstrap 5 for styling
- ✓ Semantic test attributes for Django test client
- Future: HTMX for dynamic updates (not in this iteration)

### Two-Part Architecture (FOB focus)
- ✓ This is FOB-only work (Web UI)
- No MCP changes needed (read-only, activities already queryable)
- No HOMEBASE coordination needed

---

## Reusable Components

From existing implementation:
1. **Activity list template structure** (`templates/activities/list.html`)
   - Phase grouping logic
   - Status badges
   - Action buttons with tooltips
   - Can be adapted/simplified for workflow detail inline display

2. **ActivityService methods** (`methodology/services/activity_service.py`)
   - `get_activities_for_workflow(workflow_id)` - ✓ exists
   - `get_activities_grouped_by_phase(workflow_id)` - ✓ exists

3. **Permission checks**
   - `workflow.can_edit(user)` - ✓ exists
   - Used consistently in templates

---

## Success Criteria

**Definition of Done:**
- [ ] All WF-VIEW scenarios (03, 04, 05, 10) implemented
- [ ] 8-10 new integration tests written and passing (100%)
- [ ] All existing tests still pass (44 activity + X playbook/workflow tests)
- [ ] Activities displayed in workflow detail page with proper styling
- [ ] Phase grouping works correctly
- [ ] Add Activity button visible to owners
- [ ] Activity navigation works
- [ ] Empty state handled gracefully
- [ ] All semantic data-testid attributes present
- [ ] Code committed with proper Angular convention message
- [ ] Feature file scenarios marked as implemented
- [ ] GitHub issue updated

---

## Risks and Mitigations

### Risk 1: Template Complexity
**Risk**: Workflow detail template becoming too large/complex with activities section  
**Mitigation**: Consider extracting activities section to partial template `_activities_section.html` if > 50 lines

### Risk 2: Query Performance
**Risk**: N+1 queries when fetching activities with workflow/playbook context  
**Mitigation**: Already using `select_related()` in ActivityService methods

### Risk 3: Test Flakiness
**Risk**: Integration tests might be flaky with complex DOM assertions  
**Mitigation**: Using semantic data-testid attributes for stable selectors

---

## Deferred Items

**Not in this iteration (Phase 1):**
1. **WF-VIEW-08**: Duplicate workflow - more complex, needs planning
2. **HTMX Dynamic Updates**: Server-side rendering first, HTMX later for better UX
3. **Drag-Drop Reordering**: Covered in activities-list-find.feature ACT-LIST-09 (deferred)
4. **Activity Dependencies M2M**: Currently boolean flag, full M2M relationships future work
5. **Inline Activity Editing**: Currently navigate to edit page, inline editing future enhancement

**Phase 2 - Enhanced Graph Layout (Future):**
- **Goals at Top**: Activities contribute to goals (top of graph)
- **Input Artifacts (Left)**: Artifacts required by activities
- **Output Artifacts (Right)**: Artifacts produced by activities
- **Center Flow**: Activities in execution sequence
- **Requires**: Goal model, Artifact model with input/output relationships
- **Graph Layout**: More complex multi-layer Graphviz layout
- **User Story Update**: Document Phase 2 requirements in user_journey.md

---

## Estimated Scope

**Implementation:**
- Backend: 1 view update (~20-30 lines)
- Frontend: 1 template section (~100-150 lines replacing placeholder)
- Tests: 8-10 integration tests (~400-500 lines)

**Testing:**
- Integration tests: 8-10 scenarios
- Manual smoke testing: ~15 minutes

**Total**: Small to medium feature, incremental addition to existing work

---

## Notes

- This work builds directly on the completed activities CRUDV implementation
- No new models or services needed
- Primarily frontend integration work
- Follows same patterns as playbook → workflows integration
- Can reuse significant portions of activities list template logic
