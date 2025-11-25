# Playbooks CRUDV Implementation Plan

## Scope & Decisions

**Implementing**: Create, View (all tabs), Edit, Delete operations for Playbooks  
**Feature Files**: `docs/features/act-2-playbooks/` (89 scenarios total, excluding list-find)

**Key Decisions** (from clarifications):
- ✅ Dependencies: None - this implementation creates all required models
- ✅ Replace existing templates with wizard-based approach
- ✅ Minimal workflow stub (name + description)
- ✅ Skip Family/Homebase integration
- ✅ Implement both Export and Import
- ✅ Full version history UI (integer versions: v1, v2, v3) - NO PIPs
- ✅ Skip auto-save
- ✅ Shallow copy for duplicate (mark as limitation)
- ✅ Create 4 GitHub issues (one per operation)
- ✅ Test-driven development (ALL scenarios tested)
- ✅ All view tabs: Overview + History + Settings

---

## Branch Strategy

```bash
git checkout main
git pull origin main
git checkout -b feature/playbooks-crudv
```

---

## PHASE 0: Create Models (Foundation)

**Create all required models for playbooks feature**:
- Create `Playbook` model
- Create minimal `Workflow` model (stub for playbook creation)
- Register in admin
- Create and apply migrations

---

## PHASE 1: Create Playbook Model

#### Step 1.0: Create Playbook Model
- [ ] Re-read `docs/architecture/SAO.md` - understand Repository Pattern
- [ ] Re-read `.windsurf/rules/do-skeletons-first.md`
- [ ] Re-read `.windsurf/rules/do-docstring-format.md`
- [ ] Create `methodology/models/__init__.py` if not exists
- [ ] Create `methodology/models/playbook.py`:
  ```python
  from django.db import models
  from django.contrib.auth import get_user_model
  
  User = get_user_model()
  
  class Playbook(models.Model):
      """
      Playbook represents a methodology with workflows, activities, and artifacts.
      
      Playbooks can be owned (created by user) or downloaded from families.
      Each playbook tracks versions as integer increments (v1, v2, v3).
      """
      
      # Choices
      CATEGORY_CHOICES = [
          ('product', 'Product'),
          ('development', 'Development'),
          ('research', 'Research'),
          ('design', 'Design'),
          ('other', 'Other'),
      ]
      
      VISIBILITY_CHOICES = [
          ('private', 'Private (only me)'),
          ('family', 'Family'),  # TODO: Implement family sharing
          ('local', 'Local only (not uploaded to Homebase)'),  # TODO: Implement Homebase
      ]
      
      STATUS_CHOICES = [
          ('active', 'Active'),
          ('draft', 'Draft'),
          ('disabled', 'Disabled'),
      ]
      
      SOURCE_CHOICES = [
          ('owned', 'Owned'),
          ('downloaded', 'Downloaded'),
      ]
      
      # Fields
      name = models.CharField(max_length=100)
      description = models.TextField(max_length=500)
      category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
      tags = models.JSONField(default=list, blank=True)
      visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private')
      status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
      version = models.IntegerField(default=1)
      source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='owned')
      
      # Relationships
      author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playbooks')
      
      # Timestamps
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      
      class Meta:
          ordering = ['-updated_at']
          constraints = [
              models.UniqueConstraint(fields=['author', 'name'], name='unique_playbook_per_author')
          ]
      
      def __str__(self):
          return f"{self.name} (v{self.version})"
  ```
- [ ] Add comprehensive docstrings per rules
- [ ] Commit: `feat(playbooks): create Playbook model with all required fields`

#### Step 1.1: Create Workflow Model (Minimal Stub)
- [ ] Create `methodology/models/workflow.py`:
  ```python
  from django.db import models
  
  class Workflow(models.Model):
      """
      Workflow stub for playbook creation.
      
      Minimal implementation to support playbook wizard Step 2.
      Full workflow functionality will be implemented in Act 3.
      
      TODO: Expand in Act 3 Workflows implementation
      """
      name = models.CharField(max_length=100)
      description = models.TextField(blank=True)
      playbook = models.ForeignKey('Playbook', on_delete=models.CASCADE, related_name='workflows')
      created_at = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
          return self.name
  ```
- [ ] Add docstrings and TODO comments
- [ ] Commit: `feat(playbooks): create minimal Workflow model stub`

#### Step 1.2: Update Model Init and Admin
- [ ] Update `methodology/models/__init__.py`:
  ```python
  from .playbook import Playbook
  from .workflow import Workflow
  
  __all__ = ['Playbook', 'Workflow']
  ```
