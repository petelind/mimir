"""
Integration tests for Activity VIEW operation.

Tests activity detail page display and navigation.
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow, Activity

User = get_user_model()


@pytest.mark.django_db
class TestActivityView:
    """Integration tests for activity detail view."""
    
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
            guidance='A comprehensive methodology',
            category='development',
            status='active',
            source='owned',
            author=self.user
        )
        
        self.workflow = Workflow.objects.create(
            name='Component Development',
            guidance='Develop React components',
            playbook=self.playbook,
            order=1
        )
        
        # Create activity
        self.activity = Activity.objects.create(
            workflow=self.workflow,
            name='Design Component',
            guidance='Create UI design for the component',
            phase='Planning',
            order=1
        )
    
    def test_view_01_open_activity_detail(self):
        """Test opening activity detail page."""
        url = reverse('activity_detail', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'Design Component' in response.content
        assert b'data-testid="activity-detail"' in response.content
    
    def test_view_02_display_activity_info(self):
        """Test activity information is displayed correctly."""
        url = reverse('activity_detail', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check all key information is displayed
        assert b'Design Component' in response.content
        assert b'Create UI design for the component' in response.content
        assert b'Planning' in response.content
        assert b'Has Dependencies' in response.content or b'has_dependencies' in response.content
    
    def test_view_03_display_timestamps(self):
        """Test created and updated timestamps are shown."""
        url = reverse('activity_detail', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'Created' in response.content or b'created' in response.content
        assert b'Updated' in response.content or b'updated' in response.content
    
    def test_view_05_edit_button_for_owner(self):
        """Test edit button is shown to activity owner."""
        url = reverse('activity_detail', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'data-testid="edit-btn"' in response.content
        
        # Verify URL is correct
        edit_url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        assert edit_url.encode() in response.content
    
    def test_view_06_delete_button_for_owner(self):
        """Test delete button is shown to activity owner."""
        url = reverse('activity_detail', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'data-testid="delete-btn"' in response.content
    
    def test_view_07_back_to_list_button(self):
        """Test back to list button is present."""
        url = reverse('activity_detail', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check list URL is present
        list_url = reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        assert list_url.encode() in response.content
    
    def test_view_08_breadcrumb_navigation(self):
        """Test breadcrumb navigation is present."""
        url = reverse('activity_detail', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'breadcrumb' in response.content
        assert b'Playbooks' in response.content
        assert b'Workflows' in response.content
        assert b'Activities' in response.content
