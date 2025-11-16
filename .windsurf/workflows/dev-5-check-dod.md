---
description: Definition of Done (DOD) checklist - verify compliance with all project rules
auto_execution_mode: 3
---

# Definition of Done (DOD) Checklist

This workflow validates that your feature/story implementation complies with all project rules and standards by examining current state and outputs.

## Core Development Rules

### ✅ Test-First Development (`do-test-first.md`)
- [ ] Every function/method has corresponding test(s)
- [ ] Feature files in `docs/features/` exist and comply with scenarios
- [ ] Tests use pytest framework (check test files for pytest imports/fixtures)
- [ ] Mocking is minimal (verify test files don't overuse mocks)

### ✅ Continuous Testing (`do-continuous-testing.md`)
- [ ] All tests are runnable via `pytest tests/` (run command to verify)
- [ ] Tests are pytest compatible with proper fixtures
- [ ] `tests.log` file exists and contains test output

### ✅ Concise Methods (`do-write-concise-methods.md`)
- [ ] Top-level (public) methods are 20-30 lines maximum (count lines in code)
- [ ] Supporting logic is in well-named private methods (verify method structure)
- [ ] Helper methods have single, focused responsibilities (examine method content)
- [ ] Method names are descriptive and clear (review naming conventions)

## Code Quality Rules

### ✅ Import Management (`do-import-on-module-level.md`)
- [ ] All imports are at module level (check file structure)
- [ ] No imports inside functions/methods (scan code for nested imports)
- [ ] Dependencies are properly declared (check requirements.txt)

### ✅ Informative Logging (`do-informative-logging.md`)
- [ ] Logging statements exist in methods and properties (search for logging calls)
- [ ] Log levels are appropriate (DEBUG, INFO, WARNING, ERROR used correctly)
- [ ] Error conditions have logging statements (verify exception handling)

### ✅ Minimal JavaScript Logging (`do-minimal-js-logging.md`)
- [ ] Minimal JavaScript exists for HTMX enhancements only
- [ ] HTMX event logging exists for debugging (check for htmx:beforeRequest, etc.)
- [ ] Client-side error handling includes logging (check error handlers)

## Testing and Quality Assurance

### ✅ Integration Test Standards (`do-not-mock-in-integration-tests.md`)
- [ ] Integration tests in `tests/integration/` exist
- [ ] Integration tests avoid mocking (examine test files for mock usage)
- [ ] Real dependencies are used in integration scenarios

### ✅ Commit Conventions (`do-follow-commit-convention.md`)
- [ ] Recent commit messages follow Angular conventional format (check git log)
- [ ] Commits are atomic and focused (verify commit content)
- [ ] Breaking changes are documented in commit messages

## UI and Frontend Rules

### ✅ Django Views + HTMX (`do-django-views-htmx.md`)
- [ ] No DRF views exist for new web UI features (check for DRF serializers/viewsets)
- [ ] Django views return HTML templates (verify view return types)
- [ ] HTMX attributes used for dynamic interactions (check templates for hx-*)
- [ ] Services layer is shared between MCP and Web UI (verify service usage)

### ✅ Template Context Validation (`do-validate-template-context.md`)
- [ ] View docstrings document template context (check view functions)
- [ ] All template variables are provided in context (verify render() calls)
- [ ] Form context includes related objects (check form views)

### ✅ Semantic Naming (`do-semantic-versioning-on-ui-elements.md`)
- [ ] All interactive elements have `data-testid` attributes (search templates)
- [ ] Naming follows kebab-case convention (verify testid format)
- [ ] Form inputs have proper name and id attributes (check form templates)

## Documentation and Analysis

### ✅ Scenario Writing (`do-write-scenarios.md`)
- [ ] BDD scenarios exist for features (check .feature files)
- [ ] Feature files are well-structured (verify Gherkin syntax)
- [ ] Scenarios cover edge cases and error conditions (review scenario content)
- [ ] Review GUI - do scenarios match behavior, fields, URLs, design rules etc? Report any inconsistencies to user - do not blindly fix; at this point deviations in GUI/behavior are likely intentional

### ✅ Diagram Creation (`do-diagrams-element-by-element.md`)
- [ ] Draw.io diagrams exist for the feature (check for .drawio files)
- [ ] Diagrams are visually clear and accurate (open and review diagrams)

### ✅ TODO Management (`do-add-todos-for-incomplete-items.md`)
- [ ] TODO comments exist for incomplete implementations (search codebase for TODO)
- [ ] TODO items have clear descriptions (verify TODO comment quality)
- [ ] TODOs in dependencies can be ignored

### ✅ Document Updates
- [ ] Review code: do we introduce new packages, patterns, approaches in backend/frontend/middleware worth documenting? Check if they're in docs/architecture/SAO.md already. Update them.
- [ ] Review conversation: do we need to update feature files/corrections user provided? Update them.
- [ ] Review modus operandi, bugs, and course corrections against .windsurf/workflows/* and .windsurf/rules/* - can we create/update rule(s) and workflow(s) to prevent it from happening? Suggest these improvements to the user.

## Final Validation

### ✅ Overall Quality Check
- [ ] Feature meets acceptance criteria (verify against requirements)
- [ ] Code is production-ready (no debug statements, proper error handling)
- [ ] Documentation exists and is accurate (check README, docstrings)

### ✅ Integration Validation
- [ ] Feature integrates with existing system (run integration tests)
- [ ] No breaking changes introduced (verify backward compatibility)
- [ ] Dependencies are properly declared in requirements.txt

### ✅ Deployment Readiness
- [ ] Database migrations exist if needed (check migrations folder)
- [ ] Environment variables are documented (check .env.example or docs)
- [ ] Configuration changes are documented (check config files)

### ✅ Cleanup
- [ ] Remove temporary files like debug_*.py
- [ ] Scan file structure - if there are stray misplaced tests, configs, old *.md files used to guide implementation - wipe them out
- [ ] Remove *.log files from repository

**Notes:**
- All checkboxes must be completed before considering the story "Done"
- Any deviations from the rules must be presented to the user and you must ask for explicit skip of these steps, or resolution directions, eg "implement all missing following the rules"
- If user says "collect these for cleanup but defer" - try to create a Backlog item summarizing what needs to be done in GitHub as Issue with "deferred" tag
- Otherwise resolve deviations as directed by user, commit following .windsurf/rules/do-follow-commit-convention.md
- Send Pull Request
