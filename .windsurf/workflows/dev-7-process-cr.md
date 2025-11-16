---
description: Process an enhancement or a change request in a consistent manner
auto_execution_mode: 3
---

1. Plan the implementation:
- Understand which part of the system will be changed
- If you don't understand user intent or implementation details - DO NOT ASSUME, ASK. For example: "It is unclear what shall I use to accept values from 1-5. Shall I assume we use a select dropdown, or a different UI element?"
- Identify and review feature file(s) and scenario affected: plan changes
- Read architecture (docs/architecture/SAO.md): identify if changes are required and which part of the architecture document will affect our implementation
- Identify Models to add/extend/change
- Identify Django Views to add/extend/change. Follow .windsurf/workflows/dev-2-implement-backend.md guidance to plan your backend work
- Identify Django Templates to add/extend/change. Follow .windsurf/workflows/dev-3-implement-frontend.md to plan your frontend work
- Read all the guidelines in docs/architecture/SAO.md - adjust/extend your plan to incorporate specific guidance from these
- Plan tests to be modified/added/dropped

2. Present change implementation plan as .md for the user review. Ask clarification questions.

3. Execute the plan. Commit after completing every step of the plan, but DO NOT PUSH UNTIL USER SAYS SO.
