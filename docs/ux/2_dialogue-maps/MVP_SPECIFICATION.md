# Mimir MVP Specification - Local-Only Mode

## 🎯 MVP Objective

Enable Maria to use FOB and MCP in **standalone mode** (no Homebase) to validate core value proposition:
- Create playbooks locally
- Query playbooks via MCP in Windsurf
- Improve playbooks with PIPs
- Export/import playbooks as JSON

---

## 📊 MVP Scope

**Total Screens**: 29 (vs 87 in full system)
- **Main Screens**: 16
- **Modals**: 5
- **MCP Processing**: 4
- **Windsurf Screens**: 4

**Acts Included**: 0, 1, 4, 5, 6, 7 (Subset of full 0-9 journey)

---

## 🗺️ MVP User Flow

### **ACT 0: Local Setup (No Homebase)**
**Goal**: Pull container, create local user, skip HB connection

**Screens**:
1. `FOB-STARTUP-1` - Pull container & initialize
2. `FOB-LOCAL-USER-CREATE-1` - Create local user (no HB token field)
3. `FOB-LOCAL-SUCCESS-1` *(Modal)* - Setup complete

**Key Changes from Full Flow**:
- ❌ No `HB-AUTH-REGISTER-1` (Homebase registration)
- ❌ No `HB-AUTH-TOKEN-DISPLAY-1` (Token generation)
- ❌ No `FOB-ONBOARDING-CONNECT-1` (Token setup)
- ✅ Simplified local-only user creation

---

### **ACT 1: Configure Windsurf MCP**
**Goal**: Set up MCP server connection to Windsurf IDE

**Screens**:
1. `FOB-ONBOARDING-FIRST-RUN-1` - Welcome tour
2. `FOB-ONBOARDING-MCP-CONFIG-1` - Configure Mimir MCP
3. `FOB-ONBOARDING-MCP-COMPLETE-1` *(Modal)* - MCP ready
4. `FOB-DASHBOARD-1` - Main dashboard

**Same as Full Flow**: This act is unchanged

---

### **ACT 7: Create Playbook**
**Goal**: Create playbook via GUI (Method 1) or MCP (Method 4)

**Screens**:

**Method 1: GUI Creation**
1. `FOB-CREATE-PLAYBOOK-1` - Create new entry
2. `FOB-PLAYBOOK-WIZARD-BASIC-1` - Basic info
3. `FOB-PLAYBOOK-EDITOR-1` - Manual editor

**Method 4: MCP Creation**
4. `WINDSURF-CREATE-PLAYBOOK-1` - Create via MCP
5. `MCP-PLAYBOOK-CREATED-1` *(MCP)* - Created confirmation

**Excluded from MVP**:
- ❌ Method 2: AI-powered (import notes) - Too complex for MVP
- ❌ Method 3: Templates - Not essential
- ❌ Publishing/Family management - No Homebase

**MCP Tools Required**:
- `create_playbook` - Create new playbook structure
- `add_activity` - Add activities to playbook
- `list_activities` - List playbook activities

---

### **ACT 4: Use Playbook with MCP**
**Goal**: Query playbook context in Windsurf, open GUI via links

**Screens**:
1. `WINDSURF-CHAT-1` - Ask questions in Windsurf
2. `MCP-PLAYBOOK-CONTEXT-1` *(MCP)* - Load playbook context
3. `WINDSURF-COMMANDS-1` - Use MCP commands
4. `FOB-OPEN-PLAYBOOK-1` - Open from MCP-provided link
5. `FOB-PLAYBOOK-DETAIL-VIEW-1` - View full playbook
6. `WINDSURF-MCP-COMMANDS-LIST-1` *(MCP)* - Available commands

**Excluded from MVP**:
- ❌ External work item creation (GitHub/Jira MCP) - Not core to playbook validation

**MCP Tools Required**:
- `get_playbook_context` - Query playbook content
- `get_activity_howto` - Get activity guidance
- `list_playbooks` - List available playbooks
- `open_in_gui` - Generate localhost:8000 link
- `get_activity_details` - View specific activity

---

