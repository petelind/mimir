"""
Artifact model for outputs produced by activities.

Artifacts represent deliverables/outputs produced by activities.
Examples: code files, documentation, test scenarios, templates, diagrams.
"""

from django.db import models


class Artifact(models.Model):
    """
    Artifact represents a deliverable/output produced by an activity.
    
    Artifacts are outputs that will be used as inputs by downstream activities.
    Examples: code files, documentation, test scenarios, templates, diagrams.
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
    
    # Relationships
    activity = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
        related_name='artifacts',
        help_text="Activity that produces this artifact"
    )
    playbook = models.ForeignKey(
        'Playbook',
        on_delete=models.CASCADE,
        related_name='artifacts',
        help_text="Parent playbook for breadcrumb navigation"
    )
    
    # Core fields
    name = models.CharField(
        max_length=200,
        help_text="Artifact name - must be unique within activity"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the artifact"
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
        help_text="Whether this artifact is required"
    )
    
    # File storage (optional)
    template_file = models.FileField(
        upload_to='artifacts/templates/',
        blank=True,
        null=True,
        help_text="Optional template file attachment"
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
                name='unique_artifact_per_activity'
            )
        ]
    
    def __str__(self):
        """String representation showing name."""
        return self.name
    
    def is_owned_by(self, user):
        """
        Check if user owns the parent playbook.
        
        :param user: User to check ownership for
        :returns: True if user owns parent playbook
        :rtype: bool
        
        Example:
            >>> artifact.is_owned_by(maria)
            True  # If maria owns the playbook
        """
        return self.playbook.is_owned_by(user)
    
    @property
    def reference_name(self):
        """
        Get reference name for logging.
        
        :returns: Reference name
        :rtype: str
        
        Example:
            >>> artifact.reference_name
            'API Specification'
        """
        return self.name
    
    def consumer_count(self):
        """
        Get count of activities consuming this artifact.
        
        :returns: Number of consuming activities
        :rtype: int
        
        Example:
            >>> artifact.consumer_count()
            3
        """
        return self.consuming_activities.count()
