# FOB-ARTIFACTS Implementation Plan for GitHub Copilot

## Executive Summary

**Feature**: Artifacts Management (ACT-6)  
**Complexity**: Medium-High (6 feature files with 53 total scenarios)  
**Estimated Components**: 10 classes, ~50 methods  
**Architecture Pattern**: Service-Repository-View (Django + HTMX)

**Definition**: Artifacts are **outputs produced by activities; definitely will be used as INPUT by some Activities downstream in the Workflow**. Examples:
- Code files: `ArtifactController.py`, `TestLoginFlow.py`
- Documentation: `artifacts.feature`, `API_SPEC.md`
- Scenarios: `Scenario: FOB-1 Login...`
- Templates: Component boilerplate files
- Diagrams: Architecture diagrams, flow charts

---

## Architecture Context (from SAO.md)

### Core Principles

1. **Repository Pattern**: Storage-agnostic data access
2. **Service Layer**: Business logic shared between MCP and Web UI
3. **HTMX + Django Templates**: Server-rendered UI, minimal JS
4. **Test-First**: Unit → Integration → E2E (pytest, no mocking in integration tests)
5. **Semantic testid attributes**: All interactive elements must have `data-testid`

### Existing Patterns to Follow

**Model Pattern** (from `Activity`, `Workflow`, `Playbook`):
```python
class Artifact(models.Model):
    """
    Artifact represents a deliverable/output produced by an activity.
    
    Examples: code files, documentation, test scenarios, templates, diagrams.
    """
    # Relationships
    activity = models.ForeignKey('Activity', ...)
    playbook = models.ForeignKey('Playbook', ...)  # For breadcrumbs/context
    
    # Core fields
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=ARTIFACT_TYPES)
    
    # Flags
    is_required = models.BooleanField(default=False)
    
    # File storage (optional)
    template_file = models.FileField(upload_to='artifacts/templates/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['activity', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['activity', 'name'],
                name='unique_artifact_per_activity'
            )
        ]
```

**Service Pattern** (from `ActivityService`, `WorkflowService`):
```python
class ArtifactService:
    """Service class for artifact CRUD operations."""
    
    @staticmethod
    def create_artifact(activity, name, description='', artifact_type='Document', 
                       is_required=False, template_file=None):
        """
        Create artifact with validation.
        
        :param activity: Parent activity instance. Example: Activity.objects.get(id=1)
        :param name: Artifact name as str (max 200 chars). Example: "Component Design Document"
        :param description: Artifact description as str. Example: "Detailed component architecture"
        :param artifact_type: Type as str from ARTIFACT_TYPES. Example: "Document"
        :param is_required: Required flag as bool. Example: True
        :param template_file: Uploaded file or None. Example: InMemoryUploadedFile(...)
        :returns: Created Artifact instance
        :raises ValidationError: If validation fails (empty name, invalid type, etc.)
        
        Example:
            >>> artifact = ArtifactService.create_artifact(
            ...     activity=activity,
            ...     name="API Specification",
            ...     artifact_type="Document",
            ...     is_required=True
            ... )
        """
        # Implementation with validation, logging, error handling
```

**View Pattern** (from `activity_views.py`, `playbook_views.py`):
```python
def artifact_list(request, playbook_id):
    """
    Display artifacts list for playbook with search/filter.
    
    :param request: Django HttpRequest
    :param playbook_id: Playbook ID as int from URL
    :returns: HttpResponse with rendered template
    
    Template: artifacts/list.html
    Context:
        - playbook: Playbook instance
        - artifacts: QuerySet of Artifact instances
        - search_query: str or None
        - type_filter: str or None
    """
    # Get playbook with error handling
    # Apply search/filters
    # Render template with context
```

---

## UI/UX Patterns (from IA_guidelines.md)

### Navigation Integration

**Navbar Link** (Currently disabled - will activate when feature complete):
```html
<!-- In templates/base.html navbar -->
<li class="nav-item">
  <a class="nav-link {% if '/artifacts/' in request.path %}active{% endif %}" 
     href="/artifacts/"
     data-testid="nav-artifacts"
     data-bs-toggle="tooltip"
     title="Manage artifacts and deliverables"
     {% if '/artifacts/' in request.path %}aria-current="page"{% endif %}>
    <i class="fa-solid fa-gift me-2"></i>
    Artifacts
  </a>
</li>
```

**Icon**: `fa-gift` (deliverables are "gifts" produced by the process)

### Page Structure Pattern