- [ ] Update `methodology/admin.py`:
  ```python
  from django.contrib import admin
  from .models import Playbook, Workflow
  
  @admin.register(Playbook)
  class PlaybookAdmin(admin.ModelAdmin):
      list_display = ['name', 'author', 'version', 'status', 'category', 'created_at']
      list_filter = ['status', 'category', 'visibility', 'source']
      search_fields = ['name', 'description']
      readonly_fields = ['created_at', 'updated_at']
  
  @admin.register(Workflow)
  class WorkflowAdmin(admin.ModelAdmin):
      list_display = ['name', 'playbook', 'created_at']
      list_filter = ['playbook']
      search_fields = ['name', 'description']
  ```
- [ ] Commit: `feat(playbooks): register Playbook and Workflow in admin`

#### Step 1.3: Create and Apply Migrations
- [ ] Create migrations: `python manage.py makemigrations methodology`
- [ ] Review migration file
- [ ] Apply migrations: `python manage.py migrate`
- [ ] Verify models in Django admin
- [ ] Commit: `feat(playbooks): add migrations for Playbook and Workflow models`

---

## PHASE 2: Foundation Setup

#### Step 2.1: Read Architecture Documentation
- [ ] Re-read `docs/architecture/SAO.md` (Repository Pattern, Version Management)
- [ ] Re-read `docs/features/user_journey.md` Act 2
- [ ] Re-read `.windsurf/rules/do-plan-before-doing.md`

### 1.2 Model Extensions
- [ ] Re-read `.windsurf/rules/do-skeletons-first.md`
- [ ] Create `PlaybookVersion` model in `methodology/models/playbook_version.py`:
  - Fields: `playbook`, `version_number`, `snapshot_data` (JSON), `change_summary`, `created_at`, `created_by`
- [ ] Register in admin
- [ ] Create & apply migration
- [ ] Commit: `feat(playbooks): add PlaybookVersion model for history tracking`

### 1.3 URL Structure
- [ ] Update `methodology/playbook_urls.py` per `/{entity}/{action}/{id}` convention
- [ ] Patterns: list, create, detail, edit, delete, export, import, duplicate, version view
- [ ] Commit: `feat(playbooks): define URL structure for CRUDV operations`

### 1.4 Test Fixtures
- [ ] Re-read `.windsurf/rules/do-test-fixture-data-management.md`
- [ ] Create `tests/fixtures/playbooks_seed.json` (3 playbooks, workflows, version history)
- [ ] Commit: `test(playbooks): add test fixture data`

---

## PHASE 2: CREATE (Wizard) - 21 Scenarios

**Reference**: `docs/features/act-2-playbooks/playbooks-create.feature`

### 2.1 Forms & Tests
- [ ] Re-read `.windsurf/rules/do-test-first.md`
- [ ] Create wizard form classes in `methodology/forms/playbook_forms.py`:
  - `PlaybookBasicInfoForm` (Step 1)
  - `PlaybookWorkflowForm` (Step 2)
  - `PlaybookPublishingForm` (Step 3)
- [ ] Create `tests/integration/test_playbook_create.py` with ALL 21 scenarios as FAILING tests
- [ ] Scenarios: PB-CREATE-01 through PB-CREATE-21
- [ ] Run: `pytest tests/integration/test_playbook_create.py -v` (verify all FAIL)
- [ ] Commit: `test(playbooks): add failing tests for 21 creation scenarios`

### 2.2 Step 1: Basic Info
- [ ] Re-read `.windsurf/rules/short-concise-methods.md`
- [ ] Re-read `.windsurf/rules/do-informative-logging.md`
- [ ] Implement `playbook_create` view (Step 1: name, description, category, tags, visibility)
- [ ] Create `templates/playbooks/create_wizard_step1.html` with wizard UI
- [ ] Run tests for Step 1 scenarios until passing
- [ ] Commit: `feat(playbooks): implement creation wizard Step 1`

### 2.3 Step 2: Workflows
- [ ] Implement `playbook_create_step2` view ([Skip] or [Add First Workflow])
- [ ] Create minimal Workflow record (name + description stub)
- [ ] Create `templates/playbooks/create_wizard_step2.html`
- [ ] Run tests for Step 2 scenarios until passing
- [ ] Commit: `feat(playbooks): implement creation wizard Step 2`

