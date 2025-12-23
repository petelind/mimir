#!/bin/bash
# Run all tests (unit, integration, and E2E) with proper isolation

set -e

echo "========================================"
echo "Running Unit and Integration Tests"
echo "========================================"
pytest tests/ --ignore=tests/integration/test_mcp_server_acceptance.py --ignore=tests/unit/test_activity_graph_service.py -v --tb=short

echo ""
echo "========================================"
echo "Running E2E Tests"
echo "========================================"
cd tests/e2e && pytest . -v --tb=short

echo ""
echo "========================================"
echo "✅ All tests completed successfully!"
echo "========================================"
