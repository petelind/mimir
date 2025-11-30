# MCP Integration

This directory contains documentation for the Model Context Protocol (MCP) integration in Mimir.

## Quick Start

```bash
# Start MCP server for user "maria"
python manage.py mcp_server --user=maria

# Run integration tests
pytest tests/integration/test_mcp_playbook_tools.py tests/integration/test_mcp_workflow_tools.py -v
```

## Documentation

- **[MCP_IMPLEMENTATION_STATUS.md](./MCP_IMPLEMENTATION_STATUS.md)** - Current implementation status, what's working, what's not
- **[../plans/MCP_CRUD_IMPLEMENTATION_PLAN.md](../plans/MCP_CRUD_IMPLEMENTATION_PLAN.md)** - Original implementation plan
- **[../architecture/SAO.md](../architecture/SAO.md)** - Architecture documentation (Hybrid MCP Access model)

## Feature Files (BDD Specifications)

- **[../features/act-13-mcp/interact-with-playbooks-via-mcp.feature](../features/act-13-mcp/interact-with-playbooks-via-mcp.feature)** - 18 playbook scenarios
- **[../features/act-13-mcp/interact-with-workflows-via-mcp.feature](../features/act-13-mcp/interact-with-workflows-via-mcp.feature)** - 19 workflow scenarios
- **[../features/act-13-mcp/interact-with-activities-via-mcp.feature](../features/act-13-mcp/interact-with-activities-via-mcp.feature)** - 23 activity scenarios

## Status

✅ **FUNCTIONAL** - 16 tools implemented, 7 integration tests passing (100% pass rate)

See [MCP_IMPLEMENTATION_STATUS.md](./MCP_IMPLEMENTATION_STATUS.md) for details.
