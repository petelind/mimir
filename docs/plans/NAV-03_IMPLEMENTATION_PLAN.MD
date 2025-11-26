# NAV-03 Quick Create Playbook – Implementation Plan

## 0. Scope & References

- **Feature code**: NAV-03 (from `docs/features/act-0-auth/navigation.feature`)
- **User story**:
  - As Maria, being on the dashboard (FOB-DASHBOARD-1)
  - When she clicks `[+ New Playbook]` quick action
  - Then she is redirected to **FOB-PLAYBOOKS-CREATE_PLAYBOOK-1** (playbook create wizard step 1)
- **Related artifacts**:
  - `docs/architecture/SAO.md` – Web UI architecture, URL conventions, testing strategy
  - `docs/features/user_journey.md` – Act 2: Playbooks, dashboard and navigation context
  - `docs/features/act-0-auth/navigation.feature` – NAV-01..NAV-06, especially NAV-03
  - `docs/features/act-2-playbooks/playbooks-create.feature` – FOB-PLAYBOOKS-CREATE_PLAYBOOK-1
  - `docs/plans/PLAYBOOKS_CRUDV_IMPLEMENTATION_PLAN.md` – existing playbooks CRUDV plan
  - Existing code:
    - `templates/dashboard.html` – FOB-DASHBOARD-1 stub
    - `methodology/playbook_views.py` – `playbook_create` + step2/step3
    - `methodology/playbook_urls.py` – playbook URL names (`playbook_create`, etc.)

**Goal of NAV-03**: Add a **quick action on dashboard** that takes Maria directly into the existing playbook creation wizard (Step 1). No new backend business logic is needed; we reuse `playbook_create`.

---

## 1. Current State Assessment

1. **Dashboard**
   - Template: `templates/dashboard.html`
   - Currently:
     - Shows FOB-DASHBOARD-1 stub card and textual description of future dashboard sections.
     - Has `data-testid="dashboard-stub"` hidden marker with `FOB-DASHBOARD-1` (used by tests).
     - **No quick action buttons implemented yet**, including `[+ New Playbook]`.

2. **Playbook creation wizard**
   - Implemented and fully tested (21 scenarios PB-CREATE-01..21 all green).
   - Entry view: `playbook_create` in `methodology/playbook_views.py`.
   - URL name: `playbook_create` in `methodology/playbook_urls.py` (`/playbooks/playbook/create/` pattern via project routing).
   - Templates for steps 1–3 exist and are wired.

3. **Navigation feature spec (NAV-03)**
   - From `navigation.feature`:
     - Given Maria is on the dashboard
     - When she clicks `[+ New Playbook]` quick action
     - Then she is redirected to **FOB-PLAYBOOKS-CREATE_PLAYBOOK-1**.
   - This implies:
     - Dashboard must visually contain a **quick action button** with label `[+ New Playbook]`.
     - That button must **link to the playbook create wizard** (step 1).

4. **Tests currently passing**
   - `pytest tests/` → 74 passed.
   - That means NAV-03 is **either not yet covered by tests** or is satisfied implicitly (e.g. tests not checking label/semantics yet).
   - Plan should include **adding/aligning integration/E2E tests** for NAV-03, respecting the existing testing strategy.

---

## 2. Assumptions & Open Questions

### Assumptions

1. **URL mapping**
   - Dashboard URL name already exists (e.g. `dashboard`) and is used in tests (we saw `/dashboard/` in auth E2E).
   - Playbook list and create URLs follow SAO conventions and `playbook_urls.py`.
2. **Visual design**
   - Dashboard will eventually have multiple quick actions; NAV-03 only requires one: `[+ New Playbook]`.
   - We will follow existing UI conventions (Bootstrap, Font Awesome, data-testid, tooltips).
3. **Security**
   - Only authenticated users see the dashboard and the quick action; we reuse existing dashboard auth logic.

### Questions for clarification (can be answered later, not blocking initial implementation)

1. **Placement**: Should `[+ New Playbook]` appear:
   - In a **top-right area** of the dashboard card header, or
   - As part of a **Quick Actions** button group below the header?
