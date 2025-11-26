import logging
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json

logger = logging.getLogger(__name__)


class Visibility(models.TextChoices):
    """Playbook visibility options."""
    PRIVATE = 'private', 'Private (only me)'
    FAMILY = 'family', 'Family'
    LOCAL_ONLY = 'local_only', 'Local only (not uploaded to Homebase)'


class Status(models.TextChoices):
    """Playbook status options."""
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    ARCHIVED = 'archived', 'Archived'


class Category(models.TextChoices):
    """Playbook category options."""
    DESIGN = 'design', 'Design'
    DEVELOPMENT = 'development', 'Development'
    RESEARCH = 'research', 'Research'
    MANAGEMENT = 'management', 'Management'
    PRODUCT = 'product', 'Product'
    OTHER = 'other', 'Other'


class Playbook(models.Model):
    """Playbook model for storing methodology playbooks.
    
    Represents a complete methodology playbook with activities, workflows,
    and metadata. Playbooks are static reference material.
    
    Attributes:
        id: Auto-incrementing primary key
        name: Human-readable name (3-100 chars, unique per user)
        description: Detailed description (10-500 chars)
        category: Category from predefined choices
        tags: JSON list of tag strings
        visibility: Who can see this playbook
        status: Draft/Active/Archived
        version: Semantic version string (auto v1.0 on creation)
        created_by: User who created this playbook
        created_at: When this playbook was created
        updated_at: When this playbook was last updated
    """
    name = models.CharField(
        max_length=100,
        help_text="Playbook name (3-100 characters)"
    )
    description = models.TextField(
        max_length=500,
        help_text="Detailed description (10-500 characters)"
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        help_text="Playbook category"
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="List of tag strings"
    )
    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
        help_text="Who can see this playbook"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Playbook status"
    )
    version = models.CharField(
        max_length=20,
        default="1.0.0",
        help_text="Semantic version (auto-set on creation)"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='playbooks',
        help_text="User who created this playbook"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this playbook was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this playbook was last updated"
    )

    class Meta:
        ordering = ['-updated_at']
        unique_together = ['created_by', 'name']
        indexes = [
            models.Index(fields=['created_by', 'status']),
            models.Index(fields=['category']),
            models.Index(fields=['visibility']),
        ]

    def __str__(self):
        return f"{self.name} by {self.created_by.username}"

    def clean(self):
        """Validate model fields."""
        logger.debug(f"Validating playbook: {self.name} by user {self.created_by.id}")
        
        # Name validation
        if not self.name or len(self.name.strip()) < 3:
            raise ValidationError({
                'name': 'Name is required. Must be 3-100 characters.'
            })
        if len(self.name) > 100:
            raise ValidationError({
                'name': 'Name must not exceed 100 characters.'
            })
        
        # Description validation
        if not self.description or len(self.description.strip()) < 10:
            raise ValidationError({
                'description': 'Description is required. Must be 10-500 characters.'
            })
        if len(self.description) > 500:
            raise ValidationError({
                'description': 'Description must not exceed 500 characters.'
            })
        
        # Tags validation
        if isinstance(self.tags, list):
            for tag in self.tags:
                if not isinstance(tag, str) or len(tag.strip()) == 0:
                    raise ValidationError({
                        'tags': 'All tags must be non-empty strings.'
                    })
        
        logger.info(f"Playbook validation passed: {self.name}")

    def save(self, *args, **kwargs):
        """Override save to add logging and auto-version."""
        is_new = self.pk is None
        if is_new:
            self.version = "1.0.0"
            logger.info(f"Creating new playbook: {self.name} by user {self.created_by.id}")
        else:
            logger.info(f"Updating playbook: {self.name} (ID: {self.pk}) by user {self.created_by.id}")
        
        super().save(*args, **kwargs)
        
        if is_new:
            logger.info(f"Playbook created successfully: {self.name} (ID: {self.pk})")
        else:
            logger.info(f"Playbook updated successfully: {self.name} (ID: {self.pk})")

    @property
    def display_name(self):
        """Return display name with version."""
        return f"{self.name} v{self.version}"

    @property
    def tag_list(self):
        """Return tags as comma-separated string."""
        if isinstance(self.tags, list):
            return ', '.join(self.tags)
        return ''

    def add_tag(self, tag):
        """Add a tag if not already present."""
        if not isinstance(self.tags, list):
            self.tags = []
        
        tag = tag.strip()
        if tag and tag not in self.tags:
            self.tags.append(tag)
            logger.debug(f"Added tag '{tag}' to playbook {self.name}")

    def remove_tag(self, tag):
        """Remove a tag if present."""
        if isinstance(self.tags, list):
            tag = tag.strip()
            if tag in self.tags:
                self.tags.remove(tag)
                logger.debug(f"Removed tag '{tag}' from playbook {self.name}")

    def is_visible_to_user(self, user):
        """Check if playbook is visible to given user."""
        if self.created_by == user:
            return True
        
        if self.visibility == Visibility.PRIVATE:
            return False
        elif self.visibility == Visibility.LOCAL_ONLY:
            return False
        elif self.visibility == Visibility.FAMILY:
            # TODO: Implement family membership check
            return False
        
        return False

    def get_absolute_url(self):
        """Get absolute URL for this playbook."""
        from django.urls import reverse
        return reverse('playbook_detail', kwargs={'playbook_id': self.pk})


