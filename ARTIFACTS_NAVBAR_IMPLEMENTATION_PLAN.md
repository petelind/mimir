# Implementation Plan: Wire Artifacts to Main Navbar

## Change Request Summary
**Issue**: Artifacts are not wired to main navbar - the navbar link is currently disabled.

**Root Cause Analysis**:
- Artifacts currently only has playbook-scoped list view (`artifact_list`)
- No global list view exists (unlike Activities and Workflows which have both)
- Navbar link is disabled because there's no global URL to link to
- Pattern inconsistency: Activities and Workflows have global navbar access, Artifacts doesn't

## 1. Feature File Analysis

### Current State
- ✅ `artifacts-list-find.feature` exists - covers **playbook-scoped** list view
  - Background: "she is viewing playbook 'React Frontend v1.2'"
  - Scenarios cover list within a specific playbook context

### Required Changes
- ❌ **Missing**: Global artifacts list feature file
- Need to create: `artifacts-global-list.feature` following the pattern of Activities/Workflows

### Pattern Reference
- Activities: Has both scoped (`activities-list-find.feature`) and would have global view
- Workflows: Has both scoped (`workflows-list-find.feature`) and would have global view
- Artifacts: Currently only has scoped - **needs global view added**

## 2. UX Documentation Review

### `docs/features/user_journey.md`
**Lines 1326-1456: ACT 6: ARTIFACTS**

Current documentation shows:
- **Line 1338**: "Scope Selector: 'All Playbooks' / 'Current Playbook' / 'Current Workflow'"
  - This implies global view capability exists in design
- **Line 1332**: "FOB-ARTIFACTS-LIST+FIND-1" - generic name (not playbook-specific)

**Assessment**: User journey **already anticipates** global artifact list with scope selector.

**Required Updates**: 
- ✅ User journey already supports global view concept
- ⚠️ Need to clarify navigation: navbar → global list vs playbook tab → scoped list

### `docs/ux/2_dialogue-maps/screen-flow.drawio`
**MVP Flow Tab - ACT 6 Section**

Found references:
- Line 1367: `FOB-ARTIFACTS-LIST+FIND` (entry point box)
- Line 1684: Flow from ACT 5 → ACT 6 (Activities → Artifacts)
- Line 1693: Flow from ACT 6 → ACT 7 (Artifacts → Howtos)

**Assessment**: Screen flow shows Artifacts as part of MVP progression.

**Required Updates**:
- ⚠️ Need to verify if diagram shows navbar navigation to global list
- ⚠️ May need to add global list entry point alongside playbook-scoped entry

## 3. Architecture Review (SAO.md)

### URL Patterns
Following existing patterns in `mimir/urls.py`:
```python
# Global views (navbar accessible)
path("workflows/", workflow_views.workflow_global_list, name="workflow_global_list")
path("activities/", activity_views.activity_global_list, name="activity_global_list")
# MISSING: path("artifacts/", artifact_views.artifact_global_list, name="artifact_global_list")
```

### View Pattern
Reference: `methodology/activity_views.py:23-50`
- Global list view filters by `workflow__playbook__author=request.user`
- Shows activities across all owned playbooks
- Provides counts and grouping

## 4. Models Review

**No changes required** - Artifact model already supports global queries:
```python
Artifact.objects.filter(playbook__author=request.user)
```

## 5. Django Views Changes

### File: `methodology/artifact_views.py`

**Add New View** (following `activity_global_list` pattern):
```python
@login_required
def artifact_global_list(request):
    """
    Global artifacts overview - all artifacts across all playbooks.
    
    Shows artifacts from all playbooks owned by the user.
    Useful for seeing all deliverables across entire methodology portfolio.
    
    Template: artifacts/global_list.html
    Template Context:
        - artifacts: QuerySet of all artifacts
        - playbook_count: Count of unique playbooks
        - activity_count: Count of unique producing activities
        - type_groups: Dict of artifacts grouped by type
    
    :param request: Django request object
    :return: Rendered global list template
    """
```

**Implementation Details**:
- Filter: `Artifact.objects.filter(playbook__author=request.user, playbook__source='owned')`
- Select related: `playbook`, `produced_by`, `produced_by__workflow`
- Order by: `playbook__name`, `produced_by__workflow__order`, `produced_by__order`
- Include search/filter support (reuse existing `ArtifactService.search_artifacts` logic)

## 6. URLs Changes

### File: `methodology/artifact_urls.py`
**Add** (at top of urlpatterns):
```python
path("artifacts/", artifact_views.artifact_global_list, name="artifact_global_list"),
```

### File: `mimir/urls.py`
**Add** (after activity global list):
```python
path("artifacts/", artifact_views.artifact_global_list, name="artifact_global_list"),  # Global artifacts view
```

## 7. Template Changes

### Create New Template: `templates/artifacts/global_list.html`