2. **Icon and styling**:
   - Default proposal: primary button with `fa-book-sparkles` or `fa-plus` icon.
3. **Future extensibility**:
   - Should we introduce a **generic "Quick Actions" section** now (as a small layout), or just a single button and extend later?

For now, the plan assumes a **single primary quick-action button** within the dashboard main card, implemented in a way that can be trivially extended to multiple actions.

---

## 3. High-Level Design for NAV-03

- **Backend**: No new views or URLs. Reuse existing `playbook_create` view (`name='playbook_create'`).
- **Frontend (Django template)**:
  - Extend `templates/dashboard.html` to include a **Quick Actions** area with `[+ New Playbook]` button.
  - Button should:
    - Use `{% url 'playbook_create' %}` as its `href`.
    - Have semantic `data-testid` for testing (e.g. `data-testid="dashboard-quick-new-playbook"`).
    - Follow visual/UI conventions (Bootstrap button, tooltip).
- **Tests**:
  - Add an integration test (or E2E) that:
    - Renders dashboard for authenticated user.
    - Asserts the presence of `[+ New Playbook]` quick action and correct link to `playbook_create`.
    - Optionally asserts redirect behavior when following the link.

---

## 4. Detailed TODO Plan (Atomic Steps)

### 4.1. Prep & Rules

1. **Re-read rules before coding**
   - [ ] Re-read `.windsurf/rules/do-plan-before-doing.md` (already applied for planning).
   - [ ] Re-read `.windsurf/rules/do-test-first.md` before writing tests.
   - [ ] Re-read `.windsurf/rules/do-informative-logging.md` – check if any logging additions are needed (likely minimal for template-only change).
   - [ ] Re-read `.windsurf/rules/tooltips.md` – ensure button has tooltip.
   - [ ] Re-read `.windsurf/rules/do-semantic-versioning-on-ui-elements.md` – ensure semantic `data-testid` naming.

2. **Branching & commits**
   - [ ] Create feature branch (name to confirm with repo, e.g. `feature/nav-03-quick-create-playbook`).
   - [ ] Ensure commits follow Angular convention per `.windsurf/rules/do-follow-commit-convention.md`.

---

### 4.2. Tests for NAV-03

Target: add coverage that directly corresponds to `navigation.feature` NAV-03.

1. **Locate or create appropriate test file**
   - [ ] Check for existing navigation/dashboard tests under `tests/integration/` or `tests/e2e/` (e.g. `test_dashboard_navigation.py`).
   - [ ] If none exists, create a new integration test file, e.g. `tests/integration/test_dashboard_navigation.py`.

2. **Design concrete test(s) based on NAV-03**
   - [ ] Define test case `test_dashboard_has_quick_create_playbook_action`:
     - Arrange: create/authenticate user, GET `/dashboard/` (or `reverse('dashboard')`).
     - Assert:
       - Response 200.
       - Contains `data-testid="dashboard-quick-new-playbook"`.
       - Contains button label/aria text `+ New Playbook` (exact string per feature file).
       - Link `href` resolves to `reverse('playbook_create')`.
   - [ ] Optional second test `test_dashboard_quick_create_redirects_to_playbook_create`:
     - Using Django test client, simulate GET to `reverse('playbook_create')` to ensure route exists and returns wizard step 1 template, but this is already covered by separate tests. This test can be skipped if redundant.

3. **Implement tests (TDD)**
   - [ ] Implement failing integration test(s) first; run:
     - `pytest tests/integration/test_dashboard_navigation.py -vv`.
   - [ ] Confirm tests fail due to missing quick action/button.

4. **Logging & test identifiers**
   - [ ] Ensure `data-testid` naming matches spec and SAO/user_journey naming patterns.
   - [ ] No additional server-side logging required specifically for button render (template-only), unless we later add view changes.

---

### 4.3. Frontend Implementation – Dashboard Quick Action