### 2.4 Step 3: Publishing
- [ ] Implement `playbook_create_step3` view (status, save to DB, create v1)
- [ ] Create `templates/playbooks/create_wizard_step3.html` with summary card
- [ ] Clear session, redirect to detail page
- [ ] Run tests for Step 3 scenarios until passing
- [ ] Commit: `feat(playbooks): implement creation wizard Step 3`

### 2.5 Navigation & Validation
- [ ] Implement wizard navigation ([← Back], [Cancel] with modal, breadcrumbs)
- [ ] All validation scenarios (length, duplicates, required fields)
- [ ] Run: `pytest tests/integration/test_playbook_create.py -v` (verify ALL pass)
- [ ] Manual smoke test: Create playbook end-to-end
- [ ] Commit: `feat(playbooks): complete creation wizard with full validation`

### 2.6 Update GitHub Issue
- [ ] Re-read `.windsurf/rules/do-github-issues.md`
- [ ] Update issue with implementation status
- [ ] Commit: `docs(playbooks): update CREATE issue with progress`

---

## PHASE 3: VIEW (All Tabs) - 24 Scenarios

**Reference**: `docs/features/act-2-playbooks/playbooks-view.feature`

### 3.1 Tests for Detail View
- [ ] Create `tests/integration/test_playbook_view.py` with ALL 24 scenarios as FAILING tests
- [ ] Scenarios: PB-VIEW-01 through PB-VIEW-24
- [ ] Run: `pytest tests/integration/test_playbook_view.py -v` (verify all FAIL)
- [ ] Commit: `test(playbooks): add failing tests for 24 view scenarios`

### 3.2 Header & Overview Tab
- [ ] Re-read `.windsurf/rules/tooltips.md`
- [ ] Implement `playbook_detail` view
- [ ] Create/replace `templates/playbooks/detail.html`:
  - Header (name, version badge, status badge, author, timestamp)
  - Top actions (Edit, Delete, Export, Duplicate, Disable/Enable, ...More)
  - Tab navigation (Overview*, Workflows, History, Settings)
  - Overview tab: description, Quick Stats, Metadata, Workflows list
- [ ] Run tests for PB-VIEW-01 through PB-VIEW-05 until passing
- [ ] Commit: `feat(playbooks): implement detail view with Overview tab`

### 3.3 Workflows Tab
- [ ] Create `templates/playbooks/partials/workflows_tab.html`
- [ ] [Add Workflow] button (if owned), workflow list, filters placeholder
- [ ] Run tests for PB-VIEW-06, PB-VIEW-07 until passing
- [ ] Commit: `feat(playbooks): add Workflows tab`

### 3.4 History Tab & Versions
- [ ] Implement `playbook_version_view` view (display specific version)
- [ ] Create `templates/playbooks/partials/history_tab.html` (version timeline)
- [ ] Create `templates/playbooks/version_detail.html` (past version view)
- [ ] Create `templates/playbooks/version_compare.html` (split-pane diff)
- [ ] NO PIP section
- [ ] Run tests for PB-VIEW-08 through PB-VIEW-11 until passing
- [ ] Commit: `feat(playbooks): add History tab with version viewing/comparison`

### 3.5 Settings Tab
- [ ] Create `templates/playbooks/partials/settings_tab.html`
- [ ] Only show if user is owner
- [ ] Sections: Visibility, Publishing, Sharing (placeholder), Transfer (placeholder)
- [ ] Run tests for PB-VIEW-12, PB-VIEW-13 until passing
- [ ] Commit: `feat(playbooks): add Settings tab for owned playbooks`

### 3.6 Action Handlers
- [ ] Implement `playbook_export` view (JSON serialization)
- [ ] Implement `playbook_duplicate` view (shallow copy, mark limitation)
- [ ] Implement `playbook_toggle_status` view (Disable/Enable)
- [ ] Add URL patterns
- [ ] Run tests for PB-VIEW-14 through PB-VIEW-20 until passing
- [ ] Commit: `feat(playbooks): implement export, duplicate, toggle actions`

### 3.7 Navigation & Polish
- [ ] Breadcrumb navigation
- [ ] Status badge colors
- [ ] [Back to Playbooks List] link
- [ ] Run: `pytest tests/integration/test_playbook_view.py -v` (verify ALL pass)
- [ ] Manual smoke test: Navigate all tabs, test all actions
- [ ] Commit: `feat(playbooks): complete view functionality with all tabs`

### 3.8 Update GitHub Issue
- [ ] Update issue with implementation status
- [ ] Commit: `docs(playbooks): update VIEW issue with progress`

---

## PHASE 5: EDIT - 24 Scenarios

**Reference**: `docs/features/act-2-playbooks/playbooks-edit.feature`

