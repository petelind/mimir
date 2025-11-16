---
description: Finalize feature with testing, validation, and deployment
auto_execution_mode: 3
---

# Feature Finalization Workflow

0. Run all tests and make sure none are broken. If there are discrepancies between test expectations and implementation - ask user to clarify what takes precedence. Mark these scenarios with "done" emoji and add "completed" tag.

1. Identify Playwright E2E test for this feature/scenario. If there is none - ask user if they want to create one per .windsurf/workflows/dev-4-e2e-tests.md.

2. Run the development server and validate tests:
// turbo
   - Start the server: `python manage.py runserver`
   - Execute Playwright tests to ensure they pass
   - Fix any issues found during testing

3. Run the full test suite and validate clean pass:
// turbo
   - Execute all unit tests, integration tests, and E2E tests
   - Ensure no regressions were introduced
   - Fix any failing tests

4. Update project dependencies:
   - Add any new packages to requirements.txt that were added during feature development
   - Use `pip install <package>` to add new dependencies
   - Ensure version constraints are appropriate in requirements.txt
   - Test that `pip install -r requirements.txt` works in a fresh venv

5. Present completed work:
   - Summarize implemented features and changes
   - Show test results and coverage
   - Demonstrate functionality if possible

6. Final commit:
   - Check if there is a corresponding issue. Update the status with the latest changes and associate commit.
   - Commit all remaining changes using Angular-style commit messages
   - Follow .windsurf/rules/do-follow-commit-convention.md
   - Ensure commit message clearly describes the completed feature

7. If we are on feature branch - ask user if they want to send a PR or merge into main.

8. Close issue if exists, review and mark all todos as "done" in the implementation plan, and update scenario and/or feature with "done" emoji.
