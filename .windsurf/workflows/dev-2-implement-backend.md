---
description: Implement backend services, models, and Django views
auto_execution_mode: 3
---

# Backend Implementation Workflow

1. Create all class and method skeletons with `NotImplementedError` and full docstrings.
   - Use .windsurf/rules/do-skeletons-first.md guidance
   - Include proper ReST/Sphinx docstrings for all methods

2. Write unit tests before writing method logic.
   - Follow .windsurf/rules/do-test-first.md
   - Use .windsurf/rules/do-runner.md for test execution
   - Remember: .windsurf/rules/do-not-mock-in-integration-tests.md

3. Implement logic incrementally using small increments:
   - Work method-by-method following .windsurf/rules/do-small-increments.md
   - Each method/property should be: implemented → tested → committed separately
   - Follow .windsurf/rules/do-write-concise-methods.md for clean code structure

4. Ensure comprehensive logging & error handling:
   - Follow .windsurf/rules/add-logging.md
   - Add informative logs per .windsurf/rules/do-informative-logging.md
   - Log all service calls and view actions to `logs/app.log` at INFO level
   - Always handle specific and general exceptions gracefully
   - Include correlation_id in error responses for debugging

5. After each implementation step:
   - Write → run → test → evaluate → fix
   - Commit using Angular-style commit messages (.windsurf/rules/do-follow-commit-convention.md)

6. Django Views Architecture:
   - **Services Layer**: Business logic shared between MCP and Web UI
   - **Repository Pattern**: Data access abstraction (currently Django ORM, can be swapped to Neo4j)
   - **Django Views**: Return rendered HTML templates (NOT JSON/DRF)
   - **HTMX Endpoints**: Return HTML fragments for dynamic updates
   - **Template Context**: Always validate and document context per .windsurf/rules/do-validate-template-context.md

7. View Implementation Pattern:
   ```python
   from django.shortcuts import render, get_object_or_404
   from methodology.services import MethodologyService
   from methodology.repository import DjangoORMRepository
   
   def workflow_detail(request, workflow_id):
       """
       Display workflow detail with graph.
       
       Template: methodology/workflow_detail.html
       Context:
           workflow: Workflow instance
           svg: str - SVG markup from Graphviz
           activities: QuerySet of activities
       """
       service = MethodologyService(DjangoORMRepository())
       workflow_data = service.get_workflow_with_activities(workflow_id)
       
       # Generate graph
       from methodology.services import GraphService
       graph_service = GraphService(DjangoORMRepository())
       svg = graph_service.generate_workflow_graph(workflow_id)
       
       return render(request, 'methodology/workflow_detail.html', {
           'workflow': workflow_data,
           'svg': svg
       })
   ```

8. URL Pattern Registration:
   - Register new views in app urls.py
   - Use descriptive names for URL patterns
   - Follow RESTful conventions for URL structure
   - Example: `path('workflow/<uuid:workflow_id>/', views.workflow_detail, name='workflow_detail')`

9. Testing Django Views:
   - Use Django TestCase (NOT DRF test clients)
   - Test with Django test client: `self.client.get(url)`
   - Validate template context: `self.assertIn('workflow', response.context)`
   - Check template used: `self.assertTemplateUsed(response, 'methodology/workflow_detail.html')`
   - Test HTMX endpoints: `self.client.get(url, HTTP_HX_REQUEST='true')`
