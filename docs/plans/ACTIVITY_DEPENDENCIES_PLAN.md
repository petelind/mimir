# Activity Dependencies Implementation Plan

**Feature**: Activity Predecessor/Successor with Workflow Abbreviations and Reference Names  
**Branch**: `feature/activity-dependencies`  
**Status**: Planning

---

## Requirements

### 1. Activity Dependencies
- Each activity can have **one predecessor** (upstream activity)
- Each activity can have **one successor** (downstream activity)
- If workflow has no other activities, both dropdowns are **disabled**

### 2. Workflow Abbreviation
- Auto-generated from workflow name using **consonants only**
- Example: "Workflow" → "WKF"
- Example: "Design Features" → "DSNFTRS"
- Stored on Workflow model for reuse

### 3. Activity Reference Name
- Composed of: `{workflow_abbreviation}{activity_order}`
- Example: Activity with order=1 in workflow "WKF" → "WKF1"
- Generated property (not stored, computed from workflow + order)

---

## Current State Assessment

### Existing Components
- ✅ **Activity Model**: Has `workflow` FK, `order`, `has_dependencies` boolean
- ✅ **ActivityService**: Has create/update/delete methods
- ✅ **Activity CRUD views**: create, edit, detail, list, delete
- ✅ **Templates**: create.html, edit.html, detail.html
- ⚠️ **has_dependencies**: Currently just boolean flag, will be replaced

### Components Needing Changes
- 🔧 **Activity Model**: Add `predecessor` and `successor` ForeignKeys
- 🔧 **Workflow Model**: Add `abbreviation` CharField
- 🔧 **ActivityService**: Update create/update for dependencies
- 🔧 **Activity Forms**: Add predecessor/successor dropdowns
- 🔧 **Templates**: Show reference names, dependency links
- 🔧 **Tests**: Update all existing tests, add new dependency tests

---

## Implementation Plan

### ✅ Step 0: Branch Setup
- [x] Create branch `feature/activity-dependencies`
- [ ] Read `.windsurf/rules/do-plan-before-doing.md`
- [ ] Read `.windsurf/workflows/dev-2-implement-backend.md`
- [ ] Read `.windsurf/workflows/dev-3-implement-frontend.md`

---

### 📋 Step 1: Models and Migrations

#### 1.1 Update Workflow Model
- [ ] Read `.windsurf/rules/do-write-concise-methods.md`
- [ ] Add `abbreviation` CharField to Workflow model
  - max_length=20, blank=False
  - Auto-generated on save from consonants in name
- [ ] Add `generate_abbreviation()` method
  - Extract consonants from workflow name
  - Handle spaces, special characters
  - Return uppercase abbreviation
- [ ] Override `save()` to auto-generate abbreviation if not set
- [ ] Update `__str__()` to show abbreviation: `"{name} ({abbreviation})"`
- [ ] Add tests: `tests/unit/test_workflow_model.py`
  - `test_workflow_abbreviation_generated_on_save`
  - `test_workflow_abbreviation_consonants_only`
  - `test_workflow_abbreviation_handles_spaces`
  - `test_workflow_abbreviation_uppercase`

#### 1.2 Create Migration for Workflow
- [ ] Run `python manage.py makemigrations -n add_workflow_abbreviation`
- [ ] Generate abbreviations for existing workflows in migration
- [ ] Apply migration: `python manage.py migrate`
- [ ] Commit: "feat(workflow): add abbreviation field with auto-generation"

#### 1.3 Update Activity Model
- [ ] Read `.windsurf/rules/do-write-concise-methods.md`
- [ ] **Remove**: `has_dependencies` BooleanField (no longer needed)
- [ ] **Add**: `predecessor` ForeignKey(Activity)
  - on_delete=models.SET_NULL
  - null=True, blank=True
  - related_name='successors'
  - help_text="Previous activity that must complete first"
- [ ] **Add**: `successor` ForeignKey(Activity)
  - on_delete=models.SET_NULL
  - null=True, blank=True
  - related_name='predecessors'
  - help_text="Next activity that depends on this one"
- [ ] **Add**: `@property reference_name(self)`
  - Return `f"{self.workflow.abbreviation}{self.order}"`
  - Example: "WKF1", "DSNFTRS2"
