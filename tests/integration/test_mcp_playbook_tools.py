"""
Integration tests for Playbook MCP tools.

Tests MCP tool wrappers with real database, real services, NO MOCKING.
Based on BDD scenarios from interact-with-playbooks-via-mcp.feature.
"""
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from methodology.models import Playbook
from mcp_integration.context import set_current_user
from mcp_integration.tools import (
    create_playbook,
    list_playbooks,
    get_playbook,
    update_playbook,
    delete_playbook
)

User = get_user_model()


@pytest.fixture
def maria(db):
    """Create test user maria."""
    return User.objects.create_user(username='maria', email='maria@test.com', password='test123')


@pytest.fixture
def setup_user_context(maria):
    """Set up MCP user context for maria."""
    set_current_user(maria)
    return maria


@pytest.mark.django_db
class TestMCPPlaybookCreate:
    """MCP-PB-01 to MCP-PB-03: Create playbook scenarios."""
    
    def test_mcp_pb_01_create_draft_playbook_via_mcp_tool(self, setup_user_context):
        """
        Scenario: MCP-PB-01 Create draft playbook via MCP tool
        Given Cascade receives user request
        When Cascade calls create_playbook
        Then playbook created with version 0.1, status draft
        """
        result = create_playbook(
            name="React Component Development",
            description="Best practices for building reusable React components",
            category="frontend"
        )
        
        assert result['id'] is not None
        assert result['version'] == '0.1'
        assert result['status'] == 'draft'
        
        # Verify in database
        playbook = Playbook.objects.get(id=result['id'])
        assert playbook.author == setup_user_context
        assert playbook.name == "React Component Development"
    
    def test_mcp_pb_02_create_playbook_with_duplicate_name_raises_error(self, setup_user_context):
        """Scenario: MCP-PB-02 Create playbook with duplicate name raises error"""
        create_playbook(name="React Component Development", description="Test", category="frontend")
        
        with pytest.raises(ValidationError):
            create_playbook(name="React Component Development", description="Different", category="frontend")


@pytest.mark.django_db
class TestMCPPlaybookUpdate:
    """MCP-PB-10 to MCP-PB-13: Update playbook scenarios."""
    
    def test_mcp_pb_10_update_draft_playbook_increments_version(self, setup_user_context):
        """Scenario: MCP-PB-10 Update draft playbook increments version"""
        created = create_playbook(name="Original Name", description="Original Description", category="development")
        
        result = update_playbook(playbook_id=created['id'], name="Updated Name")
        
        assert result['name'] == "Updated Name"
        assert result['version'] == '0.2'
        # Version incremented


@pytest.mark.django_db
class TestMCPPlaybookDelete:
    """MCP-PB-14: Delete playbook scenarios."""
    
    def test_mcp_pb_14_delete_draft_playbook_success(self, setup_user_context):
        """Scenario: MCP-PB-14 Delete draft playbook removes from database"""
        created = create_playbook(name="To Delete", description="Will be deleted", category="test")
        
        result = delete_playbook(playbook_id=created['id'])
        
        assert result['deleted'] is True
        assert not Playbook.objects.filter(id=created['id']).exists()
