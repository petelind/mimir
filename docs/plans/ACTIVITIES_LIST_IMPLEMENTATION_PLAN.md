# Activities LIST Implementation Plan

**Feature**: FOB-ACTIVITIES-LIST+FIND-1 (LIST scenarios only)  
**Branch**: `feature/activities-list`  
**Issue**: TBD  
**Scope**: ACT-LIST-01 through ACT-LIST-13 (excludes FIND/search - deferred)

---

## 0. Planning Mode - Assessment

### Current State Analysis

**Existing Models:**
- ✅ `Playbook` model (complete)
- ✅ `Workflow` model (complete with order, updated_at, can_edit)
- ❌ `Activity` model **DOES NOT EXIST**
- ❌ `Phase` model **DOES NOT EXIST**

**Architecture Patterns (from SAO.md):**
- Repository pattern (storage abstraction)
- Version management (all entities versioned)
- Services layer (business logic)
- HTMX + Django templates (server-rendered UI)
- Test-first approach (no mocking in integration tests)

**Reusable Components:**
- Workflow CRUDV patterns (can be template for Activity CRUDV)
- WorkflowService pattern (can create ActivityService)
- URL scoping pattern (activities under workflows)
- Bootstrap + FA icons + tooltips UI pattern
- Integration test patterns

**What Needs to be Built:**
1. ✅ Activity model (NEW)
2. ✅ Phase model (NEW) - optional, for grouping
3. ✅ ActivityService (NEW) - business logic
4. ✅ Activity views (NEW) - list, create, view, edit, delete
5. ✅ Activity templates (NEW) - list, detail, forms
6. ✅ URL patterns (NEW) - scoped to workflow
7. ✅ Tests (NEW) - model, service, integration

---

## 1. Clarification Questions

### Q1: Phase Model - Implementation Priority
**Question**: The feature file mentions phases (ACT-LIST-04, ACT-LIST-07). Should we:
- A) Implement Phase model now (full phase support)
- B) Add phase field to Activity but defer Phase model (simple grouping)
- C) Skip phases entirely in this iteration

**Recommendation**: Option B - Add `phase` CharField to Activity for simple grouping, defer full Phase model to future.

### Q2: Dependencies - Complexity Level
**Question**: ACT-LIST-08 mentions "Has Dependencies" filter. Dependencies could be:
- Simple: Boolean flag `has_dependencies` (quick to implement)
- Complex: Many-to-many relationship between activities (predecessor/successor)

**Recommendation**: Start with simple boolean flag, add M2M relationship in Activities EDIT feature.

### Q3: Reordering - Drag-Drop vs Manual
**Question**: ACT-LIST-09 mentions drag-and-drop reordering. Should we:
- A) Full drag-drop with JavaScript (complex)
- B) Manual order field editing (simple, consistent with Workflow pattern)
- C) Defer reordering to later

**Recommendation**: Option B - Use `order` field like Workflows, defer drag-drop UI.

### Q4: Activity Status Field
**Question**: ACT-LIST-02 mentions "Status" column. What statuses?
- Proposal: `not_started`, `in_progress`, `completed`, `blocked`

### Q5: Scope of ACT-LIST vs ACT-CREATE/EDIT/DELETE
**Question**: Should LIST implementation include:
- Navigation to create/edit/delete (links only)
- Or stub views for those operations

**Recommendation**: Implement full CREATE view (like Workflow), stub EDIT/DELETE for now.

---

## 2. Implementation Plan - Step by Step

### STEP 0: Reset and Setup ✅
- [x] Checkout feature/activities-list branch
- [ ] Create issue for Activities LIST
- [ ] Update this plan based on user clarifications

### STEP 1: Backend - Activity Model

**File**: `methodology/models/activity.py`

**Implementation**:
```python
class Activity(models.Model):
    """Activity within a workflow - represents a single task/step."""
    
    # Relationships
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='activities')
    
    # Core fields
    name = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=1)
    
    # Organization
    phase = models.CharField(max_length=100, blank=True, null=True)  # Simple grouping
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=[
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('blocked', 'Blocked'),
        ],
        default='not_started'
    )
    
    # Dependencies (simplified - boolean for now)
    has_dependencies = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['workflow', 'order', 'name']
        unique_together = [['workflow', 'name']]  # Unique names within workflow
    
    def __str__(self):
        return f"{self.name} (#{self.order})"
    
    def is_owned_by(self, user):
        """Check if user owns the parent workflow's playbook."""
        return self.workflow.playbook.is_owned_by(user)
    
    def can_edit(self, user):
        """Check if user can edit this activity."""
        return self.workflow.can_edit(user)
    
    def get_phase_display_name(self):
        """Get formatted phase name or default."""
        return self.phase if self.phase else "Unassigned"
```

