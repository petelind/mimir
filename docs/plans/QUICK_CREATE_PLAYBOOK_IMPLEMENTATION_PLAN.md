# Implementation Plan: Quick Create Playbook (GitHub #19)

**Feature**: Quick create playbook via [+ New Playbook] quick action on dashboard  
**Reference**: NAV-03 in `docs/features/act-0-auth/navigation.feature`  
**Target Screen**: `FOB-PLAYBOOKS-CREATE_PLAYBOOK-1` (full wizard)  
**Scope**: Dashboard quick action button to initiate the existing 3‑step playbook creation wizard

---

## 1. Architecture & Design Context

### 1.1 Relevant Architecture
- From `docs/architecture/SAO.md`: FOB is a Django app with shared services between MCP and Web UI, repository pattern, HTMX for dynamic UI, SQLite storage.
- Playbooks are static reference material; creation is a wizard that stores a new playbook in local FOB (with optional Homebase sync later).

### 1.2 User Journey & Screen Mapping
- **Dashboard**: `FOB-DASHBOARD-1` (stub) needs a quick action [+ New Playbook]
- **Wizard**: `FOB-PLAYBOOKS-CREATE_PLAYBOOK-1` (3‑step wizard defined in `docs/features/act-2-playbooks/playbooks-create.feature` and `docs/features/user_journey.md`)
- **Screen IDs**: See `docs/ux/2_dialogue-maps/act-7-create-playbooks/screen-ids.md` for detailed wizard flows

### 1.3 Existing Components to Reuse
- **Playbook list page**: Already has “Add Playbook” button (`/playbooks/add/`) → `playbook_add` view (stub)
- **Playbook views**: `methodology.playbook_views.py` provides stub `playbook_add` and `playbook_edit`
- **URLs**: `methodology.playbook_urls.py` includes `add/` route
- **Templates**: `templates/playbooks/list.html` has an “Add Playbook” button that links to `/playbooks/add/`
- **Dashboard stub**: `templates/dashboard.html` (currently just placeholder)

---

## 2. Current State Assessment

### 2.1 What Exists
- Dashboard stub view and template (`methodology.views.dashboard`, `templates/dashboard.html`)
- Playbook list and add stubs (`methodology.playbook_views.*`)
- URL routing for `/dashboard/` and `/playbooks/add/`
- Feature spec for full 3‑step creation wizard (`playbooks-create.feature`)

### 2.2 What’s Missing for #19
- **Dashboard quick action**: [+ New Playbook] button on `dashboard.html`
- **Wizard implementation**: The 3‑step wizard (Step 1: Basic Info, Step 2: Add Workflows, Step 3: Publishing) is not yet implemented; only a generic `playbook_add` stub exists.
- **Models**: No `Playbook` model (empty `models.py`)
- **Services/Repository**: No playbook service or repository layer
- **Tests**: No tests for creation flow

### 2.3 Reuse vs New
- **Reuse**: Dashboard view/template, URL patterns, overall routing
- **New**: Playbook model, PlaybookService, PlaybookRepository, wizard views/templates, tests

---

## 3. Step‑by‑Step Implementation Plan

### 3.1 Backend (Models, Services, Views)

#### 3.1.1 Create Playbook Model
- File: `methodology/models.py`
- Fields: id (slug), name, description, category, tags (JSON), visibility (enum), status (enum), version (auto v1.0), created_by, created_at, updated_at
- Constraints: Name unique per user, lengths per spec
- Add to Django admin

#### 3.1.2 Create Repository Pattern
- File: `methodology/repository.py`
- `PlaybookRepository` with methods:
  - `create_playbook(user, data)`
  - `get_by_id(user, playbook_id)`
  - `list_by_user(user)`
  - `name_exists(user, name)`

#### 3.1.3 Create Service Layer
- File: `methodology/services.py`
- `PlaybookService` with business logic:
  - `validate_basic_info(data)` (name uniqueness, lengths)
  - `create_from_wizard(user, step1_data, step2_data, step3_data)`
  - Support for optional first workflow inline creation

