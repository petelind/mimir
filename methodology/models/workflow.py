"""
Workflow model for organizing activities within playbooks.

Workflows represent execution sequences that group activities.
Each workflow belongs to a playbook and has a defined order.
"""

from django.db import models


class Workflow(models.Model):
    """
    Workflow represents an execution sequence within a playbook.
    
    Workflows organize activities into logical sequences and can optionally
    include phases for grouping. Each workflow has a specific order within
    its parent playbook.
    """
    
    # Core fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=500)
    playbook = models.ForeignKey('Playbook', on_delete=models.CASCADE, related_name='workflows')
    
    # Ordering and timestamps
    order = models.IntegerField(default=1, help_text="Execution order within playbook")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['playbook', 'name'],
                name='unique_workflow_per_playbook'
            )
        ]
    
    def __str__(self):
        return f"{self.name} (#{self.order})"
    
    def get_activity_count(self):
        """
        Get number of activities in this workflow.
        
        :returns: Activity count
        :rtype: int
        
        Example:
            >>> workflow.get_activity_count()
            0  # Returns 0 until Activity model is implemented
        """
        # TODO: Implement when Activity model exists
        return 0
    
    def get_phase_count(self):
        """
        Get number of phases in this workflow.
        
        :returns: Phase count
        :rtype: int
        
        Example:
            >>> workflow.get_phase_count()
            0  # Returns 0 until Phase model is implemented
        """
        # TODO: Implement when Phase model exists
        return 0
    
    def is_owned_by(self, user):
        """
        Check if user owns the parent playbook.
        
        :param user: User to check ownership for
        :returns: True if user owns parent playbook
        :rtype: bool
        """
        return self.playbook.is_owned_by(user)
    
    def can_edit(self, user):
        """
        Check if user can edit this workflow.
        
        User can edit if they own the parent playbook and it's an owned playbook.
        
        :param user: User to check edit permission for
        :returns: True if user can edit
        :rtype: bool
        """
        return self.playbook.can_edit(user)