### 4.1 Tests for Edit
- [ ] Create `tests/integration/test_playbook_edit.py` with ALL 24 scenarios as FAILING tests
- [ ] Scenarios: PB-EDIT-01 through PB-EDIT-24
- [ ] Run: `pytest tests/integration/test_playbook_edit.py -v` (verify all FAIL)
- [ ] Commit: `test(playbooks): add failing tests for 24 edit scenarios`

### 4.2 Edit Form & View
- [ ] Implement `playbook_edit` view (ownership check, pre-populate, save + new version)
- [ ] Create `templates/playbooks/edit.html`:
  - All editable fields
  - Version field (read-only, auto-increment note)
  - [Save Changes], [Save & Continue Editing], [Cancel] buttons
  - Validation errors
- [ ] Run tests for basic edit scenarios until passing
- [ ] Commit: `feat(playbooks): implement edit view with form`

### 4.3 Validation & Edge Cases
- [ ] All field validations (required, length, duplicate name)
- [ ] Multiple field edits in one save
- [ ] Cancel with/without changes (modal)
- [ ] Permission checks (cannot edit downloaded)
- [ ] Run: `pytest tests/integration/test_playbook_edit.py -v` (verify ALL pass)
- [ ] Manual smoke test: Edit various fields, test validation
- [ ] Commit: `feat(playbooks): complete edit with validation and edge cases`

### 4.4 Update GitHub Issue
- [ ] Update EDIT issue
- [ ] Commit: `docs(playbooks): update EDIT issue with progress`

---

## PHASE 5: DELETE - 20 Scenarios

**Reference**: `docs/features/act-2-playbooks/playbooks-delete.feature`

### 5.1 Tests for Delete
- [ ] Create `tests/integration/test_playbook_delete.py` with ALL 20 scenarios as FAILING tests
- [ ] Scenarios: PB-DELETE-01 through PB-DELETE-20
- [ ] Run: `pytest tests/integration/test_playbook_delete.py -v` (verify all FAIL)
- [ ] Commit: `test(playbooks): add failing tests for 20 delete scenarios`

### 5.2 Delete Modal & View
- [ ] Implement `playbook_delete` view (modal, ownership check, cascade delete)
- [ ] Create delete confirmation modal template:
  - Playbook details
  - Warning message ("cannot be undone")
  - Dependency counts (workflows, activities)
  - [Delete Playbook] (danger), [Cancel] buttons
  - Export suggestion
- [ ] Run tests for basic delete scenarios until passing
- [ ] Commit: `feat(playbooks): implement delete with confirmation modal`

### 5.3 Edge Cases & Permissions
- [ ] Cannot delete downloaded playbooks
- [ ] Enhanced warnings for shared/active playbooks
- [ ] Keyboard accessibility
- [ ] Error handling
- [ ] Run: `pytest tests/integration/test_playbook_delete.py -v` (verify ALL pass)
- [ ] Manual smoke test: Delete various playbooks, test warnings
- [ ] Commit: `feat(playbooks): complete delete with permissions and edge cases`

### 5.4 Update GitHub Issue
- [ ] Update DELETE issue
- [ ] Commit: `docs(playbooks): update DELETE issue with progress`

---

## PHASE 6: IMPORT

### 6.1 Tests for Import
- [ ] Create `tests/integration/test_playbook_import.py` with import scenarios
- [ ] Test valid JSON import, invalid JSON, duplicate handling
- [ ] Commit: `test(playbooks): add failing tests for import`

### 6.2 Import View & Template
- [ ] Implement `playbook_import` view (parse JSON, create playbook)
- [ ] Create `templates/playbooks/import.html` (file upload form)
- [ ] Run tests until passing
- [ ] Commit: `feat(playbooks): implement JSON import functionality`

---

## PHASE 7: Integration & E2E Testing

### 7.1 Integration Test Suite
- [ ] Re-read `.windsurf/rules/do-continuous-testing.md`
- [ ] Run full integration test suite: `pytest tests/integration/test_playbook_*.py -v`
- [ ] Fix any cross-feature issues
- [ ] Commit: `test(playbooks): verify full integration test suite passes`

### 7.2 E2E Journey Tests
- [ ] Re-read `.windsurf/workflows/dev-4-2-journey-certification.md`
- [ ] Create `tests/e2e/test_playbook_journey.py`:
  - Complete user journey: Create → View → Edit → Delete
  - Test with LiveServerTestCase + Playwright