#### 3.1.4 Implement Wizard Views
- Update `methodology/playbook_views.py`:
  - Replace `playbook_add` stub with step‑by‑step wizard views:
    - `playbook_create_step1` (GET/POST) – Basic Info form
    - `playbook_create_step2` (GET/POST) – Add Workflows (optional)
    - `playbook_create_step3` (GET/POST) – Publishing Settings
  - Use Django forms or manual form handling with HTMX for step navigation
  - Store wizard data in session or hidden fields
  - Add cancel handling with confirmation modal

#### 3.1.5 Update URLs
- `methodology/playbook_urls.py`:
  - Add wizard step routes:
    - `create/step1/` → `playbook_create_step1`
    - `create/step2/` → `playbook_create_step2`
    - `create/step3/` → `playbook_create_step3`
  - Keep existing `add/` for backward compatibility (redirect to step1)

#### 3.1.6 Add Dashboard Quick Action
- Update `methodology/views.dashboard`:
  - No logic change; just template update

#### 3.1.7 Add Logging
- Per `add-logging.md` and `do-informative-logging.md`:
  - Log all wizard steps, validation errors, creation success/failure
  - Include user, playbook name, step, validation errors

### 3.2 Frontend (Templates & HTMX)

#### 3.2.1 Dashboard Quick Action Button
- File: `templates/dashboard.html`
- Add [+ New Playbook] button with:
  - `data-testid="quick-create-playbook-button"`
  - `href="{% url 'playbook_create_step1' %}"` (or HTMX if modal preferred)
  - Styled to match existing “Add Playbook” button

#### 3.2.2 Wizard Templates
- Create directory: `templates/playbooks/wizard/`
- `step1_basic.html`:
  - Form fields: Name, Description, Category, Tags, Visibility
  - Validation error display with `data-testid` attributes
  - Navigation: Cancel, Next
- `step2_workflows.html`:
  - Option to skip or add first workflow inline
  - Inline form for Workflow name/description
  - Navigation: Back, Skip/Create
- `step3_publish.html`:
  - Summary display
  - Status radio (Active/Draft), auto-version v1.0
  - Create Playbook button
- Use `data-testid` everywhere per semantic naming rule

#### 3.2.3 HTMX for Step Navigation
- Use HTMX for form submissions within wizard to avoid full page reloads
- Target a wizard container div
- Swap innerHTML for step transitions
- Add minimal JS for tag token input and confirmation modal

#### 3.2.4 Update Playbook List Template (Optional)
- Ensure newly created playbooks appear in list immediately after creation
- Add success message display

### 3.3 Tests (Feature ATs)

#### 3.3.1 Create Test File
- File: `tests/integration/test_playbook_create_quick.py`
- Test class: `TestQuickCreatePlaybook`

#### 3.3.2 Test Scenarios (from playbooks-create.feature)
- `test_open_create_wizard_from_dashboard`: Dashboard → click quick action → wizard Step 1
- `test_step1_validation_errors`: Empty fields, duplicate name, length limits
- `test_step1_success_and_next`: Valid data → proceed to Step 2
- `test_step2_skip_workflow`: Skip → proceed to Step 3
- `test_step2_add_first_workflow`: Inline workflow creation → proceed to Step 3
- `test_step3_create_active`: Create with Active status → success, redirect to detail
- `test_step3_create_draft`: Create with Draft status → success, redirect to detail
- `test_cancel_wizard`: Cancel at any step with confirmation modal
- `test_back_navigation`: Back/forward preserves data
- `test_playbook_appears_in_list_after_creation`

#### 3.3.3 Test Coverage
- Use Django Test Client, no mocking
- Validate HTML responses, redirects, DB state, messages
- Include `data-testid` checks for UI elements

