# Mimir

**Your Self-Evolving Engineering Playbook**

Mimir helps you work more effectively by providing structured playbooks that your AI assistant can access directly in your IDE. Get guidance, generate work plans, track progress, and continuously improve your development process.

> 📖 For architecture and design details, see [docs/architecture/SAO.md](docs/architecture/SAO.md)

## Core Entities

Mimir organizes your playbooks using **7 core entities**:

1. **Playbook** - Top-level methodology container (e.g., "FDD", "Scrum")
2. **Workflow** - Sequence of activities for a process (e.g., "Build Feature")
3. **Phase** *(optional)* - Grouping for activities within workflows (e.g., "Inception", "Construction")
4. **Activity** - Unit of work with guidance (e.g., "Create screen mockup")
5. **Artifact** - Inputs/outputs of activities (e.g., "Component Specification", "Unit Tests")
6. **Role** - Who performs activities (e.g., "Frontend Engineer", "UX Designer")
7. **Howto** - Specific implementation instructions (e.g., "Creating mockups with Figma")

## What Can Mimir Do?

### 🤖 Answer Playbook Questions via MCP

Your AI assistant can query Mimir directly from your IDE (powered by FastMCP):

```
You: "How do I build a TSX component per FDD playbook?"
AI: → Queries Mimir → Returns activity guidance and relevant Howtos
```

### 📋 Generate Work Plans

Automatically create task breakdowns in GitHub or Jira:

```
You: "Plan implementation of scenario LOG1.1 and Screen LOG per FDD"
AI: → Generates work orders from playbook → Creates GitHub issues
```

### 📊 Assess Project Progress

Check if you've completed all required artifacts for a phase:

```
You: "I'm supposed to finish inception phase next week. Did I produce all required artifacts?"
AI: → Scans codebase and issues → Reports status and gaps
```

### 🔄 Evolve Through Experience

When AI encounters issues during work, it can propose playbook improvements:

```
AI: → Detects repeated corrections → Creates Playbook Improvement Proposal (PIP)
You: → Reviews PIP in web UI → Approves with notes → New playbook version created
```

### 📚 Access Playbook Library

Download playbooks from HOMEBASE based on your access level:
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
   git clone https://github.com/petelind/mimir.git
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
   
   **Note:** The default database (`mimir.db`) includes the **FeatureFactory** playbook, which was used to build Mimir itself. This playbook provides a complete feature development workflow with 8 activities covering planning, implementation, testing, and finalization.

5. **Create admin user (or use default)**
   
   The database comes with a default admin account:
   - **Username:** `admin`
   - **Password:** `admin`
   
   **For production or shared environments, create your own user:**
   ```bash
   python manage.py createsuperuser
   ```
   
   You'll be prompted for:
   - Username (required)
   - Email (optional, for password reset)
   - Password (minimum 8 characters)

6. **Run tests**
   
   Run unit and integration tests:
   ```bash
   pytest tests/
   ```
   
   > **Note**: BDD feature files in `docs/features/act-*/` serve as comprehensive UI specifications (46 files covering Acts 0-15). Step definitions will be implemented during development.

## Quick Reference

### Running the Application

```bash
# Start web UI (keep running in terminal)
python manage.py runserver 8000
# → Open http://localhost:8000

# Test MCP server manually (different terminal)
python manage.py mcp_server --user=admin
# → Press Ctrl+C to stop

# Run all tests
pytest tests/
# → Should see: 250 passed, 1 skipped

# Create a new user
python manage.py createsuperuser
```

### MCP Configuration Files

- **Windsurf**: `~/.codeium/windsurf/mcp_config.json`
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Cursor**: Workspace `.cursorrules` or settings

See configuration details in section 2 below.

---

## How to Use

Mimir runs as two processes that work together:

### 1. Start the Web Interface

```bash
python manage.py runserver 8000
```

Open http://localhost:8000 in your browser and log in with your credentials.

