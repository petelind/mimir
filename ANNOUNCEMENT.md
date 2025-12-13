Mimir is now available as a Docker container with MCP support for Claude, Cursor, and Windsurf.

Mimir is a structured engineering playbook system that runs in your IDE through the Model Context Protocol. It provides workflow guidance to your AI assistant, helping you follow consistent development processes.

The container comes with FeatureFactory, the playbook we use to build Mimir itself. It covers feature planning through deployment with 8 activities across 3 workflows. You can use it as-is to contribute to Mimir, or create your own playbooks by combining activities into custom workflows.

Installation is straightforward. Pull the container, run it with your username, and add the MCP configuration to your IDE. Your AI assistant can then query Mimir for workflow guidance. There's also a web interface at localhost:8000 for managing playbooks visually.

The container handles everything - no Python setup, no virtual environments. It works on both Intel and Apple Silicon Macs. Your data persists across updates in a mounted volume. To update, just pull the new image and restart.

To install, tell your IDE:

  docker pull acrmimir.azurecr.io/mimir:release-latest
  docker run -d --name mimir -p 8000:8000 -v ~/mimir-data:/app/data -e MIMIR_USER=yourname acrmimir.azurecr.io/mimir:release-latest

Then add this to your MCP config (Windsurf example):

  "mimir": {
    "command": "docker",
    "args": ["exec", "-i", "-e", "MIMIR_MCP_MODE=1", "mimir", "python", "manage.py", "mcp_server", "--user=yourname"]
  }

Restart your IDE and ask: "Mimir, list all playbooks"

GitHub: github.com/phainestai/mimir
Container: acrmimir.azurecr.io/mimir:release-latest
