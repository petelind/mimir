# Mimir is Now Available as a Dockerized MCP Server

We're excited to announce that **Mimir** is now available as a ready-to-use Docker container with Model Context Protocol (MCP) support!

## What is Mimir?

Mimir is your self-evolving engineering playbook that runs directly in your IDE. It provides structured guidance for software development workflows through MCP integration with AI assistants like Claude, Cursor, and Windsurf.

## What's Included?

The container comes pre-loaded with the **FeatureFactory** playbook - the same methodology used to build Mimir itself. It includes:

- **3 Workflows** covering the complete feature development lifecycle
- **8 Activities** from planning through deployment
- **Rich guidance** for each activity with best practices
- **Ready to use** for contributing to Mimir or building your own features

You can also **create your own playbooks** by combining activities into custom workflows that match your team's process.

## Installation - Just 2 Steps!

### 1. Start the Container

```bash
docker pull acrmimir.azurecr.io/mimir:release-latest

docker run -d \
  --name mimir \
  -p 8000:8000 \
  -v ~/mimir-data:/app/data \
  -e MIMIR_USER=yourusername \
  -e MIMIR_EMAIL=you@example.com \
  acrmimir.azurecr.io/mimir:release-latest
```

### 2. Configure Your IDE

**For Windsurf** - Add to `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "mimir": {
      "command": "docker",
      "args": [
        "exec", "-i", "-e", "MIMIR_MCP_MODE=1",
        "mimir", "python", "manage.py", "mcp_server",
        "--user=yourusername"
      ]
    }
  }
}
```

**For Claude Desktop** - Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "mimir": {
      "command": "docker",
      "args": [
        "exec", "-i", "-e", "MIMIR_MCP_MODE=1",
        "mimir", "python", "manage.py", "mcp_server",
        "--user=yourusername"
      ]
    }
  }
}
```

**For Cursor** - Add to workspace `.cursorrules` or settings:
```json
{
  "mcp": {
    "servers": {
      "mimir": {
        "command": "docker",
        "args": [
          "exec", "-i", "-e", "MIMIR_MCP_MODE=1",
          "mimir", "python", "manage.py", "mcp_server",
          "--user=yourusername"
        ]
      }
    }
  }
}
```

Restart your IDE, and you're ready to go!

## Use It Right Away

Ask your AI assistant:
- "Mimir, list all playbooks"
- "Mimir, show me the Build Feature workflow"
- "Mimir, what activities are in the Planning phase?"

Your assistant will query Mimir directly and provide structured guidance based on the playbook.

## Web UI Included

Access the web interface at `http://localhost:8000` to:
- Browse and edit playbooks visually
- View workflow diagrams
- Manage activities and guidance
- Track your methodology evolution

## Key Features

- **No Python/venv setup required** - Everything runs in Docker
- **Multi-platform support** - Works on Intel and Apple Silicon Macs
- **Persistent data** - Your playbooks survive container updates
- **Easy updates** - Just pull the latest image and restart
- **Production-ready** - Automated CI/CD via GitHub Actions

## Contributing

Mimir is open source! Use the included FeatureFactory playbook to guide your contributions:

```bash
# Clone the repo
git clone https://github.com/phainestai/mimir.git

# Ask your AI assistant
"Mimir, guide me through implementing a new feature using FeatureFactory"
```

## Learn More

- **Documentation**: [README.md](https://github.com/phainestai/mimir/blob/main/README.md)
- **Architecture**: [SAO.md](https://github.com/phainestai/mimir/blob/main/docs/architecture/SAO.md)
- **Container Registry**: `acrmimir.azurecr.io/mimir:release-latest`
- **GitHub**: [phainestai/mimir](https://github.com/phainestai/mimir)

---

**Version**: 0.0.3  
**License**: [License details]  
**Support**: [GitHub Issues](https://github.com/phainestai/mimir/issues)
