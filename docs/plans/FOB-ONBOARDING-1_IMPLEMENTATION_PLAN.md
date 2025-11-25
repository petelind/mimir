# FOB-ONBOARDING-1 / Issue #12 (ONBOARD-01 Welcome Screen) – Implementation Plan

## 0. Context & Scope

- **Feature code**: `FOB-ONBOARDING-1`
- **Scenario**: `ONBOARD-01 Welcome screen`
- **Issue**: `#12` (assumed to track ONBOARD-01 only)
- **Goal**: Implement the first-time user onboarding welcome screen in FOB so that a newly registered, logged-in user (Maria) landing on `FOB-ONBOARDING-1` sees:
  - A clear "Welcome to FOB" headline.
  - A concise description of what FOB is.
  - An onboarding steps overview (at least the three main steps: Create Playbook, Take Tour, Get Started).
  - Primary CTA to start onboarding (e.g., "Begin your journey" / create first playbook).
  - Option to skip onboarding and go to dashboard.

### 0.1. Current State Summary

- **View**: `accounts.views.onboarding`
  - `@login_required`, logs access, renders `onboarding/welcome.html`.
- **Templates**:
  - `templates/accounts/onboarding.html`: older stub referencing future onboarding implementation; not wired by the view.
  - `templates/onboarding/welcome.html`: current welcome stub with placeholders, Skip Tour → `dashboard` link, CTA to `/onboarding/create-playbook/` (not yet implemented), minimal structure.
- **URLs**:
  - `accounts/urls.py` exposes `/auth/user/onboarding/` → `onboarding` view (`name='onboarding'`).
- **Tests**:
  - `tests/e2e/test_onboarding_welcome.py` covers full E2E registration→onboarding→dashboard flow, but only asserts presence of a generic `data-testid="onboarding-stub"` and `FOB-ONBOARDING-1` marker.
  - No dedicated integration/unit tests exist yet for onboarding welcome page content.


## 1. Open Questions for Clarification

- **Q1 – Scope of Issue #12**: Confirm that `#12` is **only** about `ONBOARD-01 Welcome screen` and **does NOT yet** include persistence of onboarding completion state (likely later scenarios ONBOARD-04/05).
- **Q2 – Canonical URL/entrypoint**: Confirm that `/auth/user/onboarding/` is the canonical URL for `FOB-ONBOARDING-1` (as opposed to an `/onboarding/` root or similar).
- **Q3 – Copy & tone**: Should we:
  - Reuse/align copy with the **user journey Act 1 / Act 1.5** description, or
  - Keep a shorter, more generic message for now and refine copy in a later content-focused issue?
- **Q4 – CTA behavior for "Begin your journey"**: For issue #12, is it acceptable that this CTA is a **stub link** (e.g., to a not-yet-implemented create-playbook onboarding step) as long as it has a stable URL and `data-testid`, or do we need a real destination in this issue?

> Plan below assumes: scope is ONBOARD-01 only; URL is `/auth/user/onboarding/`; copy can be short but aligned with FOB concept; the main CTA may be allowed to be a stub for now, but skip-to-dashboard must work.


## 2. High-Level Implementation Strategy

- Implement **ONBOARD-01** as a **static, server-rendered Django template** powered by the existing `onboarding` view.
- Keep backend logic minimal for this issue (no DB state yet), but:
  - Ensure logging is detailed and consistent with global logging rules.
  - Ensure URL layout follows SAO URL conventions where applicable.
- Design the welcome page content and structure per UX/user-journey docs, with semantic `data-testid` attributes to support tests.
- Add **integration and E2E assertions** that directly validate the ONBOARD-01 content instead of only checking a stub marker.


## 3. Detailed TODO Plan (Issue #12 / ONBOARD-01)

### 3.1. Repo & Process Setup

- **[ ]** Create and switch to branch `feature/fob-onboarding-01-welcome`.
- **[ ]** Re-read rules before coding:
  - `.windsurf/rules/do-plan-before-doing.md`
  - `.windsurf/rules/do-test-first.md`
  - `.windsurf/rules/informative-logging.md` and `.windsurf/rules/add-logging.md`
  - `.windsurf/rules/do-import-on-module-level.md`
  - `.windsurf/rules/do-runner.md` (for tests)
  - `.windsurf/rules/do-semantic-versioning-on-ui-elements.md` (for template semantics)