**Tests to Create** (`tests/unit/test_activity_model.py`):
- test_create_activity
- test_activity_defaults
- test_activity_str_representation
- test_unique_constraint_per_workflow
- test_ordering_by_workflow_order_name
- test_is_owned_by_owner
- test_is_owned_by_non_owner
- test_can_edit_owner_owned_playbook
- test_can_edit_downloaded_playbook
- test_cascade_delete_with_workflow
- test_updated_at_changes
- test_get_phase_display_name

**Actions**:
- [ ] Create `methodology/models/activity.py`
- [ ] Update `methodology/models/__init__.py` to include Activity
- [ ] Create migration: `python manage.py makemigrations`
- [ ] Run migration: `python manage.py migrate`
- [ ] Register Activity in `methodology/admin.py`
- [ ] Write unit tests (12 tests)
- [ ] Run tests: `pytest tests/unit/test_activity_model.py -v`
- [ ] Commit: "feat(activities): add Activity model with order, status, phase fields"
- [ ] Update plan status

### STEP 2: Backend - ActivityService

**File**: `methodology/services/activity_service.py`

**Implementation** (following WorkflowService pattern):
```python
class ActivityService:
    """Service class for activity operations."""
    
    @staticmethod
    def create_activity(workflow, name, description='', phase=None, order=None):
        """Create activity with validation and auto-order."""
        # Validate name
        # Check for duplicate name in workflow
        # Auto-assign order if not provided
        # Create and return activity
        
    @staticmethod
    def get_activity(activity_id):
        """Get activity by ID."""
        
    @staticmethod
    def get_activities_for_workflow(workflow):
        """Get all activities in a workflow, ordered."""
        
    @staticmethod
    def get_activities_grouped_by_phase(workflow):
        """Get activities grouped by phase."""
        
    @staticmethod
    def update_activity(activity_id, **kwargs):
        """Update activity fields."""
        
    @staticmethod
    def delete_activity(activity_id):
        """Delete activity."""
        
    @staticmethod
    def duplicate_activity(activity_id, new_name=None):
        """Create a copy of an activity."""
```

**Tests to Create** (`tests/unit/test_activity_service.py`):
- test_create_activity_with_all_fields
- test_create_activity_auto_order
- test_create_activity_duplicate_name_fails
- test_get_activity
- test_get_activities_for_workflow
- test_get_activities_grouped_by_phase
- test_update_activity_name
- test_update_activity_status
- test_update_activity_order
- test_update_activity_duplicate_name_fails
- test_delete_activity
- test_duplicate_activity

**Actions**:
- [ ] Re-read `.windsurf/rules/do-skeletons-first.md`
- [ ] Create skeleton for `ActivityService`
- [ ] Write unit tests (12 tests)
- [ ] Implement ActivityService methods
- [ ] Run tests: `pytest tests/unit/test_activity_service.py -v`
- [ ] Commit: "feat(activities): implement ActivityService with CRUD operations"
- [ ] Update plan status

### STEP 3: Backend - Activity Views (List + Create)

**File**: `methodology/activity_views.py`

**Views to Implement**:

```python
@login_required
def activity_list(request, playbook_pk, workflow_pk):
    """List all activities in a workflow."""
    # Get workflow (with playbook check)
    # Get activities grouped by phase (if any)
    # Check edit permissions
    # Render list template
    
@login_required
def activity_create(request, playbook_pk, workflow_pk):
    """Create new activity in workflow."""
    # GET: Show form
    # POST: Validate and create activity
    # Redirect to list

# Stubs for now (implement in future features)
@login_required
def activity_detail(request, playbook_pk, workflow_pk, activity_pk):
    """View activity details (STUB)."""
    messages.info(request, 'View functionality coming soon.')
    return redirect('activity_list', playbook_pk=playbook_pk, workflow_pk=workflow_pk)

@login_required
def activity_edit(request, playbook_pk, workflow_pk, activity_pk):
    """Edit activity (STUB)."""
    messages.info(request, 'Edit functionality coming soon.')
    return redirect('activity_list', playbook_pk=playbook_pk, workflow_pk=workflow_pk)

@login_required
def activity_delete(request, playbook_pk, workflow_pk, activity_pk):
    """Delete activity (STUB)."""
    messages.info(request, 'Delete functionality coming soon.')
    return redirect('activity_list', playbook_pk=playbook_pk, workflow_pk=workflow_pk)
```

