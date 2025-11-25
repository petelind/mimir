"""
Activity model for tracking user actions in the system.

This model provides an audit trail of all user actions across playbooks,
workflows, and other entities. It enables the recent activity feed
on the dashboard and supports user engagement analytics.
"""

from django.db import models
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class Activity(models.Model):
    """
    Track user actions for activity feeds and audit trails.
    
    Activities represent user actions such as creating, updating, viewing,
    or deleting playbooks and other entities. Each activity is linked to
    a user and optionally to a specific playbook.
    
    Attributes:
        user (User): The user who performed the action
        action_type (str): Type of action performed
        playbook (Playbook): Related playbook (optional)
        description (str): Human-readable description of the action
        timestamp (datetime): When the action occurred
        metadata (dict): Additional structured data about the action
    """
    
    # Action type choices following semantic naming
    ACTION_TYPE_CHOICES = [
        ('playbook_created', 'Playbook Created'),
        ('playbook_updated', 'Playbook Updated'),
        ('playbook_deleted', 'Playbook Deleted'),
        ('playbook_viewed', 'Playbook Viewed'),
        ('dashboard_viewed', 'Dashboard Viewed'),
        ('workflow_created', 'Workflow Created'),
        ('workflow_updated', 'Workflow Updated'),
        ('workflow_deleted', 'Workflow Deleted'),
        ('activity_created', 'Activity Created'),
        ('activity_updated', 'Activity Updated'),
        ('activity_deleted', 'Activity Deleted'),
        ('pip_created', 'PIP Created'),
        ('pip_approved', 'PIP Approved'),
        ('pip_rejected', 'PIP Rejected'),
    ]
    
    # Fields
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='activities',
        help_text="The user who performed this action"
    )
    action_type = models.CharField(
        max_length=50, 
        choices=ACTION_TYPE_CHOICES,
        help_text="Type of action performed"
    )
    playbook = models.ForeignKey(
        'methodology.Playbook', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='activities',
        help_text="Related playbook if applicable"
    )
    description = models.TextField(
        max_length=500,
        help_text="Human-readable description of what happened"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When this action occurred"
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional structured data about the action"
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action_type']),
            models.Index(fields=['timestamp']),
        ]
        verbose_name_plural = "Activities"
    
    def __str__(self):
        """
        Return string representation of the activity.
        
        Returns:
            str: Description in format "User: action_type at timestamp"
        """
        return f"{self.user.username}: {self.action_type} at {self.timestamp}"
    
    @classmethod
    def get_recent_activities_for_user(cls, user, limit=10):
        """
        Get recent activities for a specific user.
        
        Args:
            user (User): The user to get activities for
            limit (int): Maximum number of activities to return
            
        Returns:
            QuerySet: Recent activities ordered by timestamp descending
            
        Raises:
            ValueError: If limit is not a positive integer
        """
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Limit must be a positive integer")
        
        logger.info(f"Getting recent activities for user {user.username}, limit={limit}")
        return cls.objects.filter(user=user).order_by('-timestamp')[:limit]
    
    @classmethod
    def log_activity(cls, user, action_type, playbook=None, description=None, metadata=None):
        """
        Create a new activity entry.
        
        Args:
            user (User): The user performing the action
            action_type (str): Type of action from ACTION_TYPE_CHOICES
            playbook (Playbook, optional): Related playbook
            description (str, optional): Human-readable description
            metadata (dict, optional): Additional structured data
            
        Returns:
            Activity: The created activity instance
            
        Raises:
            ValueError: If action_type is not valid
            ValidationError: If required fields are missing
        """
        if action_type not in dict(cls.ACTION_TYPE_CHOICES):
            raise ValueError(f"Invalid action_type: {action_type}")
        
        logger.info(f"Logging activity: {action_type} for user {user.username}")
        
        # Set default description if not provided
        if not description:
            description = dict(cls.ACTION_TYPE_CHOICES).get(action_type, action_type)
        
        # Ensure metadata is a dict
        if metadata is None:
            metadata = {}
        
        return cls.objects.create(
            user=user,
            action_type=action_type,
            playbook=playbook,
            description=description,
            metadata=metadata
        )
    
    def get_action_display_with_icon(self):
        """
        Get action display text with appropriate icon.
        
        Returns:
            str: Action display text with Font Awesome icon
            
        Example:
            "fa-plus-circle Playbook Created"
        """
        # Icon mapping for different action types
        icon_map = {
            'playbook_created': 'fa-plus-circle',
            'playbook_updated': 'fa-edit',
            'playbook_deleted': 'fa-trash',
            'playbook_viewed': 'fa-eye',
            'dashboard_viewed': 'fa-gauge',
            'workflow_created': 'fa-plus-circle',
            'workflow_updated': 'fa-edit',
            'workflow_deleted': 'fa-trash',
            'activity_created': 'fa-plus-circle',
            'activity_updated': 'fa-edit',
            'activity_deleted': 'fa-trash',
            'pip_created': 'fa-lightbulb',
            'pip_approved': 'fa-check-circle',
            'pip_rejected': 'fa-times-circle',
        }
        
        icon = icon_map.get(self.action_type, 'fa-circle')
        display_text = self.get_action_type_display()
        
        return f"{icon} {display_text}"
    
    def get_icon_class(self):
        """
        Get just the icon class for the action type.
        
        Returns:
            str: Font Awesome icon class
            
        Example:
            "fa-plus-circle"
        """
        # Icon mapping for different action types
        icon_map = {
            'playbook_created': 'fa-plus-circle',
            'playbook_updated': 'fa-edit',
            'playbook_deleted': 'fa-trash',
            'playbook_viewed': 'fa-eye',
            'dashboard_viewed': 'fa-gauge',
            'workflow_created': 'fa-plus-circle',
            'workflow_updated': 'fa-edit',
            'workflow_deleted': 'fa-trash',
            'activity_created': 'fa-plus-circle',
            'activity_updated': 'fa-edit',
            'activity_deleted': 'fa-trash',
            'pip_created': 'fa-lightbulb',
            'pip_approved': 'fa-check-circle',
            'pip_rejected': 'fa-times-circle',
        }
        
        return icon_map.get(self.action_type, 'fa-circle')
    
    def is_recent(self, minutes=30):
        """
        Check if this activity occurred within the specified minutes.
        
        Args:
            minutes (int): Number of minutes to consider as recent
            
        Returns:
            bool: True if activity is recent, False otherwise
        """
        from django.utils import timezone
        import datetime
        
        if not isinstance(minutes, int) or minutes < 0:
            raise ValueError("Minutes must be a non-negative integer")
        
        threshold = timezone.now() - datetime.timedelta(minutes=minutes)
        return self.timestamp >= threshold
