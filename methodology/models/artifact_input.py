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
        "Artifact",
        on_delete=models.CASCADE,
        related_name="inputs",
        help_text="Artifact being consumed as input",
    )

    activity = models.ForeignKey(
        "Activity",
        on_delete=models.CASCADE,
        related_name="input_artifacts",
        help_text="Activity consuming this artifact",
    )

    # Metadata
    is_required = models.BooleanField(
        default=True, help_text="Whether this input is required for activity execution"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["activity", "artifact"]
        verbose_name = "Artifact Input"
        verbose_name_plural = "Artifact Inputs"
        constraints = [
            models.UniqueConstraint(
                fields=["artifact", "activity"],
                name="unique_artifact_input_per_activity",
                violation_error_message="This artifact is already an input to this activity",
            )
        ]
        indexes = [
            models.Index(fields=["artifact", "activity"]),
            models.Index(fields=["is_required"]),
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
        # Use _id attributes to avoid database queries
        if self.artifact_id and self.activity_id:
            if self.artifact.produced_by_id == self.activity_id:
                raise ValidationError(
                    {
                        "activity": f"Circular dependency: '{self.artifact.name}' is produced by '{self.activity.name}' and cannot be its input"
                    }
                )

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
            "id": self.id,
            "artifact_id": self.artifact_id,
            "artifact_name": self.artifact.name,
            "activity_id": self.activity_id,
            "activity_name": self.activity.name,
            "is_required": self.is_required,
            "created_at": self.created_at.isoformat(),
        }
