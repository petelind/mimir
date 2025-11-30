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

## 2. BDD Feature Files - AI Assistant Using MCP Tools

**Actor**: AI assistant (Cascade) using MCP tools programmatically via stdio protocol

### Feature Files Created

1. **`docs/features/act-13-mcp/interact-with-playbooks-via-mcp.feature`** (18 scenarios)
   - Create/list/get/update/delete playbooks via MCP
   - Permission enforcement (draft vs released)
   - Version auto-increment on updates
   - Error handling and validation
   - Iterative refinement workflow

2. **`docs/features/act-13-mcp/interact-with-workflows-via-mcp.feature`** (19 scenarios)
   - Create/list/get/update/delete workflows via MCP
   - Parent playbook version incrementing
   - Permission checks on grandparent playbook
   - Workflow ordering
   - End-to-end methodology building

3. **`docs/features/act-13-mcp/interact-with-activities-via-mcp.feature`** (23 scenarios)
   - Create/list/get/update/delete activities via MCP
   - Dependency management (predecessors/successors)
   - Circular dependency validation
   - Grandparent playbook version incrementing
   - Complex dependency chains

**Total: 60 Gherkin scenarios** covering all MCP CRUD operations

### Example Scenarios

**Create Playbook** (from `interact-with-playbooks-via-mcp.feature`):
```gherkin
Scenario: MCP-PB-01 Create draft playbook via MCP tool
  Given Cascade receives user request "Help me create a React component development methodology"
  When Cascade calls MCP tool "create_playbook" with:
    | name        | React Component Development                          |
    | description | Best practices for building reusable React components |
    | category    | frontend                                              |
  Then MCP returns success response with:
    | id      | 1     |
    | version | 0.1   |
    | status  | draft |
  And playbook is saved in database with author "maria"
```

**Permission Enforcement** (from `interact-with-playbooks-via-mcp.feature`):
```gherkin
Scenario: MCP-PB-13 Update released playbook raises permission error
  Given released playbook (id=1, status=released, version=1.0) exists
  When Cascade calls MCP tool "update_playbook" with:
    | playbook_id | 1        |
    | name        | New Name |
  Then MCP returns error "PermissionError: Cannot modify released playbook. Use create_pip instead."
  And playbook is not modified
```

**Dependency Management** (from `interact-with-activities-via-mcp.feature`):
```gherkin
Scenario: MCP-ACT-19 Set predecessor validates circular dependency
  Given workflow has activities with chain: 1 → 2 → 3
  When Cascade calls "set_activity_predecessor" with:
    | activity_id    | 1 |
    | predecessor_id | 3 |
  Then MCP returns error "ValidationError: Circular dependency detected"
  And no dependency is created
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

### Phase C: MCP Tool Unit Tests (Optional - for tool wrapper logic)

**Note**: With BDD feature files as primary tests, these unit tests are optional. Only create if tool wrappers have complex logic beyond calling services.

**Skip for now** - BDD scenarios provide comprehensive coverage of tool behavior.

### Phase D: Integration Tests (Based on BDD Scenarios)

**Re-read**: `.windsurf/rules/do-not-mock-in-integration-tests.md`

**Strategy**: Write separate pytest integration tests, one per BDD scenario. BDD feature files provide specification, regular pytest provides implementation.

#### D1. Integration Tests for Playbook MCP Tools
**Task**: Write 18 integration tests based on playbook scenarios  
**Files**: `tests/integration/test_mcp_playbook_tools.py`  
**Reference**: `docs/features/act-13-mcp/interact-with-playbooks-via-mcp.feature`

**Example tests**:
```python
import pytest
from mcp.context import set_current_user
from mcp.tools import create_playbook, update_playbook, delete_playbook
from methodology.models import Playbook

