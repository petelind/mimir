# MCP CRUD Tools - Implementation Plan

## 0. Current State Assessment

### What Exists ✓
**Services (Business Logic)**:
- `methodology/services/playbook_service.py` - 7 methods (create/get/list/update/delete/duplicate/release)
- `methodology/services/workflow_service.py` - 6 methods (create/get/list/update/delete/duplicate)
- `methodology/services/activity_service.py` - 12 methods (full CRUD + dependency management)
- All services used by UI views ✓

**MCP Infrastructure**:
- `mcp/` Django app structure ✓
- `mcp/management/commands/mcp_server.py` - skeleton (raises NotImplementedError)
- `mcp/tools.py` - 16 tool function skeletons (raise NotImplementedError)
  - 5 playbook tools
  - 5 workflow tools  
  - 6 activity tools

**Architecture**:
- Services contain business logic ✓
- UI views call services ✓
- MCP tools call services ✓ (but not wired to FastMCP yet)

### What's Missing ❌
1. **FastMCP Integration**:
   - No `@mcp.tool()` decorators
   - No user context implementation (`get_current_user()` raises NotImplementedError)
   - `mcp_server` command doesn't run FastMCP server

2. **Tests**:
   - No tests for PlaybookService (7 methods untested)
   - No tests for WorkflowService (6 methods untested)
   - No tests for ActivityService (12 methods untested)
   - No tests for MCP tools
   - No integration tests for FastMCP

3. **User Stories**:
   - No documented scenarios for AI assistant using MCP tools

## 1. SAO.md Architecture Alignment

**From SAO.md (Hybrid MCP Approach - Option C)**:
- CRUD allowed on DRAFT playbooks (status='draft', version=0.x)
- Read-only on RELEASED playbooks (status='released', version≥1.0)
- Changes to released playbooks require PIP (Playbook Improvement Proposal)

**MCP Tools Specification** (SAO.md lines 373-655):
```python
# Playbook CRUD
@mcp.tool() def create_playbook(name, description, category) -> dict
@mcp.tool() def list_playbooks(status="all") -> list[dict]
@mcp.tool() def get_playbook(playbook_id) -> dict
@mcp.tool() def update_playbook(playbook_id, name=None, ...) -> dict
@mcp.tool() def delete_playbook(playbook_id) -> dict

# Workflow CRUD
@mcp.tool() def create_workflow(playbook_id, name, description) -> dict
@mcp.tool() def list_workflows(playbook_id) -> list[dict]
@mcp.tool() def get_workflow(workflow_id) -> dict
@mcp.tool() def update_workflow(workflow_id, name=None, ...) -> dict
@mcp.tool() def delete_workflow(workflow_id) -> dict

# Activity CRUD
@mcp.tool() def create_activity(workflow_id, name, guidance, ...) -> dict
@mcp.tool() def list_activities(workflow_id) -> list[dict]
@mcp.tool() def get_activity(activity_id) -> dict
@mcp.tool() def update_activity(activity_id, name=None, ...) -> dict
@mcp.tool() def delete_activity(activity_id) -> dict
@mcp.tool() def set_activity_predecessor(activity_id, predecessor_id) -> dict
```

**Our Implementation** matches this ✓

## 2. User Stories - AI Assistant Using MCP Tools

### Story 1: Create New Methodology from Scratch
**As**: AI assistant (e.g., Claude, Cascade)  
**I want to**: Create a new draft playbook with workflows and activities  
**So that**: User can iteratively develop their methodology with AI assistance

**Scenario**:
```
User: "Help me create a React component development methodology"

AI uses MCP tools:
1. create_playbook(name="React Component Development", description="...", category="frontend")
   → Returns: {"id": 1, "version": "0.1", "status": "draft"}

2. create_workflow(playbook_id=1, name="Design Phase", description="Component planning")
   → Returns: {"id": 1, "order": 1, "playbook_id": 1}

3. create_activity(workflow_id=1, name="Define Props Interface", guidance="...")
   → Returns: {"id": 1, "order": 1}

4. create_activity(workflow_id=1, name="Create Mockup", guidance="...")
   → Returns: {"id": 2, "order": 2}

5. set_activity_predecessor(activity_id=2, predecessor_id=1)
   → Returns: {"updated": True}

Result: Draft playbook v0.1 created with workflows and activities
```