**LIST+FIND Page**:
```html
<!-- Breadcrumbs -->
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="/">Home</a></li>
    <li class="breadcrumb-item"><a href="/playbooks/{{ playbook.id }}/">{{ playbook.name }}</a></li>
    <li class="breadcrumb-item active">Artifacts</li>
  </ol>
</nav>

<!-- Page Header with Actions -->
<div class="d-flex justify-content-between align-items-center mb-4">
  <h1 class="h3 mb-0">Artifacts in {{ playbook.name }}</h1>
  <button class="btn btn-primary" 
          data-testid="btn-create-artifact"
          data-bs-toggle="tooltip"
          title="Create new artifact">
    <i class="fa-solid fa-plus me-2"></i>
    Create New Artifact
  </button>
</div>

<!-- Search and Filters -->
<div class="card mb-3">
  <div class="card-body">
    <div class="row g-3">
      <div class="col-md-4">
        <input type="text" 
               class="form-control" 
               placeholder="Search artifacts..."
               data-testid="input-search-artifacts">
      </div>
      <div class="col-md-3">
        <select class="form-select" data-testid="select-type-filter">
          <option value="">All Types</option>
          <option value="Document">Document</option>
          <option value="Template">Template</option>
          <option value="Code">Code</option>
          <option value="Diagram">Diagram</option>
          <option value="Data">Data</option>
          <option value="Other">Other</option>
        </select>
      </div>
      <div class="col-md-3">
        <select class="form-select" data-testid="select-required-filter">
          <option value="">All Artifacts</option>
          <option value="required">Required Only</option>
        </select>
      </div>
    </div>
  </div>
</div>

<!-- Data Table -->
<div class="card">
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th>Activity</th>
          <th>Required</th>
          <th>Status</th>
          <th class="text-end">Actions</th>
        </tr>
      </thead>
      <tbody>
        {% for artifact in artifacts %}
        <tr data-testid="artifact-row-{{ artifact.id }}">
          <td>
            <a href="{% url 'artifact_detail' artifact.id %}" 
               data-testid="link-artifact-{{ artifact.id }}">
              {{ artifact.name }}
            </a>
          </td>
          <td>
            <span class="badge bg-info">{{ artifact.type }}</span>
          </td>
          <td>
            <a href="{% url 'activity_detail' artifact.activity.id %}">
              {{ artifact.activity.name }}
            </a>
          </td>
          <td>
            {% if artifact.is_required %}
              <span class="badge bg-danger">Required</span>
            {% else %}
              <span class="badge bg-secondary">Optional</span>
            {% endif %}
          </td>
          <td>
            <span class="badge bg-success">Active</span>
          </td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-primary"
                    data-testid="btn-view-{{ artifact.id }}"
                    data-bs-toggle="tooltip"
                    title="View artifact details">
              <i class="fa-solid fa-eye"></i>
            </button>
            <button class="btn btn-sm btn-outline-secondary"
                    data-testid="btn-edit-{{ artifact.id }}"
                    data-bs-toggle="tooltip"
                    title="Edit artifact">
              <i class="fa-solid fa-pen-to-square"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger"
                    data-testid="btn-delete-{{ artifact.id }}"
                    data-bs-toggle="tooltip"
                    title="Delete artifact">
              <i class="fa-solid fa-trash-can"></i>
            </button>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="6" class="text-center py-5">
            <i class="fa-solid fa-gift fa-3x text-muted mb-3"></i>
            <p class="text-muted">No artifacts yet</p>
            <button class="btn btn-primary" data-testid="btn-create-first-artifact">
              <i class="fa-solid fa-plus me-2"></i>
              Create First Artifact
            </button>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
```

### Form Validation Pattern

**Field-Level Errors** (underneath invalid field):
```html
<div class="mb-3">
  <label for="name" class="form-label">
    Artifact Name <span class="text-danger">*</span>
  </label>
  <input type="text" 
         class="form-control {% if errors.name %}is-invalid{% endif %}" 
         id="name"
         name="name"
         value="{{ form_data.name }}"
         data-testid="input-artifact-name"
         required>
  {% if errors.name %}
  <div class="invalid-feedback">
    <i class="fa-solid fa-circle-exclamation me-1"></i>
    {{ errors.name }}
  </div>
  {% endif %}
</div>
```

**Form-Level Errors** (top of form):
```html
{% if form_errors %}
<div class="alert alert-danger alert-dismissible fade show" role="alert">
  <i class="fa-solid fa-triangle-exclamation me-2"></i>
  <strong>Validation failed:</strong>
  <ul class="mb-0">
    {% for error in form_errors %}
    <li>{{ error }}</li>
    {% endfor %}
  </ul>
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
{% endif %}
```

### Bootstrap Components to Use

- **Cards**: `.card`, `.card-body`, `.card-header`
- **Tables**: `.table`, `.table-hover`, `.table-responsive`
- **Forms**: `.form-control`, `.form-select`, `.form-label`, `.form-check`
- **Buttons**: `.btn`, `.btn-primary`, `.btn-outline-*`, `.btn-sm`
- **Badges**: `.badge`, `.bg-primary`, `.bg-success`, `.bg-danger`
- **Modals**: `.modal`, `.modal-dialog`, `.modal-content`
- **Tooltips**: `data-bs-toggle="tooltip"`, `title="..."`
- **Alerts**: `.alert`, `.alert-success`, `.alert-danger`

---

## Implementation Plan

### Phase 1: Foundation (Models + Admin)

#### Task 1.1: Create Artifact Model

**File**: `methodology/models/artifact.py`

