# Mimir

**Self-evolving methodologies for software engineering**

Mimir helps you work more effectively by providing structured methodologies that your AI assistant can access directly in your IDE. Get guidance, generate work plans, track progress, and continuously improve your development process.

> 📖 For architecture and design details, see [docs/architecture/SAO.md](docs/architecture/SAO.md)

## What Can Mimir Do?

### 🤖 Answer Methodology Questions via MCP

Your AI assistant can query Mimir directly from your IDE (powered by FastMCP):

```
You: "How do I build a TSX component per FDD methodology?"
AI: → Queries Mimir → Returns activity guidance and relevant Howtos
```

### 📋 Generate Work Plans

Automatically create task breakdowns in GitHub or Jira:

```
You: "Plan implementation of scenario LOG1.1 and Screen LOG per FDD"
AI: → Generates work orders from methodology → Creates GitHub issues
```

### 📊 Assess Project Progress

Check if you've completed all required deliverables for a phase:

```
You: "I'm supposed to finish inception. Did I produce all required artifacts?"
AI: → Scans codebase and issues → Reports status and gaps
```

### 🔄 Evolve Through Experience

When AI encounters issues during work, it can propose methodology improvements:

```
AI: → Detects repeated corrections → Creates Process Improvement Proposal (PIP)
You: → Reviews PIP in web UI → Approves with notes → New methodology version created
```

### 📚 Access Methodology Library

Download methodologies from HOMEBASE based on your access level:
- **Family-based**: Software Engineering, UX Design, Testing, etc.
- **Version tiers**: LITE (Basic), FULL (Standard), EXTENDED (Premium)

## Installation

### Prerequisites

- Python 3.11 or higher
- IDE with MCP support (Claude Desktop, Cursor, Windsurf, etc.)
- Access credentials for HOMEBASE (optional, for syncing)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mimir.git
   cd mimir
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python manage.py migrate
   ```

5. **Download methodologies** (requires HOMEBASE access)
   ```bash
   python manage.py sync_methodology --family "Software Engineering" --level "Basic"
   ```

   Or load sample methodologies:
   ```bash
   python manage.py loaddata sample_methodologies
   ```

## How to Use

Mimir runs as two processes that work together:

### 1. Start the Web Interface

```bash
python manage.py runserver 8000
```

Open http://localhost:8000 in your browser to:
- **Browse methodologies**: View activities, workflows, howtos, and deliverables
- **Review PIPs**: Approve or reject Process Improvement Proposals
- **Compare versions**: See what changed between methodology versions
- **Edit locally**: Customize methodologies for your team

### 2. Configure MCP in Your IDE

Add Mimir to your MCP client configuration.

**For Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "mimir": {
      "command": "python",
      "args": ["/absolute/path/to/mimir/manage.py", "mcp_server"],
      "cwd": "/absolute/path/to/mimir"
    }
  }
}
```

**For Cursor** (`.cursorrules` or workspace settings):
```json
{
  "mcp": {
    "servers": {
      "mimir": {
        "command": "python",
        "args": ["/absolute/path/to/mimir/manage.py", "mcp_server"]
      }
    }
  }
}
```

Restart your IDE after configuration.

### 3. Use MCP Tools in Your IDE

Once configured, your AI assistant has access to three Mimir tools (implemented using [FastMCP](https://github.com/jlowin/fastmcp)):

#### query_methodology
Ask questions about how to perform tasks:
```
"How do I create screen mockups per FDD methodology?"
"What are the acceptance criteria for a component specification?"
"Show me howtos for React component testing"
```

#### plan_execution
Generate work plans and create tasks:
```
"Plan implementation of user login feature per FDD"
"Create GitHub issues for inception phase activities"
"Generate work breakdown for scenario LOG1.1"
```
*Requires GitHub or Jira MCP to be configured*

#### assess_progress
Check progress against methodology phases:
```
"Am I ready to complete the inception phase?"
"What deliverables am I missing for construction?"
"Assess my project against FDD inception requirements"
```

## Typical Workflow

### Daily Development

1. **Start your work session**
   ```bash
   # Terminal 1: Web UI (leave running)
   python manage.py runserver 8000
   ```

2. **Ask AI for guidance**
   ```
   "I need to implement a user profile page. What's the FDD process for this?"
   ```

3. **Generate work plan**
   ```
   "Plan this implementation and create GitHub issues"
   ```

4. **Get implementation help**
   ```
   "How should I structure the TSX component per methodology?"
   ```

### Weekly Review

1. **Check methodology improvements**
   - Open http://localhost:8000/pips/
   - Review PIPs created by AI during the week
   - Approve good suggestions, reject with reasoning

2. **Sync from HOMEBASE**
   ```bash
   python manage.py sync_methodology --all
   ```

3. **Transmit approved PIPs**
   - Select PIPs worth sharing
   - Click "Transmit to HOMEBASE" in web UI
   - HOMEBASE team reviews for global adoption

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# HOMEBASE (methodology repository)
MIMIR_HOMEBASE_URL=https://methodologies.example.com
MIMIR_API_KEY=your_api_key_here

# Database
MIMIR_DB_PATH=mimir.db

# AI Model (optional)
OPENAI_API_KEY=your_openai_key  # For AI-driven features
```

### Methodology Sync

```bash
# Sync specific methodology
python manage.py sync_methodology --name "FDD"

# Sync entire family
python manage.py sync_methodology --family "Software Engineering"

# Sync all available for your access level
python manage.py sync_methodology --all

# Force re-download even if up to date
python manage.py sync_methodology --all --force
```

## Troubleshooting

### MCP Server Not Responding

1. Check if `mcp_server` command works:
   ```bash
   python manage.py mcp_server
   ```
   Should wait for input (press Ctrl+C to exit)

2. Verify paths in MCP config are absolute, not relative

3. Check IDE logs for MCP connection errors

### Database Locked

If you see "database is locked" errors:
```bash
# Ensure only one web server is running
pkill -f "manage.py runserver"

# Restart web server
python manage.py runserver 8000
```

### No Methodologies Available

```bash
# Load sample data
python manage.py loaddata sample_methodologies

# Or sync from source
python manage.py sync_methodology --family "Software Engineering"
```

## Project Structure

```
mimir/
├── docs/
│   └── architecture/
│       └── SAO.md           # System architecture & design
├── mimir/                   # Django project
│   ├── methodology/         # Core app
│   │   ├── models/          # Node, Edge, Version, PIP
│   │   ├── repository/      # Storage abstraction layer
│   │   ├── services/        # Business logic
│   │   └── views/           # Web UI
│   └── mcp/                 # FastMCP integration
│       ├── tools.py         # @tool decorators
│       └── management/
│           └── commands/
│               └── mcp_server.py  # Calls mcp.run()
├── manage.py
└── requirements.txt         # Includes fastmcp
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[License details here]

## Learn More

- **Architecture**: [docs/architecture/SAO.md](docs/architecture/SAO.md) - Complete system design
- **Methodology Concepts**: [docs/methodology-guide.md](docs/methodology-guide.md) - Understanding activities, workflows, etc.
- **MCP Protocol**: [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mimir/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mimir/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/mimir/wiki)
