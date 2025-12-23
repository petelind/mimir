# Artifact Flow Addition to Implementation Plan

## New Model: ArtifactInput (Many-to-Many Through Table)

**File**: `methodology/models/artifact_input.py`

```python
"""
ArtifactInput model for tracking artifact consumption by activities.

Links artifacts as inputs to activities with metadata about requirement status.
"""

from django.db import models
from django.core.exceptions import ValidationError


class ArtifactInput(models.Model):
    """
    ArtifactInput represents an artifact being consumed as input by an activity.
    
    This is a through model for the many-to-many relationship between
    Artifact (as input) and Activity (as consumer).
    """
    
    # Relationships
    artifact = models.ForeignKey(
        'Artifact',
        on_delete=models.CASCADE,
        related_name='inputs',
        help_text="Artifact being consumed as input"
    )
    
    activity = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
        related_name='input_artifacts',
        help_text="Activity consuming this artifact"
    )
    
    # Metadata
    is_required = models.BooleanField(
        default=True,
        help_text="Whether this input is required for activity execution"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['activity', 'artifact']
        verbose_name = 'Artifact Input'
        verbose_name_plural = 'Artifact Inputs'
        constraints = [
            models.UniqueConstraint(
                fields=['artifact', 'activity'],
                name='unique_artifact_input_per_activity',
                violation_error_message="This artifact is already an input to this activity"
            )
        ]
        indexes = [
            models.Index(fields=['artifact', 'activity']),
            models.Index(fields=['is_required']),
        ]
    
    def __str__(self):
        """
        String representation.
        
        :returns: Description as str. Example: "API Spec → Implement Component (Required)"
        """
        req_status = "Required" if self.is_required else "Optional"
        return f"{self.artifact.name} → {self.activity.name} ({req_status})"
    
    def clean(self):
        """
        Model-level validation.
        
        :raises ValidationError: If validation fails
        """
        # Prevent circular dependency: artifact cannot be input to its producer
        if self.artifact.produced_by_id == self.activity_id:
            raise ValidationError({
                'activity': f"Circular dependency: '{self.artifact.name}' is produced by '{self.activity.name}' and cannot be its input"
            })
        
        # Warn about temporal ordering (artifact produced after it's consumed)
        if self.artifact.produced_by.order > self.activity.order:
            # This is a warning, not an error - allow override
            pass
    
    def save(self, *args, **kwargs):
        """
        Override save to run validation.
        
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    def to_dict(self):
        """
        Convert to dictionary for API/MCP responses.
        
        :returns: Dict representation
        """
        return {
            'id': self.id,
            'artifact_id': self.artifact_id,
            'artifact_name': self.artifact.name,
            'activity_id': self.activity_id,
            'activity_name': self.activity.name,
            'is_required': self.is_required,
            'created_at': self.created_at.isoformat(),
        }
```

## Updated Artifact Model

Add to existing Artifact model:

```python
# In Artifact model, add method:
def add_consumer(self, activity, is_required=True):
    """
    Add activity as consumer of this artifact.
    
    :param activity: Activity instance to add as consumer
    :param is_required: Whether input is required as bool. Example: True
    :returns: Created ArtifactInput instance
    :raises ValidationError: If circular dependency detected
    
    Example:
        >>> artifact.add_consumer(implement_activity, is_required=True)
    """
    from methodology.models import ArtifactInput
    return ArtifactInput.objects.create(
        artifact=self,
        activity=activity,
        is_required=is_required
    )

def remove_consumer(self, activity):
    """
    Remove activity as consumer of this artifact.
    
    :param activity: Activity instance to remove
    :returns: Number of deleted inputs (0 or 1)
    
    Example:
        >>> artifact.remove_consumer(test_activity)
        1
    """
    return self.inputs.filter(activity=activity).delete()[0]
```

## New Phase in Implementation Plan

### Phase 8: Artifact Flow (Input/Output Relationships)

#### Task 8.1: Create ArtifactInput Model

**File**: `methodology/models/artifact_input.py`

**Checklist**:
- [ ] Create `methodology/models/artifact_input.py` with complete model
- [ ] Add to `methodology/models/__init__.py`: `from .artifact_input import ArtifactInput`
- [ ] Create migration: `python manage.py makemigrations`
- [ ] Run migration: `python manage.py migrate`
- [ ] Create unit tests in `tests/unit/test_artifact_input_model.py`
- [ ] Run tests: `pytest tests/unit/test_artifact_input_model.py -v`
- [ ] Verify 100% pass rate
- [ ] Commit: `feat(models): add ArtifactInput model for artifact flow tracking`

---

#### Task 8.2: Add Artifact Flow Views

**New Views to Add** (in `methodology/artifact_views.py`):

```python
@login_required
def artifact_add_consumer(request, artifact_id):
    """
    Add activity as consumer of artifact (HTMX endpoint).
    
    :param request: Django HttpRequest with POST data
    :param artifact_id: Artifact ID as int
    :returns: HttpResponse with updated consumers list partial
    """
    pass

@login_required
def artifact_remove_consumer(request, artifact_id, activity_id):
    """
    Remove activity as consumer of artifact (HTMX endpoint).
    
    :param request: Django HttpRequest
    :param artifact_id: Artifact ID as int
    :param activity_id: Activity ID as int
    :returns: HttpResponse with updated consumers list partial
    """
    pass

@login_required  
def activity_manage_inputs(request, activity_id):
    """
    Manage input artifacts for activity.
    
    :param request: Django HttpRequest
    :param activity_id: Activity ID as int
    :returns: HttpResponse with input management interface
    """
    pass
```

**Checklist**:
- [ ] Add artifact flow views to `methodology/artifact_views.py`
- [ ] Add URL patterns to `methodology/artifact_urls.py`
- [ ] Create templates for artifact flow UI
- [ ] Create integration tests for flow scenarios
- [ ] Run tests: `pytest tests/integration/test_artifact_flow.py -v`
- [ ] Verify 100% pass rate
- [ ] Commit: `feat(views): add artifact flow management views`

---

#### Task 8.3: Implement Flow Scenarios

**Tests to Create**: `tests/integration/test_artifact_flow.py`

Map all 28 scenarios from `artifacts-flow.feature`:
- ART-FLOW-01 through ART-FLOW-28

**Checklist**:
- [ ] Create `tests/integration/test_artifact_flow.py`
- [ ] Implement all 28 flow scenarios as tests
- [ ] Run tests: `pytest tests/integration/test_artifact_flow.py -v`
- [ ] Verify 100% pass rate
- [ ] Commit: `test(integration): add artifact flow integration tests`

---

## Updated Scenario Count

**Total Scenarios**: 53 (was 25)
- artifacts-create.feature: 8 scenarios
- artifacts-list-find.feature: 10 scenarios  
- artifacts-view.feature: 9 scenarios (added 2 flow scenarios)
- artifacts-edit.feature: 8 scenarios
- artifacts-delete.feature: 6 scenarios
- **artifacts-flow.feature: 28 scenarios** (NEW)

**Total Feature Files**: 6 (was 5)

## Updated Complexity Estimate

**Components**: 10 classes (was 8)
- Artifact model
- ArtifactInput model (NEW)
- ArtifactService
- ArtifactInputService (NEW)
- 6 view functions (was 5)

**Methods**: ~50 (was ~35)
- Additional methods for flow management
- Validation for circular dependencies
- Consumer management methods

**Estimated Effort**: ~12-15 hours (was ~8-10 hours)