**Actions**:
- [ ] Re-read `.windsurf/rules/do-skeletons-first.md`
- [ ] Create `methodology/activity_views.py`
- [ ] Implement `activity_list` view
- [ ] Implement `activity_create` view
- [ ] Add stubs for detail/edit/delete
- [ ] Commit: "feat(activities): implement list and create views + stubs"
- [ ] Update plan status

### STEP 4: Backend - URL Patterns

**File**: `methodology/activity_urls.py` (NEW)

**URL Structure** (scoped to workflow):
```python
# /playbooks/<playbook_pk>/workflows/<workflow_pk>/activities/
urlpatterns = [
    path('', activity_list, name='activity_list'),
    path('create/', activity_create, name='activity_create'),
    path('<int:activity_pk>/', activity_detail, name='activity_detail'),
    path('<int:activity_pk>/edit/', activity_edit, name='activity_edit'),
    path('<int:activity_pk>/delete/', activity_delete, name='activity_delete'),
]
```

**Actions**:
- [ ] Create `methodology/activity_urls.py`
- [ ] Update `mimir/urls.py` to include activity URLs
- [ ] Test URL resolution manually
- [ ] Commit: "feat(activities): add URL patterns scoped to workflow"
- [ ] Update plan status

### STEP 5: Frontend - Activity List Template

**File**: `templates/activities/list.html`

**Features**:
- Breadcrumbs: Playbooks > [Playbook] > Workflows > [Workflow] > Activities
- Header with activity count
- Create Activity button (if can_edit)
- Activities grouped by phase (collapsible sections)
- OR flat list if no phases
- Activity table: Name, Description, Phase, Status, Order, Actions
- Empty state with "Create First Activity" button
- Font Awesome icons + Bootstrap tooltips
- Semantic `data-testid` attributes

**Actions**:
- [ ] Re-read `.windsurf/rules/tooltips.md`
- [ ] Create `templates/activities/list.html`
- [ ] Add breadcrumb navigation
- [ ] Implement grouped-by-phase view
- [ ] Implement flat list view (no phases)
- [ ] Add action buttons with icons + tooltips
- [ ] Add empty state
- [ ] Commit: "feat(activities): create list template with phase grouping"
- [ ] Update plan status

### STEP 6: Frontend - Activity Create Template

**File**: `templates/activities/create.html`

**Form Fields**:
- Name (required, max 200)
- Description (textarea, required)
- Phase (optional, text input)
- Order (number, optional - auto-assigned if empty)
- Status (dropdown, default: not_started)
- Has Dependencies (checkbox)

**Actions**:
- [ ] Create `templates/activities/create.html`
- [ ] Add form with all fields
- [ ] Add validation hints
- [ ] Add Cancel/Save buttons with icons + tooltips
- [ ] Commit: "feat(activities): create form template"
- [ ] Update plan status

### STEP 7: Testing - Integration Tests for LIST

**File**: `tests/integration/test_activity_list.py`

**Scenarios to Test** (based on feature file):
- test_act_list_01_navigate_from_workflow
- test_act_list_02_view_activities_table
- test_act_list_03_navigate_to_create
- test_act_list_04_view_by_phase_grouping
- test_act_list_05_view_flat_list_no_phases
- test_act_list_10_navigate_to_view_activity (stub)
- test_act_list_11_navigate_to_edit_activity (stub)
- test_act_list_12_delete_activity_button (stub)
- test_act_list_13_empty_state_display

**Deferred for FIND feature:**
- ACT-LIST-06: Search by name
- ACT-LIST-07: Filter by phase
- ACT-LIST-08: Filter by dependencies
- ACT-LIST-09: Reorder activities (drag-drop)

**Actions**:
- [ ] Re-read `.windsurf/rules/do-test-first.md`
- [ ] Re-read `.windsurf/rules/do-not-mock-in-integration-tests.md`
- [ ] Create `tests/integration/test_activity_list.py`
- [ ] Write 9 integration tests
- [ ] Run tests: `pytest tests/integration/test_activity_list.py -v`
- [ ] Fix any failing tests
- [ ] Commit: "test(activities): add integration tests for LIST operation"
- [ ] Update plan status

### STEP 8: Testing - Integration Tests for CREATE

**File**: `tests/integration/test_activity_create.py`

**Scenarios to Test**:
- test_act_create_01_open_create_form
- test_act_create_02_create_with_required_fields
- test_act_create_03_validate_required_name
- test_act_create_04_duplicate_name_validation
- test_act_create_05_auto_order_assignment
- test_act_create_06_create_with_phase
- test_act_create_07_create_with_status
- test_act_create_08_cancel_redirects_to_list

