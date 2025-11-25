"""Integration tests for dashboard view.

Tests the complete dashboard functionality including:
- Dashboard displays all 3 sections
- Recent playbooks show correctly  
- Activity feed displays recent actions
- Quick action buttons are visible and functional

Follows do-not-mock-in-integration-tests.md - uses real data.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from methodology.models.playbook import Playbook
from methodology.models.activity import Activity

User = get_user_model()


@pytest.mark.django_db
class TestDashboardView:
    """Test dashboard view functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='maria',
            email='maria@example.com',
            password='testpass123'
        )
        
        # Create test playbooks
        self.playbook1 = Playbook.objects.create(
            name='User Guide Playbook',
            description='A comprehensive user guide',
            category='development',
            author=self.user,
            status='active'
        )
        self.playbook2 = Playbook.objects.create(
            name='API Documentation',
            description='API endpoints documentation',
            category='development',
            author=self.user,
            status='draft'
        )
        
        # Create test activities
        Activity.log_activity(
            user=self.user,
            action_type='dashboard_viewed',
            description='Maria viewed dashboard'
        )
        Activity.log_activity(
            user=self.user,
            action_type='playbook_created',
            playbook=self.playbook1,
            description='Maria created playbook'
        )
        Activity.log_activity(
            user=self.user,
            action_type='playbook_viewed',
            playbook=self.playbook2,
            description='Maria viewed playbook'
        )
    
    def test_dashboard_displays_sections(self):
        """
        Test dashboard displays all 3 sections.
        
        Acceptance Criteria: Dashboard displays all 3 sections
        """
        # Login user
        self.client.login(username='maria', password='testpass123')
        
        # Get dashboard page
        response = self.client.get('/dashboard/')
        
        # Assert page loads successfully
        assert response.status_code == 200
        assert response.templates[0].name == 'dashboard.html'
        
        # Assert all 3 sections are present
        content = response.content.decode('utf-8')
        assert 'data-testid="my-playbooks-section"' in content
        assert 'data-testid="recent-activity-section"' in content
        assert 'data-testid="quick-actions-section"' in content
        
        # Assert dashboard loaded indicator
        assert 'data-testid="dashboard-loaded"' in content
    
    def test_recent_playbooks_show_correctly(self):
        """
        Test recent playbooks show correctly (5 most recent).
        
        Acceptance Criteria: Recent playbooks show correctly
        """
        # Create additional playbooks (total should be more than 5)
        for i in range(4):
            Playbook.objects.create(
                name=f'Extra Playbook {i}',
                description=f'Extra description {i}',
                category='other',
                author=self.user,
                status='draft'
            )
        
        # Login and get dashboard
        self.client.login(username='maria', password='testpass123')
        response = self.client.get('/dashboard/')
        
        # Assert context contains playbook data
        assert 'recent_playbooks' in response.context
        assert 'playbook_count' in response.context
        
        # Should show 5 most recent playbooks
        recent_playbooks = response.context['recent_playbooks']
        assert len(recent_playbooks) == 5
        
        # Assert playbook items are rendered
        content = response.content.decode('utf-8')
        assert 'data-testid="playbook-item-1"' in content
        assert 'data-testid="playbook-item-2"' in content
        assert 'User Guide Playbook' in content
        assert 'API Documentation' in content
        
        # Assert view all playbooks link
        assert 'data-testid="view-all-playbooks"' in content
    
    def test_activity_feed_displays_recent_actions(self):
        """
        Test activity feed displays recent actions (10 most recent).
        
        Acceptance Criteria: Activity feed displays recent actions
        """
        # Create additional activities (total should be more than 10)
        for i in range(8):
            Activity.log_activity(
                user=self.user,
                action_type='playbook_viewed',
                description=f'Activity {i}'
            )
        
        # Login and get dashboard
        self.client.login(username='maria', password='testpass123')
        response = self.client.get('/dashboard/')
        
        # Assert context contains activity data
        assert 'recent_activities' in response.context
        assert 'activity_count' in response.context
        
        # Should show 10 most recent activities
        recent_activities = response.context['recent_activities']
        assert len(recent_activities) == 10
        
        # Assert activity items are rendered
        content = response.content.decode('utf-8')
        assert 'data-testid="activity-item-1"' in content
        assert 'data-testid="activity-item-2"' in content
        
        # Check for some expected activity descriptions
        assert 'maria viewed dashboard' in content
        assert 'maria created playbook' in content
        
        # Assert activity with playbook link exists
        assert 'data-testid="activity-playbook-link"' in content
        assert 'User Guide Playbook' in content
    
    def test_quick_action_buttons_visible_and_functional(self):
        """
        Test quick action buttons are visible and functional.
        
        Acceptance Criteria: Quick action buttons are visible and functional
        """
        # Login and get dashboard
        self.client.login(username='maria', password='testpass123')
        response = self.client.get('/dashboard/')
        
        content = response.content.decode('utf-8')
        
        # Assert all quick action buttons are present
        assert 'data-testid="quick-action-new-playbook"' in content
        assert 'data-testid="quick-action-import-playbook"' in content
        assert 'data-testid="quick-action-sync-homebase"' in content
        
        # Assert new playbook button is functional (not disabled)
        assert '+ New Playbook' in content
        assert 'href="/playbooks/playbook/create/"' in content
        # Check that it's an anchor tag, not a disabled button
        assert '<a href="/playbooks/playbook/create/"' in content
        
        # Assert other buttons are disabled (coming soon)
        assert 'disabled' in content  # At least one disabled button should exist
        # Check that import and sync are disabled buttons
        assert 'data-testid="quick-action-import-playbook"' in content
        assert 'data-testid="quick-action-sync-homebase"' in content
        assert 'class="btn btn-outline-secondary btn-lg w-100 h-100 d-flex flex-column justify-content-center align-items-center disabled"' in content
        
        # Assert tooltips are present
        assert 'title="Create a new playbook from scratch"' in content
        assert 'title="Import playbook from file (coming soon)"' in content
        assert 'title="Sync with Homebase repository (coming soon)"' in content
    
    def test_dashboard_requires_authentication(self):
        """Test dashboard view requires authentication."""
        # Try to access dashboard without login
        response = self.client.get('/dashboard/')
        
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/user/login/' in response.url
    
    def test_dashboard_with_no_playbooks(self):
        """Test dashboard displays correctly when user has no playbooks."""
        # Delete existing playbooks
        Playbook.objects.filter(author=self.user).delete()
        
        # Login and get dashboard
        self.client.login(username='maria', password='testpass123')
        response = self.client.get('/dashboard/')
        
        content = response.content.decode('utf-8')
        
        # Should show no playbooks message
        assert 'data-testid="no-playbooks"' in content
        assert 'No playbooks yet' in content
        assert 'Create your first playbook' in content
        assert 'data-testid="create-first-playbook"' in content
    
    def test_dashboard_with_no_activities(self):
        """Test dashboard displays correctly when user has no activities."""
        # Delete existing activities
        Activity.objects.filter(user=self.user).delete()
        
        # Login and get dashboard
        self.client.login(username='maria', password='testpass123')
        response = self.client.get('/dashboard/')
        
        content = response.content.decode('utf-8')
        
        # Should show no activities message
        assert 'data-testid="no-activities"' in content
        assert 'No recent activity' in content
        assert 'Your activity will appear here' in content
    
    def test_dashboard_logs_activity(self):
        """Test dashboard view creates activity log entry."""
        # Clear existing activities
        Activity.objects.filter(user=self.user).delete()
        
        # Login and get dashboard
        self.client.login(username='maria', password='testpass123')
        response = self.client.get('/dashboard/')
        
        # Assert dashboard view activity was logged
        activities = Activity.objects.filter(user=self.user, action_type='dashboard_viewed')
        assert activities.count() == 1
        assert 'maria viewed dashboard' in activities.first().description
    
    def test_dashboard_error_handling(self):
        """Test dashboard handles errors gracefully."""
        # Mock ActivityService to raise an exception
        from unittest.mock import patch
        from methodology.services.activity_service import ActivityService
        
        with patch.object(ActivityService, 'get_activity_feed_data', side_effect=Exception("Database error")):
            # Login and get dashboard
            self.client.login(username='maria', password='testpass123')
            response = self.client.get('/dashboard/')
            
            # Should still load dashboard with error message
            assert response.status_code == 200
            content = response.content.decode('utf-8')
            assert 'data-testid="dashboard-error"' in content
            assert 'Unable to load some dashboard data' in content
    
    def test_dashboard_context_data(self):
        """Test dashboard provides correct context data."""
        # Login and get dashboard
        self.client.login(username='maria', password='testpass123')
        response = self.client.get('/dashboard/')
        
        # Assert all expected context variables
        assert 'recent_playbooks' in response.context
        assert 'recent_activities' in response.context
        assert 'activity_count' in response.context
        assert 'playbook_count' in response.context
        
        # Assert data types
        assert hasattr(response.context['recent_playbooks'], '__iter__')
        assert hasattr(response.context['recent_activities'], '__iter__')
        assert isinstance(response.context['activity_count'], int)
        assert isinstance(response.context['playbook_count'], int)
        
        # Assert counts are correct
        assert response.context['playbook_count'] == 2  # 2 playbooks created
        assert response.context['activity_count'] == 3  # 3 activities created