**Skeleton**:
```python
"""
Artifact model for deliverables produced by activities.

Artifacts represent outputs like code files, documentation, test scenarios,
templates, and diagrams that are created as part of workflow execution.
"""

from django.db import models
from django.core.exceptions import ValidationError


class Artifact(models.Model):
    """
    Artifact represents a deliverable/output produced by an activity.
    
    Examples: code files (TestLoginFlow.py), documentation (API_SPEC.md),
    scenarios (Scenario: FOB-1 Login...), templates, diagrams.
    
    Each artifact belongs to an activity and can optionally have a template file.
    """
    
    # Type choices
    ARTIFACT_TYPES = [
        ('Document', 'Document'),
        ('Template', 'Template'),
        ('Code', 'Code'),
        ('Diagram', 'Diagram'),
        ('Data', 'Data'),
        ('Other', 'Other'),
    ]
    
    # Producer relationship (1:1 - every artifact has exactly one producer)
    produced_by = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
        related_name='output_artifacts',
        help_text="Activity that produces this artifact as output"
    )
    
    # For breadcrumbs and context (denormalized for performance)
    playbook = models.ForeignKey(
        'Playbook',
        on_delete=models.CASCADE,
        related_name='artifacts',
        help_text="Playbook containing this artifact (via activity->workflow->playbook)"
    )
    
    # Core fields
    name = models.CharField(
        max_length=200,
        help_text="Artifact name - must be unique within activity"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the artifact and its purpose"
    )
    type = models.CharField(
        max_length=50,
        choices=ARTIFACT_TYPES,
        default='Document',
        help_text="Type of artifact"
    )
    
    # Flags
    is_required = models.BooleanField(
        default=False,
        help_text="Whether this artifact is required for activity completion"
    )
    
    # File storage (optional template)
    template_file = models.FileField(
        upload_to='artifacts/templates/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Optional template file for this artifact"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['activity', 'name']
        verbose_name = 'Artifact'
        verbose_name_plural = 'Artifacts'
        constraints = [
            models.UniqueConstraint(
                fields=['activity', 'name'],
                name='unique_artifact_per_activity',
                violation_error_message="An artifact with this name already exists in this activity"
            )
        ]
        indexes = [
            models.Index(fields=['activity', 'name']),
            models.Index(fields=['playbook', 'type']),
            models.Index(fields=['is_required']),
        ]
    
    def __str__(self):
        """
        String representation.
        
        :returns: Artifact name as str. Example: "Component Design Document"
        """
        return self.name
    
    def clean(self):
        """
        Model-level validation.
        
        :raises ValidationError: If validation fails
        """
        # Validate name
        if not self.name or not self.name.strip():
            raise ValidationError({'name': "Artifact name cannot be empty"})
        
        # Validate type
        valid_types = [choice[0] for choice in self.ARTIFACT_TYPES]
        if self.type not in valid_types:
            raise ValidationError({'type': f"Invalid artifact type. Must be one of: {', '.join(valid_types)}"})
        
        # Auto-set playbook from producer activity if not set
        if self.produced_by_id and not self.playbook_id:
            self.playbook = self.produced_by.workflow.playbook
    
    def save(self, *args, **kwargs):
        """
        Override save to run validation.
        
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """
        Get URL for artifact detail page.
        
        :returns: URL path as str. Example: "/artifacts/123/"
        """
        from django.urls import reverse
        return reverse('artifact_detail', kwargs={'pk': self.pk})
    
    def get_producer_link(self):
        """
        Get URL for producer activity.
        
        :returns: URL path as str. Example: "/activities/45/"
        """
        return self.produced_by.get_absolute_url()
    
    def get_consumers(self):
        """
        Get all activities that consume this artifact as input.
        
        :returns: QuerySet of ArtifactInput instances
        """
        return self.inputs.all()
    
    def get_consumer_count(self):
        """
        Get count of activities consuming this artifact.
        
        :returns: int count. Example: 3
        """
        return self.inputs.count()
    
    def get_playbook_link(self):
        """
        Get URL for parent playbook.
        
        :returns: URL path as str. Example: "/playbooks/12/"
        """
        return self.playbook.get_absolute_url()
    
    def has_template(self):
        """
        Check if artifact has a template file.
        
        :returns: True if template exists, False otherwise
        """
        return bool(self.template_file)
    
    def get_template_filename(self):
        """
        Get template filename without path.
        
        :returns: Filename as str or None. Example: "component_template.tsx"
        """
        if self.template_file:
            return self.template_file.name.split('/')[-1]
        return None
    
    def to_dict(self):
        """
        Convert to dictionary for API/MCP responses.
        
        :returns: Dict representation. Example: {"id": 1, "name": "API Spec", "type": "Document", ...}
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'is_required': self.is_required,
            'has_template': self.has_template(),
            'template_filename': self.get_template_filename(),
            'produced_by_id': self.produced_by_id,
            'produced_by_name': self.produced_by.name,
            'consumer_count': self.get_consumer_count(),
            'playbook_id': self.playbook_id,
            'playbook_name': self.playbook.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
```

**Tests to Create**: `tests/unit/test_artifact_model.py`
- `test_create_artifact_minimal`
- `test_create_artifact_full`
- `test_artifact_unique_per_activity`
- `test_artifact_validation_empty_name`
- `test_artifact_validation_invalid_type`
- `test_artifact_auto_set_playbook`
- `test_artifact_str_representation`
- `test_artifact_to_dict`
- `test_artifact_has_template`

**Checklist**:
- [ ] Create `methodology/models/artifact.py` with complete model
- [ ] Add to `methodology/models/__init__.py`: `from .artifact import Artifact`
- [ ] Create migration: `python manage.py makemigrations`
- [ ] Run migration: `python manage.py migrate`
- [ ] Create unit tests in `tests/unit/test_artifact_model.py`
- [ ] Run tests: `pytest tests/unit/test_artifact_model.py -v`
- [ ] Verify 100% pass rate
- [ ] Commit: `feat(models): add Artifact model with validation and file upload`

---

#### Task 1.2: Register Artifact in Admin

**File**: `methodology/admin.py`

**Add**:
```python
from methodology.models import Artifact

@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    """Admin interface for Artifact model."""
    
    list_display = ['name', 'type', 'activity', 'playbook', 'is_required', 'has_template', 'created_at']
    list_filter = ['type', 'is_required', 'created_at']
    search_fields = ['name', 'description', 'activity__name', 'playbook__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'description', 'type']
        }),
        ('Relationships', {
            'fields': ['activity', 'playbook']
        }),
        ('Settings', {
            'fields': ['is_required', 'template_file']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def has_template(self, obj):
        """Display whether artifact has template file."""
        return obj.has_template()
    has_template.boolean = True
    has_template.short_description = 'Has Template'
```

**Checklist**:
- [ ] Add `ArtifactAdmin` to `methodology/admin.py`
- [ ] Test in Django admin: `python manage.py runserver`
- [ ] Verify CRUD operations work in admin
- [ ] Commit: `feat(admin): register Artifact model in Django admin`

---

### Phase 2: Service Layer

#### Task 2.1: Create ArtifactService

**File**: `methodology/services/artifact_service.py`

