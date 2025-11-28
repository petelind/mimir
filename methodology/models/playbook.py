"""
Playbook model for methodology management.

Playbooks represent methodologies with workflows, activities, and artifacts.
Each playbook can be owned (created by user) or downloaded from families.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Playbook(models.Model):
    """
    Playbook represents a methodology with workflows, activities, and artifacts.
    
    Playbooks can be owned (created by user) or downloaded from families.
    Each playbook tracks versions as integer increments (v1, v2, v3).
    """
    
    # Choices
    CATEGORY_CHOICES = [
        ('product', 'Product'),
        ('development', 'Development'),
        ('research', 'Research'),
        ('design', 'Design'),
        ('other', 'Other'),
    ]
    
    VISIBILITY_CHOICES = [
        ('private', 'Private (only me)'),
        ('family', 'Family'),  # TODO: Implement family sharing
        ('local', 'Local only (not uploaded to Homebase)'),  # TODO: Implement Homebase
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('draft', 'Draft'),
        ('disabled', 'Disabled'),
    ]
    
    SOURCE_CHOICES = [
        ('owned', 'Owned'),
        ('downloaded', 'Downloaded'),
    ]
    
    # Fields
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list, blank=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    version = models.IntegerField(default=1)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='owned')
    
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playbooks')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(fields=['author', 'name'], name='unique_playbook_per_author')
        ]
    
    def __str__(self):
        return f"{self.name} (v{self.version})"
    
    def is_owned_by(self, user):
        return self.author == user
    
    def can_edit(self, user):
        return self.source == 'owned' and self.is_owned_by(user)
    
    def get_quick_stats(self):
        """
        Get quick statistics for the playbook dashboard.
        
        Returns dictionary with counts of related objects.
        
        :returns: Dictionary with stat counts
        :rtype: dict
        """
        return {
            'workflows': self.workflows.count(),
            'phases': 0,  # TODO: Implement when Phase model exists
            'activities': 0,  # TODO: Implement when Activity model exists
            'artifacts': 0,  # TODO: Implement when Artifact model exists
            'roles': 0,  # TODO: Implement when Role model exists
            'howtos': 0,  # TODO: Implement when Howto model exists
            'goals': 'Coming soon (v2.1)'
        }
    
    def get_status_badge_color(self):
        """
        Get Bootstrap color class for status badge.
        
        Maps playbook status to Bootstrap badge color.
        
        :returns: Bootstrap color class name
        :rtype: str
        """
        status_colors = {
            'active': 'success',
            'draft': 'warning',
            'disabled': 'secondary'
        }
        return status_colors.get(self.status, 'secondary')
