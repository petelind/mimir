# FOB-ONBOARDING-1 / ONBOARD-03 Tour of Features – Implementation Plan

## 0. Context & Scope

- **Feature code**: `FOB-ONBOARDING-1`
- **Scenario**: `ONBOARD-03 Tour of features`
- **Goal**: Implement the feature tour step in FOB onboarding so that after completing first playbook, Maria sees highlights of: Workflows, Activities, Artifacts, Sync

### 0.1. Current State Summary

**Existing Infrastructure:**
- **Models**: `UserOnboardingState` with `current_step` field for tracking progress
- **Views**: `accounts.views.onboarding` (welcome screen), `skip_onboarding` (ONBOARD-04)
- **Templates**: `templates/onboarding/welcome.html` (ONBOARD-01 implemented)
- **URLs**: `/auth/user/onboarding/` → welcome, `/auth/user/onboarding/skip/` → skip
- **Tests**: Integration tests for welcome screen and skip functionality

**What's Missing:**
- Tour view at `/onboarding/tour/` 
- Feature highlight cards for Workflows, Activities, Artifacts, Sync
- Progress indicator (Step 2 of 3)
- Continue button with navigation to completion
- Tests for tour display

## 1. Implementation Requirements Analysis

### 1.1. Feature Requirements
```gherkin
Scenario: ONBOARD-03 Tour of features
  Given Maria completed first playbook
  When she proceeds with tour
  Then she sees highlights of: Workflows, Activities, Artifacts, Sync
```

### 1.2. Implementation Checklist
- ✅ Create tour view at `/onboarding/tour/`
- ✅ Feature highlight cards: 
  - Workflows ("Organize activities into structured processes")
  - Activities ("Define specific tasks") 
  - Artifacts ("Track deliverables")
  - Sync ("Collaborate via Homebase")
- ✅ Progress indicator (Step 2 of 3)
- ✅ Continue button with icon `fa-solid fa-arrow-right` and tooltip "Proceed to next step"
- ✅ Test: `test_tour_display()` - verify all 4 cards shown

### 1.3. Acceptance Criteria
- ✅ All 4 feature cards display
- ✅ Progress indicator shows correct step
- ✅ Continue button proceeds to completion

## 2. High-Level Implementation Strategy

- Implement **ONBOARD-03** as a **server-rendered Django template** with minimal JavaScript
- Extend existing onboarding infrastructure using `UserOnboardingState.current_step` 
- Follow SAO URL conventions and existing patterns from welcome screen
- Use Bootstrap components consistent with existing templates
- Add comprehensive integration tests following existing test patterns

## 3. Detailed TODO Plan

### 3.1. Backend: Tour View Implementation

**New View Function:**
```python
@login_required
def tour(request):
    """
    Feature tour view (ONBOARD-03).
    
    Shows 4 feature highlight cards with progress indicator.
    Updates onboarding state to step=2.
    
    Template: onboarding/tour.html
    Context: None (static content)
    
    :param request: Django request object
    :return: Rendered tour template
    """
```

**Implementation Steps:**
- **[ ]** Add `tour` view function to `accounts/views.py`
- **[ ]** Implement step tracking: set `current_step = 2` when tour is accessed
- **[ ]** Add comprehensive logging per global rules
- **[ ]** Follow concise method pattern (20-30 lines max)
- **[ ]** Add private helper for step state management if needed

**URL Routing:**
- **[ ]** Add `/auth/user/onboarding/tour/` URL pattern to `accounts/urls.py`
- **[ ]** Follow existing convention: `path('user/onboarding/tour/', tour, name='onboarding_tour')`

### 3.2. Frontend: Tour Template Design

**Template Structure:**
```html
{% extends "base.html" %}
<!-- Progress indicator: Step 2 of 3 -->
<!-- 4 feature cards in grid layout -->
<!-- Continue button with arrow icon -->
```