1. **Update `templates/dashboard.html`**
   - [ ] Re-read `.windsurf/rules/do-semantic-versioning-on-ui-elements.md` and `tooltips.md` before editing template.
   - [ ] Extend the existing dashboard card body to include a **Quick Actions** section, for example:
     - A horizontal button group under the description, or a right-aligned primary button.
   - [ ] Add `[+ New Playbook]` button with the following characteristics:
     - Uses `{% url 'playbook_create' %}` as `href`.
     - Text: `+ New Playbook` (exact label per feature file).
     - Bootstrap styles: e.g. `btn btn-primary` and an icon like `<i class="fa-solid fa-book-sparkles"></i>` or `<i class="fa-solid fa-plus"></i>`.
     - Tooltip attribute per `tooltips.md`, e.g.:
       - `data-bs-toggle="tooltip"`
       - `title="Create a new playbook"`.
     - Semantic test ID, e.g.:
       - `data-testid="dashboard-quick-new-playbook"`.
   - [ ] Keep existing `data-testid="dashboard-stub"` marker and feature code text `FOB-DASHBOARD-1` unchanged to avoid breaking existing tests.

2. **Check URL name and import**
   - [ ] Verify `playbook_create` URL name is resolvable in templates (project `urls.py` includes `methodology/playbook_urls.py` under `/playbooks/playbook/` or similar path).
   - [ ] If for any reason the URL name is different in final routing, adjust `{% url '...' %}` accordingly.

3. **Manual visual sanity check**
   - [ ] Run dev server and visually confirm the dashboard shows the `[+ New Playbook]` button.
   - [ ] Hover to confirm tooltip works.

4. **Commit step**
   - [ ] Commit changes with message, e.g.:
     - `feat(nav): add quick create playbook action on dashboard`

---

### 4.4. Re-run Tests & Continuous Testing Integration

1. **Focused tests**
   - [ ] Run integration tests for dashboard/navigation:
     - `pytest tests/integration/test_dashboard_navigation.py -vv`

2. **Full suite**
   - [ ] Run full test suite per rules:
     - `pytest tests/`
   - [ ] Ensure all tests remain green (auth, playbooks CRUDV, onboarding, dashboard, etc.).

3. **Logging to tests.log**
   - [ ] Verify pytest logging configuration still writes to `tests.log` (if already configured).
   - [ ] If NAV-03 tests expose any gaps, plan follow-up improvements in `tests.log` analysis.

4. **Check app logs**
   - [ ] Run any relevant flows and check `logs/app.log` for errors/warnings related to dashboard or playbook create navigation.

5. **Commit step**
   - [ ] Commit with message, e.g.:
     - `test(nav): add dashboard quick create playbook tests`

---

### 4.5. Documentation & Issue Tracking

1. **Update documentation**
   - [ ] Add short note to `docs/features/act-0-auth/navigation.feature` or related docs if behavior changed beyond the existing text (likely not needed; behavior matches spec).
   - [ ] Optionally, add a short mention of the quick action in any dashboard-related docs if they exist.

2. **GitHub Issue #19**
   - [ ] Re-read `.windsurf/rules/do-github-issues.md`.
   - [ ] Update GitHub Issue #19 with:
     - Implementation summary.
     - Links to relevant commits.
     - Test coverage description (new tests added).
   - [ ] Mark NAV-03 as implemented / done.

3. **Final verification**
   - [ ] Re-read `.windsurf/workflows/dev-5-check-dod.md` if applicable.
   - [ ] Verify this NAV-03 slice respects DoD:
     - Tests exist and pass.
     - UI aligned with UX spec.
     - Logging/tests/logs unaffected or improved.

---

## 5. Summary

This plan implements NAV-03 (Quick create playbook) as a **thin UI/navigation layer** on top of the already completed playbook creation wizard:

- Add a **dashboard quick action** `[+ New Playbook]` linking to `playbook_create`.
- Ensure the button is **discoverable**, **semantically testable** (`data-testid`), and styled per UI rules.
- Add **integration test(s)** that assert the presence and correct target of the quick action, directly mapping to `navigation.feature` NAV-03.
- Keep the scope minimal and focused, without introducing new backend logic, while following all existing rules (test-first, logging, semantic test IDs, Angular commit messages).
