# Playbooks EDIT Implementation Plan

**Feature**: FOB-PLAYBOOKS-EDIT_PLAYBOOK-1  
**Issue**: #30  
**Branch**: `feature/playbooks-edit`  
**Scenarios**: 24 total from `docs/features/act-2-playbooks/playbooks-edit.feature`

## Current State Assessment

### Existing Code ✅
**Playbook Model** (`methodology/models/playbook.py`):
- All fields present: name, description, category, tags, visibility, status, version, source
- Constraints: unique (author + name)
- Methods: `is_owned_by()`, `can_edit()`

**Playbook Views** (`methodology/playbook_views.py`):
- ✅ `playbook_create` - Full wizard implementation exists
- ✅ `playbook_detail` - View exists
- ✅ `playbook_export` - Export to JSON exists
- ❌ `playbook_edit` - **STUB** (line 310-314)

**Reusable Patterns:**
- Workflow EDIT just implemented - can follow same pattern
- CREATE wizard has form validation logic we can reuse
- Playbook model already has all necessary fields

### What's Missing
- ❌ No PlaybookService (views access model directly)
- ❌ Edit form template
- ❌ Edit view implementation
- ❌ Integration tests for EDIT scenarios
- ❌ Unsaved changes warning (optional nice-to-have)

---

## Implementation Approach

**Strategy**: Lightweight implementation following Workflow EDIT pattern
- No service layer needed (PlaybookService not used elsewhere)
- Direct model access from views (matching existing pattern)
- Focus on core EDIT scenarios (1-21)
- Defer advanced features (22-24) as optional enhancements

**Core Scenarios**: 21 scenarios  
**Deferred**: 3 scenarios (breadcrumb navigation warnings, auto-save)

---

## Implementation Plan

### Step 1: Create Branch & Setup
- [ ] Checkout `feature/playbooks-edit` from current branch
- [ ] Re-read `.windsurf/rules/do-test-first.md`
- [ ] Re-read `.windsurf/rules/do-write-concise-methods.md`

### Step 2: Integration Tests (Test-First Development)

#### 2.1 Create Test File
**File**: `tests/integration/test_playbook_edit.py`

**Test Scenarios** (priority scenarios):
1. `test_pb_edit_01_open_edit_form` - GET request loads form
2. `test_pb_edit_02_form_prepopulated` - Fields show current values
3. `test_pb_edit_03_edit_name` - Update name successfully
4. `test_pb_edit_04_edit_description` - Update description
5. `test_pb_edit_05_change_category` - Change category dropdown
6. `test_pb_edit_06_add_tags` - Add new tags (JSON field)
7. `test_pb_edit_07_remove_tags` - Remove existing tags
8. `test_pb_edit_08_change_visibility` - Change visibility dropdown
9. `test_pb_edit_10_change_status_to_draft` - Change status
10. `test_pb_edit_11_change_status_to_active` - Change status back
11. `test_pb_edit_12_version_readonly` - Version field not editable
12. `test_pb_edit_13_validate_required_name` - Name validation
13. `test_pb_edit_14_duplicate_name_validation` - Unique name check
14. `test_pb_edit_15_validate_name_length` - Min/max length
15. `test_pb_edit_16_cancel_without_changes` - Cancel button works
16. `test_pb_edit_20_multiple_fields` - Update multiple fields at once
17. `test_pb_edit_23_cannot_edit_downloaded` - Ownership check

**Total**: ~17 core integration tests

#### 2.2 Run Tests (Should Fail)
```bash
pytest tests/integration/test_playbook_edit.py -v
# Expected: All tests fail (view not implemented)
```

- [ ] Commit: `test(playbooks): add EDIT integration tests (17 scenarios)`

---

### Step 3: Implement Edit View

#### 3.1 Update `playbook_edit` View
**File**: `methodology/playbook_views.py` (lines 310-314)