**Actions**:
- [ ] Create `tests/integration/test_activity_create.py`
- [ ] Write 8 integration tests
- [ ] Run tests: `pytest tests/integration/test_activity_create.py -v`
- [ ] Fix any failing tests
- [ ] Commit: "test(activities): add integration tests for CREATE operation"
- [ ] Update plan status

### STEP 9: Integration - Wire Activities to Workflow Detail

**File**: `templates/workflows/detail.html`

**Enhancement**:
- Add "Activities" section showing activity count
- Add "View Activities" button linking to activity_list
- Show first 5 activities with quick links

**Actions**:
- [ ] Update `templates/workflows/detail.html`
- [ ] Add activities section
- [ ] Add navigation to activity list
- [ ] Commit: "feat(workflows): add activities section to workflow detail"
- [ ] Update plan status

### STEP 10: Final Validation

**Actions**:
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] Verify 100% test pass rate
- [ ] Manual testing via browser:
  - [ ] Create activity in workflow
  - [ ] View activities list (with and without phases)
  - [ ] View empty state
  - [ ] Check breadcrumbs work
  - [ ] Check permissions (owned vs downloaded)
- [ ] Fix any issues found
- [ ] Commit: "fix(activities): address issues found in manual testing"
- [ ] Update plan status

### STEP 11: Documentation and Finalization

**Actions**:
- [ ] Update feature file with implementation status
- [ ] Mark completed scenarios (ACT-LIST-01 through ACT-LIST-05, ACT-LIST-10 through ACT-LIST-13)
- [ ] Note deferred scenarios (ACT-LIST-06 through ACT-LIST-09)
- [ ] Create PR
- [ ] Update GitHub issue
- [ ] Commit: "docs(activities): update feature file with implementation status"

---

## 3. Test Coverage Summary

**Unit Tests:**
- 12 Activity model tests
- 12 ActivityService tests
- Total: **24 unit tests**

**Integration Tests:**
- 9 LIST scenarios
- 8 CREATE scenarios
- Total: **17 integration tests**

**Grand Total: 41 new tests**

---

## 4. Deferred to Future Features

**ACT-LIST-06 through ACT-LIST-09 (FIND functionality):**
- Search by name
- Filter by phase
- Filter by dependencies
- Drag-drop reordering

**Activity EDIT operation:**
- Full edit form
- Update all fields
- Dependencies management (M2M relationships)

**Activity DELETE operation:**
- Delete confirmation modal
- Cascade implications

**Activity VIEW/DETAIL operation:**
- Full detail page
- Show dependencies graph
- Version history

---

## 5. Files to Create/Modify

**NEW Files:**
- `methodology/models/activity.py`
- `methodology/services/activity_service.py`
- `methodology/activity_views.py`
- `methodology/activity_urls.py`
- `templates/activities/list.html`
- `templates/activities/create.html`
- `tests/unit/test_activity_model.py`
- `tests/unit/test_activity_service.py`
- `tests/integration/test_activity_list.py`
- `tests/integration/test_activity_create.py`
- `docs/plans/ACTIVITIES_LIST_IMPLEMENTATION_PLAN.md` (this file)

**MODIFIED Files:**
- `methodology/models/__init__.py` (add Activity)
- `methodology/admin.py` (register Activity)
- `mimir/urls.py` (include activity URLs)
- `templates/workflows/detail.html` (add activities section)
- `docs/features/act-5-activities/activities-list-find.feature` (mark completed scenarios)

**Total: 10 new files, 5 modified files**

---

## 6. Architecture Adherence

This plan follows SAO.md principles:

✅ **Repository Pattern**: ActivityService abstracts business logic  
✅ **Version Management**: Ready for future versioning  
✅ **HTMX + Django**: Server-rendered templates  
✅ **Test-First**: Unit tests before implementation  
✅ **No Mocking**: Integration tests use real Django Test Client  
✅ **Semantic Attributes**: `data-testid` for all testable elements  
✅ **UI Conventions**: Bootstrap 5, Font Awesome Pro, tooltips  
✅ **URL Scoping**: Activities under workflows under playbooks  

---

## 7. Estimated Complexity

**Model**: Simple (similar to Workflow)  
**Service**: Medium (CRUD + grouping logic)  
**Views**: Medium (list with grouping, create with validation)  
**Templates**: Medium (grouped list, form)  
**Tests**: High volume (41 tests total)

**Overall**: Medium complexity, well-scoped iteration.

---

## Next Steps

1. User reviews this plan
2. User answers clarification questions (Q1-Q5)
3. Update plan based on answers
4. Begin implementation starting with STEP 1