**Skeleton** (following `ActivityService` pattern):
```python
"""
Service layer for Artifact operations.

Provides business logic for artifact CRUD operations, validation,
and filtering functionality.
"""

import logging
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from methodology.models import Artifact, Activity

logger = logging.getLogger(__name__)


class ArtifactService:
    """Service class for artifact operations."""
    
    @staticmethod
    def create_artifact(activity, name, description='', artifact_type='Document',
                       is_required=False, template_file=None):
        """
        Create artifact with validation.
        
        :param activity: Parent activity instance. Example: Activity.objects.get(id=1)
        :param name: Artifact name as str (max 200 chars). Example: "Component Design Document"
        :param description: Artifact description as str. Example: "Detailed component architecture"
        :param artifact_type: Type as str from Artifact.ARTIFACT_TYPES. Example: "Document"
        :param is_required: Required flag as bool. Example: True
        :param template_file: Uploaded file or None. Example: InMemoryUploadedFile(...)
        :returns: Created Artifact instance
        :raises ValidationError: If validation fails (empty name, invalid type, duplicate, etc.)
        
        Example:
            >>> artifact = ArtifactService.create_artifact(
            ...     activity=activity,
            ...     name="API Specification",
            ...     description="RESTful API documentation",
            ...     artifact_type="Document",
            ...     is_required=True
            ... )
        """
        # Implementation
        pass
    
    @staticmethod
    def update_artifact(artifact, name=None, description=None, artifact_type=None,
                       is_required=None, template_file=None):
        """
        Update artifact fields.
        
        :param artifact: Artifact instance to update
        :param name: New name as str or None. Example: "Updated API Spec"
        :param description: New description as str or None
        :param artifact_type: New type as str or None
        :param is_required: New required flag as bool or None
        :param template_file: New template file or None
        :returns: Updated Artifact instance
        :raises ValidationError: If validation fails
        
        Example:
            >>> artifact = ArtifactService.update_artifact(
            ...     artifact=artifact,
            ...     name="Updated Component Design",
            ...     is_required=True
            ... )
        """
        # Implementation
        pass
    
    @staticmethod
    def delete_artifact(artifact):
        """
        Delete artifact and associated template file.
        
        :param artifact: Artifact instance to delete
        :returns: Dict with deletion confirmation. Example: {"deleted": True, "artifact_id": 123}
        
        Example:
            >>> result = ArtifactService.delete_artifact(artifact)
            >>> result
            {"deleted": True, "artifact_id": 123, "name": "API Spec"}
        """
        # Implementation
        pass
    
    @staticmethod
    def get_artifacts_for_activity(activity):
        """
        Get all artifacts for an activity.
        
        :param activity: Activity instance
        :returns: QuerySet of Artifact instances ordered by name
        
        Example:
            >>> artifacts = ArtifactService.get_artifacts_for_activity(activity)
            >>> artifacts.count()
            5
        """
        # Implementation
        pass
    
    @staticmethod
    def get_artifacts_for_playbook(playbook, artifact_type=None, required_only=False):
        """
        Get all artifacts for a playbook with optional filters.
        
        :param playbook: Playbook instance
        :param artifact_type: Filter by type as str or None. Example: "Document"
        :param required_only: Filter required artifacts only as bool. Example: True
        :returns: QuerySet of Artifact instances
        
        Example:
            >>> artifacts = ArtifactService.get_artifacts_for_playbook(
            ...     playbook=playbook,
            ...     artifact_type="Document",
            ...     required_only=True
            ... )
        """
        # Implementation
        pass
    
    @staticmethod
    def search_artifacts(playbook, search_query):
        """
        Search artifacts by name or description.
        
        :param playbook: Playbook instance to search within
        :param search_query: Search term as str. Example: "design"
        :returns: QuerySet of matching Artifact instances
        
        Example:
            >>> artifacts = ArtifactService.search_artifacts(playbook, "component")
            >>> [a.name for a in artifacts]
            ["Component Design Document", "Component Template"]
        """
        # Implementation
        pass
    
    @staticmethod
    def validate_artifact_data(name, artifact_type, activity=None, artifact_id=None):
        """
        Validate artifact data before save.
        
        :param name: Artifact name as str
        :param artifact_type: Artifact type as str
        :param activity: Activity instance or None (for uniqueness check)
        :param artifact_id: Existing artifact ID or None (for update vs create)
        :returns: Dict with validation result. Example: {"valid": True} or {"valid": False, "errors": {...}}
        
        Example:
            >>> result = ArtifactService.validate_artifact_data(
            ...     name="",
            ...     artifact_type="Document",
            ...     activity=activity
            ... )
            >>> result
            {"valid": False, "errors": {"name": "Artifact name cannot be empty"}}
        """
        # Implementation
        pass
```

**Tests to Create**: `tests/unit/test_artifact_service.py`
- `test_create_artifact_success`
- `test_create_artifact_with_template`
- `test_create_artifact_duplicate_name_fails`
- `test_create_artifact_empty_name_fails`
- `test_create_artifact_invalid_type_fails`
- `test_update_artifact_name`
- `test_update_artifact_type`
- `test_update_artifact_template`
- `test_delete_artifact_success`
- `test_get_artifacts_for_activity`
- `test_get_artifacts_for_playbook`
- `test_get_artifacts_for_playbook_filtered_by_type`
- `test_get_artifacts_for_playbook_required_only`
- `test_search_artifacts_by_name`
- `test_search_artifacts_by_description`
- `test_validate_artifact_data_valid`
- `test_validate_artifact_data_empty_name`
- `test_validate_artifact_data_invalid_type`

**Checklist**:
- [ ] Re-read `.windsurf/rules/do-skeletons-first.md` before implementing
- [ ] Create `methodology/services/artifact_service.py` with all methods
- [ ] Add to `methodology/services/__init__.py`: `from .artifact_service import ArtifactService`
- [ ] Create unit tests in `tests/unit/test_artifact_service.py`
- [ ] Run tests: `pytest tests/unit/test_artifact_service.py -v`
- [ ] Verify 100% pass rate
- [ ] Commit: `feat(services): add ArtifactService with CRUD operations`

