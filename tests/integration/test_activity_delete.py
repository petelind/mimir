"""
Integration tests for Activity DELETE operation.

Tests activity deletion confirmation and execution.
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow, Activity

User = get_user_model()


@pytest.mark.django_db
class TestActivityDelete:
    """Integration tests for activity delete functionality."""
    
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
            guidance='Create UI design',
            phase='Planning',
            order=1
        )
    
    def test_delete_01_open_delete_confirmation(self):
        """Test opening delete confirmation page."""
        url = reverse('activity_delete', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'Delete Activity' in response.content
        assert b'data-testid="activity-delete"' in response.content
        assert b'Confirm Deletion' in response.content
    
    def test_delete_02_display_activity_details(self):
        """Test activity details are shown on confirmation page."""
        url = reverse('activity_delete', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'Design Component' in response.content
        assert b'Create UI design' in response.content
        assert b'Planning' in response.content
        assert b'data-testid="activity-details"' in response.content
    
    def test_delete_03_display_warning_message(self):
        """Test warning message is shown."""
        url = reverse('activity_delete', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'cannot be undone' in response.content or b'Cannot be undone' in response.content
        assert b'Warning' in response.content or b'warning' in response.content
    
    def test_delete_04_confirm_and_delete_activity(self):
        """Test confirming deletion removes the activity."""
        url = reverse('activity_delete', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        # POST to confirm deletion
        response = self.client.post(url)
        
        # Should redirect to list
        assert response.status_code == 302
        assert response.url == reverse('activity_list', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk
        })
        
        # Verify activity was deleted
        assert not Activity.objects.filter(pk=self.activity.pk).exists()
    
    def test_delete_05_cancel_redirects_to_detail(self):
        """Test cancel button redirects to activity detail."""
        url = reverse('activity_delete', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check cancel button exists
        assert b'data-testid="cancel-btn"' in response.content
        detail_url = reverse('activity_detail', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        assert detail_url.encode() in response.content
    
    def test_delete_06_cancel_does_not_delete(self):
        """Test clicking cancel does not delete activity."""
        initial_count = Activity.objects.count()
        
        url = reverse('activity_delete', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        # GET (showing confirmation) should not delete
        self.client.get(url)
        
        # Activity should still exist
        assert Activity.objects.count() == initial_count
        assert Activity.objects.filter(pk=self.activity.pk).exists()
    
    def test_delete_07_delete_form_has_confirm_button(self):
        """Test delete confirmation form has the confirm button."""
        url = reverse('activity_delete', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'data-testid="confirm-delete-btn"' in response.content
        assert b'data-testid="delete-form"' in response.content
    
    def test_delete_08_multiple_activities_cascade(self):
        """Test deleting one activity doesn't affect others."""
        # Create another activity
        other_activity = Activity.objects.create(
            workflow=self.workflow,
            name='Other Activity',
            guidance='Other',
            order=2
        )
        
        url = reverse('activity_delete', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        # Delete first activity
        self.client.post(url)
        
        # First activity should be deleted
        assert not Activity.objects.filter(pk=self.activity.pk).exists()
        
        # Second activity should still exist
        assert Activity.objects.filter(pk=other_activity.pk).exists()
        assert Activity.objects.count() == 1