- [ ] Run: `pytest tests/e2e/test_playbook_journey.py -v`
- [ ] Commit: `test(playbooks): add E2E journey certification tests`

### 7.3 Manual Testing Checklist
- [ ] Create playbook via wizard (all 3 steps)
- [ ] View all tabs (Overview, Workflows, History, Settings)
- [ ] Edit playbook (verify version increments)
- [ ] Export to JSON
- [ ] Import from JSON
- [ ] Duplicate playbook
- [ ] Toggle status (Active ↔ Disabled)
- [ ] Delete playbook (test modal)
- [ ] Test validation errors
- [ ] Test permission checks

---

## PHASE 8: Documentation & Issue Management

### 8.1 Create GitHub Issues
- [ ] Re-read `.windsurf/rules/do-github-issues.md`
- [ ] Create issue: "Playbooks: CREATE operation" (link to feature file)
- [ ] Create issue: "Playbooks: VIEW operation" (link to feature file)
- [ ] Create issue: "Playbooks: EDIT operation" (link to feature file)
- [ ] Create issue: "Playbooks: DELETE operation" (link to feature file)
- [ ] Add labels: "Act-2", "Playbooks", "Feature", milestone: "MVP"
- [ ] Commit: `docs(playbooks): create GitHub issues for CRUDV operations`

### 8.2 Update Documentation
- [ ] Update `README.md` if needed
- [ ] Add implementation notes to SAO.md if architecture changed
- [ ] Commit: `docs(playbooks): update documentation`

---

## PHASE 9: Code Review & Refinement

### 9.1 Definition of Done Check
- [ ] Re-read `.windsurf/workflows/dev-5-check-dod.md`
- [ ] Verify all DoD criteria:
  - ✅ All 89 scenarios have tests
  - ✅ All tests pass
  - ✅ Code follows Repository Pattern
  - ✅ Logging implemented per rules
  - ✅ Templates follow semantic versioning
  - ✅ All buttons have tooltips
  - ✅ data-testid attributes present
  - ✅ Docstrings follow format rules
  - ✅ GitHub issues created and updated

### 9.2 Code Quality
- [ ] Review all methods: concise, single responsibility
- [ ] Check logging: INFO level, informative messages
- [ ] Verify no hardcoded values
- [ ] Check error handling complete
- [ ] Run linter/formatter if configured
- [ ] Commit: `refactor(playbooks): code quality improvements`

### 9.3 Final Testing
- [ ] Run full test suite: `pytest tests/ -v --cov=methodology`
- [ ] Verify 100% coverage for playbook CRUDV code
- [ ] Check `logs/app.log` for errors
- [ ] Commit: `test(playbooks): final testing verification`

---

## PHASE 10: Finalization

### 10.1 Merge Preparation
- [ ] Re-read `.windsurf/rules/do-pull-frequently.md`
- [ ] Pull latest from main: `git pull origin main`
- [ ] Resolve any conflicts
- [ ] Re-run all tests after merge
- [ ] Commit: `chore(playbooks): merge latest main and resolve conflicts`

### 10.2 Final Commit & Push
- [ ] Re-read `.windsurf/rules/do-follow-commit-convention.md`
- [ ] Review all commits follow Angular convention
- [ ] Push branch: `git push origin feature/playbooks-crudv`
- [ ] Create PR with description linking to issues and feature files

### 10.3 Close Issues
- [ ] Close GitHub issues for CREATE, VIEW, EDIT, DELETE
- [ ] Reference PR in closing comments
- [ ] Add "shallow copy limitation" note to Duplicate issue

---

## Summary

**Total Steps**: ~100 atomic tasks  
**Total Scenarios**: 89 (21 CREATE + 24 VIEW + 24 EDIT + 20 DELETE)  
**Test Files**: 5 (create, view, edit, delete, import + 1 E2E journey)  
**GitHub Issues**: 4 (one per operation)  
**Branch**: `feature/playbooks-crudv`

**Key Rules to Follow Throughout**:
- `.windsurf/rules/do-test-first.md` - Every feature has tests before implementation
- `.windsurf/rules/do-informative-logging.md` - INFO level logging everywhere
- `.windsurf/rules/short-concise-methods.md` - Keep methods focused
- `.windsurf/rules/tooltips.md` - All buttons have tooltips
- `.windsurf/rules/do-github-issues.md` - Track via issues
- `.windsurf/rules/do-follow-commit-convention.md` - Angular convention

**Deferred to Later**:
- List & Find operations (separate PR)
- PIP workflow
- Family/Homebase integration
- Deep workflow integration
- Deep clone for duplicate
