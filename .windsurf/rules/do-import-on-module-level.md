---
trigger: model_decision
description: When writing code and importing other modules and/or methods/constants
---

Do not import locally inside the method - import at the module level. It will make patching and mocking easier for you.