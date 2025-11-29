"""
Integration tests for Activity LIST operation.

Covers ACT-LIST-01 through ACT-LIST-05 and ACT-LIST-10 through ACT-LIST-13
from docs/features/act-5-activities/activities-list-find.feature.

Deferred to FIND feature:
- ACT-LIST-06: Search by name
- ACT-LIST-07: Filter by phase
- ACT-LIST-08: Filter by dependencies
- ACT-LIST-09: Reorder activities (drag-drop)
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow, Activity

User = get_user_model()


@pytest.mark.django_db
class TestActivityList:
    """Integration tests for activity list view (ACT-LIST scenarios)."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data for each test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='maria_test',
            email='maria@test.com',
            password='testpass123'
        )
        self.client.login(username='maria_test', password='testpass123')
        
        # Create playbook and workflow
        self.playbook = Playbook.objects.create(
            name='React Frontend Development',
            description='A comprehensive methodology',
            category='development',
            status='active',
            source='owned',
            author=self.user
        )
        
        self.workflow = Workflow.objects.create(
            name='Component Development',
            description='Develop React components',
            playbook=self.playbook,
            order=1
        )
    
    def test_act_list_01_navigate_from_workflow(self):
        """ACT-LIST-01: Navigate to activities list from workflow."""
        # Navigate to activities list
        url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'Activities in Component Development' in response.content
        assert b'data-testid="activities-list"' in response.content
    
    def test_act_list_02_view_activities_table(self):
        """ACT-LIST-02: View activities table with all columns."""
        # Create activities
        Activity.objects.create(
            workflow=self.workflow,
            name='Design Component',
            description='Create UI design',
            order=1
        )
        Activity.objects.create(
            workflow=self.workflow,
            name='Write Tests',
            description='Unit tests',
            order=2,
            has_dependencies=True
        )
        
        url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check both activities are displayed
        assert b'Design Component' in response.content
        assert b'Write Tests' in response.content
        # Check columns exist
        assert b'Name' in response.content
        assert b'Guidance' in response.content
        assert b'Dependencies' in response.content
        assert b'Actions' in response.content
    
    def test_act_list_03_navigate_to_create(self):
        """ACT-LIST-03: Click Create New Activity button."""
        url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check Create Activity button exists
        assert b'data-testid="create-activity-btn"' in response.content
        assert b'Create Activity' in response.content
        
        # Verify URL is correct
        create_url = reverse('activity_create', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        assert create_url.encode() in response.content
    
    def test_act_list_04_view_by_phase_grouping(self):
        """ACT-LIST-04: Activities grouped by phase with counts."""
        # Create activities with phases
        Activity.objects.create(
            workflow=self.workflow,
            name='Plan Features',
            description='Feature planning',
            phase='Planning',
            order=1
        )
        Activity.objects.create(
            workflow=self.workflow,
            name='Write Specs',
            description='Technical specs',
            phase='Planning',
            order=2
        )
        Activity.objects.create(
            workflow=self.workflow,
            name='Implement Code',
            description='Write code',
            phase='Execution',
            order=3
        )
        
        url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check phase headers exist
        assert b'Planning' in response.content
        assert b'Execution' in response.content
        # Check phase groups have data-testid
        assert b'data-testid="phase-group-planning"' in response.content
        assert b'data-testid="phase-group-execution"' in response.content
        # Check counts are displayed
        assert b'2 Phases' in response.content or b'2 phases' in response.content
    
    def test_act_list_05_view_flat_list_no_phases(self):
        """ACT-LIST-05: Flat list when no phases assigned."""
        # Create activities without phases
        Activity.objects.create(
            workflow=self.workflow,
            name='Activity 1',
            description='First activity',
            order=1
        )
        Activity.objects.create(
            workflow=self.workflow,
            name='Activity 2',
            description='Second activity',
            order=2
        )
        
        url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check flat list is displayed (not phase-grouped)
        assert b'data-testid="activities-flat-list"' in response.content
        # Activities should be ordered by sequence
        assert b'Activity 1' in response.content
        assert b'Activity 2' in response.content
    
    def test_act_list_10_navigate_to_view_activity(self):
        """ACT-LIST-10: Click View button for an activity."""
        activity = Activity.objects.create(
            workflow=self.workflow,
            name='Test Activity',
            description='Test',
            order=1
        )
        
        url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check View button exists with correct data-testid
        assert f'data-testid="view-btn-{activity.pk}"'.encode() in response.content
    
    def test_act_list_11_navigate_to_edit_activity(self):
        """ACT-LIST-11: Click Edit button for an activity."""
        activity = Activity.objects.create(
            workflow=self.workflow,
            name='Test Activity',
            description='Test',
            order=1
        )
        
        url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check Edit button exists with correct data-testid
        assert f'data-testid="edit-btn-{activity.pk}"'.encode() in response.content
    
    def test_act_list_12_delete_activity_button(self):
        """ACT-LIST-12: Click Delete button shows modal."""
        activity = Activity.objects.create(
            workflow=self.workflow,
            name='Test Activity',
            description='Test',
            order=1
        )
        
        url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check Delete button exists with correct data-testid
        assert f'data-testid="delete-btn-{activity.pk}"'.encode() in response.content
    
    def test_act_list_13_empty_state_display(self):
        """ACT-LIST-13: Empty state when no activities exist."""
        # Don't create any activities
        url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check empty state is displayed
        assert b'data-testid="empty-state"' in response.content
        assert b'No activities yet' in response.content
        assert b'data-testid="create-first-activity-btn"' in response.content