**Feature Cards Content:**
1. **Workflows Card**
   - Icon: `fa-solid fa-sitemap`
   - Title: "Workflows"
   - Description: "Organize activities into structured processes"
   - Test ID: `data-testid="tour-card-workflows"`

2. **Activities Card**
   - Icon: `fa-solid fa-tasks`
   - Title: "Activities" 
   - Description: "Define specific tasks"
   - Test ID: `data-testid="tour-card-activities"`

3. **Artifacts Card**
   - Icon: `fa-solid fa-folder-open`
   - Title: "Artifacts"
   - Description: "Track deliverables"
   - Test ID: `data-testid="tour-card-artifacts"`

4. **Sync Card**
   - Icon: `fa-solid fa-sync`
   - Title: "Sync"
   - Description: "Collaborate via Homebase"
   - Test ID: `data-testid="tour-card-sync"`

**UI Components:**
- **[ ]** Progress indicator: `data-testid="tour-progress-indicator"`
- **[ ]** Continue button: `data-testid="tour-continue-button"` with `fa-solid fa-arrow-right`
- **[ ]** Tooltip: "Proceed to next step"
- **[ ]** Feature code marker: `data-testid="tour-feature-code"` → "FOB-ONBOARDING-1-TOUR"

### 3.3. Navigation Flow Integration

**From Welcome to Tour:**
- **[ ]** Update welcome template "Begin your journey" button to point to tour
- **[ ]** Change URL from `{% url 'playbook_create' %}` to `{% url 'onboarding_tour' %}`

**From Tour to Completion:**
- **[ ]** Continue button should navigate to completion step (ONBOARD-05)
- **[ ]** For now, point to `/auth/user/onboarding/complete/` (to be implemented later)
- **[ ]** Ensure the button works as a stable link even if completion step isn't implemented yet

### 3.4. Testing Implementation

**Integration Tests:**
- **[ ]** Create `tests/integration/test_onboarding_tour.py`
- **[ ]** Implement `test_tour_display()` function:
  ```python
  def test_tour_display(self):
      """Verify all 4 feature cards are shown with correct content."""
      # Test authenticated access
      # Test all 4 cards present with correct test IDs
      # Test progress indicator shows "Step 2 of 3"
      # Test continue button exists with arrow icon
      # Test onboarding state updated to step=2
  ```

**Additional Tests:**
- **[ ]** Test anonymous user redirect to login
- **[ ]** Test step tracking (current_step set to 2)
- **[ ]** Test template used is `onboarding/tour.html`

**E2E Tests:**
- **[ ]** Update `tests/e2e/test_onboarding_welcome.py` to include tour flow
- **[ ]** Add journey test: welcome → tour → completion (stub)

### 3.5. Step State Management

**Onboarding Step Mapping:**
- Step 0: Welcome screen (ONBOARD-01) - current implementation
- Step 1: Create first playbook (ONBOARD-02) - separate issue  
- Step 2: Tour of features (ONBOARD-03) - this implementation
- Step 3: Complete onboarding (ONBOARD-05) - separate issue

**State Updates:**
- **[ ]** When tour is accessed: `current_step = 2`
- **[ ]** Ensure `get_or_create_onboarding_state()` is called
- **[ ]** Log step transitions for debugging

### 3.6. Logging & Monitoring

**View Logging:**
- **[ ]** Log tour access with username and step info
- **[ ]** Log step state changes 
- **[ ]** Follow global logging pattern to `logs/app.log`

**Console Logging (Frontend):**
- **[ ]** Add console.log for continue button click
- **[ ]** Add console.log for tour page load
- **[ ]** Follow existing pattern from welcome template

## 4. Implementation Order & Dependencies

### Phase 1: Backend Foundation
1. **[ ]** Add tour view function to `accounts/views.py`
2. **[ ]** Add URL pattern to `accounts/urls.py`
3. **[ ]** Create basic tour template file

