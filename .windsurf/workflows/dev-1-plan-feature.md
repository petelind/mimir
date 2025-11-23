---
description: Plan and specify a new feature implementation
auto_execution_mode: 3
---

# Feature Planning Workflow

0. Reset the plan. If there were work in progress - follow .windsurf/rules/do-add-todos-for-incomplete-items.md.

1. Read the docs/architecture/SAO.md - identify parts relevant to the current implementation. Use it to guide your implementation.

2. Check docs/features/user_journey.md [if it exists] - understand what we are building and how it integrates with other parts.

3. Read the feature specification thoroughly. If none exists - suggest we create one for starter. Use .windsurf/rules/do-write-scenarios.md as guidance. If there are more than 2 scenarios inside and user did not specify scenario we are working on, or there are scenarios longer than 10 lines - suggest that we go scenario-by-scenario.

4. Assess current state of the codebase:
   a) If there are components/views/services you can reuse/extend/hook to - tell user about that, and ask if we shall integrate them or replace them.
   b) When looking at components/methods - check that implementation actually exists, and it's not just a stub raising NotImplementedError.
   c) If there are items we can reuse but they are not covered with tests - add implementing tests for them into the plan to restore test coverage.

5. Ask any clarification questions about the feature requirements, scenario by scenario. Update feature file and implementation plan based on answers. If there are more than 5 questions total - create $FEAT.X.Y.Z_Clarifications.MD, put questions there, and present it to user so they can answer.

6. Write a step-by-step, todo-style, highly atomic implementation plan covering:
   - Start a new branch feature/feature-name and checkout there
   - Use "Plan mode" for planning
   - Read .windsurf/workflows/dev-2-implement-backend.md
   - Go scenario-by-scenario, and plan per dev-2-implement-backend.md:
      - Models and data design
      - Registering new models with the /admin module
      - Utility/helper functions
      - Services (business logic shared by MCP and Web UI)
      - Repository methods for data access
      - Django Views (returning HTML templates)
      - Django Templates with HTMX
      - URL patterns
      - Associated tests: unit, integration (NO MOCKING!), view tests
      - Explicitly list tests you will create and what they are testing for in the plan
   - Read .windsurf/workflows/dev-3-implement-frontend.md. Plan for:
      - New/changed Django templates
      - HTMX interactions
      - Template partials for dynamic content
      - Graph visualizations with Graphviz (if needed)
      - Form handling
      - Semantic `data-testid` attributes for testing
   - Add task to commit, push, and associate update with the issue we are working on after every principal step following .windsurf/rules/do-github-issues.md (as separate tasks)
   - Whatever else needs to be done

7. Now review the plan and for every major step:
   a) For each of the tasks add "re-read do-some-relevant-rule-name.md before implementing and act accordingly" for every major step
   b) Add committing and updating implementation plan/associated issue after each major step

8. Do not add hours/days to the plan - it's for AI to execute, so human estimates are pointless.

9. Submit the plan to the user for review and approval before proceeding to implementation. Create FEATURECODE_IMPLEMENTATION_PLAN.MD in the docs/plans.

10. If there is a GitHub repo for this project - find or create an issue for this scenario/enhancement (if there is none). Follow .windsurf/rules/do-github-issues.md