"""Integration tests for Workflow MCP tools."""
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from methodology.models import Playbook, Workflow
from mcp_integration.context import set_current_user
from mcp_integration.tools import create_playbook, create_workflow, update_workflow, delete_workflow

User = get_user_model()

@pytest.fixture
def maria(db):
    return User.objects.create_user(username='maria', email='maria@test.com', password='test123')

@pytest.fixture
def setup_user_context(maria):
    set_current_user(maria)
    return maria

@pytest.fixture
def draft_playbook(setup_user_context):
    return create_playbook(name="Test Playbook", description="Test", category="dev")

@pytest.mark.django_db
class TestMCPWorkflowCreate:
    def test_mcp_wf_01_create_workflow_increments_parent_version(self, setup_user_context, draft_playbook):
        """Scenario: MCP-WF-01 Create workflow increments parent playbook version"""
        result = create_workflow(playbook_id=draft_playbook['id'], name="Design Phase", description="Test")
        
        assert result['id'] is not None
        assert result['playbook_id'] == draft_playbook['id']
        
        playbook = Playbook.objects.get(id=draft_playbook['id'])
        assert playbook.version > Decimal('0.1')  # Version incremented
    
    def test_mcp_wf_02_create_workflow_duplicate_name_raises_error(self, setup_user_context, draft_playbook):
        """Scenario: MCP-WF-02 Duplicate workflow name raises ValidationError"""
        create_workflow(playbook_id=draft_playbook['id'], name="Design Phase", description="Test")
        
        with pytest.raises(ValidationError):
            create_workflow(playbook_id=draft_playbook['id'], name="Design Phase", description="Different")

@pytest.mark.django_db
class TestMCPWorkflowDelete:
    def test_mcp_wf_13_delete_workflow_success(self, setup_user_context, draft_playbook):
        """Scenario: MCP-WF-13 Delete workflow removes from database"""
        workflow = create_workflow(playbook_id=draft_playbook['id'], name="To Delete", description="Test")
        
        result = delete_workflow(workflow_id=workflow['id'])
        
        assert result['deleted'] is True
        assert not Workflow.objects.filter(id=workflow['id']).exists()