### Phase 2: Template & UI
4. **[ ]** Implement tour template with 4 feature cards
5. **[ ]** Add progress indicator and continue button
6. **[ ]** Update welcome template navigation to tour

### Phase 3: Testing & Validation
7. **[ ]** Create integration tests
8. **[ ]** Update E2E tests
9. **[ ]** Run full test suite and fix issues

### Phase 4: Polish & Documentation
10. **[ ]** Add logging and error handling
11. **[ ]** Update documentation
12. **[ ]** Final testing and cleanup

## 5. What This Issue Explicitly Does NOT Cover

To maintain small increments:
- **ONBOARD-02** (Create first playbook) - separate issue
- **ONBOARD-05** (Complete onboarding) - separate issue  
- Complex HTMX interactions - static server-rendered only
- Dynamic content based on user's actual playbooks/workflows
- Advanced tour features (step-by-step guides, interactive demos)

## 6. Technical Specifications

### 6.1. File Structure
```
accounts/
├── views.py          # Add tour() function
├── urls.py           # Add tour URL pattern
└── models.py         # Reuse UserOnboardingState

templates/onboarding/
├── welcome.html      # Update navigation button
└── tour.html         # New tour template

tests/
├── integration/
│   └── test_onboarding_tour.py  # New test file
└── e2e/
    └── test_onboarding_welcome.py  # Update for tour flow
```

### 6.2. URL Design
- Welcome: `/auth/user/onboarding/` (existing)
- Tour: `/auth/user/onboarding/tour/` (new)
- Skip: `/auth/user/onboarding/skip/` (existing)

### 6.3. Template Design Patterns
- Bootstrap 5 components (card, btn, progress)
- Font Awesome icons for visual consistency
- Semantic `data-testid` attributes for testing
- Progressive enhancement friendly

### 6.4. Database Changes
- No schema changes needed
- Reuse existing `UserOnboardingState.current_step` field
- Step 2 = Tour view accessed

## 7. Success Criteria

### 7.1. Functional Requirements
- [ ] Tour page loads successfully for authenticated users
- [ ] All 4 feature cards display with correct content
- [ ] Progress indicator shows "Step 2 of 3"
- [ ] Continue button navigates to completion step
- [ ] Onboarding state tracked correctly (current_step=2)

### 7.2. Non-Functional Requirements  
- [ ] Page loads in < 2 seconds
- [ ] All tests pass (pytest tests/)
- [ ] Logging follows global standards
- [ ] Mobile responsive design
- [ ] Accessibility compliance (semantic HTML, ARIA labels)

### 7.3. Integration Requirements
- [ ] Fits seamlessly between welcome and completion steps
- [ ] Maintains existing skip functionality
- [ ] Doesn't break current onboarding flow
- [ ] Consistent UI/UX with welcome screen

## 8. Risk Assessment & Mitigations

### 8.1. Technical Risks
- **Risk**: URL routing conflicts with existing patterns
- **Mitigation**: Follow established `/auth/user/onboarding/` prefix convention

- **Risk**: Template inheritance issues
- **Mitigation**: Test template rendering early in development

### 8.2. Integration Risks  
- **Risk**: Breaking existing onboarding flow
- **Mitigation**: Comprehensive integration tests, maintain backward compatibility

- **Risk**: Step state management confusion
- **Mitigation**: Clear documentation of step numbering, thorough state testing

## 9. Next Steps After Implementation

Once ONBOARD-03 is complete:
1. **ONBOARD-02**: Implement "Create first playbook" step
2. **ONBOARD-05**: Implement completion step with dashboard redirect
3. **Integration**: Test full end-to-end onboarding journey
4. **Enhancement**: Add interactive tour features, personalization

---

**Implementation Priority**: High (core onboarding flow)
**Estimated Complexity**: Medium (static template + view + tests)
**Dependencies**: Existing onboarding infrastructure (ready)
