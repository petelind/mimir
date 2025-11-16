---
trigger: model_decision
description: When user found a bug, you found a bug via logs, or we investigated indesired behavior, or bug was otherwise reported
---

When the bug was discovered, you performed and investigation anf fix, ask yourself - "why our current test(s) was not able to find it?"
If there is no test for that part of functionality - time to create it.
If there are test(s) for that part of functionality - extend it to prove that the bug does not exist anymore.
When completing the fix - run the test to prove that bug does not exist.