---

### Phase 3: Views and Templates

#### Task 3.1: Create Artifact URLs

**File**: `methodology/artifact_urls.py`

```python
"""URL patterns for artifact views."""

from django.urls import path
from methodology import artifact_views

urlpatterns = [
    # List and search
    path('playbooks/<int:playbook_id>/artifacts/', 
         artifact_views.artifact_list, 
         name='artifact_list'),
    
    # CRUD operations
    path('artifacts/create/<int:activity_id>/', 
         artifact_views.artifact_create, 
         name='artifact_create'),
    path('artifacts/<int:pk>/', 
         artifact_views.artifact_detail, 
         name='artifact_detail'),
    path('artifacts/<int:pk>/edit/', 
         artifact_views.artifact_edit, 
         name='artifact_edit'),
    path('artifacts/<int:pk>/delete/', 
         artifact_views.artifact_delete, 
         name='artifact_delete'),
    
    # HTMX partials
    path('artifacts/search/', 
         artifact_views.artifact_search_htmx, 
         name='artifact_search_htmx'),
]
```

**Add to main `urls.py`**:
```python
path('', include('methodology.artifact_urls')),
```

**Checklist**:
- [ ] Create `methodology/artifact_urls.py`
- [ ] Add to main `mimir/urls.py`
- [ ] Commit: `feat(urls): add artifact URL patterns`

---

#### Task 3.2: Create Artifact Views

**File**: `methodology/artifact_views.py`

**Skeleton** (following `activity_views.py` pattern):
```python
"""
Views for artifact management.

Provides CRUD operations and listing/search functionality for artifacts.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from methodology.models import Artifact, Activity, Playbook
from methodology.services import ArtifactService

logger = logging.getLogger(__name__)


@login_required
def artifact_list(request, playbook_id):
    """
    Display artifacts list for playbook with search/filter.
    
    :param request: Django HttpRequest
    :param playbook_id: Playbook ID as int from URL. Example: 12
    :returns: HttpResponse with rendered template
    
    Template: artifacts/list.html
    Context:
        - playbook: Playbook instance
        - artifacts: QuerySet of Artifact instances
        - search_query: str or None
        - type_filter: str or None
        - required_filter: bool or None
        - artifact_types: List of type choices
    
    Example URL: /playbooks/12/artifacts/
    """
    # Implementation
    pass


@login_required
def artifact_create(request, activity_id):
    """
    Create new artifact for activity.
    
    :param request: Django HttpRequest
    :param activity_id: Activity ID as int from URL. Example: 45
    :returns: HttpResponse with rendered form or redirect on success
    
    Template: artifacts/create.html
    Context:
        - activity: Activity instance
        - playbook: Playbook instance (for breadcrumbs)
        - artifact_types: List of type choices
        - form_data: Dict with form values (on validation error)
        - errors: Dict with field errors (on validation error)
    
    Example URL: /artifacts/create/45/
    """
    # Implementation
    pass


@login_required
def artifact_detail(request, pk):
    """
    Display artifact details.
    
    :param request: Django HttpRequest
    :param pk: Artifact ID as int from URL. Example: 123
    :returns: HttpResponse with rendered template
    
    Template: artifacts/detail.html
    Context:
        - artifact: Artifact instance
        - playbook: Playbook instance (for breadcrumbs)
        - activity: Activity instance
    
    Example URL: /artifacts/123/
    """
    # Implementation
    pass


@login_required
def artifact_edit(request, pk):
    """
    Edit existing artifact.
    
    :param request: Django HttpRequest
    :param pk: Artifact ID as int from URL. Example: 123
    :returns: HttpResponse with rendered form or redirect on success
    
    Template: artifacts/edit.html
    Context:
        - artifact: Artifact instance
        - playbook: Playbook instance (for breadcrumbs)
        - activity: Activity instance
        - artifact_types: List of type choices
        - form_data: Dict with form values
        - errors: Dict with field errors (on validation error)
    
    Example URL: /artifacts/123/edit/
    """
    # Implementation
    pass


@login_required
def artifact_delete(request, pk):
    """
    Delete artifact (POST only, returns HTMX response).
    
    :param request: Django HttpRequest
    :param pk: Artifact ID as int from URL. Example: 123
    :returns: HttpResponse with redirect or HTMX partial
    
    Template: artifacts/delete_modal.html (for confirmation)
    
    Example URL: /artifacts/123/delete/
    """
    # Implementation
    pass


@login_required
def artifact_search_htmx(request):
    """
    HTMX endpoint for live search/filter.
    
    :param request: Django HttpRequest with GET params
    :returns: HttpResponse with table rows partial
    
    Template: artifacts/partials/artifact_rows.html
    Context:
        - artifacts: Filtered QuerySet
    
    Query params:
        - playbook_id: int
        - search: str
        - type: str
        - required: bool
    
    Example URL: /artifacts/search/?playbook_id=12&search=design&type=Document
    """
    # Implementation
    pass
```

**Tests to Create**: `tests/integration/test_artifact_views.py`
- `test_artifact_list_authenticated`
- `test_artifact_list_unauthenticated_redirects`
- `test_artifact_list_with_search`
- `test_artifact_list_with_type_filter`
- `test_artifact_list_with_required_filter`
- `test_artifact_list_empty_state`
- `test_artifact_create_get_form`
- `test_artifact_create_post_success`
- `test_artifact_create_post_validation_error`
- `test_artifact_create_duplicate_name_fails`
- `test_artifact_detail_view`
- `test_artifact_detail_not_found`
- `test_artifact_edit_get_form`
- `test_artifact_edit_post_success`
- `test_artifact_edit_post_validation_error`
- `test_artifact_delete_post_success`
- `test_artifact_delete_get_not_allowed`
- `test_artifact_search_htmx`

