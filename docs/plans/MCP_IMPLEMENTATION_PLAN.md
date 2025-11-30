# MCP FastMCP Integration - Implementation Plan

## Overview

Implement FastMCP-based MCP server with CRUD tools for draft playbooks, workflows, and activities following the hybrid approach (Option C).

**Key Principle**: MCP can CRUD draft playbooks (status='draft', v0.x), read-only for released (status='released', v≥1.0).

## Development Rules

Following `.windsurf/rules/`:
- **do-skeletons-first.md**: Create stubs with full docstrings, type hints, examples, `raise NotImplementedError()`
- **test-first.md**: Write tests before implementation
- **do-small-increments.md**: Method-by-method, write → run → test → evaluate → fix
- **do-informative-logging.md**: Extensive INFO level logging with who/what/why/where/when

## Implementation Phases

### Phase 1: Foundation (MCP Infrastructure)

**Goal**: Set up FastMCP server infrastructure

#### Step 1.1: Create MCP App Structure
```
mcp/
├── __init__.py
├── tools.py                    # FastMCP tool definitions
├── services/                   # MCP-specific service adapters
│   ├── __init__.py
│   ├── playbook_mcp_service.py
│   ├── workflow_mcp_service.py
│   └── activity_mcp_service.py
└── management/
    └── commands/
        └── mcp_server.py       # Django command: python manage.py mcp_server
```

**Tasks**:
- [ ] Create `mcp/` Django app
- [ ] Add to `INSTALLED_APPS` in settings
- [ ] Create directory structure
- [ ] Add `fastmcp` to requirements.txt

**Test Strategy**: Test directory structure exists, imports work

**Time**: 15 min

---

#### Step 1.2: Skeleton - MCP Management Command
**File**: `mcp/management/commands/mcp_server.py`

**Skeleton**:
```python
import os
import django
import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Django management command to run MCP server via FastMCP."""
    
    help = 'Run the MCP server for AI assistant integration'
    
    def handle(self, *args, **options):
        """
        Start the MCP server.
        
        Initializes Django, configures logging, and starts FastMCP server.
        
        :param args: command args (unused)
        :param options: command options (unused)
        :raises ImportError: if fastmcp not installed
        :raises RuntimeError: if Django setup fails
        """
        # TODO: Setup Django environment
        # TODO: Configure logging to logs/mcp.log
        # TODO: Import and run FastMCP server
        # TODO: Handle graceful shutdown
        raise NotImplementedError()
```

**Tests**:
```python
# tests/unit/test_mcp_server_command.py
def test_mcp_server_command_exists():
    """Test that mcp_server command is available."""
    
def test_mcp_server_command_help():
    """Test command help text."""
```

**Implementation Notes**:
- Log to `logs/mcp.log` (rotate on restart)
- Log: server starting, tools loaded count, server ready

**Time**: 30 min

---

#### Step 1.3: Skeleton - FastMCP Initialization
**File**: `mcp/tools.py`

**Skeleton**:
```python
"""
FastMCP tool definitions for Mimir MCP server.

All tools follow hybrid access model:
- CRUD operations allowed on DRAFT playbooks (status='draft', v0.x)
- Read-only on RELEASED playbooks (status='released', v≥1.0)
"""
import logging
from fastmcp import FastMCP
from typing import Literal

logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("Mimir Methodology Assistant")

def get_repository():
    """
    Factory function for repository.
    
    :return: DjangoORMRepository instance
    :raises ImportError: if repository not available
    """
    # TODO: Import DjangoORMRepository
    # TODO: Log repository creation
    raise NotImplementedError()

# Tools will be added in subsequent steps
```

**Tests**:
```python
# tests/unit/test_mcp_tools.py
def test_mcp_initialized():
    """Test FastMCP instance is created."""

def test_get_repository_returns_django_orm():
    """Test repository factory returns correct type."""
```

**Time**: 20 min

---

### Phase 2: Playbook CRUD Services

**Goal**: Implement service layer for playbook operations with draft/released permission checks

#### Step 2.1: Skeleton - PlaybookService for MCP
**File**: `methodology/services/playbook_service.py` (extend existing)