### **ACT 5: Submit & Approve PIPs**
**Goal**: MCP suggests improvements, Maria reviews and approves in GUI

**Screens**:
1. `WINDSURF-CHAT-PIP-SUGGEST-1` - MCP suggests PIP
2. `MCP-PIP-GENERATE-1` *(MCP)* - Generate PIP proposal
3. `MCP-PIP-ANALYZE-1` *(MCP)* - Analyze changes
4. `FOB-PIP-REVIEW-DETAIL-1` - Review PIP in GUI
5. `FOB-PIP-REVIEW-MODAL-1` *(Modal)* - PIP details modal
6. `FOB-PIP-APPROVED-1` - Approved! (v1.0 → v1.1)

**Same as Full Flow**: PIP workflow unchanged

**MCP Tools Required**:
- `suggest_pip` - Suggest playbook improvement
- `submit_pip` - Submit PIP for review
- `list_pending_pips` - View PIPs needing review
- `approve_pip` - Approve PIP (triggers version bump)

---

### **ACT 6: Export & Import (No Sync)**
**Goal**: Share playbooks via JSON dumps (no Homebase sync)

**Screens**:
1. `FOB-PLAYBOOK-EXPORT-1` - Export JSON dump
2. `FOB-PLAYBOOK-EXPORT-MODAL-1` *(Modal)* - Export options
3. `FOB-IMPORT-UPLOAD-1` - Upload JSON file
4. `FOB-IMPORT-VALIDATE-1` - Validate schema
5. `FOB-IMPORT-VALIDATE-MODAL-1` *(Modal)* - Validation result
6. `FOB-IMPORT-COMPLETE-1` - Import complete

**Key Changes from Full Flow**:
- ❌ No `FOB-SYNC-ANALYSIS-1` (HB sync)
- ❌ No `FOB-SYNC-PIP-SUBMIT-1` (Upload to HB)
- ❌ No `FOB-SYNC-CONFLICT-1` (Conflict resolution)
- ✅ Simple file-based import/export only

---

## 🚫 What's NOT in MVP

### **Excluded Acts**:
- **Act 2: Family Management** - No Homebase = No families
- **Act 3: Sync & Download** - No Homebase sync
- **Act 8-9: Settings & Errors** - Minimal settings needed for MVP

### **Excluded Screens** (from included acts):
- All Homebase-related screens (HB-*)
- All sync/conflict resolution screens
- External MCP integrations (GitHub, Jira)
- Family/community features
- Advanced settings

### **Excluded Features**:
- Homebase token management
- Multi-family membership
- Playbook approval workflows
- Community sharing
- Auto-sync
- Offline conflict resolution

---

## 📦 MVP Deliverables

### **1. Docker Container**
```bash
docker pull mimir/fob:mvp
docker run -p 8000:8000 -p 5000:5000 mimir/fob:mvp
```
- Port 8000: FOB Django GUI
- Port 5000: Mimir MCP Server

### **2. MCP Configuration**
`.windsurf/mcp_settings.json`:
```json
{
  "mcpServers": {
    "mimir": {
      "command": "docker",
      "args": ["exec", "-i", "mimir-fob", "python", "/app/mcp/server.py"],
      "env": {}
    }
  }
}
```

### **3. FOB GUI Routes**
- `/` - Dashboard
- `/auth/local-register/` - Local user creation
- `/onboarding/mcp/` - MCP configuration
- `/playbooks/` - Playbook list
- `/playbooks/create/` - Create playbook
- `/playbooks/<id>/` - Playbook detail
- `/playbooks/<id>/edit/` - Edit playbook
- `/pips/` - PIP list
- `/pips/<id>/` - PIP detail
- `/import/` - Import JSON
- `/export/<playbook_id>/` - Export JSON

### **4. MCP Tools**
**Playbook Management**:
- `create_playbook` - Create new playbook
- `list_playbooks` - List all playbooks
- `get_playbook_context` - Get playbook content
- `open_in_gui` - Generate localhost link

**Activity Management**:
- `add_activity` - Add activity to playbook
- `list_activities` - List playbook activities
- `get_activity_details` - Get activity details
- `get_activity_howto` - Get activity guidance

