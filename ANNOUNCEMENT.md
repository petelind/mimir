Mimir is now available as a Docker container with MCP support for Claude, Cursor, and Windsurf.

Mimir is a structured engineering playbook system that runs in your IDE through the Model Context Protocol. It provides workflow guidance to your AI assistant, helping you follow consistent development processes.

The container comes with FeatureFactory, the playbook we use to build Mimir itself. It covers feature planning through deployment with 8 activities across 3 workflows. You can use it as-is to contribute to Mimir, or create your own playbooks by combining activities into custom workflows.

Installation is straightforward - just tell your AI assistant:

  "Pull and run acrmimir.azurecr.io/mimir:release-latest as a container named mimir on port 8000, with ~/mimir-data mounted to /app/data, and set MIMIR_USER to my username. Then add mimir to my MCP config using docker exec with args: exec, -i, -e, MIMIR_MCP_MODE=1, mimir, python, manage.py, mcp_server, --user=myusername. Restart the IDE after."

Then ask: "Mimir, list all playbooks"

The container handles everything - no Python setup, works on Intel and Apple Silicon, data persists across updates. Web interface at localhost:8000.

GitHub: github.com/phainestai/mimir
Container: acrmimir.azurecr.io/mimir:release-latest