"""
ArtifactInput model for tracking artifact consumption by activities.

ArtifactInput represents the relationship between an activity and the artifacts
it consumes as inputs.
"""

from django.db import models


class ArtifactInput(models.Model):
    """
    ArtifactInput represents an artifact consumed by an activity.
    
    This is a many-to-many relationship between activities and artifacts,
    tracking which activities use which artifacts as inputs.
    """
    
    # Relationships
    activity = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
        related_name='artifact_inputs',
        help_text="Activity that consumes this artifact"
    )
    artifact = models.ForeignKey(
        'Artifact',
        on_delete=models.CASCADE,
        related_name='consuming_activities',
        help_text="Artifact being consumed"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['activity', 'artifact']
        verbose_name = 'Artifact Input'
        verbose_name_plural = 'Artifact Inputs'
        constraints = [
            models.UniqueConstraint(
                fields=['activity', 'artifact'],
                name='unique_artifact_input_per_activity'
            )
        ]
    
    def __str__(self):
        """String representation showing relationship."""
        return f"{self.activity.name} <- {self.artifact.name}"