Once logged in, you can:
- **Browse playbooks**: View activities, workflows, phases, artifacts, roles, and howtos
- **Review PIPs**: Approve or reject Playbook Improvement Proposals
- **Compare versions**: See what changed between playbook versions
- **Edit locally**: Customize playbooks for your team

### 2. Configure MCP in Your IDE

Add Mimir to your MCP client configuration.

**For Windsurf** (`~/.codeium/windsurf/mcp_config.json`):
```json
{
  "mcpServers": {
    "mimir": {
      "command": "/absolute/path/to/mimir/venv/bin/python",
      "args": [
        "/absolute/path/to/mimir/manage.py",
        "mcp_server",
        "--user=admin"
      ],
      "env": {
        "DJANGO_SETTINGS_MODULE": "mimir.settings",
        "PYTHONPATH": "/absolute/path/to/mimir",
        "MIMIR_MCP_MODE": "1"
      },
      "disabled": false
    }
  }
}
```

**For Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "mimir": {
      "command": "/absolute/path/to/mimir/venv/bin/python",
      "args": [
        "/absolute/path/to/mimir/manage.py",
        "mcp_server",
        "--user=admin"
      ],
      "env": {
        "DJANGO_SETTINGS_MODULE": "mimir.settings",
        "PYTHONPATH": "/absolute/path/to/mimir",
        "MIMIR_MCP_MODE": "true"
      }
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
        "command": "/absolute/path/to/mimir/venv/bin/python",
        "args": [
          "/absolute/path/to/mimir/manage.py",
          "mcp_server",
          "--user=admin"
        ],
        "env": {
          "DJANGO_SETTINGS_MODULE": "mimir.settings",
          "PYTHONPATH": "/absolute/path/to/mimir",
          "MIMIR_MCP_MODE": "true"
        }
      }
    }
  }
}
```

**Important Notes:**
- Replace `/absolute/path/to/mimir` with your actual project path
- Replace `admin` with your username (created in step 5 above)
- Use the full path to your virtual environment's Python binary
- The `MIMIR_MCP_MODE` environment variable disables console logging for Windsurf

Restart your IDE after configuration.

### 3. Use MCP Tools in Your IDE

Once configured, your AI assistant has access to **16 Mimir MCP tools** for managing playbooks, workflows, and activities:

#### Playbook Management (5 tools)
- **`create_playbook`** - Create new draft playbooks
- **`list_playbooks`** - List playbooks (filter by status: draft/released/all)
- **`get_playbook`** - Get detailed playbook info with nested workflows
- **`update_playbook`** - Update playbook details (auto-increments version)
- **`delete_playbook`** - Delete draft playbooks

#### Workflow Management (5 tools)
- **`create_workflow`** - Add workflows to playbooks
- **`list_workflows`** - List workflows for a playbook
- **`get_workflow`** - Get workflow details with activities
- **`update_workflow`** - Update workflow details
- **`delete_workflow`** - Delete workflows from playbooks

#### Activity Management (6 tools)
- **`create_activity`** - Add activities to workflows
- **`list_activities`** - List activities in a workflow
- **`get_activity`** - Get activity details with dependencies
- **`update_activity`** - Update activity guidance, name, phase
- **`delete_activity`** - Remove activities
- **`set_predecessor`** - Define activity dependencies (validates no circular deps)

**Example Usage:**
```
"Create a new playbook called 'Frontend Best Practices'"
"Add a workflow called 'Component Development' to playbook 5"
"List all activities in workflow 3"
"Update activity 7 to add more detailed guidance"
```

All tools support async operations and validate user permissions automatically.

## Typical Workflow

### Daily Development

1. **Configure your IDE** (one-time setup)
   
   Add Mimir to your IDE's MCP configuration (see section 2 above):
   - **Windsurf:** `~/.codeium/windsurf/mcp_config.json`
   - **Claude Desktop:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Cursor:** Workspace settings or `.cursorrules`
   
   Restart your IDE after configuration.

2. **Start working with Mimir**
   
   Once configured, interact with Mimir through your IDE's AI assistant:
   
   ```
   "Mimir, list available playbooks"
   "Mimir, show me the Build Page workflow"
   "Mimir, plan FOB-LOGIN-1 per BPE1 Plan Feature"
   "Mimir, implement backend per BPE2"
   ```

3. **Optional: Web UI for management**
   
   Start the web interface to manage playbooks visually:
   ```bash
   python manage.py runserver 8000
   ```
   
   Open http://localhost:8000 to:
   - Browse and edit playbooks
   - View workflows and activities
   - Manage methodology content
   
   **Note:** While a Playbook is in draft status, you can work with it directly: update, extend, and even delete - via both MCP and GUI. Once it's released, it can be revised only via PIPs (Playbook Improvement Proposals).

## Troubleshooting

### MCP Server Not Responding

1. **Test the MCP server manually:**
   ```bash
   python manage.py mcp_server --user=admin
   ```
   The server should start and wait for JSON-RPC input. Press Ctrl+C to exit.
   
   To test a simple tool call, send:
   ```bash
   echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python manage.py mcp_server --user=admin
   ```
   You should see a list of 16 available tools.

2. **Verify configuration:**
   - Ensure paths in MCP config are **absolute**, not relative
   - Check that `--user=admin` matches an existing user in your database
   - Verify virtual environment path points to correct Python binary

3. **Check IDE logs:**
   - **Windsurf**: View logs in MCP settings panel
   - **Claude Desktop**: Check `~/Library/Logs/Claude/`
   - **Cursor**: Check IDE console for MCP connection errors

4. **Common issues:**
   - **"Command not found"**: Path to Python or manage.py is incorrect
   - **"User not found"**: Username doesn't exist, create it with `python manage.py createsuperuser`
   - **"Database is locked"**: Ensure web server isn't running simultaneously
   - **Timeout errors**: Check `app.log` for stderr contamination issues

### Database Locked

If you see "database is locked" errors:
```bash
# Ensure only one web server is running
pkill -f "manage.py runserver"

