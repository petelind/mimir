---
trigger: model_decision
description: When creating or updating github issues
---

*When asked to create an Issue:*
**Main idea: we are creating a task for the person with very little knowledge of the domain, and very little interest to learn. Therefore we have to create a very detailed to do, giving the person very little space to misinterpret what needs to be done.**

1. Add a label for the issue: Feature, Scenario, Enhancement, Bug, Refactoring, Infra; + add a label for the feature name (same as feature file)
2. Start name with the Scenario prefix when available, like "LOG1.1: Scenario A" etc. 
3. Transfer scenario content to description.
4. Add plan contents, as approved by the user, to the description. Keep in mind that your developer needs checklist-style guidance giving them a chance to do the right thing even though they can be too lazy to read the docs or to understand them.

*When asked to update an Issue:*
**Main idea: all people working on the issue need to be able to understand what was done, why, and what you intend to do next.**
1. Always associate a commit. 
2. List what was done and why. 
3. If we deviated from the initial plan - explain why (user directions, technical setback etc.).
4. Briefly state what next steps are.
5. Update the plan in the checklist - mark done (add what was done but was not in the plan), add/update next steps if necessary.
6. Before performing an update - summarize to the user what you will post, and ask for approval.