**Structure** (following `templates/activities/global_list.html` pattern):
- Extends `base.html`
- Header: "Artifacts" with total count
- Stats cards: Total artifacts, Playbooks, Types, Required vs Optional
- Search & filter section
- Artifacts table with columns:
  - Name | Type | Playbook | Produced By | Required | Actions
- Grouping options: By Playbook, By Type, By Workflow
- Empty state: "No artifacts yet" with [Create First Artifact] button

### Update: `templates/base.html`

**Line 92-98**: Enable Artifacts navbar link
```html
<li class="nav-item">
    <a class="nav-link {% if '/artifacts/' in request.path %}active{% endif %}" 
       href="{% url 'artifact_global_list' %}" 
       data-testid="nav-artifacts"
       data-bs-toggle="tooltip" data-bs-placement="bottom"
       title="View all artifacts across your playbooks"
       {% if '/artifacts/' in request.path %}aria-current="page"{% endif %}>
        <i class="fas fa-gift"></i> Artifacts
    </a>
</li>
```

**Changes**:
- Remove `disabled` class
- Change `href="#"` to `href="{% url 'artifact_global_list' %}"`
- Update tooltip from "Coming soon" to "View all artifacts across your playbooks"
- Add active state logic

## 8. Tests to Add/Modify

### New Integration Test: `tests/integration/test_artifact_global_list.py`

**Scenarios to cover**:
1. `test_artifact_global_list_access` - Authenticated user can access
2. `test_artifact_global_list_shows_owned_artifacts` - Only shows user's artifacts
3. `test_artifact_global_list_counts` - Correct playbook/activity counts
4. `test_artifact_global_list_search` - Search functionality works
5. `test_artifact_global_list_filter_by_type` - Type filtering works
6. `test_artifact_global_list_filter_by_playbook` - Playbook filtering works
7. `test_artifact_global_list_empty_state` - Empty state displays correctly
8. `test_artifact_global_list_navbar_link` - Navbar link is active and working

### Update Existing Test: `tests/integration/test_navbar.py`
- Update `test_navbar_artifacts_link` to verify it's **enabled** and navigates correctly
- Add assertion for active state when on artifacts page

### New E2E Test: `tests/e2e/test_artifact_global_navigation.py`

**Journey scenarios**:
1. Navigate from navbar to global artifacts list
2. Filter artifacts by playbook
3. Navigate from global list to artifact detail
4. Navigate from global list to playbook-scoped list

## 9. Feature File to Create

### New File: `docs/features/act-6-artifacts/artifacts-global-list.feature`

```gherkin
Feature: FOB-ARTIFACTS-GLOBAL-LIST-1 Global Artifacts List
  As a methodology author (Maria)
  I want to view all artifacts across all my playbooks
  So that I can manage deliverables across my entire methodology portfolio

  Background:
    Given Maria is authenticated in FOB
    And she owns 3 playbooks:
      | name                      | artifacts |
      | React Frontend v1.2       |        12 |
      | UX Research Methodology   |         8 |
      | Design System Patterns    |         5 |

  Scenario: ARTG-01 Navigate to global artifacts from navbar
    Given Maria is on any FOB page
    When she clicks "Artifacts" in the main navbar
    Then she is redirected to FOB-ARTIFACTS-GLOBAL-LIST-1
    And she sees "Artifacts" header with count "(25 artifacts)"

  Scenario: ARTG-02 View global artifacts table
    Given Maria is on global artifacts list
    Then she sees all 25 artifacts
    And each artifact shows: Name, Type, Playbook, Produced By, Required, Actions
    And artifacts are grouped by playbook by default

  Scenario: ARTG-03 Filter by playbook
    Given Maria is on global artifacts list
    When she filters by playbook "React Frontend v1.2"
    Then she sees only 12 artifacts
    And all shown artifacts belong to "React Frontend v1.2"

  Scenario: ARTG-04 Filter by type
    Given artifacts have types: Document, Code, Design, Data
    When she filters by type "Document"
    Then only Document artifacts are shown

  Scenario: ARTG-05 Search across all playbooks
    Given Maria is on global artifacts list
    When she enters "API" in search
    Then artifacts matching "API" from all playbooks are shown

  Scenario: ARTG-06 Navigate to playbook-scoped list
    Given Maria is on global artifacts list
    When she clicks on playbook name "React Frontend v1.2"
    Then she is redirected to playbook-scoped artifacts list
    And she sees "Artifacts in React Frontend v1.2" header

  Scenario: ARTG-07 Navigate to artifact detail
    Given Maria is on global artifacts list
    When she clicks [View] for an artifact
    Then she is redirected to FOB-ARTIFACTS-VIEW_ARTIFACT-1

  Scenario: ARTG-08 Empty state display
    Given Maria owns zero playbooks with artifacts
    Then she sees "No artifacts yet"
    And she sees "Create your first playbook and add artifacts"

  Scenario: ARTG-09 Navbar link is active
    Given Maria is on global artifacts list
    Then the "Artifacts" navbar link has "active" class
    And the navbar link is highlighted
```

