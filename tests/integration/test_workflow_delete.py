"""Integration tests for Workflow DELETE operation."""

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
        name='To Delete',
        description='Will be deleted',
        playbook=test_playbook,
        order=1
    )


@pytest.mark.django_db
class TestWorkflowDelete:
    """Test workflow delete operation."""
    
    def test_wf_delete_01_delete_workflow(self, test_user, test_playbook, test_workflow):
        """WF-DELETE-01: Delete workflow successfully."""
        client = Client()
        client.force_login(test_user)
        
        workflow_id = test_workflow.pk
        
        response = client.post(
            reverse('workflow_delete', kwargs={
                'playbook_pk': test_playbook.pk,
                'pk': workflow_id
            }),
            follow=True
        )
        
        assert response.status_code == 200
        assert not Workflow.objects.filter(pk=workflow_id).exists()