- **[ ]** Ensure local test runner is in place (`pytest tests/`) and `tests.log` logging is configured (per global continuous testing rule).

### 3.2. Backend: Onboarding View (ONBOARD-01)

_No new models or complex services for this issue; just ensure the view is a solid entrypoint with good logging and future-proofing._

- **[ ]** Review `accounts.views.onboarding` implementation and confirm:
  - **[ ]** It is annotated with `@login_required` and returns HTTP 302 to login for anonymous users.
  - **[ ]** It uses `render(request, 'onboarding/welcome.html')` as the single entrypoint for `FOB-ONBOARDING-1`.
  - **[ ]** It logs at `INFO` level with sufficient context (user, path, any query params if relevant).
- **[ ]** If needed, refactor `onboarding` view to keep it concise (20–30 lines max) and prepare for future steps:
  - **[ ]** Keep the public view small.
  - **[ ]** Add private helper(s) for any future branching logic (e.g., checking onboarding completion) but **do not implement completion state yet**.
- **[ ]** Ensure logging aligns with app-wide logging strategy (logs to `logs/app.log` with rotation at app start); if onboarding-specific logger name/format is needed, add now.

_Backend Tests_

- **[ ]** Add **integration test file** if missing, e.g. `tests/integration/test_onboarding_welcome.py`:
  - **[ ]** Test that **authenticated** user GET `/auth/user/onboarding/`:
    - Returns `200`.
    - Uses template `onboarding/welcome.html`.
    - Contains `data-testid="onboarding-welcome"` and headline "Welcome to FOB".
    - Contains onboarding steps overview markers (see 3.3).
  - **[ ]** Test that **anonymous** user GET `/auth/user/onboarding/`:
    - Redirects to login (status 302, `Location` startswith `/auth/user/login/`).


### 3.3. Frontend: Welcome Template Content & Semantics

_Target: implement ONBOARD-01 welcome screen per feature file and user journey._

- **[ ]** Decide canonical template:
  - Use `templates/onboarding/welcome.html` as the **canonical** welcome screen for `FOB-ONBOARDING-1`.
  - Keep `templates/accounts/onboarding.html` as historical stub for now; consider cleanup or consolidation in a later issue (after explicit user confirmation, per deletion rules).

- **[ ]** Update `onboarding/welcome.html` to match ONBOARD-01 requirements:
  - **[ ]** Clear hero message:
    - H1: "Welcome to FOB".
    - Subtext explaining FOB briefly (aligned with SAO/user-journey: local FOB workspace, playbooks, workflows).
  - **[ ]** Onboarding steps overview (at least three steps):
    - Step 1: Create your first playbook.
    - Step 2: Take a quick tour (Workflows, Activities, Artifacts, Sync).
    - Step 3: Get started / go to dashboard.
    - Each step should have short explanatory text.
  - **[ ]** Buttons / CTAs with semantic attributes:
    - Primary CTA button, e.g. "Begin your journey" or "Create My First Playbook":
      - Has `data-testid="onboarding-begin-journey-button"`.
      - For now, may point to a stub URL such as `/onboarding/create-playbook/` (to be implemented in later issue) or to `#` with a TODO comment, depending on your decision for Q4.
    - Secondary CTA: "Skip tour" / "Skip onboarding" button:
      - Uses `{% url 'dashboard' %}`.
      - Has `data-testid="onboarding-skip-button"`.
  - **[ ]** Test identifiers:
    - Root container `data-testid="onboarding-welcome"`.
    - Optional per-step identifiers: `data-testid="onboarding-step-1"`, `-2`, `-3` for more robust tests.
  - **[ ]** Keep a marker for feature code to help traceability, e.g. small text: `FOB-ONBOARDING-1` with `data-testid="onboarding-feature-code"`.

- **[ ]** Ensure HTML follows IA/UX guidelines:
  - Use Bootstrap layout patterns consistent with existing templates (`container`, `row`, `col-*`, `card`).
  - Respect `.windsurf/rules/do-semantic-versioning-on-ui-elements.md` for future template evolution (e.g., non-breaking changes vs. breaking changes in DOM structure).

_Frontend Tests_

