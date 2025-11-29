"""
Activity model for individual tasks within workflows.

Activities represent discrete work items that make up a workflow.
Each activity belongs to a workflow and can be organized into phases.
"""

from django.db import models


class Activity(models.Model):
    """
    Activity represents a single task/step within a workflow.
    
    Activities are ordered work items that can be grouped by phase,
    tracked by status, and can have dependencies on other activities.
    """
    
    # Relationships
    workflow = models.ForeignKey(
        'Workflow',
        on_delete=models.CASCADE,
        related_name='activities',
        help_text="Parent workflow containing this activity"
    )
    
    # Core fields
    name = models.CharField(
        max_length=200,
        help_text="Activity name - must be unique within workflow"
    )
    guidance = models.TextField(
        help_text="Rich Markdown guidance with instructions, examples, images, and diagrams"
    )
    
    # Organization
    order = models.IntegerField(
        default=1,
        help_text="Execution order within workflow"
    )
    phase = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional phase grouping (e.g., 'Planning', 'Execution')"
    )
    
    # Dependencies (simplified - boolean for now, M2M relationship added later)
    has_dependencies = models.BooleanField(
        default=False,
        help_text="Whether this activity has prerequisite dependencies"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['workflow', 'order', 'name']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        constraints = [
            models.UniqueConstraint(
                fields=['workflow', 'name'],
                name='unique_activity_per_workflow'
            )
        ]
    
    def __str__(self):
        """String representation showing name and order."""
        return f"{self.name} (#{self.order})"
    
    def is_owned_by(self, user):
        """
        Check if user owns the parent workflow's playbook.
        
        :param user: User to check ownership for
        :returns: True if user owns parent playbook
        :rtype: bool
        
        Example:
            >>> activity.is_owned_by(maria)
            True  # If maria owns the playbook
        """
        return self.workflow.playbook.is_owned_by(user)
    
    def can_edit(self, user):
        """
        Check if user can edit this activity.
        
        User can edit if they own the parent playbook and it's an owned playbook.
        
        :param user: User to check edit permission for
        :returns: True if user can edit
        :rtype: bool
        
        Example:
            >>> activity.can_edit(maria)
            True  # If maria owns the playbook
        """
        return self.workflow.can_edit(user)
    
    def get_phase_display_name(self):
        """
        Get formatted phase name or default.
        
        :returns: Phase name or 'Unassigned' if no phase set
        :rtype: str
        
        Example:
            >>> activity.get_phase_display_name()
            'Planning'  # If phase is set
            >>> no_phase_activity.get_phase_display_name()
            'Unassigned'  # If phase is None or empty
        """
        return self.phase if self.phase else "Unassigned"