**Skeleton Methods** (add to existing PlaybookService):
```python
def create_draft_playbook(self, name: str, description: str, category: str = "general") -> dict:
    """
    Create new DRAFT playbook (v0.1).
    
    :param name: playbook name. Example: "React Component Development"
    :param description: description. Example: "Best practices for React components"
    :param category: category. Example: "frontend"
    :return: Created playbook dict. Example: {"id": 1, "name": "React...", "version": "0.1", "status": "draft"}
    :raises ValidationError: if name empty/duplicate
    :raises IntegrityError: if database constraint violated
    """
    logger.info(f'MCP: Creating draft playbook name="{name}", category="{category}"')
    # TODO: Validate name not empty
    # TODO: Check for duplicate name
    # TODO: Create Playbook(name, description, category, status='draft', version=Decimal('0.1'))
    # TODO: Log success with playbook ID
    # TODO: Return serialized dict
    raise NotImplementedError()

def list_playbooks(self, status: Literal["draft", "released", "all"] = "all") -> list[dict]:
    """
    List playbooks filtered by status.
    
    :param status: filter. Example: "draft"
    :return: List of dicts. Example: [{"id": 1, "name": "...", "version": "0.2", "status": "draft"}]
    """
    logger.info(f'MCP: Listing playbooks with status={status}')
    # TODO: Query Playbook.objects based on status filter
    # TODO: Log count found
    # TODO: Serialize to list of dicts
    raise NotImplementedError()

def get_playbook_detail(self, playbook_id: int) -> dict:
    """
    Get playbook with workflows.
    
    :param playbook_id: ID. Example: 1
    :return: Dict with workflows. Example: {"id": 1, "workflows": [...]}
    :raises Playbook.DoesNotExist: if not found
    """
    logger.info(f'MCP: Getting playbook detail id={playbook_id}')
    # TODO: Get playbook with prefetch workflows
    # TODO: Serialize with nested workflows
    raise NotImplementedError()

def update_draft_playbook(self, playbook_id: int, name: str | None, description: str | None, category: str | None) -> dict:
    """
    Update DRAFT playbook. Auto-increments version (0.1 → 0.2).
    
    :param playbook_id: ID. Example: 1
    :param name: new name or None. Example: "Updated React Development"
    :param description: new description or None
    :param category: new category or None
    :return: Updated dict. Example: {"id": 1, "version": "0.2"}
    :raises PermissionError: if status='released'
    :raises Playbook.DoesNotExist: if not found
    """
    logger.info(f'MCP: Updating draft playbook id={playbook_id}, name={name}, desc={description}, category={category}')
    # TODO: Get playbook
    # TODO: CHECK status=='draft' (raise PermissionError if not)
    # TODO: Update fields if provided
    # TODO: Increment version (0.1 → 0.2)
    # TODO: Save and log new version
    raise NotImplementedError()

def delete_draft_playbook(self, playbook_id: int) -> dict:
    """
    Delete DRAFT playbook (cascades).
    
    :param playbook_id: ID. Example: 1
    :return: Confirmation. Example: {"deleted": True, "playbook_id": 1}
    :raises PermissionError: if status='released'
    :raises Playbook.DoesNotExist: if not found
    """
    logger.info(f'MCP: Deleting draft playbook id={playbook_id}')
    # TODO: Get playbook
    # TODO: CHECK status=='draft' (raise PermissionError if not)
    # TODO: Log cascade info (workflows/activities count)
    # TODO: Delete and return confirmation
    raise NotImplementedError()
```

**Tests**:
```python
# tests/unit/test_playbook_service_mcp.py

@pytest.mark.django_db
class TestPlaybookServiceMCP:
    
    def test_create_draft_playbook_success(self):
        """Test creating draft playbook returns v0.1 with status=draft."""
        
    def test_create_draft_playbook_duplicate_name_fails(self):
        """Test duplicate name raises ValidationError."""
        
    def test_list_playbooks_filters_by_draft(self):
        """Test listing draft playbooks only."""
        
    def test_list_playbooks_filters_by_released(self):
        """Test listing released playbooks only."""
        
    def test_get_playbook_detail_includes_workflows(self):
        """Test detail includes nested workflows."""
        
    def test_update_draft_increments_version(self):
        """Test update increments 0.1 → 0.2."""
        
    def test_update_released_raises_permission_error(self):
        """Test updating released playbook raises PermissionError."""
        
    def test_delete_draft_cascades_workflows(self):
        """Test delete removes workflows and activities."""
        
    def test_delete_released_raises_permission_error(self):
        """Test deleting released playbook raises PermissionError."""
```

**Time**: 2 hours (skeleton 30min, tests 1hr, implementation 30min)

---

#### Step 2.2: MCP Tools - Playbook CRUD
**File**: `mcp/tools.py`