### Story 2: Iteratively Refine Draft Methodology
**As**: AI assistant  
**I want to**: Update/add/remove components in draft playbook  
**So that**: User can refine methodology through conversation

**Scenario**:
```
User: "Add a testing workflow to the React methodology"

AI uses MCP tools:
1. get_playbook(playbook_id=1)
   → Returns full playbook structure

2. create_workflow(playbook_id=1, name="Testing Phase", description="...")
   → Playbook version auto-increments: 0.1 → 0.2

3. create_activity(workflow_id=2, name="Write Unit Tests", ...)
   → Playbook version: 0.2 → 0.3

Result: Draft playbook v0.3 with new testing workflow
```

### Story 3: Query Existing Methodology
**As**: AI assistant  
**I want to**: Read playbook structure to answer user questions  
**So that**: User gets accurate information about their methodologies

**Scenario**:
```
User: "What activities are in the Design Phase?"

AI uses MCP tools:
1. list_playbooks(status="draft")
   → Returns list of draft playbooks

2. get_playbook(playbook_id=1)
   → Returns playbook with workflows

3. get_workflow(workflow_id=1)
   → Returns workflow with activities

AI responds: "The Design Phase has 2 activities: 1) Define Props Interface, 2) Create Mockup"
```

### Story 4: Permission Enforcement
**As**: AI assistant  
**I want to**: Attempt to modify released playbook and get clear error  
**So that**: User understands PIP workflow is required

**Scenario**:
```
User: "Update the production React methodology"

AI uses MCP tools:
1. get_playbook(playbook_id=1)
   → Returns: {"status": "released", "version": "1.0"}

2. update_playbook(playbook_id=1, name="New Name")
   → Raises: PermissionError("Cannot modify released playbook. Use create_pip instead.")

AI responds: "This playbook is released (v1.0). To make changes, you need to create a PIP (Playbook Improvement Proposal)."
```

## 3. Detailed Implementation Plan

### Branch Setup
- [x] Already on `feature/mcp-integration` branch

### Phase A: FastMCP Integration (Core Functionality)

#### A1. Install and Configure FastMCP
**Task**: Verify FastMCP library installed  
**Files**: `requirements.txt`  
**Actions**:
- Check `fastmcp` in requirements.txt ✓ (already there)
- No installation needed

#### A2. Initialize FastMCP Server
**Task**: Create FastMCP instance in mcp/tools.py  
**Files**: `mcp/tools.py`  
**Actions**:
- Import FastMCP: `from fastmcp import FastMCP`
- Create global instance: `mcp = FastMCP("Mimir Methodology Assistant")`
- Add `initialize_mcp()` function that returns `mcp`

**Test**: None yet (will test in integration)

#### A3. Add @mcp.tool() Decorators to 16 Tools
**Task**: Decorate all tool functions with @mcp.tool()  
**Files**: `mcp/tools.py`  
**Actions**:
- Add `@mcp.tool()` above each of 16 functions:
  - `create_playbook_tool` → `create_playbook`
  - `list_playbooks_tool` → `list_playbooks`
  - `get_playbook_tool` → `get_playbook`
  - `update_playbook_tool` → `update_playbook`
  - `delete_playbook_tool` → `delete_playbook`
  - (Same for workflow + activity tools)
- Rename functions to match SAO.md spec (remove `_tool` suffix)

**Test**: Write `tests/unit/test_mcp_tool_decorators.py`
- Test that all 16 functions have @mcp.tool decorator
- Test function signatures match SAO.md spec

#### A4. Implement User Context Management
**Task**: Implement `get_current_user()` from MCP context  
**Files**: `mcp/tools.py`, `mcp/context.py` (new)  
**Actions**:
- Create `mcp/context.py`:
  ```python
  import contextvars
  
  _current_user = contextvars.ContextVar('current_user')
  
  def set_current_user(user):
      _current_user.set(user)
  
  def get_current_user():
      user = _current_user.get(None)
      if user is None:
          raise ValueError("No user context available")
      return user
  ```
- Update `mcp/tools.py`:
  - Replace `get_current_user()` stub with import from context
  - `from mcp.context import get_current_user`

**Test**: Write `tests/unit/test_mcp_context.py`
- Test `set_current_user()` + `get_current_user()` roundtrip
- Test `get_current_user()` raises when no context set

