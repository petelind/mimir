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