# Restart web server
python manage.py runserver 8000
```

## Project Structure

> **Note**: Internal code uses `methodology` as the technical term for accuracy (e.g., Django app name, models, commands), while user-facing terminology uses "playbooks" for accessibility. This is intentional - see [SAO.md](docs/architecture/SAO.md) for details.

```
mimir/
├── docs/
│   ├── architecture/
│   │   └── SAO.md              # System architecture & design
│   ├── features/               # BDD specifications (46+ files)
│   │   ├── act-0-auth/         # Authentication, Onboarding, Navigation
│   │   ├── act-2-playbooks/    # Playbooks CRUDLF (5 files)
│   │   ├── act-3-workflows/    # Workflows CRUDLF (5 files)
│   │   ├── act-4-phases/       # Phases CRUDLF (5 files, optional entity)
│   │   ├── act-5-activities/   # Activities CRUDLF (5 files)
│   │   ├── act-6-artifacts/    # Artifacts CRUDLF (5 files)
│   │   ├── act-7-roles/        # Roles CRUDLF (5 files)
│   │   ├── act-8-howtos/       # Howtos CRUDLF (5 files)
│   │   ├── act-9-15/           # PIPs, Import/Export, Family, Sync, MCP, Settings, Errors
│   │   └── act-13-mcp/         # MCP integration specifications (4 files)
│   ├── mcp/                    # MCP documentation
│   │   ├── README.md           # MCP overview
│   │   └── *.md                # Implementation status documents
│   └── ux/
│       ├── user_journey.md     # Complete Acts 0-15 narrative
│       └── 2_dialogue-maps/
│           └── screen-flow.drawio  # Visual MVP flow diagram
├── mimir/                      # Django project
│   ├── methodology/            # Core app (internal name)
│   │   ├── models/             # Playbook, Workflow, Activity, etc.
│   │   ├── services/           # Business logic (PlaybookService, etc.)
│   │   ├── repository/         # Storage abstraction layer
│   │   └── views/              # Web UI views
│   └── mcp_integration/        # MCP server integration (Django app)
│       ├── tools.py            # 16 MCP tool functions (async)
│       ├── context.py          # User context management
│       └── management/
│           └── commands/
│               └── mcp_server.py  # Django command: mcp_server
├── tests/
│   ├── unit/                   # Unit tests (services, models)
│   ├── integration/            # Integration tests (MCP tools, workflows)
│   └── e2e/                    # End-to-end tests (Playwright)
├── manage.py
└── requirements.txt            # Includes fastmcp, pytest-asyncio
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### IDE-Specific Rules