- [ ] **Add**: validation in `clean()` method
  - Predecessor must be in same workflow
  - Successor must be in same workflow
  - Cannot be self-referential (predecessor != self, successor != self)
  - No circular dependencies (if A.successor=B, then B.predecessor must != A)
- [ ] Add tests: `tests/unit/test_activity_model.py`
  - `test_activity_reference_name_generated`
  - `test_activity_predecessor_same_workflow_only`
  - `test_activity_successor_same_workflow_only`
  - `test_activity_cannot_be_own_predecessor`
  - `test_activity_cannot_be_own_successor`
  - `test_activity_circular_dependency_prevented`

#### 1.4 Create Migration for Activity
- [ ] Run `python manage.py makemigrations -n add_activity_dependencies`
- [ ] Apply migration: `python manage.py migrate`
- [ ] Commit: "feat(activity): add predecessor/successor dependencies and reference_name"

---

### 📋 Step 2: Service Layer

#### 2.1 Update ActivityService
- [ ] Read `.windsurf/rules/do-write-concise-methods.md`
- [ ] Read `.windsurf/rules/do-informative-logging.md`
- [ ] Update `create_activity()`:
  - Add `predecessor=None`, `successor=None` parameters
  - Validate predecessor/successor are in same workflow
  - Log dependency relationships
- [ ] Update `update_activity()`:
  - Support updating `predecessor`, `successor`
  - Validate changes don't create circular dependencies
  - Log dependency changes
- [ ] Add `get_available_predecessors(workflow, exclude_activity_id=None)`
  - Return queryset of activities in workflow
  - Exclude the current activity being edited
  - Order by `order` ASC
- [ ] Add `get_available_successors(workflow, exclude_activity_id=None)`
  - Return queryset of activities in workflow
  - Exclude the current activity being edited
  - Order by `order` ASC
