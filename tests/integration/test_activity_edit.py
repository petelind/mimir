"""
Integration tests for Activity EDIT operation.

Tests activity editing form, validation, and success scenarios.
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow, Activity

User = get_user_model()


@pytest.mark.django_db
class TestActivityEdit:
    """Integration tests for activity edit functionality."""
    
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
        
        # Create activity
        self.activity = Activity.objects.create(
            workflow=self.workflow,
            name='Design Component',
            description='Create UI design',
            phase='Planning',
            order=1,
            has_dependencies=False
        )
    
    def test_edit_01_open_edit_form(self):
        """Test opening activity edit form."""
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'Edit Activity' in response.content
        assert b'data-testid="activity-form"' in response.content
        assert b'Design Component' in response.content
    
    def test_edit_02_form_prefilled_with_current_values(self):
        """Test form is pre-filled with current activity values."""
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert b'Design Component' in response.content
        assert b'Create UI design' in response.content
        assert b'Planning' in response.content
    
    def test_edit_03_update_activity_name(self):
        """Test updating activity name."""
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        data = {
            'name': 'Updated Component Design',
            'description': 'Create UI design',
            'phase': 'Planning',
            'order': 1,
        }
        response = self.client.post(url, data)
        
        # Should redirect to detail on success
        assert response.status_code == 302
        
        # Verify activity was updated
        self.activity.refresh_from_db()
        assert self.activity.name == 'Updated Component Design'
    
    def test_edit_04_update_description(self):
        """Test updating activity description."""
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        data = {
            'name': 'Design Component',
            'description': 'Updated description with more details',
            'phase': 'Planning',
            'order': 1,
        }
        response = self.client.post(url, data)
        
        assert response.status_code == 302
        self.activity.refresh_from_db()
        assert self.activity.description == 'Updated description with more details'
    
    def test_edit_05_update_phase(self):
        """Test updating activity phase."""
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        data = {
            'name': 'Design Component',
            'description': 'Create UI design',
            'phase': 'Execution',
            'order': 1,
        }
        response = self.client.post(url, data)
        
        assert response.status_code == 302
        self.activity.refresh_from_db()
        assert self.activity.phase == 'Execution'
    
    def test_edit_06_update_order(self):
        """Test updating activity order."""
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        data = {
            'name': 'Design Component',
            'description': 'Create UI design',
            'phase': 'Planning',
            'order': 5,
        }
        response = self.client.post(url, data)
        
        assert response.status_code == 302
        self.activity.refresh_from_db()
        assert self.activity.order == 5
    
    def test_edit_07_update_dependencies_flag(self):
        """Test updating has_dependencies flag."""
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        data = {
            'name': 'Design Component',
            'description': 'Create UI design',
            'phase': 'Planning',
            'order': 1,
            'has_dependencies': 'on',  # Checkbox checked
        }
        response = self.client.post(url, data)
        
        assert response.status_code == 302
        self.activity.refresh_from_db()
        assert self.activity.has_dependencies is True
    
    def test_edit_08_validate_required_name(self):
        """Test validation error when name is empty."""
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        data = {
            'name': '',  # Empty name
            'description': 'Create UI design',
            'order': 1,
        }
        response = self.client.post(url, data)
        
        # Should stay on form with error
        assert response.status_code == 200
        assert b'cannot be empty' in response.content or b'This field is required' in response.content
        
        # Activity should not be changed
        self.activity.refresh_from_db()
        assert self.activity.name == 'Design Component'
    
    def test_edit_09_validate_duplicate_name(self):
        """Test validation error for duplicate activity name in workflow."""
        # Create another activity
        Activity.objects.create(
            workflow=self.workflow,
            name='Existing Activity',
            description='Exists',
            order=2
        )
        
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        
        data = {
            'name': 'Existing Activity',  # Duplicate
            'description': 'Create UI design',
            'order': 1,
        }
        response = self.client.post(url, data)
        
        # Should stay on form with error
        assert response.status_code == 200
        assert b'already exists' in response.content
        
        # Original activity should not be changed
        self.activity.refresh_from_db()
        assert self.activity.name == 'Design Component'
    
    def test_edit_10_cancel_redirects_to_detail(self):
        """Test cancel button redirects to activity detail."""
        url = reverse('activity_edit', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        response = self.client.get(url)
        
        assert response.status_code == 200
        # Check cancel button exists with correct link
        detail_url = reverse('activity_detail', kwargs={
            'playbook_pk': self.playbook.pk,
            'workflow_pk': self.workflow.pk,
            'activity_pk': self.activity.pk
        })
        assert detail_url.encode() in response.content
        assert b'data-testid="cancel-btn"' in response.content
