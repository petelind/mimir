---
description: Implement Django templates and HTMX interactions
auto_execution_mode: 3
---

# Frontend Implementation Workflow

**IMPORTANT**: 
I. Frontend is Django templates with HTMX for interactivity. Server-side rendering with minimal JavaScript.
II. Read docs/ux/IA_guidelines.md before implementing the form and identify sections which will be applied to the page/component we are working on.

1. Review URL routing and template structure:
   - Check Django URL patterns - does anything need to be added or changed?
   - Plan template hierarchy (base templates, partials, pages)
   - Identify HTMX interactions needed
   - Read and follow .windsurf/rules/do-django-views-htmx.md

2. Implement Django templates with HTMX:
   - **A. Page Templates**: Full HTML pages (inherit from base.html)
   - **B. Template Partials**: HTML fragments for HTMX updates (in templates/*/partials/)
   - **C. HTMX Attributes**: Use hx-get, hx-post, hx-target, hx-swap for interactions
   - **D. Forms**: Django forms with HTMX submission
   - **E. Graph Visualizations**: Graphviz SVG embedded in templates
   - Follow .windsurf/rules/do-semantic-versioning-on-ui-elements.md for naming
   - Add `data-testid` attributes to all interactive elements
   - Work in small increments per .windsurf/rules/do-small-increments.md

3. Template Implementation Pattern:
   ```django
   {# templates/methodology/workflow_detail.html #}
   {% extends "base.html" %}
   
   {% block content %}
   <div data-testid="workflow-detail">
       <h1 data-testid="workflow-title">{{ workflow.name }}</h1>
       
       {# Graphviz SVG graph #}
       <div data-testid="workflow-graph-container" class="graph-container">
           {{ svg|safe }}
       </div>
       
       {# HTMX activity list #}
       <div id="activity-list" data-testid="activity-list">
           {% include 'methodology/partials/activity_list.html' %}
       </div>
       
       {# HTMX button to load detail #}
       <button data-testid="create-activity-button"
               hx-get="{% url 'activity_create' workflow.id %}"
               hx-target="#detail-panel"
               hx-swap="innerHTML">
           Create Activity
       </button>
   </div>
   {% endblock %}
   ```

4. HTMX Interaction Patterns:
   - **Navigation**: hx-get with target div swap
   - **Forms**: hx-post returning updated content or form validation
   - **Dynamic Lists**: hx-get to refresh list partials
   - **Modals/Dialogs**: HTML dialog element with HTMX content loading
   - Add minimal JavaScript only for:
     * Making SVG links work with HTMX
     * Client-side validation enhancement
     * Tooltips/hover effects
   - Follow .windsurf/rules/do-minimal-js-logging.md for any JS needed

5. Form Handling with HTMX:
   ```django
   {# templates/methodology/partials/activity_form.html #}
   <form hx-post="{% url 'activity_edit' activity.id %}"
         hx-target="#detail-panel"
         hx-swap="innerHTML"
         data-testid="activity-form">
       {% csrf_token %}
       
       <div data-testid="activity-name-field">
           <label for="id_name">Name *</label>
           <input type="text" 
                  id="id_name" 
                  name="name"
                  data-testid="activity-name-input"
                  value="{{ form.name.value|default:'' }}"
                  required>
           {% if form.name.errors %}
               <div data-testid="activity-name-error" class="error">
                   {{ form.name.errors }}
               </div>
           {% endif %}
       </div>
       
       <button type="submit" data-testid="save-activity-button">
           Save
       </button>
   </form>
   ```

6. Development testing:
   - Start Django development server: `python manage.py runserver`
   - Test at http://localhost:8000
   - Check browser console for HTMX events and errors
   - Verify forms submit correctly
   - Test graph visualizations render properly
   - Validate HTMX updates work without full page reloads

7. Add semantic test IDs for E2E compatibility:
   - Follow `.windsurf/rules/do-semantic-versioning-on-ui-elements.md` for naming conventions
   - Add `data-testid` attributes using kebab-case
   - Example: `data-testid="activity-card"`, `data-testid="create-activity-button"`
   - Use semantic names that describe purpose, not structure
   - Required on: buttons, links, form inputs, containers, error messages

8. Styling:
   - Read docs/ux/IA_guidelines.md to identify what applies to the page/component we are building and apply them
   - Use simple CSS (no complex frameworks needed)
   - Keep styles in static/css/
   - Use semantic HTML elements
   - Ensure responsive design

9. Commit frontend changes using Angular-style commit messages.

10. Integration validation:
   - Verify all Django views return correct templates
   - Check HTMX interactions update correct target elements
   - Ensure forms handle validation errors properly
   - Test Graphviz SVG graphs render correctly
   - Validate `data-testid` attributes are present for testing