## 10. Documentation Updates Required

### `docs/features/user_journey.md`
**Section: ACT 6 (Lines 1326-1456)**

Add clarification:
```markdown
#### Navigation Paths to Artifacts

**Global Access** (All Playbooks):
- Main navbar → "Artifacts" → FOB-ARTIFACTS-GLOBAL-LIST-1
- Shows artifacts across all owned playbooks
- Scope selector defaults to "All Playbooks"

**Playbook-Scoped Access**:
- Playbook detail → "Artifacts" tab → FOB-ARTIFACTS-LIST+FIND-1
- Shows artifacts only for current playbook
- Scope selector defaults to "Current Playbook"
```

### `docs/ux/2_dialogue-maps/screen-flow.drawio`
**MVP Flow Tab - ACT 6**

Update needed:
- Add navbar entry point to `FOB-ARTIFACTS-GLOBAL-LIST`
- Show distinction between global and scoped list views
- Add navigation arrow from navbar to global list

## 11. Implementation Steps

### Step 1: Create Feature File
- [ ] Create `docs/features/act-6-artifacts/artifacts-global-list.feature`
- [ ] Commit: `docs(features): add global artifacts list feature file`

### Step 2: Implement Backend
- [ ] Add `artifact_global_list` view to `methodology/artifact_views.py`
- [ ] Add URL pattern to `methodology/artifact_urls.py`
- [ ] Add URL pattern to `mimir/urls.py`
- [ ] Commit: `feat(artifacts): add global artifacts list view`

### Step 3: Create Template
- [ ] Create `templates/artifacts/global_list.html`
- [ ] Commit: `feat(artifacts): add global artifacts list template`

### Step 4: Wire Navbar
- [ ] Update `templates/base.html` - enable Artifacts link
- [ ] Commit: `feat(navbar): wire Artifacts to global list view`

### Step 5: Add Tests
- [ ] Create `tests/integration/test_artifact_global_list.py`
- [ ] Update `tests/integration/test_navbar.py`
- [ ] Create `tests/e2e/test_artifact_global_navigation.py`
- [ ] Commit: `test(artifacts): add global list tests`

### Step 6: Update Documentation
- [ ] Update `docs/features/user_journey.md` - clarify navigation
- [ ] Update `docs/ux/2_dialogue-maps/screen-flow.drawio` - add global entry
- [ ] Commit: `docs(ux): update artifacts navigation documentation`

### Step 7: Verify & Test
- [ ] Run all tests: `pytest tests/`
- [ ] Manual verification: navbar link works, global list displays
- [ ] Check active state highlighting
- [ ] Verify filtering and search

## 12. Questions for User

1. **Scope Selector**: Should the global list template include a scope selector to switch between "All Playbooks" / "Current Playbook", or should these be separate URLs?
   - Recommendation: Separate URLs (simpler, clearer navigation)

2. **Default Grouping**: Should global list default to grouping by Playbook, or flat list?
   - Recommendation: Group by Playbook (easier to navigate large lists)

3. **Create Artifact**: From global list, clicking [Create Artifact] should:
   - Option A: Show playbook selector first
   - Option B: Redirect to playbook list to choose context
   - Recommendation: Option A (inline playbook selector)

4. **Icon**: Current icon is `fa-gift`. Is this appropriate or should we change it?
   - Recommendation: Keep `fa-gift` (consistent with existing design)

## 13. Estimated Effort

- Feature file: 30 min
- Backend view: 1 hour
- Template: 2 hours
- Navbar wiring: 15 min
- Tests: 2 hours
- Documentation: 1 hour
- **Total**: ~6.5 hours

## 14. Dependencies

- No blocking dependencies
- Can be implemented independently
- Should be done before any Artifacts-related E2E journey tests

## 15. Risks & Mitigations

**Risk**: Breaking existing playbook-scoped artifact list
- **Mitigation**: Keep existing `artifact_list` view unchanged, add new view separately

**Risk**: URL conflict between global and scoped lists
- **Mitigation**: Use distinct URL patterns (`/artifacts/` vs `/playbooks/<id>/artifacts/`)

**Risk**: Performance with large artifact counts
- **Mitigation**: Add pagination (follow Activities pattern)

## 16. Success Criteria

- ✅ Navbar "Artifacts" link is enabled and functional
- ✅ Clicking navbar link navigates to global artifacts list
- ✅ Global list shows artifacts from all owned playbooks
- ✅ Active state highlighting works correctly
- ✅ Search and filtering work across all playbooks
- ✅ All tests pass (100% pass rate)
- ✅ Documentation updated and accurate
- ✅ Feature file scenarios all implemented