**Checklist**:
- [ ] Re-read `.windsurf/rules/do-skeletons-first.md` before implementing
- [ ] Re-read `.windsurf/rules/do-informative-logging.md` before implementing
- [ ] Create `methodology/artifact_views.py` with all views
- [ ] Add extensive logging (info level) for all operations
- [ ] Create integration tests in `tests/integration/test_artifact_views.py`
- [ ] Run tests: `pytest tests/integration/test_artifact_views.py -v`
- [ ] Verify 100% pass rate
- [ ] Commit: `feat(views): add artifact CRUD views with logging`

---

#### Task 3.3: Create Artifact Templates

**Templates to Create**:

1. **`templates/artifacts/list.html`** - Artifacts list with search/filter
2. **`templates/artifacts/create.html`** - Create artifact form
3. **`templates/artifacts/detail.html`** - Artifact detail view
4. **`templates/artifacts/edit.html`** - Edit artifact form
5. **`templates/artifacts/delete_modal.html`** - Delete confirmation modal
6. **`templates/artifacts/partials/artifact_rows.html`** - HTMX table rows partial

**Key Requirements for ALL Templates**:
- [ ] Extend `base.html`
- [ ] Include breadcrumbs with playbook context
- [ ] Use Bootstrap 5.3+ components
- [ ] Add `data-testid` attributes to ALL interactive elements
- [ ] Include Font Awesome Pro icons (per IA guidelines)
- [ ] Add Bootstrap tooltips to ALL action buttons
- [ ] Follow form validation pattern (field-level + form-level errors)
- [ ] Use semantic HTML5 elements
- [ ] Ensure accessibility (ARIA labels, alt text, etc.)

**Example: `templates/artifacts/list.html`** (see UI/UX Patterns section above for full structure)

**Checklist**:
- [ ] Re-read `.windsurf/rules/do-semantic-versioning-on-ui-elements.md` before implementing
- [ ] Re-read `.windsurf/rules/tooltips.md` before implementing
- [ ] Create all 6 templates following IA guidelines
- [ ] Verify all `data-testid` attributes present
- [ ] Verify all tooltips present on action buttons
- [ ] Verify all Font Awesome icons present
- [ ] Test manually in browser
- [ ] Commit: `feat(templates): add artifact CRUD templates with Bootstrap 5`

---

### Phase 4: Integration Tests

#### Task 4.1: Create Integration Tests

**File**: `tests/integration/test_artifact_integration.py`

**Test Scenarios** (map to `.feature` files):

```python
"""
Integration tests for artifact functionality.

Tests complete user workflows without mocking.
"""

import pytest
from django.test import Client
from django.urls import reverse
from methodology.models import Playbook, Workflow, Activity, Artifact


@pytest.mark.django_db(transaction=True)
class TestArtifactListIntegration:
    """Test artifact list view integration."""
    
    def test_art_list_01_navigate_from_playbook(self, authenticated_client, test_playbook):
        """
        ART-LIST-01: Navigate to artifacts list from playbook.
        
        Given Maria is on FOB-PLAYBOOKS-VIEW_PLAYBOOK-1
        When she clicks the "Artifacts" tab
        Then she is redirected to FOB-ARTIFACTS-LIST+FIND-1
        And she sees "Artifacts in React Frontend v1.2" header
        """
        # Implementation
        pass
    
    def test_art_list_02_view_artifacts_table(self, authenticated_client, test_playbook_with_artifacts):
        """
        ART-LIST-02: View artifacts table.
        
        Given Maria is on artifacts list
        Then she sees all 15 artifacts
        And each artifact shows: Name, Type, Activity, Required, Status, Actions
        """
        # Implementation
        pass
    
    # ... more tests mapping to scenarios


@pytest.mark.django_db(transaction=True)
class TestArtifactCreateIntegration:
    """Test artifact creation integration."""
    
    def test_art_create_01_open_create_form(self, authenticated_client, test_activity):
        """
        ART-CREATE-01: Open create artifact form.
        
        Given Maria is on artifacts list
        When she clicks [Create New Artifact]
        Then she is redirected to FOB-ARTIFACTS-CREATE_ARTIFACT-1
        And the Parent Playbook field shows "React Frontend v1.2" (read-only)
        """
        # Implementation
        pass
    
    def test_art_create_02_create_artifact_successfully(self, authenticated_client, test_activity):
        """
        ART-CREATE-02: Create artifact successfully.
        
        Given Maria is on the create artifact form
        When she enters "Component Design Document" in Name
        And she enters "Detailed component architecture and patterns" in Description
        And she selects "Document" as Type
        And she clicks [Create Artifact]
        Then the artifact is created
        And she sees success notification
        """
        # Implementation
        pass
    
    # ... more tests for all create scenarios


@pytest.mark.django_db(transaction=True)
class TestArtifactViewIntegration:
    """Test artifact detail view integration."""
    
    # Tests for ART-VIEW-01 through ART-VIEW-07
    pass


@pytest.mark.django_db(transaction=True)
class TestArtifactEditIntegration:
    """Test artifact editing integration."""
    
    # Tests for ART-EDIT-01 through ART-EDIT-08
    pass


@pytest.mark.django_db(transaction=True)
class TestArtifactDeleteIntegration:
    """Test artifact deletion integration."""
    
    # Tests for ART-DELETE-01 through ART-DELETE-06
    pass
```

**Fixtures to Create** (in `tests/conftest.py`):
```python
@pytest.fixture
def test_playbook_with_artifacts(test_user, test_playbook, test_workflow, test_activity):
    """Create playbook with 15 artifacts for testing."""
    artifacts = []
    for i in range(15):
        artifact = Artifact.objects.create(
            activity=test_activity,
            playbook=test_playbook,
            name=f"Artifact {i+1}",
            description=f"Description for artifact {i+1}",
            type=['Document', 'Template', 'Code', 'Diagram'][i % 4],
            is_required=(i % 3 == 0)
        )
        artifacts.append(artifact)
    return artifacts
```