**Implementation**:
```python
@login_required
def playbook_edit(request, pk):
    """Edit playbook metadata."""
    playbook = get_object_or_404(Playbook, pk=pk)
    
    # Ownership check
    if not playbook.can_edit(request.user):
        messages.error(request, "You can only edit playbooks you own.")
        return redirect('playbook_detail', pk=pk)
    
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category')
        tags = request.POST.get('tags', '')  # Comma-separated
        visibility = request.POST.get('visibility')
        status = request.POST.get('status')
        
        # Validation
        errors = {}
        
        if not name:
            errors['name'] = "Name is required"
        elif len(name) < 3:
            errors['name'] = "Name must be at least 3 characters"
        elif len(name) > 100:
            errors['name'] = "Name must not exceed 100 characters"
        
        # Check duplicate name (exclude self)
        if name and name != playbook.name:
            if Playbook.objects.filter(author=request.user, name=name).exists():
                errors['name'] = "A playbook with this name already exists"
        
        if not description or len(description) < 10:
            errors['description'] = "Description must be at least 10 characters"
        elif len(description) > 500:
            errors['description'] = "Description must not exceed 500 characters"
        
        if errors:
            for field, error in errors.items():
                messages.error(request, error)
            return render(request, 'playbooks/edit.html', {
                'playbook': playbook,
                'form_data': request.POST
            })
        
        # Update playbook
        playbook.name = name
        playbook.description = description
        playbook.category = category
        playbook.visibility = visibility
        playbook.status = status
        
        # Parse tags (comma-separated to list)
        if tags:
            playbook.tags = [t.strip() for t in tags.split(',') if t.strip()]
        else:
            playbook.tags = []
        
        playbook.save()
        
        logger.info(f"User {request.user.username} updated playbook {pk}")
        messages.success(request, "Playbook updated successfully")
        return redirect('playbook_detail', pk=pk)
    
    # GET request
    return render(request, 'playbooks/edit.html', {
        'playbook': playbook,
        'tags_string': ', '.join(playbook.tags) if playbook.tags else ''
    })
```

**Key Features**:
- Ownership check via `can_edit()`
- Field validation (name, description length)
- Duplicate name check (exclude current playbook)
- Tags as comma-separated input → JSON list
- Version field read-only (not in form)
- Proper logging
- Success/error messages

- [ ] Re-read `.windsurf/rules/do-informative-logging.md`
- [ ] Implement view with validation
- [ ] Commit: `feat(playbooks): implement playbook_edit view with validation`

---

### Step 4: Create Edit Template

#### 4.1 Create Template
**File**: `templates/playbooks/edit.html`

**Structure**:
- Extends `base.html`
- Breadcrumbs: Playbooks > [Playbook Name] > Edit
- Form with all editable fields
- Pre-populated values
- Version field (read-only, displayed for reference)
- Cancel and Save buttons with FA icons + tooltips
- Bootstrap validation styling
- Semantic `data-testid` attributes

**Fields**:
1. Name (text input, required, 3-100 chars)
2. Description (textarea, required, 10-500 chars)
3. Category (dropdown from CATEGORY_CHOICES)
4. Tags (text input, comma-separated)
5. Visibility (dropdown from VISIBILITY_CHOICES)
6. Status (dropdown from STATUS_CHOICES)
7. Version (read-only display)

**Buttons**:
- Cancel → `playbook_detail`
- Save Changes → POST to `playbook_edit`

- [ ] Re-read `.windsurf/rules/tooltips.md`
- [ ] Re-read `docs/architecture/SAO.md` (UI guidelines)
- [ ] Create template with Bootstrap + FA icons
- [ ] Add tooltips on all buttons
- [ ] Add `data-testid` attributes
- [ ] Commit: `feat(playbooks): add edit template with validation styling`

---

### Step 5: Run and Fix Tests

#### 5.1 Run Integration Tests
```bash
pytest tests/integration/test_playbook_edit.py -v
```

- [ ] Fix any failing tests
- [ ] Ensure all 17 tests pass
- [ ] Run full test suite: `pytest tests/`
- [ ] Verify 100% pass rate
- [ ] Commit: `fix(playbooks): resolve EDIT integration test failures`

