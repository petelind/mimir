---
description: Provision project infrastructure for testing with pytest and Playwright
auto_execution_mode: 3
---

1. Initialize git repo. Commit after every step following angular convention.
3. Create .venv
4. Switch to uv, maintain pyproject.toml
2. Create django app using django scaffolding command.
3. Create React TS app with the zite and zustand; use their scaffolding tools not file generation.
4. Install shadcdn per https://ui.shadcn.com/docs/installation/vite
5. Enable static files being served with whitenoise.
6. Create a logging configuration with the context_id propagation to have app.log like this: 2025-08-14 15:56:58,033 [INFO] [req_mebl16ky_wagsey] apps.workshop.models.indicator.evaluate:387 [user=anonymous|session=None|ip=unknown] [stack=req_mebl16ky_wagsey|duration=0.157s] - Retrieved DataFrame for dataset 'dataset' with shape (470, 112)
7. install spectacular