**Checklist**:
- [ ] Re-read `.windsurf/rules/do-not-mock-in-integration-tests.md` before implementing
- [ ] Re-read `.windsurf/rules/do-runner.md` before implementing
- [ ] Create `tests/integration/test_artifact_integration.py`
- [ ] Create test fixtures in `tests/conftest.py`
- [ ] Implement ALL 25 scenario tests (5 files × ~5 scenarios each)
- [ ] Run tests: `pytest tests/integration/test_artifact_integration.py -v`
- [ ] Verify 100% pass rate
- [ ] Update progress in this issue
- [ ] Commit: `test(integration): add artifact integration tests for all scenarios`

---

### Phase 5: Navbar Integration

#### Task 5.1: Activate Artifacts Navbar Link

**File**: `templates/base.html`

**Changes**:
1. Remove `disabled` class from Artifacts link
2. Change `href="#"` to `href="/playbooks/"` (or dedicated artifacts page)
3. Update tooltip from "Coming soon..." to active description
4. Add active state highlighting

**Before**:
```html
<li class="nav-item">
  <a class="nav-link disabled" 
     href="#"
     data-testid="nav-artifacts"
     data-bs-toggle="tooltip"
     title="Coming soon: Manage artifacts and deliverables">
    <i class="fa-solid fa-gift me-2"></i>
    Artifacts
  </a>
</li>
```

**After**:
```html
<li class="nav-item">
  <a class="nav-link {% if '/artifacts/' in request.path %}active{% endif %}" 
     href="/artifacts/"
     data-testid="nav-artifacts"
     data-bs-toggle="tooltip"
     title="Manage artifacts and deliverables"
     {% if '/artifacts/' in request.path %}aria-current="page"{% endif %}>
    <i class="fa-solid fa-gift me-2"></i>
    Artifacts
  </a>
</li>
```

**Add Navbar Scenarios to Feature File**:

Add to `docs/features/act-6-artifacts/artifacts-list-find.feature`:

```gherkin
# ============================================================
# NAVBAR INTEGRATION - Wire when Artifacts block is complete
# ============================================================

Scenario: ART-NAVBAR-01 Artifacts link appears in main navigation
  Given the Artifacts feature is fully implemented
  And Maria is authenticated in FOB
  When she views any page in FOB
  Then she sees "Artifacts" link in the main navbar
  And the link has icon "fa-gift"
  And the link has tooltip "Manage artifacts and deliverables"
  
Scenario: ART-NAVBAR-02 Navigate to Artifacts from any page
  Given Maria is authenticated in FOB
  And she is on any page in FOB
  When she clicks "Artifacts" in the main navbar
  Then she is redirected to FOB-ARTIFACTS-LIST+FIND-1
  And the Artifacts nav link is highlighted as active
```

**Tests to Create**: `tests/integration/test_artifact_navbar.py`
```python
@pytest.mark.django_db(transaction=True)
def test_art_navbar_01_link_appears(authenticated_client):
    """ART-NAVBAR-01: Artifacts link appears in main navigation."""
    response = authenticated_client.get('/dashboard/')
    assert response.status_code == 200
    assert 'data-testid="nav-artifacts"' in response.content.decode()
    assert 'fa-gift' in response.content.decode()
    assert 'Manage artifacts and deliverables' in response.content.decode()


@pytest.mark.django_db(transaction=True)
def test_art_navbar_02_navigate_to_artifacts(authenticated_client, test_playbook):
    """ART-NAVBAR-02: Navigate to Artifacts from any page."""
    response = authenticated_client.get(f'/playbooks/{test_playbook.id}/artifacts/')
    assert response.status_code == 200
    # Verify active state
    assert 'nav-link active' in response.content.decode()
```

**Checklist**:
- [ ] Update `templates/base.html` navbar
- [ ] Add navbar scenarios to feature file
- [ ] Create `tests/integration/test_artifact_navbar.py`
- [ ] Run tests: `pytest tests/integration/test_artifact_navbar.py -v`
- [ ] Verify 100% pass rate
- [ ] Update progress in this issue
- [ ] Commit: `feat(navbar): activate Artifacts navigation link`

---

### Phase 6: Definition of Done

#### Task 6.1: Verify Against DOD Checklist

**File**: `.windsurf/workflows/dev-5-check-dod.md`

**Checklist** (verify each section):

- [ ] **Test-First Development**
  - [ ] Unit tests created before implementation
  - [ ] Integration tests created before implementation
  - [ ] All tests pass with 100% rate
  - [ ] Tests runnable via `pytest tests/`

- [ ] **Continuous Testing**
  - [ ] Tests add output to `tests.log`
  - [ ] Tests run continuously during development
  - [ ] Errors monitored and fixed automatically

- [ ] **Code Quality**
  - [ ] Methods are concise (20-30 lines max for public methods)
  - [ ] Supporting logic in well-named private methods
  - [ ] Docstrings with `:param:`, `:returns:`, `:raises:` and examples
  - [ ] Extensive logging on info level
  - [ ] No mindless deletions (checked for usage first)

- [ ] **UI/Frontend**
  - [ ] Bootstrap 5.3+ components used
  - [ ] Font Awesome Pro icons on all action buttons
  - [ ] Bootstrap tooltips on all action buttons
  - [ ] Semantic `data-testid` attributes on all interactive elements
  - [ ] Form validation (field-level + form-level errors)
  - [ ] Accessibility (ARIA labels, alt text, etc.)

- [ ] **Documentation**
  - [ ] Feature files updated with implementation notes
  - [ ] Architecture docs updated if needed
  - [ ] README updated if needed

- [ ] **Commits**
  - [ ] Follow Angular convention
  - [ ] Atomic commits after each major step
  - [ ] Associated with GitHub issue

