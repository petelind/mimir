"""Unit tests for ActivityService.

Tests cover service methods, error handling, and business logic.
Follows do-test-first.md - tests written before implementation.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import DatabaseError
from methodology.services.activity_service import ActivityService
from methodology.models.activity import Activity
from methodology.models.playbook import Playbook

User = get_user_model()


@pytest.mark.django_db
class TestActivityService(TestCase):
    """Test ActivityService functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.playbook = Playbook.objects.create(
            name='Test Playbook',
            description='A test playbook',
            category='development',
            author=self.user
        )
        self.service = ActivityService()
    
    def test_service_initialization(self):
        """Test ActivityService initializes correctly."""
        service = ActivityService()
        assert service is not None
        assert hasattr(service, 'log_activity')
        assert hasattr(service, 'get_recent_activities')
        assert hasattr(service, 'get_recent_playbooks')
    
    def test_log_activity_success_minimal(self):
        """Test log_activity with minimal required parameters."""
        activity = self.service.log_activity(
            user=self.user,
            action_type='dashboard_viewed',
            description='User viewed dashboard'
        )
        
        assert isinstance(activity, Activity)
        assert activity.user == self.user
        assert activity.action_type == 'dashboard_viewed'
        assert activity.description == 'User viewed dashboard'
        assert activity.playbook is None
        assert activity.metadata == {}
    
    def test_log_activity_success_with_playbook(self):
        """Test log_activity with playbook parameter."""
        activity = self.service.log_activity(
            user=self.user,
            action_type='playbook_viewed',
            playbook=self.playbook,
            description='User viewed playbook'
        )
        
        assert activity.playbook == self.playbook
        assert activity.user == self.user
        assert activity.action_type == 'playbook_viewed'
    
    def test_log_activity_success_with_metadata(self):
        """Test log_activity with metadata parameter."""
        metadata = {'ip_address': '192.168.1.1', 'version': 2}
        activity = self.service.log_activity(
            user=self.user,
            action_type='playbook_updated',
            playbook=self.playbook,
            description='Updated playbook',
            metadata=metadata
        )
        
        assert activity.metadata == metadata
    
    def test_log_activity_none_user_raises_error(self):
        """Test log_activity with None user raises ValueError."""
        with pytest.raises(ValueError, match="User cannot be None"):
            self.service.log_activity(
                user=None,
                action_type='dashboard_viewed',
                description='Invalid activity'
            )
    
    def test_log_activity_empty_action_type_raises_error(self):
        """Test log_activity with empty action_type raises ValueError."""
        with pytest.raises(ValueError, match="Action type cannot be empty"):
            self.service.log_activity(
                user=self.user,
                action_type='',
                description='Invalid activity'
            )
        
        with pytest.raises(ValueError, match="Action type cannot be empty"):
            self.service.log_activity(
                user=self.user,
                action_type=None,
                description='Invalid activity'
            )
    
    def test_log_activity_invalid_action_type_raises_error(self):
        """Test log_activity with invalid action_type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid action_type"):
            self.service.log_activity(
                user=self.user,
                action_type='invalid_action',
                description='Invalid activity'
            )
    
    def test_get_recent_activities_success(self):
        """Test get_recent_activities with valid parameters."""
        # Create test activities
        Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='Activity 1'
        )
        Activity.objects.create(
            user=self.user,
            action_type='playbook_viewed',
            playbook=self.playbook,
            description='Activity 2'
        )
        
        activities = self.service.get_recent_activities(self.user, limit=5)
        
        assert activities.count() == 2
        assert activities[0].action_type == 'playbook_viewed'  # Most recent
        assert activities[1].action_type == 'dashboard_viewed'
    
    def test_get_recent_activities_limit_parameter(self):
        """Test get_recent_activities respects limit parameter."""
        # Create more activities than limit
        for i in range(5):
            Activity.objects.create(
                user=self.user,
                action_type='dashboard_viewed',
                description=f'Activity {i}'
            )
        
        activities = self.service.get_recent_activities(self.user, limit=3)
        assert activities.count() == 3
    
    def test_get_recent_activities_none_user_raises_error(self):
        """Test get_recent_activities with None user raises ValueError."""
        with pytest.raises(ValueError, match="User cannot be None"):
            self.service.get_recent_activities(user=None, limit=10)
    
    def test_get_recent_activities_invalid_limit_raises_error(self):
        """Test get_recent_activities with invalid limit raises ValueError."""
        with pytest.raises(ValueError, match="Limit must be positive"):
            self.service.get_recent_activities(self.user, limit=0)
        
        with pytest.raises(ValueError, match="Limit must be positive"):
            self.service.get_recent_activities(self.user, limit=-5)
    
    def test_get_recent_playbooks_success(self):
        """Test get_recent_playbooks with valid parameters."""
        # Create additional playbooks
        for i in range(3):
            Playbook.objects.create(
                name=f'Playbook {i}',
                description=f'Description {i}',
                category='development',
                author=self.user
            )
        
        playbooks = self.service.get_recent_playbooks(self.user, limit=5)
        
        assert len(playbooks) == 4  # Original + 3 new
        assert all(isinstance(pb, Playbook) for pb in playbooks)
        # Should be ordered by updated_at descending
        assert playbooks[0].updated_at >= playbooks[1].updated_at
    
    def test_get_recent_playbooks_limit_parameter(self):
        """Test get_recent_playbooks respects limit parameter."""
        # Create more playbooks than limit
        for i in range(5):
            Playbook.objects.create(
                name=f'Playbook {i}',
                description=f'Description {i}',
                category='development',
                author=self.user
            )
        
        playbooks = self.service.get_recent_playbooks(self.user, limit=3)
        assert len(playbooks) == 3
    
    def test_get_recent_playbooks_none_user_raises_error(self):
        """Test get_recent_playbooks with None user raises ValueError."""
        with pytest.raises(ValueError, match="User cannot be None"):
            self.service.get_recent_playbooks(user=None, limit=5)
    
    def test_get_recent_playbooks_invalid_limit_raises_error(self):
        """Test get_recent_playbooks with invalid limit raises ValueError."""
        with pytest.raises(ValueError, match="Limit must be positive"):
            self.service.get_recent_playbooks(self.user, limit=0)
    
    def test_get_activity_statistics_success(self):
        """Test get_activity_statistics with valid parameters."""
        # Create various activities
        Activity.objects.create(
            user=self.user,
            action_type='playbook_created',
            playbook=self.playbook,
            description='Created playbook'
        )
        Activity.objects.create(
            user=self.user,
            action_type='playbook_viewed',
            playbook=self.playbook,
            description='Viewed playbook'
        )
        Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='Viewed dashboard'
        )
        
        stats = self.service.get_activity_statistics(self.user, days=30)
        
        assert isinstance(stats, dict)
        assert 'total_activities' in stats
        assert 'playbook_created_count' in stats
        assert 'playbook_viewed_count' in stats
        assert 'dashboard_viewed_count' in stats
        assert stats['total_activities'] == 3
        assert stats['playbook_created_count'] == 1
    
    def test_get_activity_statistics_none_user_raises_error(self):
        """Test get_activity_statistics with None user raises ValueError."""
        with pytest.raises(ValueError, match="User cannot be None"):
            self.service.get_activity_statistics(user=None, days=30)
    
    def test_get_activity_statistics_invalid_days_raises_error(self):
        """Test get_activity_statistics with invalid days raises ValueError."""
        with pytest.raises(ValueError, match="Days must be positive"):
            self.service.get_activity_statistics(self.user, days=0)
    
    def test_cleanup_old_activities_success(self):
        """Test cleanup_old_activities with valid parameters."""
        # Note: This test would require mocking time or creating old activities
        # For now, just test the method exists and handles parameters
        result = self.service.cleanup_old_activities(days_to_keep=90)
        assert isinstance(result, int)
    
    def test_cleanup_old_activities_invalid_days_raises_error(self):
        """Test cleanup_old_activities with invalid days raises ValueError."""
        with pytest.raises(ValueError, match="Days to keep must be positive"):
            self.service.cleanup_old_activities(days_to_keep=0)
    
    def test_get_activity_feed_data_success(self):
        """Test get_activity_feed_data returns complete data."""
        # Create test data
        Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='Viewed dashboard'
        )
        Activity.objects.create(
            user=self.user,
            action_type='playbook_viewed',
            playbook=self.playbook,
            description='Viewed playbook'
        )
        
        data = self.service.get_activity_feed_data(self.user)
        
        assert isinstance(data, dict)
        assert 'recent_activities' in data
        assert 'recent_playbooks' in data
        assert len(data['recent_activities']) == 2
        assert len(data['recent_playbooks']) == 1  # self.playbook
    
    def test_get_activity_feed_data_none_user_raises_error(self):
        """Test get_activity_feed_data with None user raises ValueError."""
        with pytest.raises(ValueError, match="User cannot be None"):
            self.service.get_activity_feed_data(user=None)