---

### Step 6: Manual Testing & Polish

#### 6.1 Test Edit Flow Manually
1. Start dev server: `python manage.py runserver`
2. Navigate to playbook detail
3. Click Edit button
4. Test all form fields
5. Test validation errors
6. Test success flow
7. Verify downloaded playbooks can't be edited

#### 6.2 Polish UI
- [ ] Verify Bootstrap styling matches other forms
- [ ] Check responsive design
- [ ] Test keyboard navigation
- [ ] Verify tooltips display correctly
- [ ] Check error message styling

- [ ] Commit: `polish(playbooks): improve EDIT form UX and styling`

---

### Step 7: Update Documentation

#### 7.1 Mark Scenarios Complete
**File**: `docs/features/act-2-playbooks/playbooks-edit.feature`

Mark implemented scenarios with ✅:
- PB-EDIT-01 through PB-EDIT-21 (21 scenarios)

Note deferred scenarios:
- PB-EDIT-22: Breadcrumb navigation warnings (optional)
- PB-EDIT-23: Already working (ownership check in view)
- PB-EDIT-24: Auto-save (future enhancement)

- [ ] Update feature file with status
- [ ] Commit: `docs(playbooks): mark EDIT scenarios as complete`

---

### Step 8: Final Validation & Merge Preparation

#### 8.1 Run Definition of Done Check
- [ ] Follow `.windsurf/workflows/dev-5-check-dod.md`
- [ ] Verify all rules compliance:
  - ✅ Test-first development
  - ✅ Concise methods (<30 lines per method)
  - ✅ Informative logging
  - ✅ No mocking in integration tests
  - ✅ Semantic naming (`data-testid`)
  - ✅ Tooltips on all buttons
  - ✅ Import management
  - ✅ Commit conventions (Angular style)

#### 8.2 Final Test Run
```bash
pytest tests/ -v --tb=short
# Expected: 100% pass rate
```

- [ ] Verify all tests pass
- [ ] Check test count increased by ~17
- [ ] Commit any final fixes

#### 8.3 Push and Update Issue
```bash
git push origin feature/playbooks-edit
gh issue comment 30 --body "[Implementation summary]"
```

- [ ] Push branch to remote
- [ ] Update issue #30 with progress
- [ ] Request code review

---

## Success Criteria

**Must Have:**
- ✅ 17 integration tests passing (100%)
- ✅ Edit form with all fields
- ✅ Validation (required, length, duplicate name)
- ✅ Pre-populated form values
- ✅ Ownership check (can't edit downloaded)
- ✅ Version field read-only
- ✅ Tags as comma-separated input
- ✅ Success/error messages
- ✅ Icons + tooltips on buttons
- ✅ Semantic `data-testid` attributes

**Nice to Have (Deferred)**:
- ❌ Unsaved changes warning on Cancel
- ❌ Breadcrumb navigation warnings
- ❌ Auto-save draft feature

---

## Complexity Estimate

**Low-Medium Complexity**

**Reasoning**:
- Similar to Workflow EDIT (just completed)
- Model already has all fields
- No service layer needed
- Straightforward form validation
- Pattern established from CREATE wizard

**Estimated Tests**: 17 integration tests  
**Estimated Lines**: ~150 lines (view) + ~200 lines (template) + ~300 lines (tests)

---

## Risks & Mitigations

**Risk**: Tags field (JSON) handling in form  
**Mitigation**: Use comma-separated input, convert to/from JSON list

**Risk**: Duplicate name validation complexity  
**Mitigation**: Simple query excluding current playbook

**Risk**: Version field confusion  
**Mitigation**: Display as read-only with explanation note

**Risk**: Downloaded playbooks edit attempt  
**Mitigation**: Already have `can_edit()` method checking source=='owned'

---

## Approval Required

Ready to implement Playbooks EDIT following this plan?

This will deliver:
- Full edit functionality for owned playbooks
- 17 passing integration tests
- Professional form UI with validation
- Following all project rules and patterns

Should I proceed with implementation?
