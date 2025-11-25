"""Unit tests for Activity model.

Tests cover model creation, validation, methods, and queries.
Follows do-test-first.md - tests written before implementation.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from methodology.models.activity import Activity
from methodology.models.playbook import Playbook

User = get_user_model()


@pytest.mark.django_db
class TestActivityModel(TestCase):
    """Test Activity model functionality."""
    
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
    
    def test_activity_creation_minimal_fields(self):
        """Test creating activity with minimal required fields."""
        activity = Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='User viewed dashboard'
        )
        
        assert activity.user == self.user
        assert activity.action_type == 'dashboard_viewed'
        assert activity.description == 'User viewed dashboard'
        assert activity.playbook is None
        assert activity.metadata == {}
        assert activity.timestamp is not None
        assert str(activity) == f"{self.user.username}: dashboard_viewed at {activity.timestamp}"
    
    def test_activity_creation_with_playbook(self):
        """Test creating activity with related playbook."""
        activity = Activity.objects.create(
            user=self.user,
            action_type='playbook_viewed',
            playbook=self.playbook,
            description='User viewed playbook'
        )
        
        assert activity.playbook == self.playbook
        assert activity.user == self.user
        assert activity.action_type == 'playbook_viewed'
    
    def test_activity_creation_with_metadata(self):
        """Test creating activity with metadata."""
        metadata = {'ip_address': '192.168.1.1', 'user_agent': 'Chrome'}
        activity = Activity.objects.create(
            user=self.user,
            action_type='playbook_created',
            playbook=self.playbook,
            description='User created playbook',
            metadata=metadata
        )
        
        assert activity.metadata == metadata
    
    def test_activity_str_representation(self):
        """Test string representation of activity."""
        activity = Activity.objects.create(
            user=self.user,
            action_type='playbook_created',
            description='User created playbook'
        )
        
        expected = f"{self.user.username}: playbook_created at {activity.timestamp}"
        assert str(activity) == expected
    
    def test_activity_ordering(self):
        """Test activities are ordered by timestamp descending."""
        # Create activities with delay to ensure different timestamps
        import time
        activity1 = Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='First activity'
        )
        time.sleep(0.01)  # Small delay
        activity2 = Activity.objects.create(
            user=self.user,
            action_type='playbook_viewed',
            description='Second activity'
        )
        
        activities = Activity.objects.all()
        assert activities[0] == activity2  # Most recent first
        assert activities[1] == activity1
    
    def test_invalid_action_type_raises_validation_error(self):
        """Test that invalid action type raises validation error."""
        with pytest.raises(ValidationError):
            activity = Activity(
                user=self.user,
                action_type='invalid_action',
                description='Invalid action'
            )
            activity.full_clean()
    
    def test_activity_user_relationship(self):
        """Test activity-user relationship."""
        activity = Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='User viewed dashboard'
        )
        
        # Test reverse relationship
        user_activities = self.user.activities.all()
        assert activity in user_activities
        assert user_activities.count() == 1
    
    def test_activity_playbook_relationship(self):
        """Test activity-playbook relationship."""
        activity = Activity.objects.create(
            user=self.user,
            action_type='playbook_viewed',
            playbook=self.playbook,
            description='User viewed playbook'
        )
        
        # Test reverse relationship
        playbook_activities = self.playbook.activities.all()
        assert activity in playbook_activities
        assert playbook_activities.count() == 1
    
    def test_get_recent_activities_for_user_success(self):
        """Test get_recent_activities_for_user with valid parameters."""
        # Create multiple activities
        Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='Dashboard view 1'
        )
        Activity.objects.create(
            user=self.user,
            action_type='playbook_viewed',
            playbook=self.playbook,
            description='Playbook view 1'
        )
        
        # Test the method
        activities = Activity.get_recent_activities_for_user(self.user, limit=5)
        assert activities.count() == 2
        assert activities[0].action_type == 'playbook_viewed'  # Most recent
    
    def test_get_recent_activities_for_user_invalid_limit(self):
        """Test get_recent_activities_for_user with invalid limit."""
        with pytest.raises(ValueError, match="Limit must be a positive integer"):
            Activity.get_recent_activities_for_user(self.user, limit=0)
        
        with pytest.raises(ValueError, match="Limit must be a positive integer"):
            Activity.get_recent_activities_for_user(self.user, limit=-1)
        
        with pytest.raises(ValueError, match="Limit must be a positive integer"):
            Activity.get_recent_activities_for_user(self.user, limit='invalid')
    
    def test_log_activity_success(self):
        """Test log_activity with valid parameters."""
        activity = Activity.log_activity(
            user=self.user,
            action_type='playbook_created',
            playbook=self.playbook,
            description='Created new playbook',
            metadata={'version': 1}
        )
        
        assert activity.user == self.user
        assert activity.action_type == 'playbook_created'
        assert activity.playbook == self.playbook
        assert activity.description == 'Created new playbook'
        assert activity.metadata == {'version': 1}
    
    def test_log_activity_invalid_action_type(self):
        """Test log_activity with invalid action type."""
        with pytest.raises(ValueError, match="Invalid action_type"):
            Activity.log_activity(
                user=self.user,
                action_type='invalid_action',
                description='Invalid action'
            )
    
    def test_get_action_display_with_icon(self):
        """Test get_action_display_with_icon method."""
        activity = Activity.objects.create(
            user=self.user,
            action_type='playbook_created',
            description='Created playbook'
        )
        
        icon_display = activity.get_action_display_with_icon()
        assert 'fa-plus-circle' in icon_display
        assert 'Playbook Created' in icon_display
    
    def test_is_recent_true(self):
        """Test is_recent method for recent activity."""
        activity = Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='Recent activity'
        )
        
        # Should be recent within 30 minutes
        assert activity.is_recent(minutes=30) is True
    
    def test_is_recent_false(self):
        """Test is_recent method for old activity."""
        activity = Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='Old activity'
        )
        
        # Should not be recent within 0 minutes
        assert activity.is_recent(minutes=0) is False
    
    def test_activity_metadata_default(self):
        """Test metadata defaults to empty dict."""
        activity = Activity.objects.create(
            user=self.user,
            action_type='dashboard_viewed',
            description='Test activity'
        )
        
        assert activity.metadata == {}
    
    def test_activity_choices_are_valid(self):
        """Test all action_type choices are valid."""
        valid_choices = dict(Activity.ACTION_TYPE_CHOICES)
        
        for choice, display in valid_choices.items():
            activity = Activity.objects.create(
                user=self.user,
                action_type=choice,
                description=f'Test {display}'
            )
            assert activity.action_type == choice
            assert activity.get_action_type_display() == display
