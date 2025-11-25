"""
Activity service for managing user activity tracking and logging.

This service provides a clean interface for logging and retrieving user activities
throughout the application. It abstracts the database operations and provides
business logic for activity management.
"""

import logging
from typing import List, Dict, Optional, Any
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from methodology.models.activity import Activity
from methodology.models.playbook import Playbook

logger = logging.getLogger(__name__)

User = get_user_model()


class ActivityService:
    """
    Service for managing user activities and recent actions.
    
    This service handles the business logic for:
    - Logging user activities
    - Retrieving recent activities for feeds
    - Getting recent playbooks for dashboard
    - Activity analytics and reporting
    """
    
    def __init__(self):
        """
        Initialize the activity service.
        
        Sets up logging and any required dependencies.
        """
        logger.info("ActivityService initialized")
        pass
    
    def log_activity(
        self, 
        user: User, 
        action_type: str, 
        playbook: Optional[Playbook] = None, 
        description: Optional[str] = None, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Activity:
        """
        Log a user activity with comprehensive error handling.
        
        Args:
            user (User): The user performing the action
            action_type (str): Type of action from Activity.ACTION_TYPE_CHOICES
            playbook (Playbook, optional): Related playbook instance
            description (str, optional): Human-readable description
            metadata (dict, optional): Additional structured data
            
        Returns:
            Activity: The created activity instance
            
        Raises:
            ValueError: If action_type is invalid or user is None
            ValidationError: If required fields are missing
            DatabaseError: If database operation fails
            
        Example:
            >>> service = ActivityService()
            >>> activity = service.log_activity(
            ...     user=request.user,
            ...     action_type='playbook_created',
            ...     playbook=new_playbook,
            ...     description="Created new playbook 'User Guide'"
            ... )
        """
        if not user:
            raise ValueError("User cannot be None")
        
        if not action_type:
            raise ValueError("Action type cannot be empty")
        
        logger.info(f"Logging activity: {action_type} for user {user.username}")
        
        try:
            # Validate action type by attempting to create the activity
            # This will raise ValueError if invalid
            activity = Activity.log_activity(
                user=user,
                action_type=action_type,
                playbook=playbook,
                description=description,
                metadata=metadata or {}
            )
            
            logger.info(f"Successfully logged activity {activity.id} for user {user.username}")
            return activity
            
        except ValueError as e:
            logger.error(f"Validation error logging activity: {e}")
            raise
        except Exception as e:
            logger.error(f"Database error logging activity: {e}")
            raise
    
    def get_recent_activities(self, user: User, limit: int = 10) -> QuerySet[Activity]:
        """
        Get recent activities for a user with optimized queries.
        
        Args:
            user (User): The user to get activities for
            limit (int): Maximum number of activities to return
            
        Returns:
            QuerySet[Activity]: Recent activities ordered by timestamp descending
            
        Raises:
            ValueError: If user is None or limit is invalid
            DatabaseError: If database query fails
            
        Example:
            >>> service = ActivityService()
            >>> activities = service.get_recent_activities(user, limit=5)
            >>> for activity in activities:
            ...     print(f"{action.action_type}: {action.description}")
        """
        if not user:
            raise ValueError("User cannot be None")
        
        if limit <= 0:
            raise ValueError("Limit must be positive")
        
        logger.info(f"Getting recent activities for user {user.username}, limit={limit}")
        
        try:
            # Use select_related for playbook to optimize queries
            activities = Activity.objects.filter(
                user=user
            ).select_related(
                'playbook'
            ).order_by(
                '-timestamp'
            )[:limit]
            
            logger.info(f"Retrieved {len(activities)} activities for user {user.username}")
            return activities
            
        except Exception as e:
            logger.error(f"Database error getting recent activities: {e}")
            raise
    
    def get_recent_playbooks(self, user: User, limit: int = 5) -> List[Playbook]:
        """
        Get recent playbooks for a user with optimized queries.
        
        Args:
            user (User): The user to get playbooks for
            limit (int): Maximum number of playbooks to return
            
        Returns:
            List[Playbook]: Recent playbooks ordered by updated_at descending
            
        Raises:
            ValueError: If user is None or limit is invalid
            DatabaseError: If database query fails
            
        Example:
            >>> service = ActivityService()
            >>> playbooks = service.get_recent_playbooks(user, limit=3)
            >>> for playbook in playbooks:
            ...     print(f"{playbook.name} (v{playbook.version})")
        """
        if not user:
            raise ValueError("User cannot be None")
        
        if limit <= 0:
            raise ValueError("Limit must be positive")
        
        logger.info(f"Getting recent playbooks for user {user.username}, limit={limit}")
        
        try:
            playbooks = Playbook.objects.filter(
                author=user
            ).order_by(
                '-updated_at'
            )[:limit]
            
            logger.info(f"Retrieved {len(playbooks)} playbooks for user {user.username}")
            return list(playbooks)
            
        except Exception as e:
            logger.error(f"Database error getting recent playbooks: {e}")
            raise
    
    def get_activity_statistics(self, user: User, days: int = 30) -> Dict[str, Any]:
        """
        Get activity statistics for a user within a time period.
        
        Args:
            user (User): The user to get statistics for
            days (int): Number of days to look back
            
        Returns:
            Dict[str, Any]: Statistics including counts by action type
            
        Raises:
            ValueError: If user is None or days is invalid
            DatabaseError: If database query fails
            
        Example:
            >>> service = ActivityService()
            >>> stats = service.get_activity_statistics(user, days=7)
            >>> print(f"Total activities: {stats['total_activities']}")
            >>> print(f"Playbooks created: {stats['playbook_created_count']}")
        """
        if not user:
            raise ValueError("User cannot be None")
        
        if days <= 0:
            raise ValueError("Days must be positive")
        
        logger.info(f"Getting activity statistics for user {user.username}, days={days}")
        
        try:
            from django.utils import timezone
            import datetime
            
            cutoff_date = timezone.now() - datetime.timedelta(days=days)
            
            # Get all activities within the time period
            activities = Activity.objects.filter(
                user=user,
                timestamp__gte=cutoff_date
            )
            
            # Calculate statistics
            stats = {
                'total_activities': activities.count(),
                'date_range': {
                    'start': cutoff_date,
                    'end': timezone.now()
                }
            }
            
            # Count by action type
            action_counts = {}
            for action_type, _ in Activity.ACTION_TYPE_CHOICES:
                count = activities.filter(action_type=action_type).count()
                if count > 0:
                    action_counts[f"{action_type}_count"] = count
            
            stats.update(action_counts)
            
            logger.info(f"Generated statistics for user {user.username}: {stats['total_activities']} activities")
            return stats
            
        except Exception as e:
            logger.error(f"Database error getting activity statistics: {e}")
            raise
    
    def cleanup_old_activities(self, days_to_keep: int = 90) -> int:
        """
        Clean up old activities beyond retention period.
        
        Args:
            days_to_keep (int): Number of days to keep activities
            
        Returns:
            int: Number of activities deleted
            
        Raises:
            ValueError: If days_to_keep is invalid
            DatabaseError: If database operation fails
        """
        if days_to_keep <= 0:
            raise ValueError("Days to keep must be positive")
        
        logger.info(f"Cleaning up activities older than {days_to_keep} days")
        
        try:
            from django.utils import timezone
            import datetime
            
            cutoff_date = timezone.now() - datetime.timedelta(days=days_to_keep)
            
            # Delete old activities
            deleted_count, _ = Activity.objects.filter(
                timestamp__lt=cutoff_date
            ).delete()
            
            logger.info(f"Deleted {deleted_count} old activities")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Database error cleaning up old activities: {e}")
            raise
    
    def get_activity_feed_data(self, user: User) -> Dict[str, Any]:
        """
        Get complete dashboard activity feed data in one query.
        
        Args:
            user (User): The user to get feed data for
            
        Returns:
            Dict[str, Any]: Dictionary with recent_activities and recent_playbooks
            
        Raises:
            ValueError: If user is None
            DatabaseError: If database query fails
            
        Example:
            >>> service = ActivityService()
            >>> data = service.get_activity_feed_data(user)
            >>> activities = data['recent_activities']
            >>> playbooks = data['recent_playbooks']
        """
        if not user:
            raise ValueError("User cannot be None")
        
        logger.info(f"Getting activity feed data for user {user.username}")
        
        try:
            # Get both recent activities and playbooks
            recent_activities = self.get_recent_activities(user, limit=10)
            recent_playbooks = self.get_recent_playbooks(user, limit=5)
            
            data = {
                'recent_activities': recent_activities,
                'recent_playbooks': recent_playbooks,
                'activity_count': len(recent_activities),
                'playbook_count': len(recent_playbooks)
            }
            
            logger.info(f"Retrieved feed data for user {user.username}: {data['activity_count']} activities, {data['playbook_count']} playbooks")
            return data
            
        except Exception as e:
            logger.error(f"Database error getting activity feed data: {e}")
            raise