#### A5. Implement mcp_server Management Command
**Task**: Wire FastMCP to Django management command  
**Files**: `mcp/management/commands/mcp_server.py`  
**Actions**:
- Import FastMCP initialization
- Set up logging to `logs/mcp.log`
- Get user from Django (for development/testing)
- Set user context
- Run FastMCP stdio server: `mcp.run()`

**Code**:
```python
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mcp.tools import initialize_mcp
from mcp.context import set_current_user

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run MCP server for AI assistant integration (stdio protocol)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Username for MCP session'
        )
    
    def handle(self, *args, **options):
        # Get user
        User = get_user_model()
        username = options.get('user') or 'admin'
        user = User.objects.get(username=username)
        
        # Set context
        set_current_user(user)
        logger.info(f'MCP server starting for user: {user.username}')
        
        # Run FastMCP
        mcp = initialize_mcp()
        mcp.run()
```

**Test**: Write `tests/integration/test_mcp_server_command.py`
- Test command can be discovered: `python manage.py help mcp_server`
- Test command starts without errors (mock mcp.run())

### Phase B: Service Testing (Retroactive)

**Re-read**: `.windsurf/rules/test-first.md` before each test file

#### B1. Test PlaybookService
**Task**: Write comprehensive unit tests for PlaybookService  
**Files**: `tests/unit/test_playbook_service.py`  
**Tests to create**:
1. `test_create_playbook_sets_version_0_1_for_draft`
2. `test_create_playbook_sets_version_1_0_for_released`
3. `test_create_playbook_raises_on_empty_name`
4. `test_create_playbook_raises_on_duplicate_name`
5. `test_get_playbook_returns_instance`
6. `test_get_playbook_raises_when_not_found`
7. `test_list_playbooks_filters_by_status`
8. `test_list_playbooks_returns_all_when_no_filter`
9. `test_update_playbook_changes_fields`
10. `test_update_playbook_raises_on_duplicate_name`
11. `test_delete_playbook_cascades_to_workflows`
12. `test_duplicate_playbook_creates_copy_with_version_0_1`
13. `test_duplicate_playbook_raises_on_duplicate_name`
14. `test_release_playbook_transitions_draft_to_released`
15. `test_release_playbook_sets_version_1_0`
16. `test_release_playbook_raises_when_not_draft`
17. `test_release_playbook_raises_when_not_owner`

**Fixtures needed**:
- `user` - test user
- `draft_playbook` - playbook with status='draft', version=0.1
- `released_playbook` - playbook with status='released', version=1.0

**NO MOCKING** per `.windsurf/rules/do-not-mock-in-integration-tests.md`

#### B2. Test WorkflowService
**Task**: Write comprehensive unit tests for WorkflowService  
**Files**: `tests/unit/test_workflow_service.py`  
**Tests to create**:
1. `test_create_workflow_auto_assigns_order`
2. `test_create_workflow_respects_provided_order`
3. `test_create_workflow_raises_on_duplicate_name`
4. `test_create_workflow_raises_on_empty_name`
5. `test_get_workflow_returns_instance`
6. `test_get_workflow_raises_when_not_found`
7. `test_get_workflows_for_playbook_ordered_by_order`
8. `test_update_workflow_changes_fields`
9. `test_update_workflow_raises_on_duplicate_name`
10. `test_delete_workflow_cascades_to_activities`
11. `test_duplicate_workflow_creates_copy`
12. `test_duplicate_workflow_raises_on_duplicate_name`

**Fixtures needed**:
- `playbook` - parent playbook
- `workflow` - workflow instance

#### B3. Test ActivityService
**Task**: Write comprehensive unit tests for ActivityService  
**Files**: `tests/unit/test_activity_service.py`  
**Tests to create**:
1. `test_create_activity_auto_assigns_order`
2. `test_create_activity_respects_provided_order`
3. `test_create_activity_raises_on_duplicate_name`
4. `test_create_activity_raises_on_empty_name`
5. `test_create_activity_validates_predecessor_in_same_workflow`
6. `test_create_activity_validates_successor_in_same_workflow`
7. `test_get_activity_returns_instance`
8. `test_get_activities_for_workflow_ordered_by_order`
9. `test_update_activity_changes_fields`
10. `test_delete_activity_removes_from_database`
11. `test_set_predecessor_creates_link`
12. `test_set_predecessor_validates_circular_dependency`
13. `test_remove_predecessor_breaks_link`
14. `test_set_successor_creates_link`
15. `test_remove_successor_breaks_link`
16. `test_get_predecessors_returns_list`
17. `test_get_successors_returns_list`
18. `test_validate_dependencies_detects_circular`

