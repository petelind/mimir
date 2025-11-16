---
trigger: model_decision
description: When working on a test, especially on the integration tests in the tests/integration/
---

Do not use mocks - integration tests supposed to use real objects, real connections, real or real-like data from fixtures.
Think of them as acceptance tests - just without UI.