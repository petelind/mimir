"""Unit tests for Activity model."""

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from methodology.models import Playbook, Workflow, Activity

User = get_user_model()


@pytest.fixture
def test_user():
    """Create test user."""
    return User.objects.create_user(username='maria', password='test123')


@pytest.fixture
def test_playbook(test_user):
    """Create test playbook."""
    return Playbook.objects.create(
        name='Test Playbook',
        description='Test description',
        author=test_user,
        source='owned',
        status='active'
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
class TestActivityModel:
    """Test Activity model functionality."""
    
    def test_create_activity(self, test_workflow):
        """Test creating an activity with all fields."""
        activity = Activity.objects.create(
            workflow=test_workflow,
            name='Design Component',
            guidance='Create component design',
            order=1,
            phase='Planning'
        )
        
        assert activity.id is not None
        assert activity.name == 'Design Component'
        assert activity.guidance == 'Create component design'
        assert activity.order == 1
        assert activity.phase == 'Planning'
        assert activity.workflow == test_workflow
    
    def test_activity_defaults(self, test_workflow):
        """Test activity default values."""
        activity = Activity.objects.create(
            workflow=test_workflow,
            name='Test Activity',
            guidance='Test guidance'
        )
        
        assert activity.order == 1
        assert activity.phase is None        
        assert activity.created_at is not None
        assert activity.updated_at is not None
    
    def test_activity_str_representation(self, test_workflow):
        """Test __str__ method shows name and order."""
        activity = Activity.objects.create(
            workflow=test_workflow,
            name='Setup Environment',
            guidance='Configure dev environment',
            order=3
        )
        
        assert str(activity) == 'Setup Environment (#3)'
    
    def test_unique_constraint_per_workflow(self, test_workflow):
        """Test unique constraint: same name within workflow not allowed."""
        Activity.objects.create(
            workflow=test_workflow,
            name='Duplicate Name',
            guidance='First activity'
        )
        
        with pytest.raises(IntegrityError):
            Activity.objects.create(
                workflow=test_workflow,
                name='Duplicate Name',  # Same name in same workflow
                guidance='Second activity'
            )
    
    def test_unique_constraint_across_workflows(self, test_playbook):
        """Test that same name is allowed across different workflows."""
        workflow1 = Workflow.objects.create(
            name='Workflow 1',
            playbook=test_playbook,
            order=1
        )
        workflow2 = Workflow.objects.create(
            name='Workflow 2',
            playbook=test_playbook,
            order=2
        )
        
        # Should allow same name in different workflows
        activity1 = Activity.objects.create(
            workflow=workflow1,
            name='Same Name',
            guidance='In workflow 1'
        )
        activity2 = Activity.objects.create(
            workflow=workflow2,
            name='Same Name',
            guidance='In workflow 2'
        )
        
        assert activity1.name == activity2.name
        assert activity1.workflow != activity2.workflow
    
    def test_ordering_by_workflow_order_name(self, test_workflow):
        """Test default ordering is by workflow, order, name."""
        Activity.objects.create(workflow=test_workflow, name='B Activity', guidance='B', order=2)
        Activity.objects.create(workflow=test_workflow, name='A Activity', guidance='A', order=1)
        Activity.objects.create(workflow=test_workflow, name='C Activity', guidance='C', order=1)
        
        activities = list(Activity.objects.all())
        
        # Should be ordered by order first, then name
        assert activities[0].name == 'A Activity'  # order=1, alphabetically first
        assert activities[1].name == 'C Activity'  # order=1, alphabetically second
        assert activities[2].name == 'B Activity'  # order=2
    
    def test_is_owned_by_owner(self, test_user, test_workflow):
        """Test is_owned_by returns True for playbook owner."""
        activity = Activity.objects.create(
            workflow=test_workflow,
            name='Test Activity',
            guidance='Test'
        )
        
        assert activity.is_owned_by(test_user) is True
    
    def test_is_owned_by_non_owner(self, test_workflow):
        """Test is_owned_by returns False for non-owner."""
        other_user = User.objects.create_user(username='john', password='test123')
        activity = Activity.objects.create(
            workflow=test_workflow,
            name='Test Activity',
            guidance='Test'
        )
        
        assert activity.is_owned_by(other_user) is False
    
    def test_can_edit_owner_owned_playbook(self, test_user, test_workflow):
        """Test can_edit returns True for owner of owned playbook."""
        activity = Activity.objects.create(
            workflow=test_workflow,
            name='Test Activity',
            guidance='Test'
        )
        
        assert activity.can_edit(test_user) is True
    
    def test_can_edit_downloaded_playbook(self, test_user):
        """Test can_edit returns False for downloaded playbook."""
        playbook = Playbook.objects.create(
            name='Downloaded Playbook',
            description='Test',
            author=test_user,
            source='downloaded',  # Not owned
            status='active'
        )
        workflow = Workflow.objects.create(
            name='Test Workflow',
            playbook=playbook,
            order=1
        )
        activity = Activity.objects.create(
            workflow=workflow,
            name='Test Activity',
            guidance='Test'
        )
        
        assert activity.can_edit(test_user) is False
    
    def test_cascade_delete_with_workflow(self, test_workflow):
        """Test that deleting workflow deletes its activities."""
        Activity.objects.create(
            workflow=test_workflow,
            name='Activity 1',
            guidance='Test'
        )
        Activity.objects.create(
            workflow=test_workflow,
            name='Activity 2',
            guidance='Test'
        )
        
        assert Activity.objects.count() == 2
        
        test_workflow.delete()
        
        assert Activity.objects.count() == 0
    
    def test_updated_at_changes(self, test_workflow):
        """Test that updated_at changes on save."""
        activity = Activity.objects.create(
            workflow=test_workflow,
            name='Test Activity',
            guidance='Original description'
        )
        
        original_updated = activity.updated_at
        
        # Update activity
        activity.guidance = 'New description'
        activity.save()
        activity.refresh_from_db()
        
        assert activity.updated_at > original_updated
    
    def test_get_phase_display_name_with_phase(self, test_workflow):
        """Test get_phase_display_name returns phase when set."""
        activity = Activity.objects.create(
            workflow=test_workflow,
            name='Test Activity',
            guidance='Test',
            phase='Planning'
        )
        
        assert activity.get_phase_display_name() == 'Planning'
    
    def test_get_phase_display_name_without_phase(self, test_workflow):
        """Test get_phase_display_name returns Unassigned when no phase."""
        activity = Activity.objects.create(
            workflow=test_workflow,
            name='Test Activity',
            guidance='Test'
        )
        
        assert activity.get_phase_display_name() == 'Unassigned'
    
