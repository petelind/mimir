"""Integration tests for Workflow CREATE operation."""

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
        name='React Frontend Development',
        description='Test playbook',
        category='development',
        author=test_user,
        source='owned'
    )


@pytest.mark.django_db
class TestWorkflowCreate:
    """Test workflow creation views."""
    
    def test_wf_create_01_open_create_form(self, test_user, test_playbook):
        """WF-CREATE-01: Open create workflow form."""
        client = Client()
        client.force_login(test_user)
        
        response = client.get(reverse('workflow_create', kwargs={'playbook_pk': test_playbook.pk}))
        
        assert response.status_code == 200
        assert b'Create Workflow' in response.content
        assert test_playbook.name.encode() in response.content
    
    def test_wf_create_02_create_with_required_fields(self, test_user, test_playbook):
        """WF-CREATE-02: Create workflow with required fields."""
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('workflow_create', kwargs={'playbook_pk': test_playbook.pk}),
            {
                'name': 'Design System Integration',
                'description': 'Integrate design tokens and components'
            },
            follow=True
        )
        
        assert response.status_code == 200
        assert Workflow.objects.filter(name='Design System Integration').exists()
        workflow = Workflow.objects.get(name='Design System Integration')
        assert workflow.playbook == test_playbook
    
    def test_wf_create_03_validate_required_name(self, test_user, test_playbook):
        """WF-CREATE-03: Validate required name field."""
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('workflow_create', kwargs={'playbook_pk': test_playbook.pk}),
            {'name': '', 'description': 'Test'}
        )
        
        assert response.status_code == 200
        assert b'This field is required' in response.content or b'Name is required' in response.content
    
    def test_wf_create_04_duplicate_name_validation(self, test_user, test_playbook):
        """WF-CREATE-04: Duplicate name validation."""
        Workflow.objects.create(
            name='Component Development',
            playbook=test_playbook,
            order=1
        )
        
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('workflow_create', kwargs={'playbook_pk': test_playbook.pk}),
            {'name': 'Component Development', 'description': 'Test'}
        )
        
        assert response.status_code == 200
        assert b'already exists' in response.content
    
    def test_wf_create_05_auto_order(self, test_user, test_playbook):
        """WF-CREATE-05: Auto-assign order at end."""
        Workflow.objects.create(name='First', playbook=test_playbook, order=1)
        Workflow.objects.create(name='Second', playbook=test_playbook, order=2)
        Workflow.objects.create(name='Third', playbook=test_playbook, order=3)
        
        client = Client()
        client.force_login(test_user)
        
        client.post(
            reverse('workflow_create', kwargs={'playbook_pk': test_playbook.pk}),
            {'name': 'Fourth', 'description': 'Test'}
        )
        
        workflow = Workflow.objects.get(name='Fourth')
        assert workflow.order == 4
