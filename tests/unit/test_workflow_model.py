"""Unit tests for Workflow model."""

import pytest
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow

User = get_user_model()


@pytest.fixture
def test_user():
    """Create test user."""
    return User.objects.create_user(username='testuser', password='test123')


@pytest.fixture
def test_playbook(test_user):
    """Create test playbook."""
    return Playbook.objects.create(
        name='Test Playbook',
        description='Test description',
        category='development',
        author=test_user,
        source='owned'
    )


@pytest.fixture
def test_workflow(test_playbook):
    """Create test workflow."""
    return Workflow.objects.create(
        name='Test Workflow',
        description='Test workflow description',
        playbook=test_playbook,
        order=1
    )


@pytest.mark.django_db
class TestWorkflowModel:
    """Test Workflow model functionality."""
    
    def test_create_workflow(self, test_playbook):
        """Test creating a workflow with all fields."""
        workflow = Workflow.objects.create(
            name='Component Development',
            description='Build and test components',
            playbook=test_playbook,
            order=1
        )
        
        assert workflow.name == 'Component Development'
        assert workflow.description == 'Build and test components'
        assert workflow.playbook == test_playbook
        assert workflow.order == 1
        assert workflow.created_at is not None
        assert workflow.updated_at is not None
    
    def test_create_workflow_defaults(self, test_playbook):
        """Test workflow creation with default values."""
        workflow = Workflow.objects.create(
            name='Simple Workflow',
            playbook=test_playbook
        )
        
        assert workflow.description == ''
        assert workflow.order == 1
    
    def test_workflow_str_representation(self, test_workflow):
        """Test workflow string representation includes order."""
        assert str(test_workflow) == 'Test Workflow (#1)'
    
    def test_unique_constraint_per_playbook(self, test_playbook):
        """Test that workflow names must be unique within a playbook."""
        Workflow.objects.create(
            name='Duplicate Name',
            playbook=test_playbook,
            order=1
        )
        
        with pytest.raises(IntegrityError):
            Workflow.objects.create(
                name='Duplicate Name',
                playbook=test_playbook,
                order=2
            )
    
    def test_same_name_different_playbooks(self, test_user):
        """Test that same workflow name is allowed in different playbooks."""
        playbook1 = Playbook.objects.create(
            name='Playbook 1',
            description='First',
            category='development',
            author=test_user,
            source='owned'
        )
        playbook2 = Playbook.objects.create(
            name='Playbook 2',
            description='Second',
            category='development',
            author=test_user,
            source='owned'
        )
        
        workflow1 = Workflow.objects.create(
            name='Same Name',
            playbook=playbook1
        )
        workflow2 = Workflow.objects.create(
            name='Same Name',
            playbook=playbook2
        )
        
        assert workflow1.name == workflow2.name
        assert workflow1.playbook != workflow2.playbook
    
    def test_ordering_by_order_field(self, test_playbook):
        """Test workflows are ordered by order field, then created_at."""
        workflow3 = Workflow.objects.create(
            name='Third',
            playbook=test_playbook,
            order=3
        )
        workflow1 = Workflow.objects.create(
            name='First',
            playbook=test_playbook,
            order=1
        )
        workflow2 = Workflow.objects.create(
            name='Second',
            playbook=test_playbook,
            order=2
        )
        
        workflows = list(Workflow.objects.all())
        
        assert workflows[0].name == 'First'
        assert workflows[1].name == 'Second'
        assert workflows[2].name == 'Third'
    
    def test_get_activity_count(self, test_workflow):
        """Test get_activity_count returns 0 (no Activity model yet)."""
        count = test_workflow.get_activity_count()
        assert count == 0
    
    def test_get_phase_count(self, test_workflow):
        """Test get_phase_count returns 0 (no Phase model yet)."""
        count = test_workflow.get_phase_count()
        assert count == 0
    
    def test_is_owned_by_owner(self, test_user, test_workflow):
        """Test is_owned_by returns True for playbook owner."""
        assert test_workflow.is_owned_by(test_user) is True
    
    def test_is_owned_by_non_owner(self, test_workflow):
        """Test is_owned_by returns False for non-owner."""
        other_user = User.objects.create_user(username='other', password='test123')
        assert test_workflow.is_owned_by(other_user) is False
    
    def test_can_edit_owner_owned_playbook(self, test_user, test_workflow):
        """Test can_edit returns True for owner of owned playbook."""
        assert test_workflow.can_edit(test_user) is True
    
    def test_can_edit_non_owner(self, test_workflow):
        """Test can_edit returns False for non-owner."""
        other_user = User.objects.create_user(username='other', password='test123')
        assert test_workflow.can_edit(other_user) is False
    
    def test_can_edit_downloaded_playbook(self, test_user):
        """Test can_edit returns False for downloaded playbook."""
        downloaded_playbook = Playbook.objects.create(
            name='Downloaded Playbook',
            description='From library',
            category='development',
            author=test_user,
            source='downloaded'
        )
        workflow = Workflow.objects.create(
            name='Test',
            playbook=downloaded_playbook
        )
        
        assert workflow.can_edit(test_user) is False
    
    def test_workflow_relationship_with_playbook(self, test_playbook):
        """Test workflow is accessible from playbook via reverse relationship."""
        workflow = Workflow.objects.create(
            name='Related Workflow',
            playbook=test_playbook
        )
        
        assert workflow in test_playbook.workflows.all()
    
    def test_cascade_delete_with_playbook(self, test_playbook, test_workflow):
        """Test workflow is deleted when playbook is deleted."""
        workflow_id = test_workflow.id
        test_playbook.delete()
        
        assert not Workflow.objects.filter(id=workflow_id).exists()
    
    def test_updated_at_changes(self, test_workflow):
        """Test updated_at timestamp changes on save."""
        original_updated = test_workflow.updated_at
        test_workflow.name = 'Updated Name'
        test_workflow.save()
        
        assert test_workflow.updated_at > original_updated