**PIP Management**:
- `suggest_pip` - Suggest improvement
- `submit_pip` - Submit PIP
- `list_pending_pips` - List PIPs
- `approve_pip` - Approve PIP

---

## ✅ MVP Success Criteria

1. ✅ Maria can pull and run container with single command
2. ✅ Maria can create local user without Homebase
3. ✅ Maria can configure Windsurf MCP
4. ✅ Maria can create playbook via GUI or MCP
5. ✅ Maria can query playbooks in Windsurf
6. ✅ Maria can click MCP-provided links to open GUI
7. ✅ MCP can suggest PIPs based on usage
8. ✅ Maria can review and approve PIPs in GUI
9. ✅ Playbook versions increment (v1.0 → v1.1)
10. ✅ Maria can export playbook as JSON
11. ✅ Maria can import playbook from JSON

---

## 🚀 Post-MVP Roadmap

### **Phase 2: Add Homebase (Acts 2-3, 6 full)**
- Homebase registration & token management
- Family browsing & joining
- Sync with Homebase
- Download shared playbooks
- Upload PIPs to Homebase
- Conflict resolution

### **Phase 3: Community Features (Act 2 full)**
- Create families
- Family admin dashboard
- Submit playbooks to families
- Playbook approval workflows
- Family settings

### **Phase 4: Advanced Features (Acts 8-9)**
- Advanced settings
- Error recovery flows
- Storage management
- Notification preferences
- Comprehensive error handling

---

## 📐 MVP Architecture

### **Component Stack**:
```
┌─────────────────┐
│  Windsurf IDE   │
└────────┬────────┘
         │ MCP Protocol
         ▼
┌─────────────────┐
│ Mimir MCP Server│ (Port 5000)
└────────┬────────┘
         │ HTTP API
         ▼
┌─────────────────┐
│  FOB Django GUI │ (Port 8000)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL DB  │ (Local SQLite for MVP)
└─────────────────┘
```

### **Data Model** (Simplified for MVP):
- **User**: Local-only (no HB_token)
- **Playbook**: Activities, PIPs, version
- **Activity**: Name, description, how-to
- **PIP**: Proposed changes, status, version
- **No Family/Membership models** (MVP)

---

## 📝 MVP Implementation Order

### **Sprint 1: Foundation (Week 1)**
1. Docker container setup
2. Django project + PostgreSQL
3. Local user model & auth
4. Basic routing structure

### **Sprint 2: Playbook CRUD (Week 2)**
5. Playbook model
6. Activity model
7. FOB GUI: List, create, detail, edit
8. JSON export/import

### **Sprint 3: MCP Integration (Week 3)**
9. MCP server setup
10. Playbook context tools
11. Activity query tools
12. GUI link generation

### **Sprint 4: PIP Workflow (Week 4)**
13. PIP model
14. PIP submission flow
15. MCP PIP suggestion
16. PIP approval + versioning

### **Sprint 5: Polish & Testing (Week 5)**
17. E2E testing
18. UX polish
19. Documentation
20. MVP release

---

## 🎬 MVP Demo Script

1. **Pull & Start**: `docker run -p 8000:8000 -p 5000:5000 mimir/fob:mvp`
2. **Create User**: Visit http://localhost:8000, create "maria@example.com"
3. **Configure MCP**: Follow onboarding, set up Windsurf MCP
4. **Create Playbook**: Create "Frontend Testing" playbook via GUI
5. **Use in Windsurf**: Ask "What's in Frontend Testing playbook?"
6. **Follow Link**: Click MCP-provided link to open GUI view
7. **Get Guidance**: Ask "How do I run E2E tests?"
8. **Suggest PIP**: MCP suggests "Add Playwright example"
9. **Review PIP**: Open PIP in GUI, review changes
10. **Approve**: Click approve, see v1.0 → v1.1
11. **Export**: Export playbook as JSON file
12. **Share**: Send JSON to colleague
13. **Import**: Colleague imports JSON into their FOB

**Result**: Full local workflow validated! Ready for Homebase integration.