**Fixtures needed**:
- `workflow` - parent workflow
- `activity1`, `activity2`, `activity3` - for dependency testing

### Phase C: MCP Tool Testing

**Re-read**: `.windsurf/rules/test-first.md` before each test file

#### C1. Test MCP Tool Wrappers (Playbook)
**Task**: Test playbook MCP tools with mocked services  
**Files**: `tests/unit/test_mcp_playbook_tools.py`  
**Tests to create**:
1. `test_create_playbook_calls_service_with_user_context`
2. `test_create_playbook_returns_serialized_dict`
3. `test_list_playbooks_filters_by_status`
4. `test_get_playbook_includes_workflows`
5. `test_update_playbook_checks_released_status`
6. `test_update_playbook_increments_version`
7. `test_delete_playbook_checks_released_status`
8. `test_all_tools_require_user_context`

**Mocking strategy**:
- Mock `get_current_user()` to return test user
- Mock service calls to verify correct parameters passed
- Verify permission checks happen before service calls

#### C2. Test MCP Tool Wrappers (Workflow)
**Task**: Test workflow MCP tools  
**Files**: `tests/unit/test_mcp_workflow_tools.py`  
**Tests to create**:
1. `test_create_workflow_checks_parent_playbook_status`
2. `test_create_workflow_increments_parent_version`
3. `test_list_workflows_returns_for_playbook`
4. `test_get_workflow_includes_activities`
5. `test_update_workflow_checks_parent_playbook_status`
6. `test_update_workflow_increments_parent_version`
7. `test_delete_workflow_checks_parent_playbook_status`
8. `test_delete_workflow_increments_parent_version`

#### C3. Test MCP Tool Wrappers (Activity)
**Task**: Test activity MCP tools with dependency management  
**Files**: `tests/unit/test_mcp_activity_tools.py`  
**Tests to create**:
1. `test_create_activity_checks_grandparent_playbook_status`
2. `test_create_activity_increments_grandparent_version`
3. `test_create_activity_validates_predecessor_in_same_workflow`
4. `test_list_activities_returns_with_dependencies`
5. `test_get_activity_includes_predecessor_successor`
6. `test_update_activity_checks_grandparent_playbook_status`
7. `test_delete_activity_checks_grandparent_playbook_status`
8. `test_set_predecessor_validates_circular_dependency`
9. `test_set_predecessor_increments_grandparent_version`

### Phase D: Integration Testing

**Re-read**: `.windsurf/rules/do-not-mock-in-integration-tests.md`

#### D1. E2E Test: Create Methodology via MCP
**Task**: End-to-end test of creating playbook → workflow → activities via MCP tools  
**Files**: `tests/integration/test_mcp_create_methodology.py`  
**Test scenario**:
```python
def test_create_react_methodology_via_mcp(user):
    """E2E: Create complete React methodology using MCP tools."""
    # Set user context
    set_current_user(user)
    
    # Create playbook
    playbook = create_playbook(
        name="React Component Development",
        description="Best practices",
        category="frontend"
    )
    assert playbook['status'] == 'draft'
    assert playbook['version'] == '0.1'
    
    # Create workflow
    workflow = create_workflow(
        playbook_id=playbook['id'],
        name="Design Phase",
        description="Component planning"
    )
    assert workflow['playbook_id'] == playbook['id']
    
    # Verify version incremented
    updated_playbook = get_playbook(playbook['id'])
    assert updated_playbook['version'] == '0.2'
    
    # Create activities
    act1 = create_activity(
        workflow_id=workflow['id'],
        name="Define Props",
        guidance="Document component interface"
    )
    
    act2 = create_activity(
        workflow_id=workflow['id'],
        name="Create Mockup",
        guidance="Design component visuals"
    )
    
    # Set dependency
    set_activity_predecessor(
        activity_id=act2['id'],
        predecessor_id=act1['id']
    )
    
    # Verify final structure
    final_playbook = get_playbook(playbook['id'])
    assert final_playbook['version'] == '0.4'  # 0.1 + workflow + 2 activities
    assert len(final_playbook['workflows']) == 1
    
    final_workflow = get_workflow(workflow['id'])
    assert len(final_workflow['activities']) == 2
    
    final_act2 = get_activity(act2['id'])
    assert final_act2['predecessor']['id'] == act1['id']
```