- [ ] Add tests: `tests/unit/test_activity_service.py` (create if doesn't exist)
  - `test_create_activity_with_predecessor`
  - `test_create_activity_with_successor`
  - `test_create_activity_with_both_dependencies`
  - `test_update_activity_predecessor`
  - `test_update_activity_successor`
  - `test_get_available_predecessors_excludes_self`
  - `test_get_available_successors_excludes_self`
  - `test_validation_prevents_different_workflow_predecessor`
  - `test_validation_prevents_circular_dependency`
- [ ] Commit: "feat(service): add dependency management to ActivityService"

---

### 📋 Step 3: Django Admin

#### 3.1 Update Activity Admin
- [ ] Read `methodology/admin.py`
- [ ] Add `predecessor`, `successor` to `list_display` (remove `has_dependencies`)
- [ ] Add `predecessor`, `successor` to fieldsets
- [ ] Add inline display of reference_name (read-only)
- [ ] Test in `/admin/` interface manually
- [ ] Commit: "feat(admin): add dependency fields to Activity admin"

---

### 📋 Step 4: Django Views

#### 4.1 Update activity_create View
- [ ] Read `.windsurf/rules/do-write-concise-methods.md`
- [ ] Read `methodology/activity_views.py::activity_create`
- [ ] Extract `predecessor` and `successor` from POST data
- [ ] Pass to `ActivityService.create_activity()`
- [ ] Add to form context:
  - `available_predecessors`: Use `ActivityService.get_available_predecessors(workflow)`
  - `available_successors`: Use `ActivityService.get_available_successors(workflow)`
  - `disable_dependencies`: `workflow.get_activity_count() == 0`
- [ ] Handle validation errors for circular dependencies
- [ ] Add logging for dependency assignments
- [ ] Test manually: create activity with predecessor/successor

#### 4.2 Update activity_edit View
- [ ] Read `.windsurf/rules/do-write-concise-methods.md`
- [ ] Read `methodology/activity_views.py::activity_edit`
- [ ] Extract `predecessor` and `successor` from POST data
- [ ] Pass to `ActivityService.update_activity()`
- [ ] Add to form context:
  - `available_predecessors`: Exclude current activity
  - `available_successors`: Exclude current activity
  - `disable_dependencies`: `workflow.get_activity_count() <= 1`
  - Pre-select current predecessor/successor IDs
- [ ] Handle validation errors
- [ ] Test manually: edit activity dependencies

#### 4.3 Update activity_detail View
- [ ] Read `methodology/activity_views.py::activity_detail`
- [ ] Add to template context:
  - `reference_name`: activity.reference_name
  - `predecessor`: activity.predecessor (if exists)
  - `successor`: activity.successor (if exists)
- [ ] Test manually: view activity with dependencies

#### 4.4 Integration Tests
- [ ] Read `.windsurf/rules/do-runner.md`
- [ ] Read `.windsurf/rules/do-not-mock-in-integration-tests.md`
- [ ] Update `tests/integration/test_activity_create.py`:
  - Remove has_dependencies tests
  - Add `test_create_activity_with_predecessor`
  - Add `test_create_activity_with_successor`
  - Add `test_create_first_activity_dependencies_disabled`
  - Add `test_create_activity_circular_dependency_rejected`
- [ ] Update `tests/integration/test_activity_edit.py`:
  - Remove has_dependencies tests
  - Add `test_edit_activity_add_predecessor`
  - Add `test_edit_activity_add_successor`
  - Add `test_edit_activity_remove_dependencies`
  - Add `test_edit_activity_exclude_self_from_dropdowns`
- [ ] Update `tests/integration/test_activity_view.py`:
  - Add `test_view_shows_reference_name`
  - Add `test_view_shows_predecessor_link`
  - Add `test_view_shows_successor_link`
- [ ] Run tests: `pytest tests/integration/test_activity_*.py -v`
- [ ] Commit: "feat(views): implement dependency selection in activity CRUD"

---

### 📋 Step 5: Django Templates

#### 5.1 Update create.html
- [ ] Read `.windsurf/rules/tooltips.md`
- [ ] Read `templates/activities/create.html`
- [ ] **Remove**: "Has Dependencies" checkbox section
- [ ] **Add**: Predecessor dropdown
  ```html
  <label for="predecessor">
    Predecessor Activity
    <i class="fa-solid fa-info-circle" data-bs-toggle="tooltip"
       title="Activity that must complete before this one"></i>
  </label>
  <select name="predecessor" id="predecessor" class="form-select"
          {% if disable_dependencies %}disabled{% endif %}
          data-testid="predecessor-select">
    <option value="">-- None --</option>
    {% for act in available_predecessors %}
      <option value="{{ act.id }}" {% if form_data.predecessor == act.id %}selected{% endif %}>
        {{ act.reference_name }} - {{ act.name }}
      </option>
    {% endfor %}
  </select>
  ```
- [ ] **Add**: Successor dropdown (similar structure)
- [ ] **Add**: Disabled state message if `disable_dependencies`:
  - "No other activities yet - dependencies will be available after creating more activities"
- [ ] Update Tips sidebar: Explain predecessor/successor

#### 5.2 Update edit.html
- [ ] Read `templates/activities/edit.html`
- [ ] Same changes as create.html
- [ ] Pre-select current predecessor/successor values

#### 5.3 Update detail.html
- [ ] Read `.windsurf/rules/tooltips.md`
- [ ] Read `templates/activities/detail.html`
- [ ] **Add**: Reference name display in header
  ```html
  <h2>
    <span class="badge bg-secondary">{{ activity.reference_name }}</span>
    {{ activity.name }}
  </h2>
  ```
- [ ] **Replace**: "Has Dependencies" badge with actual dependency links
  ```html
  {% if activity.predecessor %}
    <div class="mb-2">
      <strong>Predecessor:</strong>
      <a href="{% url 'activity_detail' playbook_pk=playbook.pk workflow_pk=workflow.pk activity_pk=activity.predecessor.id %}">
        {{ activity.predecessor.reference_name }} - {{ activity.predecessor.name }}
      </a>
    </div>
  {% endif %}
  {% if activity.successor %}
    <div class="mb-2">
      <strong>Successor:</strong>
      <a href="{% url 'activity_detail' playbook_pk=playbook.pk workflow_pk=workflow.pk activity_pk=activity.successor.id %}">
        {{ activity.successor.reference_name }} - {{ activity.successor.name }}
      </a>
    </div>
  {% endif %}
  ```

#### 5.4 Update list.html
- [ ] Read `templates/activities/list.html`
- [ ] **Replace**: "Has Dependencies" column with "Reference" column
- [ ] Show activity.reference_name in table
- [ ] Show predecessor/successor reference names (if exist)

#### 5.5 Update delete.html
- [ ] Read `templates/activities/delete.html`
- [ ] **Remove**: "Has Dependencies" row
- [ ] **Add**: Warning if activity has predecessor or successor
  - "This activity is a predecessor for: {successor.reference_name}"
  - "This activity is a successor for: {predecessor.reference_name}"

#### 5.6 Update global_list.html
- [ ] Read `templates/activities/global_list.html`
- [ ] Show reference_name column
- [ ] Commit: "feat(templates): replace has_dependencies with predecessor/successor UI"

---

### 📋 Step 6: Update Graphviz Visualization

#### 6.1 Update ActivityGraphService
- [ ] Read `.windsurf/rules/do-write-concise-methods.md`
- [ ] Read `methodology/services/activity_graph_service.py`
- [ ] Update `_add_activity_node()`:
  - Include reference_name in node label
  - Format: `"{reference_name}\n{name}"`
- [ ] Update `_add_dependency_edges()`:
  - Draw edges based on predecessor/successor relationships
  - Arrow from predecessor to activity
  - Arrow from activity to successor
  - Style: `style="solid", arrowhead="normal", color="blue"`
- [ ] Add tests: `tests/unit/test_activity_graph_service.py`
  - Update existing tests to use reference_name
  - Add `test_graph_shows_predecessor_edge`
  - Add `test_graph_shows_successor_edge`
  - Add `test_graph_shows_dependency_chain`
- [ ] Test manually: View workflow detail with dependencies
- [ ] Commit: "feat(graph): show activity dependencies in Graphviz diagram"

---

### 📋 Step 7: Feature Files and Documentation

#### 7.1 Create Feature File
- [ ] Read `.windsurf/rules/do-write-scenarios.md`
- [ ] Create `docs/features/act-5-activities/activities-dependencies.feature`
  ```gherkin
  Feature: Activity Dependencies
    As a methodology author
    I want to define predecessor and successor relationships between activities
    So that I can show the execution sequence clearly
  
  Scenario: Create activity with predecessor
    Given I have a workflow "Design Features" with abbreviation "DSNFTRS"
    And the workflow has activity "Build Domain Model" with order 1
    When I create a new activity "Develop Feature List" with order 2
    And I select "DSNFTRS1 - Build Domain Model" as predecessor
    Then the activity is created with predecessor relationship
    And the activity shows reference name "DSNFTRS2"
  
  Scenario: Edit activity to add successor
    Given activity "DSNFTRS1 - Build Domain Model" exists
    And activity "DSNFTRS2 - Develop Feature List" exists
    When I edit "Build Domain Model"
    And I select "DSNFTRS2 - Develop Feature List" as successor
    Then the successor relationship is saved
    And "Develop Feature List" shows "DSNFTRS1" as predecessor
  
  Scenario: Dropdowns disabled for first activity
    Given I have an empty workflow "New Workflow"
    When I create the first activity
    Then the predecessor dropdown is disabled
    And the successor dropdown is disabled
    And I see message "No other activities yet"
  
  Scenario: Prevent circular dependencies
    Given activity "DSNFTRS1" has successor "DSNFTRS2"
    When I try to edit "DSNFTRS2" to set predecessor as "DSNFTRS1"
    Then I see validation error "Circular dependency detected"
  
  Scenario: View activity with dependencies
    Given activity "DSNFTRS2" has predecessor "DSNFTRS1" and successor "DSNFTRS3"
    When I view activity details
    Then I see reference name "DSNFTRS2" in the header
    And I see link to predecessor "DSNFTRS1 - Build Domain Model"
    And I see link to successor "DSNFTRS3 - Plan by Feature"
  
  Scenario: Workflow abbreviation auto-generated
    When I create workflow "Design Features"
    Then the abbreviation "DSNFTRS" is generated automatically
    When I create workflow "Build System"
    Then the abbreviation "BLDSYSTM" is generated automatically
  ```

#### 7.2 Update User Journey
- [ ] Read `docs/features/user_journey.md`
- [ ] Update Act 5 (Activities) section:
  - Replace "Has Dependencies" checkbox with predecessor/successor dropdowns
  - Add workflow abbreviation explanation
  - Add reference name display examples
  - Update screen mockups with new fields
  - Show dependency visualization in activity detail view
- [ ] Commit: "docs(user_journey): update Act 5 with dependency relationships"

#### 7.3 Update Screen Flow Diagram
- [ ] Open `docs/ux/2_dialogue-maps/screen-flow.drawio` in draw.io editor
- [ ] Navigate to "MVP Flow - Local FOB" tab
- [ ] Locate ACT 5: Activities section
- [ ] Update FOB-ACTIVITIES-CREATE screen:
  - Remove "Has Dependencies" checkbox
  - Add "Predecessor Activity" dropdown (shows reference names)
  - Add "Successor Activity" dropdown (shows reference names)
  - Add disabled state indicator when workflow has 0 activities
  - Show dropdown format: "{REF} - {Name}" (e.g., "DFT1 - Build Domain Model")
- [ ] Update FOB-ACTIVITIES-EDIT screen:
  - Same changes as CREATE
  - Show current selections pre-selected
  - Exclude current activity from both dropdowns
- [ ] Update FOB-ACTIVITIES-VIEW screen:
  - Add reference name badge in header: "[DFT1]" or badge style
  - Replace "Has Dependencies" badge with actual links:
    - "Predecessor: [DFT1 - Build Domain Model]" (clickable link)
    - "Successor: [DFT3 - Plan by Feature]" (clickable link)
  - Show reference names in activity cards
- [ ] Update FOB-WORKFLOWS-CREATE screen:
  - Add note: "3-letter abbreviation will be auto-generated"
  - Show example: "Design Features → DFT"
- [ ] Update FOB-WORKFLOWS-VIEW screen:
  - Show workflow abbreviation in header or badge
  - Activities in diagram show reference names
  - Dependency arrows between activities
- [ ] Save diagram
- [ ] Commit: "docs(screen-flow): update MVP flow with activity dependencies and abbreviations"

---

### 📋 Step 8: Final Testing and Validation

#### 8.1 Run Full Test Suite
- [ ] Read `.windsurf/rules/do-continuous-testing.md`
- [ ] Run unit tests: `pytest tests/unit/ -v`
- [ ] Run integration tests: `pytest tests/integration/ -v`
- [ ] Check test coverage for new code
- [ ] Fix any failing tests
- [ ] Achieve 100% pass rate

#### 8.2 Manual Testing
- [ ] Create FDD demo playbook (if not exists): `python manage.py create_demo_fdd`
- [ ] Test workflow abbreviation generation
- [ ] Test activity reference names displayed correctly
- [ ] Test creating activity with predecessor
- [ ] Test creating activity with successor
- [ ] Test editing dependencies
- [ ] Test disabled dropdowns for first activity
- [ ] Test circular dependency validation
- [ ] Test Graphviz diagram shows dependency arrows
- [ ] Test deleting activity with dependencies (warnings)

#### 8.3 Final Commit and Push
- [ ] Commit any remaining changes
- [ ] Run full test suite one more time
- [ ] Push branch: `git push origin feature/activity-dependencies`
- [ ] Create PR with description of changes
- [ ] Link to feature file and implementation plan

---

## Success Criteria

✅ **Models**:
- Workflow has `abbreviation` field (auto-generated from consonants)
- Activity has `predecessor` and `successor` ForeignKeys
- Activity has `reference_name` property
- Validation prevents circular dependencies and different-workflow dependencies

✅ **UI**:
- Create/Edit forms show predecessor/successor dropdowns
- Dropdowns disabled if workflow has 0 (create) or ≤1 (edit) activities
- Activity detail shows reference name prominently
- Activity detail shows predecessor/successor links
- List views show reference names
- Graphviz diagram shows dependency arrows

✅ **Tests**:
- All unit tests passing (100%)
- All integration tests passing (100%)
- New dependency scenarios covered
- Validation scenarios tested

✅ **Documentation**:
- Feature file created with BDD scenarios
- User journey updated with new UI
- Implementation plan this document) complete

---

## Notes

- **has_dependencies boolean**: Will be **removed** entirely - replaced by actual FK relationships
- **Workflow abbreviation**: Stored to avoid regenerating, but can be regenerated if workflow name changes
- **Reference names**: Computed property, not stored - always reflects current state
- **Circular dependency check**: Implemented in model validation, not just service layer
- **Single predecessor/successor**: Keeps the model simple - can extend to M2M later if needed

---

**End of Implementation Plan**  
**Status**: Ready for Implementation  
**Next Step**: Begin with Step 1.1 (Update Workflow Model)