- **[ ]** Update `tests/e2e/test_onboarding_welcome.py` to assert ONBOARD-01 content, not just the stub:
  - In `test_e2e_new_user_registration_to_dashboard` after redirect to onboarding:
    - **[ ]** Assert presence of `data-testid="onboarding-welcome"`.
    - **[ ]** Assert headline contains "Welcome to FOB".
    - **[ ]** Assert the onboarding steps overview markers exist (e.g., `onboarding-step-1/2/3`).
    - **[ ]** Assert both CTAs exist: begin journey button and skip button.
  - **[ ]** Optionally add a **dedicated E2E test** `test_onboarding_welcome_direct_access`:
    - Logs in a pre-created user.
    - GET `/auth/user/onboarding/` and validates same content as above.


### 3.4. URL & Navigation Review

- **[ ]** Confirm URL pattern in `accounts/urls.py` aligns with SAO URL convention:
  - Current pattern: `/auth/user/onboarding/` (system-part=`auth`, entity=`user`, action=`onboarding`).
  - For now, accept as the canonical onboarding entrypoint for ONBOARD-01.
- **[ ]** Ensure navigation flows are coherent with user journey:
  - Registration success → redirect to `/auth/user/onboarding/` (already implemented in `register` view).
  - Onboarding skip button → dashboard (`/dashboard/`).
  - Later issues can add navigation from onboarding steps to playbooks list or create-playbook wizard.


### 3.5. Logging, Monitoring, and Test Runner Integration

- **[ ]** Verify onboarding view logs at `INFO` level include:
  - Username.
  - Path (`request.path`).
  - Whether this is first-time vs. returning onboarding (even if we only log "onboarding accessed" for now).
- **[ ]** Ensure logging configuration still writes to `logs/app.log` with rotation on app relaunch.
- **[ ]** Make sure tests continue to be runnable via `pytest tests/` and that test output is captured in `tests.log`.
- **[ ]** Run targeted tests after implementation:
  - `pytest tests/integration/test_onboarding_welcome.py -v`.
  - `pytest tests/e2e/test_onboarding_welcome.py -v`.
  - Then `pytest tests/` for regression.


### 3.6. Documentation & Housekeeping

- **[ ]** If necessary, add a short note into `docs/features/act-0-auth/onboarding.feature` comments (if that pattern exists) to clarify that ONBOARD-01 is implemented and traced to issue #12 (only if this repo uses inline annotations; otherwise, keep feature file unchanged).
- **[ ]** Optionally add a brief mention in `docs/features/user_journey.md` that ONBOARD-01 is implemented in `onboarding/welcome.html` (if that document tracks implementation status; otherwise, skip to avoid noise).


### 3.7. Git & Issue Workflow

For each major step below, follow commit/message and GitHub issue rules (`do-github-issues.md`, `commit-after-change.md`):

1. **Backend + template skeleton & tests (red phase)**
   - **[ ]** Add/adjust integration/E2E tests for ONBOARD-01.
   - **[ ]** Commit with message like:
     - `test(onboarding): add ONBOARD-01 welcome screen tests (#12)`
2. **Implementation (green phase)**
   - **[ ]** Implement/adjust onboarding view and `onboarding/welcome.html` template to satisfy tests.
   - **[ ]** Commit with message like:
     - `feat(onboarding): implement FOB-ONBOARDING-1 welcome screen (#12)`
3. **Refine, cleanup, docs (refactor phase)**
   - **[ ]** Any small refactors, doc nudges, and logging polish.
   - **[ ]** Commit with message like:
     - `refactor(onboarding): polish welcome UX and logging (#12)`
4. **Final checks**
   - **[ ]** Ensure CI/pytest all green locally.
   - **[ ]** Push branch and link PR to issue #12.


## 4. What This Issue Explicitly Does NOT Cover

To keep work in small increments, this plan **does not** include:

- Persistent onboarding completion tracking (flags on user model, settings, or separate table).
- Routing logic based on onboarding completion (e.g., skip onboarding on subsequent logins).
- Implementation of `ONBOARD-02` (create first playbook), `ONBOARD-03` (tour), `ONBOARD-04` (skip onboarding flow logic beyond redirect), or `ONBOARD-05` (mark onboarding complete) beyond what is necessary for ONBOARD-01 page content.
- Complex HTMX interactions; ONBOARD-01 is server-rendered only.

These will be addressed in subsequent issues (#13–#16) tied to their respective scenarios.
