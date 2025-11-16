---
description: Review PR from copilot
auto_execution_mode: 3
---

1. If user does not specify PR # - check what do we have in github. If more than one - ask which one user wants you to review. If there is one - confirm that its the one user wants to work on.

2. Identify issue we've been working on. Check the description - note what needs to be done.merge and note [ ] expected to be completed.

3. Checkout PRs branch. Review what actually was done - the diff and the code added. Update completed [ ]. 

4. Check .windsurf/workflows/dev-5-check-dod.md - is anything amiss?

5. Summarize review for the user:
a) what was done and what is outstanding
b) rules violated / DOD items amiss
c) any other error misgivings
d) your suggestion: approve/request changes [ list of changes ].

5. Follow user gudiance - if approve then:
a) perform .windsurf/workflows/dev-6-finalize-feature.md
b) merge and close PR
c) close issue if not closed via PR

6. If rejected:
a) state list of changes requested
b) create a comment calling out @copilot and asking to implement work
