"""Integration tests for Workflow EDIT operation."""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow

User = get_user_model()


@pytest.fixture
def test_user():
    """Create test user."""
    return User.objects.create_user(username='maria', password='test123')


@pytest.fixture
def test_playbook(test_user):
    """Create test playbook."""
    return Playbook.objects.create(
        name='React Frontend',
        description='Test',
        category='development',
        author=test_user,
        source='owned'
    )


@pytest.fixture
def test_workflow(test_playbook):
    """Create test workflow."""
    return Workflow.objects.create(
        name='Component Development',
        description='Original description',
        playbook=test_playbook,
        order=1
    )


@pytest.mark.django_db
class TestWorkflowEdit:
    """Test workflow edit operation."""
    
    def test_wf_edit_01_open_edit_form(self, test_user, test_playbook, test_workflow):
        """WF-EDIT-01: Open edit form."""
        client = Client()
        client.force_login(test_user)
        
        response = client.get(reverse('workflow_edit', kwargs={
            'playbook_pk': test_playbook.pk,
            'pk': test_workflow.pk
        }))
        
        assert response.status_code == 200
        assert b'Edit Workflow' in response.content
    
    def test_wf_edit_02_form_prepopulated(self, test_user, test_playbook, test_workflow):
        """WF-EDIT-02: Form is pre-populated with existing data."""
        client = Client()
        client.force_login(test_user)
        
        response = client.get(reverse('workflow_edit', kwargs={
            'playbook_pk': test_playbook.pk,
            'pk': test_workflow.pk
        }))
        
        assert test_workflow.name.encode() in response.content
        assert test_workflow.description.encode() in response.content
    
    def test_wf_edit_03_update_name(self, test_user, test_playbook, test_workflow):
        """WF-EDIT-03: Update workflow name."""
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('workflow_edit', kwargs={
                'playbook_pk': test_playbook.pk,
                'pk': test_workflow.pk
            }),
            {
                'name': 'Updated Name',
                'description': test_workflow.description
            },
            follow=True
        )
        
        assert response.status_code == 200
        test_workflow.refresh_from_db()
        assert test_workflow.name == 'Updated Name'