Mimir maintains project rules in two formats to support different AI-powered IDEs:
- **`.windsurf/rules/*.md`** - For Windsurf IDE
- **`.cursor/rules/*.mdc`** - For Cursor IDE

Both rule sets contain identical content with different formatting. **If you use Cursor and modify rules**, ask your IDE to maintain sync between both formats to keep them consistent.

## License

[License details here]

## Learning Resources

### New to Django?

**Quick Read** (20 min): [Django at a Glance](https://docs.djangoproject.com/en/stable/intro/overview/)
- Official Django overview
- Covers models, views, templates, URL routing
- Perfect primer before diving into Mimir's codebase

**Video Tutorial** (30 min): [Django For Everybody - Introduction](https://www.youtube.com/watch?v=o0XbHvKxw7Y)
- Dr. Chuck's accessible introduction
- Covers request/response cycle and MTV pattern
- From the popular "Django for Everybody" course

**Bonus Quick Reference**: [Django Cheat Sheet](https://github.com/lucrae/django-cheat-sheet)
- One-page reference for common patterns
- Models, views, templates, forms at a glance

### New to HTMX?

**Quick Read** (15 min): [HTMX Documentation - Introduction](https://htmx.org/docs/)
- Official docs covering core concepts
- AJAX requests with HTML attributes
- Swap strategies and event handling

**Video Tutorial** (25 min): [HTMX Crash Course](https://www.youtube.com/watch?v=r-GSGH2RxJs)
- Practical examples of HTMX in action
- Progressive enhancement without JavaScript
- Perfect complement to Mimir's server-side approach

**Interactive Examples** (10 min): [HTMX Examples](https://htmx.org/examples/)
- Click Delete Row, Edit Row, Infinite Scroll examples
- Shows patterns Mimir uses for CRUD operations
- Live demos you can inspect

### How Mimir Uses These Technologies

- **Django**: Custom views (no Django Forms), repository pattern, pytest testing
- **HTMX**: Partial page updates, form submissions, dynamic content loading
- **Together**: Server-rendered UI with smooth interactivity, testable without browser automation

See [docs/architecture/SAO.md](docs/architecture/SAO.md) for Mimir's specific implementation patterns.

---

## Learn More

- **Architecture**: [docs/architecture/SAO.md](docs/architecture/SAO.md) - Complete system design
- **User Journey**: [docs/features/user_journey.md](docs/features/user_journey.md) - Complete Acts 0-15 narrative with all screens
- **Feature Files**: [docs/features/](docs/features/) - 46 BDD specifications covering full CRUDLF for all entities
- **Screen Flow**: [docs/ux/2_dialogue-maps/screen-flow.drawio](docs/ux/2_dialogue-maps/screen-flow.drawio) - Visual MVP flow diagram
- **UI Guidelines**: [docs/ux/IA_guidelines.md](docs/ux/IA_guidelines.md) - Bootstrap design system, forms, validation, toasts
- **GitHub Issues**: [MVP Milestone](https://github.com/petelind/mimir/milestone/2) - Track development progress
- **MCP Protocol**: [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)

## Support

- **Issues**: [GitHub Issues](https://github.com/petelind/mimir/issues)
- **Discussions**: [GitHub Discussions](https://github.com/petelind/mimir/discussions)
- **Project Board**: [MVP Milestone](https://github.com/petelind/mimir/milestone/2)