class TestPlaybookMCPTools:
    """Integration tests for Playbook MCP tools (based on BDD scenarios)."""
    
    def test_mcp_pb_01_create_draft_playbook_via_mcp_tool(self, maria_user):
        """
        Scenario: MCP-PB-01 Create draft playbook via MCP tool
        Given Cascade receives user request
        When Cascade calls create_playbook
        Then playbook created with version 0.1, status draft
        """
        # Set user context
        set_current_user(maria_user)
        
        # Call MCP tool
        result = create_playbook(
            name="React Component Development",
            description="Best practices for building reusable React components",
            category="frontend"
        )
        
        # Verify response
        assert result['id'] == 1
        assert result['version'] == '0.1'
        assert result['status'] == 'draft'
        
        # Verify in database
        playbook = Playbook.objects.get(id=result['id'])
        assert playbook.author == maria_user
        assert playbook.name == "React Component Development"
    
    def test_mcp_pb_02_create_playbook_with_duplicate_name_raises_error(self, maria_user):
        """
        Scenario: MCP-PB-02 Create playbook with duplicate name raises error
        Given draft playbook exists
        When Cascade calls create_playbook with same name
        Then ValidationError raised
        """
        set_current_user(maria_user)
        
        # Create first playbook
        create_playbook(
            name="React Component Development",
            description="Test",
            category="frontend"
        )
        
        # Attempt duplicate
        with pytest.raises(ValidationError, match="already exists"):
            create_playbook(
                name="React Component Development",
                description="Different description",
                category="frontend"
            )
    
    def test_mcp_pb_13_update_released_playbook_raises_permission_error(self, maria_user):
        """
        Scenario: MCP-PB-13 Update released playbook raises permission error
        Given released playbook exists
        When Cascade calls update_playbook
        Then PermissionError raised
        """
        set_current_user(maria_user)
        
        # Create and release playbook
        result = create_playbook(name="Test", description="Test", category="test")
        from methodology.services import PlaybookService
        PlaybookService.release_playbook(result['id'], maria_user)
        
        # Attempt to update
        with pytest.raises(PermissionError, match="released playbook"):
            update_playbook(result['id'], name="New Name")
        
        # Verify not modified
        playbook = Playbook.objects.get(id=result['id'])
        assert playbook.name == "Test"
        assert playbook.version == Decimal('1.0')
```

**NO MOCKING** - uses real database, real services, real MCP tools

#### D2. Integration Tests for Workflow MCP Tools
**Task**: Write 19 integration tests based on workflow scenarios  
**Files**: `tests/integration/test_mcp_workflow_tools.py`  
**Reference**: `docs/features/act-13-mcp/interact-with-workflows-via-mcp.feature`

**Example tests**:
```python
class TestWorkflowMCPTools:
    """Integration tests for Workflow MCP tools."""
    
    def test_mcp_wf_01_create_workflow_increments_parent_version(self, maria_user, draft_playbook):
        """
        Scenario: MCP-WF-01 Create workflow in draft playbook increments parent version
        """
        set_current_user(maria_user)
        
        old_version = draft_playbook.version
        assert old_version == Decimal('0.1')
        
        # Create workflow via MCP
        result = create_workflow(
            playbook_id=draft_playbook.id,
            name="Design Phase",
            description="Component architecture and planning"
        )
        
        # Verify workflow created
        assert result['id'] == 1
        assert result['playbook_id'] == draft_playbook.id
        assert result['order'] == 1
        
        # Verify parent version incremented
        draft_playbook.refresh_from_db()
        assert draft_playbook.version == Decimal('0.2')
```

#### D3. Integration Tests for Activity MCP Tools
**Task**: Write 23 integration tests based on activity scenarios  
**Files**: `tests/integration/test_mcp_activity_tools.py`  
**Reference**: `docs/features/act-13-mcp/interact-with-activities-via-mcp.feature`

**Example tests**:
```python
class TestActivityMCPTools:
    """Integration tests for Activity MCP tools."""
    
    def test_mcp_act_19_set_predecessor_validates_circular_dependency(self, maria_user, workflow_with_chain):
        """
        Scenario: MCP-ACT-19 Set predecessor validates circular dependency
        Given workflow has activities with chain: 1 → 2 → 3
        When Cascade tries to set activity 1 predecessor to activity 3
        Then ValidationError raised (circular dependency)
        """
        set_current_user(maria_user)
        
        # workflow_with_chain fixture has 3 activities: 1 → 2 → 3
        act1, act2, act3 = workflow_with_chain.activities.all().order_by('order')
        
        # Attempt to create circular dependency
        with pytest.raises(ValidationError, match="Circular dependency"):
            set_activity_predecessor(
                activity_id=act1.id,
                predecessor_id=act3.id
            )
        
        # Verify no dependency created
        act1.refresh_from_db()
        assert act1.predecessor is None
```

#### D4. Test Execution
**Command**: `pytest tests/integration/ -v`

**Success criteria**: All 60 integration tests pass (100% pass rate)

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

**BDD Feature Scenarios**: 60 scenarios (test-first)
- `interact-with-playbooks-via-mcp.feature`: 18 scenarios
- `interact-with-workflows-via-mcp.feature`: 19 scenarios
- `interact-with-activities-via-mcp.feature`: 23 scenarios

**Unit tests to create** (~45 tests - retroactive for services):
- PlaybookService: 17 tests (create/get/list/update/delete/duplicate/release)
- WorkflowService: 12 tests (create/get/list/update/delete/duplicate)
- ActivityService: 18 tests (CRUD + dependency management)

**Integration tests to create** (~60 tests based on BDD scenarios):
- Separate pytest tests (NOT pytest-bdd step definitions)
- NO MOCKING per project rules
- Real database, real services, real MCP tools
- Each test implements one BDD scenario
- Example: `test_mcp_pb_01_create_draft_playbook()` implements scenario MCP-PB-01

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