### 3.4 Optional Journey Certification
- If deemed critical UX, add Playwright journey:
  - File: `tests/e2e/test_journey_quick_create.py`
  - Journey: Dashboard → quick action → complete wizard (happy path)

---

## 4. Implementation Sequence (Atomic Commits)

1. **Models & Admin**
   - Create Playbook model
   - Add to Django admin
   - Run migrations
   - Commit: `feat(playbooks): add Playbook model and admin`

2. **Repository & Service Skeletons**
   - Create repository.py with PlaybookRepository (skeleton)
   - Create services.py with PlaybookService (skeleton)
   - Add unit tests for repository/service
   - Commit: `feat(playbooks): add repository and service skeletons`

3. **Wizard Views Step 1**
   - Implement `playbook_create_step1` view with validation
   - Create template `step1_basic.html`
   - Add URL route
   - Add tests for Step 1 scenarios
   - Commit: `feat(playbooks): implement wizard step 1 (basic info)`

4. **Wizard Views Step 2**
   - Implement `playbook_create_step2` view
   - Create template `step2_workflows.html`
   - Add URL route
   - Add tests for Step 2 scenarios
   - Commit: `feat(playbooks): implement wizard step 2 (add workflows)`

5. **Wizard Views Step 3**
   - Implement `playbook_create_step3` view
   - Create template `step3_publish.html`
   - Add URL route
   - Add tests for Step 3 scenarios
   - Commit: `feat(playbooks): implement wizard step 3 (publishing)`

6. **Dashboard Quick Action**
   - Update `dashboard.html` to add [+ New Playbook] button
   - Add test for dashboard quick action
   - Commit: `feat(dashboard): add quick create playbook button`

7. **Service Logic & Repository Implementation**
   - Implement repository methods
   - Implement service methods
   - Wire up views to use service/repository
   - Add comprehensive logging
   - Update tests to use real DB
   - Commit: `feat(playbooks): wire up service layer and logging`

8. **HTMX & Frontend Polish**
   - Add HTMX attributes for step navigation
   - Implement tag token input JS
   - Implement cancel confirmation modal
   - Add `data-testid` everywhere
   - Commit: `feat(playbooks): add HTMX interactions and UI polish`

9. **Finalize & DOD Check**
   - Run full test suite
   - Check DOD checklist per `dev-5-check-dod.md`
   - Update dependencies if any added
   - Final commit: `feat(playbooks): complete quick create playbook feature (#19)`

---

## 5. Deviation Notes & Questions

- **Dashboard stub**: Current dashboard is a stub; per navigation.feature issues #17-22, full dashboard is planned. For #19, we only need to add the quick action button to the existing stub.
- **Wizard complexity**: The feature spec is rich (visibility options, tags, workflows). We will implement all scenarios in `playbooks-create.feature` to stay compliant.
- **Model design**: Tags as JSON field (simple) vs many-to-many (complex). Recommend JSON for simplicity per project preference.
- **Session vs hidden fields for wizard state**: Prefer hidden fields within wizard forms to keep stateless; session is fallback if needed.

---

## 6. Definition of Done Checklist

- [ ] Playbook model exists and migrations run
- [ ] Repository and service layers implemented with tests
- [ ] Wizard views (3 steps) implemented with HTMX navigation
- [ ] Dashboard quick action button exists and links to wizard
- [ ] All scenarios in `playbooks-create.feature` have corresponding tests
- [ ] Logging added per `add-logging.md`
- [ ] `data-testid` attributes on all interactive elements
- [ ] No DRF/JSON APIs for web UI (Django views + HTML only)
- [ ] Code follows concise methods, import-at-module-level, and other project rules
- [ ] `pytest tests/` passes
- [ ] Optional: Journey certification test added if UX-critical

---

**Next Step**: Ask user to approve this plan or request adjustments (e.g., implement only Step 1 first, simplify tags handling, defer workflows). After approval, proceed with implementation sequence starting with Playbook model.