**Skeleton**:
```python
@mcp.tool()
def create_playbook(name: str, description: str, category: str = "general") -> dict:
    """
    Create new DRAFT playbook (starts at v0.1).
    
    :param name: playbook name as str. Example: "React Component Development"
    :param description: playbook description as str. Example: "Best practices..."
    :param category: playbook category as str. Example: "frontend"
    :return: Created playbook dict. Example: {"id": 1, "name": "React...", "version": "0.1", "status": "draft"}
    :raises ValidationError: If name is empty or duplicate
    """
    logger.info(f'MCP Tool: create_playbook called with name="{name}"')
    from methodology.services import PlaybookService
    service = PlaybookService(get_repository())
    result = service.create_draft_playbook(name, description, category)
    logger.info(f'MCP Tool: create_playbook created playbook id={result["id"]}')
    return result

# Similar for: list_playbooks, get_playbook, update_playbook, delete_playbook
```

**Tests**:
```python
# tests/integration/test_mcp_playbook_tools.py

@pytest.mark.django_db
class TestMCPPlaybookTools:
    
    def test_create_playbook_tool(self):
        """Test MCP create_playbook tool creates draft playbook."""
        
    def test_update_playbook_tool_on_released_fails(self):
        """Test MCP update_playbook raises error for released playbooks."""
```

**Time**: 1.5 hours

---

### Phase 3: Workflow CRUD Services

**Goal**: Implement workflow CRUD with parent playbook permission checks

#### Step 3.1: Skeleton - WorkflowService for MCP
**File**: `methodology/services/workflow_service.py` (extend existing)

**Skeleton Methods**:
```python
def create_workflow(self, playbook_id: int, name: str, description: str, abbreviation: str | None = None) -> dict:
    """
    Create workflow in DRAFT playbook.
    
    :param playbook_id: parent playbook ID. Example: 1
    :param name: workflow name. Example: "Component Development"
    :param description: description. Example: "Steps to build..."
    :param abbreviation: abbreviation or None. Example: "COMP-DEV"
    :return: Created workflow dict. Example: {"id": 1, "name": "...", "playbook_id": 1}
    :raises PermissionError: if parent playbook status='released'
    :raises Playbook.DoesNotExist: if playbook not found
    """
    logger.info(f'MCP: Creating workflow in playbook={playbook_id}, name="{name}"')
    # TODO: Get parent playbook
    # TODO: CHECK playbook.status=='draft' (raise PermissionError if not)
    # TODO: Create Workflow
    # TODO: Increment parent playbook version
    raise NotImplementedError()

# Similar for: list_workflows, get_workflow_detail, update_workflow, delete_workflow
```

**Tests**: Similar pattern to playbook tests

**Time**: 2 hours

---

#### Step 3.2: MCP Tools - Workflow CRUD
**File**: `mcp/tools.py`

**Time**: 1.5 hours

---

### Phase 4: Activity CRUD Services

**Goal**: Implement activity CRUD with dependency management

#### Step 4.1: Skeleton - ActivityService for MCP
**File**: `methodology/services/activity_service.py` (extend existing)

**Skeleton Methods**:
```python
def create_activity(self, workflow_id: int, name: str, guidance: str, order: int = 1, phase: str | None = None) -> dict:
    """
    Create activity in workflow (DRAFT playbook only).
    
    :param workflow_id: parent workflow ID. Example: 1
    :param name: activity name. Example: "Design Component API"
    :param guidance: markdown guidance. Example: "## API Design..."
    :param order: execution order. Example: 1
    :param phase: phase grouping or None. Example: "Planning"
    :return: Created activity dict. Example: {"id": 1, "name": "...", "workflow_id": 1}
    :raises PermissionError: if parent playbook status='released'
    :raises Workflow.DoesNotExist: if workflow not found
    """
    logger.info(f'MCP: Creating activity in workflow={workflow_id}, name="{name}", order={order}')
    # TODO: Get workflow and parent playbook
    # TODO: CHECK playbook.status=='draft'
    # TODO: Create Activity
    # TODO: Increment parent playbook version
    raise NotImplementedError()

def set_predecessor(self, activity_id: int, predecessor_id: int) -> dict:
    """
    Set predecessor dependency (DRAFT only).
    
    :param activity_id: activity ID. Example: 2
    :param predecessor_id: predecessor ID. Example: 1
    :return: Updated activity. Example: {"id": 2, "predecessors": [{"id": 1}]}
    :raises PermissionError: if parent playbook status='released'
    :raises ValidationError: if creates circular dependency
    :raises Activity.DoesNotExist: if activity not found
    """
    logger.info(f'MCP: Setting predecessor for activity={activity_id}, predecessor={predecessor_id}')
    # TODO: Get both activities
    # TODO: CHECK parent playbook.status=='draft'
    # TODO: Detect circular dependencies (graph traversal)
    # TODO: Set predecessor relationship
    raise NotImplementedError()

# Similar for: list_activities, get_activity_detail, update_activity, delete_activity, set_successor
```