**NO MOCKING** - uses real database, real services, real MCP tools

#### D2. E2E Test: Permission Enforcement
**Task**: Test that released playbooks reject modifications  
**Files**: `tests/integration/test_mcp_permissions.py`  
**Test scenario**:
```python
def test_cannot_modify_released_playbook_via_mcp(user):
    """E2E: Verify permission checks for released playbooks."""
    set_current_user(user)
    
    # Create and release playbook
    playbook = create_playbook(name="Test", description="Test", category="test")
    
    # Release it (using service directly for setup)
    PlaybookService.release_playbook(playbook['id'], user)
    
    # Attempt to update - should fail
    with pytest.raises(PermissionError, match="released playbook"):
        update_playbook(playbook['id'], name="New Name")
    
    # Attempt to delete - should fail
    with pytest.raises(PermissionError, match="released playbook"):
        delete_playbook(playbook['id'])
    
    # Attempt to create workflow - should fail
    with pytest.raises(PermissionError, match="released playbook"):
        create_workflow(playbook['id'], name="New Workflow", description="Test")
```

#### D3. Integration Test: MCP Server Command
**Task**: Test mcp_server command actually runs  
**Files**: `tests/integration/test_mcp_server_startup.py`  
**Test scenario**:
```python
def test_mcp_server_command_starts(capsys):
    """Test mcp_server management command can start."""
    from django.core.management import call_command
    
    # This will hang on mcp.run(), so we mock just the run() call
    with patch('mcp.tools.initialize_mcp') as mock_init:
        mock_mcp = Mock()
        mock_init.return_value = mock_mcp
        
        call_command('mcp_server', '--user=testuser')
        
        # Verify it tried to run
        mock_mcp.run.assert_called_once()
```

### Phase E: Documentation & Finalization

#### E1. Update SAO.md with Implementation Details
**Task**: Document actual implementation details in SAO.md  
**Files**: `docs/architecture/SAO.md`  
**Actions**:
- Add section: "MCP Implementation Status"
- Document user context management approach
- Document command usage: `python manage.py mcp_server --user=username`

#### E2. Create MCP Usage Guide
**Task**: Document how to use MCP tools  
**Files**: `docs/mcp/USAGE_GUIDE.md`  
**Content**:
- How to start mcp_server
- How to connect AI assistant (Cascade, Claude Desktop)
- Example MCP tool calls
- Troubleshooting

#### E3. Update IMPLEMENTATION_STATUS.md
**Task**: Mark implementation complete  
**Files**: `docs/mcp/IMPLEMENTATION_STATUS.md`  
**Actions**:
- Mark all phases complete
- Document test coverage
- Document known limitations

### Phase F: Commit Strategy

After each major step above:
1. Run tests: `pytest tests/unit/test_X.py -v`
2. Verify all tests pass
3. Commit with Angular convention:
   ```
   test(services): add PlaybookService unit tests
   feat(mcp): implement user context management
   feat(mcp): wire FastMCP to mcp_server command
   ```
4. Update this implementation plan with status

## 4. Test Summary

**Total tests to create**: ~60 tests

**Service tests** (~45 tests):
- PlaybookService: 17 tests
- WorkflowService: 12 tests
- ActivityService: 18 tests

**MCP tool tests** (~25 tests):
- Playbook tools: 8 tests
- Workflow tools: 8 tests
- Activity tools: 9 tests

**Integration tests** (~3 tests):
- E2E create methodology: 1 test
- E2E permissions: 1 test
- mcp_server startup: 1 test

**NO MOCKING in integration tests** per project rules

## 5. Success Criteria

- [ ] All 16 MCP tools have @mcp.tool() decorators
- [ ] User context management working
- [ ] mcp_server command runs FastMCP
- [ ] All 60 tests passing (100% pass rate required)
- [ ] E2E test: AI can create playbook → workflow → activities via MCP
- [ ] E2E test: Permission checks enforce draft-only modifications
- [ ] Documentation complete

## 6. Estimated Effort

**Not applicable** - AI execution, not human estimation

## 7. GitHub Issue

**TODO**: Find or create GitHub issue for MCP integration feature
- Follow `.windsurf/rules/do-github-issues.md`
- Link this plan to issue
- Update issue after each phase completion