**Checklist**:
- [ ] Review each DOD section
- [ ] Fix any gaps found
- [ ] Update progress in this issue
- [ ] Commit: `docs: verify Artifacts feature against DOD checklist`

---

#### Task 6.2: Finalize Feature

**File**: `.windsurf/workflows/dev-6-finalize-feature.md`

**Checklist**:

- [ ] **Testing**
  - [ ] Run full test suite: `pytest tests/`
  - [ ] Verify 100% pass rate
  - [ ] Check `tests.log` for errors

- [ ] **Manual Testing**
  - [ ] Test all CRUD operations in browser
  - [ ] Test search/filter functionality
  - [ ] Test file upload (template files)
  - [ ] Test validation errors
  - [ ] Test navbar integration

- [ ] **Code Review**
  - [ ] Review all code for quality
  - [ ] Check for TODOs or FIXMEs
  - [ ] Verify logging is extensive
  - [ ] Verify docstrings are complete

- [ ] **Documentation**
  - [ ] Update feature files with completion status
  - [ ] Update screen flow diagram if needed
  - [ ] Update IA guidelines if new patterns added

- [ ] **GitHub**
  - [ ] Update issue with completion status
  - [ ] Link all commits to issue
  - [ ] Request review if needed

**Checklist**:
- [ ] Complete all finalization steps
- [ ] Update progress in this issue
- [ ] Commit: `feat(artifacts): finalize Artifacts feature implementation`

---

### Phase 7: Recommendations for Next Time

#### Task 7.1: Reflect and Recommend

**Add comment to PR calling out @user**:

```markdown
## 🎯 Recommendations for Future Issues

@user - To make issue implementation faster and better next time, it would help if you provide:

### 1. **Clearer Model Relationships**
- Specify whether artifacts should have direct `playbook` FK or derive via `activity->workflow->playbook`
- Current implementation uses denormalized `playbook` FK for performance - confirm this is desired

### 2. **File Upload Requirements**
- Specify max file size for template uploads
- Specify allowed file types (e.g., `.tsx`, `.py`, `.md`)
- Specify storage backend (local filesystem vs S3)

### 3. **Search/Filter Specifications**
- Specify which fields should be searchable (name, description, both?)
- Specify filter combinations (type + required, activity + type, etc.)
- Specify sort options (name, created_at, type, etc.)

### 4. **UI/UX Mockups**
- Provide wireframes or mockups for complex forms
- Specify exact button placement and grouping
- Specify empty state messaging

### 5. **Test Data Fixtures**
- Provide realistic test data examples
- Specify edge cases to test (empty strings, special characters, etc.)

### 6. **Performance Requirements**
- Specify expected data volumes (100 artifacts? 10,000?)
- Specify pagination requirements
- Specify caching strategy if needed

### 7. **Access Control**
- Specify who can create/edit/delete artifacts
- Specify if artifacts are playbook-scoped or global

These details would reduce ambiguity and speed up implementation significantly.
```

**Checklist**:
- [ ] Add recommendations comment to PR
- [ ] Tag @user in comment
- [ ] Update progress in this issue

---

## Success Criteria

**Feature is complete when**:
- [ ] All 25 scenarios pass (5 feature files × ~5 scenarios each)
- [ ] 100% test pass rate (`pytest tests/`)
- [ ] Navbar link activated and working
- [ ] DOD checklist verified
- [ ] All commits follow Angular convention
- [ ] Issue updated with progress throughout

---

## Notes for @Copilot

### Critical Rules to Follow

1. **Test-First**: Write tests BEFORE implementation
2. **No Mocking**: Integration tests use real database (pytest-django)
3. **Concise Methods**: Public methods 20-30 lines max, extract to private methods
4. **Extensive Logging**: Info level logging for all operations
5. **Docstrings**: All methods need `:param:`, `:returns:`, `:raises:` with examples
6. **Semantic testid**: ALL interactive elements need `data-testid` attributes
7. **Bootstrap Tooltips**: ALL action buttons need tooltips
8. **Font Awesome Icons**: ALL action buttons need icons
9. **Atomic Commits**: Commit after each major step with Angular convention
10. **100% Pass Rate**: Only mark complete when ALL tests pass

### Architecture Patterns

- **Models**: Follow `Activity` model pattern
- **Services**: Follow `ActivityService` pattern
- **Views**: Follow `activity_views.py` pattern
- **Templates**: Follow IA guidelines (Bootstrap 5.3+, HTMX, semantic HTML)
- **Tests**: Follow existing test patterns in `tests/integration/`

### Common Pitfalls to Avoid

1. **Don't** use Django Forms - we build custom views with manual validation
2. **Don't** mock in integration tests - use real database
3. **Don't** forget `data-testid` attributes - tests will fail
4. **Don't** forget tooltips on buttons - DOD will fail
5. **Don't** forget to update navbar when feature is complete
6. **Don't** commit without running tests first
7. **Don't** mark issue complete without 100% pass rate

### Questions to Ask Before Starting

1. Should artifacts have direct `playbook` FK or derive via activity?
2. What file types are allowed for template uploads?
3. What is the max file size for uploads?
4. Should artifacts be searchable by description or name only?
5. Should there be a global artifacts list or only playbook-scoped?

---

## Estimated Effort

**Total**: ~8-10 hours for experienced developer, ~15-20 hours for junior

**Breakdown**:
- Phase 1 (Models): 1-2 hours
- Phase 2 (Services): 2-3 hours
- Phase 3 (Views/Templates): 3-4 hours
- Phase 4 (Integration Tests): 2-3 hours
- Phase 5 (Navbar): 0.5 hours
- Phase 6 (DOD/Finalize): 1-2 hours
- Phase 7 (Recommendations): 0.5 hours

**Note**: These are human estimates. AI execution time may vary.