**Tests**: Activity CRUD + dependency tests including circular dependency detection

**Time**: 3 hours (includes circular dependency logic)

---

#### Step 4.2: MCP Tools - Activity CRUD
**File**: `mcp/tools.py`

**Time**: 1.5 hours

---

### Phase 5: Integration and E2E Testing

**Goal**: Test MCP server end-to-end with actual FastMCP

#### Step 5.1: MCP Server Integration Tests

**Tests**:
```python
# tests/integration/test_mcp_server_integration.py

def test_mcp_server_starts_successfully():
    """Test MCP server can start and initialize."""

def test_mcp_server_loads_all_tools():
    """Test all expected tools are registered."""
    
def test_mcp_create_playbook_e2e():
    """E2E: Create playbook via MCP, verify in database."""
    
def test_mcp_create_workflow_e2e():
    """E2E: Create playbook + workflow via MCP."""
    
def test_mcp_permission_errors_on_released():
    """E2E: Verify PermissionError when updating released playbook."""
```

**Time**: 2 hours

---

#### Step 5.2: Logging Configuration

**File**: `mcp/logging_config.py`

```python
import logging
import logging.handlers
from pathlib import Path

def setup_mcp_logging():
    """
    Configure MCP server logging to logs/mcp.log.
    
    Rotates log on every server start for clean diagnosis.
    """
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / 'mcp.log'
    
    # Clear log on startup
    if log_file.exists():
        log_file.unlink()
    
    # Configure handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    logger.info('MCP server logging initialized')
```

**Time**: 30 min

---

### Phase 6: Documentation and Finalization

#### Step 6.1: Update Dependencies
**File**: `requirements.txt`

Add:
```
fastmcp>=0.2.0
```

#### Step 6.2: Create MCP Configuration Doc
**File**: `docs/mcp/MCP_SETUP.md`

Content:
- How to install dependencies
- How to run MCP server: `python manage.py mcp_server`
- How to configure IDE (Claude Desktop, Cursor, Windsurf)
- Available tools reference
- Permission model explanation

**Time**: 1 hour

---

## Summary Timeline

| Phase | Task | Time | Cumulative |
|-------|------|------|------------|
| 1.1 | MCP app structure | 15m | 15m |
| 1.2 | MCP server command skeleton | 30m | 45m |
| 1.3 | FastMCP initialization | 20m | 1h 5m |
| 2.1 | PlaybookService MCP methods | 2h | 3h 5m |
| 2.2 | Playbook MCP tools | 1.5h | 4h 35m |
| 3.1 | WorkflowService MCP methods | 2h | 6h 35m |
| 3.2 | Workflow MCP tools | 1.5h | 8h 5m |
| 4.1 | ActivityService MCP methods | 3h | 11h 5m |
| 4.2 | Activity MCP tools | 1.5h | 12h 35m |
| 5.1 | Integration tests | 2h | 14h 35m |
| 5.2 | Logging configuration | 30m | 15h 5m |
| 6.1 | Dependencies | 15m | 15h 20m |
| 6.2 | Documentation | 1h | 16h 20m |

**Total Estimated Time**: ~16.5 hours (2 days)

## Implementation Order (Small Increments)

1. ✅ Phase 1: Foundation (1h) - Get MCP infrastructure in place
2. ✅ Phase 2.1: Playbook service skeletons + tests (2h) - Core functionality
3. ✅ Phase 2.1: Implement + validate (write → test → fix loop)
4. ✅ Phase 2.2: Playbook MCP tools (1.5h)
5. ✅ Phase 3: Workflow CRUD (3.5h total)
6. ✅ Phase 4: Activity CRUD (4.5h total)
7. ✅ Phase 5: Integration testing (2.5h total)
8. ✅ Phase 6: Documentation (1.25h total)

## Success Criteria

- [ ] All 17 MCP tools functional (5 playbook + 5 workflow + 7 activity)
- [ ] 100% test pass rate (unit + integration)
- [ ] Permission model enforced (draft CRUD, released read-only)
- [ ] Comprehensive logging (who/what/why/where/when)
- [ ] MCP server starts and registers all tools
- [ ] Documentation complete
- [ ] Can create full playbook via MCP tools only

## Next Steps

After approval:
1. Create branch `feature/mcp-integration`
2. Start with Phase 1.1 (15 min task)
3. Commit after each phase
4. Run tests after each implementation
5. Fix issues immediately before proceeding