class Workflow(models.Model):
    """Workflow model for playbook steps and procedures.
    
    Represents individual workflows within a playbook, containing
    the specific steps and procedures to complete a task.
    """
    
    class Status(models.TextChoices):
        """Workflow status choices."""
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        ARCHIVED = 'archived', 'Archived'
    
    # Core fields
    name = models.CharField(
        max_length=200,
        help_text="Workflow name (e.g., 'Discovery Phase', 'User Research')"
    )
    description = models.TextField(
        help_text="Detailed description of what this workflow accomplishes"
    )
    
    # Relationships
    playbook = models.ForeignKey(
        Playbook,
        on_delete=models.CASCADE,
        related_name='workflows',
        help_text="Playbook this workflow belongs to"
    )
    
    # Metadata
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Current status of this workflow"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of workflows within playbook"
    )
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        help_text="User who created this workflow"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name_plural = 'Workflows'
        constraints = [
            models.UniqueConstraint(
                fields=['playbook', 'name'],
                name='unique_workflow_name_per_playbook'
            )
        ]
    
    def __str__(self):
        return f"{self.playbook.name} - {self.name}"
    
    def clean(self):
        """Validate workflow data."""
        logger.info(f"Validating workflow: {self.name}")
        
        errors = {}
        
        # Name validation
        if not self.name or not self.name.strip():
            errors['name'] = 'Workflow name is required.'
        elif len(self.name.strip()) < 3:
            errors['name'] = 'Workflow name must be at least 3 characters.'
        elif len(self.name.strip()) > 200:
            errors['name'] = 'Workflow name cannot exceed 200 characters.'
        
        # Description validation
        if not self.description or not self.description.strip():
            errors['description'] = 'Workflow description is required.'
        elif len(self.description.strip()) < 10:
            errors['description'] = 'Workflow description must be at least 10 characters.'
        elif len(self.description.strip()) > 2000:
            errors['description'] = 'Workflow description cannot exceed 2000 characters.'
        
        # Check for duplicate name within same playbook
        if self.playbook_id:
            existing = Workflow.objects.filter(
                playbook=self.playbook,
                name=self.name.strip()
            ).exclude(pk=self.pk).first()
            if existing:
                errors['name'] = 'A workflow with this name already exists in this playbook.'
        
        if errors:
            raise ValidationError(errors)
        
        logger.info(f"Workflow validation passed: {self.name}")
    
    def save(self, *args, **kwargs):
        """Override save to add logging and auto-ordering."""
        if not self.pk and self.order == 0:
            # Auto-set order for new workflows
            max_order = Workflow.objects.filter(
                playbook=self.playbook
            ).aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
            logger.info(f"Auto-set workflow order to {self.order}")
        
        # Clean data before saving
        self.full_clean()
        
        super().save(*args, **kwargs)
        logger.info(f"Workflow saved: {self.playbook.name} - {self.name}")
    
    @property
    def is_active(self):
        """Check if workflow is in active status."""
        return self.status == self.Status.ACTIVE
    
    @property
    def is_draft(self):
        """Check if workflow is in draft status."""
        return self.status == self.Status.DRAFT

