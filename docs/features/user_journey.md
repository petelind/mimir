# Mimir User Journey

## Personas

**Mike Chen** - Homebase Administrator  
Senior developer at a tech community. Maintains shared playbooks for common development patterns to help the community adopt best practices.

**Maria Rodriguez** - UX Consultant  
Runs an independent UX consulting practice. Needs to organize her personal workflows, collaborate with her team, and leverage community methodologies.

---

---

## System Architecture Note

**Homebase (HB)**: Central server with two interfaces:
- **HB Django Admin**: System administrator functions (approvals, user management) - uses standard Django Admin interface
- **HB Web Interface**: Public-facing registration and information pages

**FOB (Forward Operating Base)**: Local containerized application with:
- **FOB Web GUI**: Custom Django application with full UI for playbook and family management
- **Mimir MCP Server**: Provides playbook context, guidance, and PIP suggestions to AI assistants in Windsurf
- **FOB Database**: Local PostgreSQL with playbook graph storage
- **HB Connection**: Optional token-based authentication to sync with Homebase
  - Can operate standalone (local-only) or connected to one HB
  - Django DRF token issued upon HB registration
  - Token can be added, changed, or removed in FOB Settings
  - **Limitation**: Only one Homebase connection supported per FOB

**External Integrations**:
- **Work Item Management**: Handled by external 3rd party MCP servers (GitHub MCP, Jira MCP, GitLab MCP, etc.)
- **Note**: Mimir MCP provides playbook context; external MCPs handle work item creation/tracking

**Domain Model Notes**:
- **7 Core Entities**: Playbook, Workflow, Phase, Activity, Artifact, Role, Howto
- **Phase is OPTIONAL**: Workflows MAY contain Phases for grouping Activities, but Phase is not required. A Workflow can organize Activities with or without Phase grouping.
- **Artifact**: Formerly called "Deliverable" in some contexts. Use "Artifact" consistently for outputs produced by Activities.

---

## ⚠️ Critical Architectural Principle

**Playbooks Are STATIC Reference Material (Like a Book)**

- **Mimir playbooks** = Documentation and guidance ONLY
  - Show activity structure, descriptions, best practices
  - NO work item tracking, NO status indicators, NO checkmarks
  - Think of them as reference books or documentation wiki pages

- **Work item tracking** = Happens ONLY in external systems
  - GitHub Issues, Jira Tickets, Atlassian boards
  - Status, progress, assignments managed there
  - Actual work execution tracked there

- **AI/MCP integration** = Cross-references between the two
  - Reads static playbook from Mimir: "Activity 1: Setup Project - install dependencies, configure environment"
  - Reads live status from GitHub: "Issue #47: Setup React project - Status: Closed"
  - Provides combined context: "According to the playbook, Activity 1 covers setup. GitHub shows issue #47 for this work is complete."

**Example**:
- **FOB displays**: "Activity 1: Setup Project" with rich Markdown guidance (static)
- **GitHub displays**: "Issue #47: Setup React project structure - Closed on Nov 15" (live tracking)
- **AI combines**: "Per the React Frontend Development playbook, you need to set up the project. GitHub issue #47 shows this work is complete."

**This separation ensures**:
- Playbooks remain reusable across projects and teams
- Work tracking stays in familiar developer tools
- No duplicate tracking systems

---

## Journey: From Discovery to Contribution

### Act 0: System Entry & Authentication

**Context**: Users need to access the system. FOB and HB have separate authentication flows.

**Background**: Mike previously registered on Homebase and received his Django DRF authentication token (`mimir_x7k9m2...`). As a system administrator, he primarily works through the Django Admin interface on HB and doesn't need a FOB instance.

#### Screen: HB Login Page
Mike navigates to Homebase login at `https://homebase.mimir.io/login`:
- Email field
- Password field
- "Remember me" checkbox
- "Forgot password?" link
- "Sign up" link (→ Registration, generates token upon email verification)
- "Login" button

Mike enters credentials and clicks Login.

#### Screen: HB Django Admin Dashboard (System Admin View)
Mike (system admin) sees standard Django Admin interface:
- Django Admin navigation sidebar
- Recent actions log
- Quick links to models:
  - Users
  - Families
  - Playbooks (pending approval)
  - Notifications
- System health indicators

**Note**: This is Django's built-in admin interface, not custom UI.

#### Screen: FOB Login/Startup
Maria's FOB container starts automatically with her dev environment:
- Container initialization screen
- FOB authentication:
  - If first time: Setup wizard (covered in Act 1)
  - If returning: Automatic login with stored credentials
- Database connection check
- MCP server status: ✓ Running

#### Error Path: FOB Connection Failed
If FOB can't reach Homebase:
- Error modal: "Cannot connect to Homebase"
- Options:
  - "Retry Connection"
  - "Work Offline" (limited features)
  - "Check Connection Settings"

---

### Act 0.1: The Foundation (Mike's Setup)

**Context**: Mike wants to share his React development methodology with the community.

#### Screen: HB Admin Dashboard
Mike logs into the Homebase admin interface. He sees the main dashboard with playbook management tools and family administration.

#### Screen: HB Create Playbook Wizard
Mike clicks "Create New Playbook" and enters:
- **Name**: "React Frontend Development"
- **Description**: "Component architecture, state management, and testing patterns"
- **Category**: Development

#### Screen: HB Playbook Editor
Mike uses the visual editor to structure his playbook:
- Adds Activities: "Setup Project", "Create Components", "Implement State Management"
- Adds Artifacts: "Component Library", "State Diagram", "Test Suite"
- Links Activities with dependencies (upstream/downstream relationships)

#### Screen: HB Family Assignment
Mike assigns the playbook to the "Usability" family:
- Selects "Usability" from family dropdown
- Sets visibility to "Public" (anyone in family can access)
- Clicks "Publish"

#### Screen: HB Pending Approval
After publishing, Mike sees:
- Status: "Pending Admin Approval"
- Message: "Your playbook has been submitted for review by Homebase administrators"

#### Django Admin: HB Playbook Approval (System Administrator)
Sarah, the Homebase system administrator, receives a notification in Django Admin:
- Navigates to **Django Admin → Playbooks → Pending Approvals**
- Sees list view with pending playbooks
- Clicks on "React Frontend Development" playbook
- Django Admin detail view shows:
  - Playbook structure, description, target family
  - Author information
  - Submission timestamp
- Actions dropdown: "Approve", "Reject", "Request Changes"
- Selects "Approve" and saves

#### Screen: HB Playbook Activated
Mike receives notification:
- "Your playbook 'React Frontend Development' has been approved"
- Status: "Active in Usability family"

**Result**: The playbook is now available to all members of the Usability family.

---

### Act 1: Maria's Onboarding

**Context**: Maria heard about Mimir and wants to try it for her UX practice.

#### Screen: HB Registration Page
Maria navigates to Mimir's registration page on Homebase and fills out the form:
- Email: maria@uxconsulting.com
- Password: (creates secure password)
- Full Name: Maria Rodriguez
- Clicks "Register"

#### Screen: HB Email Verification
Maria receives a verification email and clicks the confirmation link. She's redirected back to Homebase.

#### Screen: HB Registration Success - Authentication Token
After email verification, Maria sees her account details page:
- **Congratulations!** Your Mimir account is active.
- **Your Authentication Token** (copy button):
  ```
  Token: mimir_a8f3d9e2b1c4567890abcdef12345678
  ```
- **Important**: Save this token securely. You'll need it to connect your FOB to Homebase.
- **Homebase URL**: `https://homebase.mimir.io`
- Options:
  - "Download FOB Setup Guide" (PDF with token and URL)
  - "Regenerate Token" (invalidates old token)
  - "Continue to FOB Setup"

**Note**: This Django DRF token authenticates FOB to HB for sync operations.

#### Screen: HB/FOB Setup Wizard
After saving her token, Maria is guided through FOB (local workspace) setup:
- Downloads FOB container image (Docker-based Mimir container)
- Container includes:
  - Django web application (FOB GUI)
  - PostgreSQL database (local playbook graph storage)
  - Mimir MCP server (provides playbook context to AI assistants)
- Maria configures the container in Windsurf as a dev container
- Configures local storage volume mount

#### Screen: FOB First Launch - Homebase Connection (Optional)
FOB starts and shows connection configuration:
- **Connect to Homebase** (Optional)
  - Homebase URL: [https://homebase.mimir.io]
  - Authentication Token: [paste token here]
  - "Test Connection" button
- **Or skip this step**:
  - "Skip - Work Locally" button
  - Note: "You can always add Homebase connection later in Settings. Without HB connection, you won't be able to sync playbooks from families."

Maria pastes her token and clicks "Test Connection":
- ✓ Connection successful
- Shows her account: maria@uxconsulting.com
- "Continue" button

#### Screen: FOB Sync Preferences
After connecting to Homebase:
- Sets sync preferences (manual vs. notification-based)
- Configures auto-sync settings

#### Screen: FOB External MCP Configuration
Maria **separately configures external MCP servers in Windsurf**:
- GitHub MCP for work item management
- (Optional: Jira MCP, GitLab MCP, etc.)

**Result**: Maria now has a working FOB connected to Homebase with token-based authentication.

---

### Act 1.5: FOB Navigation Structure

**Context**: Understanding the persistent navigation and UI structure of FOB.

#### Screen: FOB Main Interface Layout
Maria's FOB web GUI (http://localhost:8000) has a consistent layout:

**Top Navigation Bar** (persistent across all screens):
- **Logo**: "Mimir FOB" (links to Dashboard)
- **Connection Status**: 
  - If connected to HB: Green indicator "✓ Connected to Homebase"
  - If local only: Gray indicator "⊝ Local FOB" with tooltip "Not connected to Homebase. Sync disabled."
- **Search**: Global search bar (playbooks, families, activities)
- **Navigation Menu**:
  - Dashboard
  - Playbooks (with count badge)
  - Families (with count badge)
  - Sync (disabled if no HB connection)
  - Settings
- **Notifications**: Bell icon with badge count (unread notifications)
- **User Menu**: Maria Rodriguez dropdown
  - My Profile
  - Account Settings
  - Homebase Connection (manage token)
  - Log Out

**Left Sidebar** (contextual, shown on detail pages):
- Quick links based on current context
- Recently viewed playbooks
- Active playbook indicator

#### Screen: FOB Notification Center
Maria clicks the bell icon (badge shows "3"):
- Dropdown panel appears:
  - "New user wants to join UX family" (12 min ago) [View Request]
  - "React Frontend Development v1.2 available" (2 hours ago) [Download]
  - "Tom joined Usability family" (1 day ago) [Dismiss]
- "Mark all as read" button
- "View all notifications" link → Full notification page

#### Screen: FOB Notifications (Full View)
Clicking "View all notifications" opens dedicated page:
- Tabs: "All", "Pending Actions", "Updates", "Mentions"
- Filterable list of all notifications
- Each notification has:
  - Icon (family, playbook, sync, error, etc.)
  - Message
  - Timestamp
  - Action buttons (context-specific)
  - Dismiss button

#### Screen: FOB Global Search
Maria types "React" in search bar:
- Live dropdown suggestions appear:
  - **Playbooks** (2):
    - React Frontend Development (Usability)
    - React Testing Patterns (Archived)
  - **Activities** (5):
    - Setup React Project
    - Create React Components
    - ...
  - **Families** (0)
- "See all results" link → Full search results page

#### Screen: FOB Search Results
Full search page with filters:
- **Left sidebar filters**:
  - Type: Playbooks, Activities, Artifacts, Goals, Families
  - Status: Active, Disabled, Archived
  - Source: Local, Downloaded, Owned
- **Results list** with relevance ranking
- **Empty state**: "No results found" with suggestions

---

### Act 2: PLAYBOOKS - Complete CRUDLF

**Context**: After onboarding, Maria needs to manage playbooks - the top-level container for methodologies. She can create her own, view downloaded ones, edit them, and delete obsolete ones.

**Pattern**: Playbook follows the standard CRUDLF pattern with LIST+FIND as the entry point.

#### Screen: FOB-PLAYBOOKS-LIST+FIND-1

Maria clicks "Playbooks" in the main navigation. The playbooks list page appears (this is the entry point for all playbook operations, marked with bold border in flow diagrams):

**Layout**:
- **Header**: "Playbooks" with count badge (e.g., "Playbooks (3)")
- **Top Actions**:
  - [Create New Playbook] button (primary action, bold blue)
  - [Import from JSON] button
  - [Sync with Homebase] button (if connected)
- **Search & Filter Section**:
  - Search box: "Find playbooks..." (searches name, description, author)
  - Filters: Status (Active/Disabled), Source (Local/Downloaded/Owned), Category dropdown
  - [Clear Filters] button
- **Playbooks Table** with columns:
  - Name | Description | Author | Version | Status | Last Modified | Actions
  - Sort by any column
- **Row Actions** (dropdown menu per playbook):
  - [View] - Opens FOB-PLAYBOOKS-VIEW_PLAYBOOK
  - [Edit] - Opens FOB-PLAYBOOKS-EDIT_PLAYBOOK  
  - [Delete] - Opens FOB-PLAYBOOKS-DELETE_PLAYBOOK modal
  - [Export JSON] - (only for authored playbooks)
  - [...More] - Additional actions
- **Empty State** (if no playbooks):
  - Illustration: Empty bookshelf
  - "No playbooks yet"
  - "Create your first playbook, download from Homebase, or import from JSON"
  - [Create Playbook] [Browse Families] [Import JSON] buttons
- **Pagination**: Shows 20 per page with page controls

**Example Data**:
- "React Frontend Development" | Mike Chen | v1.2 | Active | Downloaded
- "UX Research Methodology" | Maria Rodriguez | v2.1 | Active | Owned
- "Design System Patterns" | Community | v1.0 | Disabled | Downloaded

Maria sees her existing playbooks and can search/filter to find specific ones.

---

#### Screen: FOB-PLAYBOOKS-CREATE_PLAYBOOK-1

Maria clicks [Create New Playbook]. The creation wizard opens:

**Wizard Step 1: Basic Information**
- **Name**: Text input (required)
  - Example: "Product Discovery Framework"
  - Validation: Unique name, 3-100 characters
- **Description**: Textarea (required)
  - Example: "Comprehensive methodology for discovering and validating product opportunities"
  - Validation: 10-500 characters
- **Category**: Dropdown (required)
  - Options: Design, Development, Research, Management, Product, Other
- **Tags**: Multi-select/token input (optional)
  - Example: "product management, discovery, validation, user research"
- **Visibility**: Radio buttons
  - ○ Private (only me)
  - ○ Family (select family from dropdown)
  - ○ Local only (not uploaded to Homebase)
- [Cancel] [Next: Add Workflows →] buttons

**Wizard Step 2: Add Workflows** (optional first workflow)
- "You can add workflows now or later"
- [Skip for Now] [Add First Workflow] buttons
- If Add First Workflow clicked:
  - Quick workflow creation inline
  - Workflow name and description fields
  - [Add Workflow] [Cancel] buttons

**Wizard Step 3: Publishing Settings**
- **Status**: Radio buttons
  - ● Active (ready to use)
  - ○ Draft (work in progress)
- **Initial Version**: Auto-set to v1.0
- Review summary of playbook being created
- [Cancel] [Create Playbook] buttons

**Success Flow**:
- Playbook created in local FOB
- Success notification: "Playbook 'Product Discovery Framework' created successfully"
- Redirects to FOB-PLAYBOOKS-VIEW_PLAYBOOK-1 for the new playbook
- New playbook appears in FOB-PLAYBOOKS-LIST+FIND-1

**Error Handling**:
- Duplicate name: "A playbook with this name already exists. Please choose a different name."
- Validation errors highlighted inline with red borders and error messages
- [Fix Errors] to return to form

---

#### Screen: FOB-PLAYBOOKS-VIEW_PLAYBOOK-1

Maria clicks [View] on "React Frontend Development" from the list. The detail view opens:

**Layout**:
- **Header**:
  - Playbook name: "React Frontend Development" (h1)
  - Version badge: v1.2
  - Status badge: Active (green) / Disabled (gray) / Draft (yellow)
  - Author: Mike Chen (Usability family)
  - Last modified: 2 weeks ago
- **Top Actions**:
  - [Edit] button (if editable - owned or local)
  - [Delete] button (if owned)
  - [Export JSON] button (if authored)
  - [Duplicate] button
  - [Disable]/[Enable] toggle
  - [...More] dropdown

**Tabs**:
1. **Overview Tab** (default):
   - **Description**: Full playbook description
   - **Quick Stats Card**:
     - Workflows: 3
     - Phases: 8 (optional, may show "N/A" if workflow doesn't use phases)
     - Activities: 24
     - Artifacts: 12
     - Roles: 5
     - Howtos: 24
     - Goals: 6 (note: Goal deferred to v2.1, shows "Coming soon")
   - **Metadata**:
     - Category: Development
     - Tags: react, frontend, component-architecture
     - Created: 3 months ago
     - Source: Downloaded from Usability family
   - **Workflows Section**:
     - List of workflows in this playbook
     - Each workflow shows: Name, Description, Activity count
     - [View Workflow] link for each → jumps to ACT 3: WORKFLOWS

2. **Workflows Tab**:
   - Full list of workflows with filtering
   - Workflow dependency visualization (if any)
   - [Add Workflow] button (if editable)

3. **History Tab**:
   - Version timeline: v1.0, v1.1, v1.2
   - Each version shows:
     - Version number, Date, Author, Change summary
     - [View This Version] [Compare with Current] buttons
   - PIP history (proposals that led to new versions)

4. **Settings Tab** (if owned):
   - Visibility settings
   - Publishing settings
   - Sharing options
   - [Transfer Ownership] button

**Version Comparison View** (if clicked from History):
- Split-pane diff viewer
- Left: Selected version | Right: Current version
- Highlighting: Added (green), Removed (red), Modified (yellow)
- Shows differences in workflows, activities, artifacts

**Navigation**:
- [Back to Playbooks List] link at top
- Breadcrumb: Playbooks > React Frontend Development > Overview

Maria can explore the complete playbook structure, drill into workflows, view version history, and understand the methodology comprehensively.

---

#### Screen: FOB-PLAYBOOKS-EDIT_PLAYBOOK-1

Maria clicks [Edit] on her "Product Discovery Framework" playbook. The edit form opens:

**Form Layout** (similar to CREATE wizard but single page):
- **Basic Information Section**:
  - Name: Pre-populated, editable
  - Description: Pre-populated, editable textarea
  - Category: Pre-populated dropdown
  - Tags: Pre-populated multi-select
  - Visibility: Pre-populated radio buttons
    - Note: "Changing visibility from Family to Private will recall from family members"

- **Status Section**:
  - Current Status: Active/Disabled/Draft radio buttons
  - Version: v1.0 (read-only, changes via PIPs create new versions)

- **Workflows Section**:
  - List of current workflows
  - [Edit Workflow] [Remove Workflow] buttons per workflow
  - [Add New Workflow] button
  - Note: "Removing a workflow will delete all its phases, activities, and downstream entities"

- **Conflict Detection**:
  - If playbook was modified remotely (synced from HB):
    - Warning banner: "Remote version v1.3 available. Your local version is v1.2."
    - [Review Changes] [Override with Local] [Discard Local Changes] options

**Validation**:
- Same validation as CREATE
- Additional check: Cannot remove last workflow if playbook is Active
- Warn if removing workflows that have work items linked (via external MCP)

**Actions**:
- [Cancel] - Returns to VIEW without saving, confirmation if changes made
- [Save as Draft] - Saves but keeps in Draft status
- [Save Changes] - Saves and keeps current status
  - For published playbooks: "Save will create local v1.1. Sync to submit as PIP."

**Success Flow**:
- Changes saved
- Success notification: "Playbook updated successfully"
- If visibility changed: Additional notification about impact
- Returns to FOB-PLAYBOOKS-VIEW_PLAYBOOK-1
- Updated data visible in FOB-PLAYBOOKS-LIST+FIND-1

**Permission Handling**:
- Downloaded playbooks (not owned): Edit button disabled or opens read-only view
- Tooltip: "You cannot edit playbooks from other authors. Create a local copy or submit a PIP."
- [Create Local Copy] button offered as alternative

---

#### Screen: FOB-PLAYBOOKS-DELETE_PLAYBOOK-1 (Confirmation Modal)

Maria clicks [Delete] on an old "Test Playbook 123" she no longer needs. A confirmation modal appears:

**Modal Layout**:
- **Title**: "Delete Playbook?"
- **Icon**: Warning triangle (red)
- **Playbook Info**:
  - Name: "Test Playbook 123"
  - Version: v1.0
  - Author: Maria Rodriguez
  - Created: 2 weeks ago

**Impact Statement**:
"This will permanently delete:"
- ✗ 2 Workflows
- ✗ 0 Phases (if phases exist, shows count)
- ✗ 8 Activities
- ✗ 5 Artifacts
- ✗ 3 Roles
- ✗ 8 Howtos
- ✗ All version history

**Warnings**:
- "This action cannot be undone"
- If playbook has external work items linked:
  - Warning: "This playbook has 3 GitHub issues linked. Work items will remain but lose playbook context."
- If playbook is published to family:
  - Warning: "This playbook is shared with UX family (12 members). Family members will lose access on next sync."

**Confirmation**:
- Checkbox: ☐ "I understand this will permanently delete the playbook and all related content"
- Text input: "Type the playbook name to confirm" (must match exactly)
  - Placeholder: "Test Playbook 123"

**Actions**:
- [Cancel] - Closes modal, no changes
- [Delete Playbook] - Disabled until checkbox checked and name entered correctly
  - Button turns red when enabled
  - Final confirmation: "Are you absolutely sure?" (if high-impact)

**Success Flow**:
- Playbook and all related entities deleted from local graph
- Success notification: "Playbook 'Test Playbook 123' deleted"
- Modal closes
- Returns to FOB-PLAYBOOKS-LIST+FIND-1
- Deleted playbook no longer in list
- If was published: Notification sent to Homebase for family recall

**Special Cases**:
- **Cannot Delete Downloaded Playbooks**: Modal shows:
  - "You cannot delete playbooks from other authors"
  - "Instead, you can Disable this playbook to hide it from your views"
  - [Disable Playbook] [Cancel] buttons
- **Delete Draft**: Simpler confirmation, less dramatic warnings

Maria confirms deletion by typing the name and checking the box. The playbook and all its contents are permanently removed.

---

**Act 2 Summary**: Maria can now perform complete CRUDLF operations on Playbooks:
- ✅ **LIST+FIND**: Browse, search, and filter all playbooks
- ✅ **CREATE**: Create new playbooks with wizard guidance
- ✅ **VIEW**: Explore playbook details, workflows, and history
- ✅ **EDIT**: Update playbook metadata, workflows, and settings
- ✅ **DELETE**: Remove playbooks with full impact warnings

**Navigation Flow**: Dashboard → Playbooks LIST+FIND (entry point) → Individual operations (CREATE/VIEW/EDIT/DELETE) → Back to LIST+FIND

**Next**: Maria proceeds to manage Workflows within her playbooks (ACT 3).

---

### Act 3: WORKFLOWS - Complete CRUDLF

**Context**: Within a playbook, Maria needs to manage workflows - the execution sequences that contain activities. A playbook typically has multiple workflows representing different paths or phases of the methodology.

**Pattern**: Workflow follows standard CRUDLF with LIST+FIND as entry point. Workflows are always scoped within a parent playbook.

**Important Note**: Workflows MAY optionally contain Phases for grouping Activities, but Phases are not required. See Act 4 for Phase management.

#### Screen: FOB-WORKFLOWS-LIST+FIND-1

From FOB-PLAYBOOKS-VIEW_PLAYBOOK-1, Maria clicks on the "Workflows" tab or [View Workflows] button. The workflows list appears:

**Layout**:
- **Breadcrumb**: Playbooks > React Frontend Development > Workflows
- **Header**: "Workflows in React Frontend Development" with count (e.g., "3 workflows")
- **Context Banner**: Shows parent playbook info (name, version, author)
- **Top Actions**:
  - [Create New Workflow] button (primary)
  - [Import Workflow from Template] button
  - [Reorder Workflows] button (drag-and-drop mode)
- **Search & Filter**:
  - Search: "Find workflows..."
  - Filter by: Has Phases (Yes/No), Activity count range, Status
- **Workflows Table**:
  - Name | Description | Activities | Phases | Order | Actions
  - Drag handle for reordering
- **Row Actions**:
  - [View] → FOB-WORKFLOWS-VIEW_WORKFLOW
  - [Edit] → FOB-WORKFLOWS-EDIT_WORKFLOW
  - [Delete] → FOB-WORKFLOWS-DELETE_WORKFLOW modal
  - [Duplicate] 
  - [...More]
- **Empty State**:
  - "No workflows yet"
  - "Create your first workflow to organize activities"
  - [Create Workflow] button

**Example Data**:
- "Component Development" | 8 Activities | 2 Phases | Order: 1
- "State Management Setup" | 6 Activities | 0 Phases | Order: 2
- "Testing & Documentation" | 10 Activities | 3 Phases | Order: 3

**Visualization Toggle**:
- [List View] / [Flow View] toggle
- Flow View shows workflows as connected boxes with activity counts

Maria sees all workflows in the playbook and their structure.

---

#### Screen: FOB-WORKFLOWS-CREATE_WORKFLOW-1

Maria clicks [Create New Workflow]. Creation form opens:

**Form Fields**:
- **Name**: Text input (required)
  - Example: "Design System Integration"
  - Validation: Unique within playbook, 3-100 chars
- **Description**: Textarea (required)
  - Example: "Integrate design tokens and component library into the React application"
  - 10-500 chars
- **Parent Playbook**: Read-only display (already scoped)
  - Shows: "React Frontend Development v1.2"
- **Order/Sequence**: Number input or "Add to end" checkbox
  - Default: Adds after last workflow
  - Can specify position: 1, 2, 3, etc.
- **Phase Organization**: Radio buttons
  - ○ No phases (Activities directly in workflow)
  - ○ Use phases (Group activities into phases)
  - Tooltip: "Phases are optional. Use them to organize activities into logical groups or stages."
- **Initial Setup** (collapsible section):
  - "Add first activity now?" checkbox
  - If checked: Quick activity creation fields appear
  - [Skip - Add Activities Later] option

**Actions**:
- [Cancel] [Create Workflow]

**Success Flow**:
- Workflow created within playbook
- Success notification: "Workflow 'Design System Integration' created in React Frontend Development"
- Redirects to FOB-WORKFLOWS-VIEW_WORKFLOW-1
- New workflow appears in FOB-WORKFLOWS-LIST+FIND-1 at specified order

**Validation**:
- Duplicate name within playbook: Error message
- If "Use phases" selected: Note shown that phases can be added in edit view

---

#### Screen: FOB-WORKFLOWS-VIEW_WORKFLOW-1

Maria clicks [View] on "Component Development" workflow. Detail view opens:

**Layout**:
- **Breadcrumb**: Playbooks > React Frontend Development > Workflows > Component Development
- **Header**:
  - Workflow name: "Component Development"
  - Parent playbook badge with link
  - Order badge: "#1 of 3"
- **Top Actions**:
  - [Edit Workflow]
  - [Delete Workflow]
  - [Duplicate]
  - [Reorder] (move up/down)
  - [...More]

**Tabs**:

1. **Overview Tab**:
   - **Description**: Full workflow description
   - **Stats**:
     - Activities: 8
     - Phases: 2 (or "No phases used")
     - Estimated effort: Calculated from activities
   - **Phase Summary** (if using phases):
     - Phase 1: "Foundation" (3 activities)
     - Phase 2: "Implementation" (5 activities)
     - Note: "Phases are optional groupings. Activities can be reorganized without phases."
   - **Activities Summary**:
     - List of activities in execution order
     - Shows dependencies (upstream/downstream)
     - [View Full Activity List] → jumps to Activities tab

2. **Activities Tab**:
   - Full activity list with filtering
   - Grouped by phase (if using phases) or flat list
   - Activity dependency graph visualization
   - [Add Activity] button → jumps to ACT 5: ACTIVITIES-CREATE
   - [Manage Phases] button (if using phases) → jumps to ACT 4: PHASES

3. **Dependencies Tab**:
   - Visual DAG (Directed Acyclic Graph) of activity dependencies
   - Shows upstream/downstream relationships
   - Identifies critical path
   - Warns about circular dependencies (validation error)

4. **Structure Tab** (if using phases):
   - Phase breakdown with activities per phase
   - [Reorganize Phases] button
   - [Convert to Non-Phased] button (warning: removes phase groupings)

**Navigation**:
- [Back to Workflows] → returns to LIST+FIND
- [View Parent Playbook] → FOB-PLAYBOOKS-VIEW_PLAYBOOK
- Quick links to activities and phases

Maria can explore the workflow structure, see activity organization, and understand execution flow.

---

#### Screen: FOB-WORKFLOWS-EDIT_WORKFLOW-1

Maria clicks [Edit Workflow]. Edit form opens:

**Form Layout**:
- **Basic Info Section**:
  - Name: Editable
  - Description: Editable textarea
  - Order: Number input with [Move Up] [Move Down] buttons
  
- **Phase Organization Section**:
  - Current: "Uses 2 phases" or "No phases"
  - [Change Phase Structure] button opens modal:
    - Convert to phased/non-phased
    - Warning: "This will reorganize activities"
    - [Cancel] [Convert] buttons

- **Activities Section**:
  - List of activities in this workflow
  - Drag-and-drop reordering
  - [Add Activity] [Remove Activity] per row
  - Shows activity dependencies
  - Warning if removing activity with dependencies

- **Phases Section** (if using phases):
  - List of phases with activity counts
  - [Add Phase] [Edit Phase] [Remove Phase] buttons
  - [Manage Phases] → jumps to ACT 4: PHASES-LIST+FIND

**Validation**:
- Cannot remove all activities from an active workflow
- Cannot create circular dependencies
- Warning if reordering breaks logical flow

**Actions**:
- [Cancel] [Save Changes]

**Success Flow**:
- Workflow updated
- Success notification: "Workflow updated successfully"
- Returns to FOB-WORKFLOWS-VIEW_WORKFLOW-1
- Changes reflected in FOB-WORKFLOWS-LIST+FIND-1

---

#### Screen: FOB-WORKFLOWS-DELETE_WORKFLOW-1 (Confirmation Modal)

Maria clicks [Delete] on an obsolete workflow. Confirmation modal appears:

**Modal Layout**:
- **Title**: "Delete Workflow?"
- **Workflow Info**: "Component Development" in "React Frontend Development"
- **Impact Statement**:
  "This will permanently delete:"
  - ✗ 8 Activities
  - ✗ 2 Phases (if applicable)
  - ✗ 12 Artifacts (produced by activities)
  - ✗ 8 Howtos (activity guides)
  - ✗ All activity dependencies

**Warnings**:
- "This action cannot be undone"
- "Parent playbook will be updated to v1.1 (local)"
- If workflow has activities with work items:
  - "5 GitHub issues are linked to activities in this workflow"

**Confirmation**:
- Checkbox: "I understand this will delete all activities and related content"
- Type workflow name to confirm

**Actions**:
- [Cancel] [Delete Workflow]

**Success Flow**:
- Workflow and all activities/phases/artifacts deleted
- Success notification: "Workflow 'Component Development' deleted"
- Returns to FOB-WORKFLOWS-LIST+FIND-1
- Remaining workflows reordered automatically

Maria confirms and the workflow is removed from the playbook.

---

**Act 3 Summary**: Maria can now manage workflows:
- ✅ **LIST+FIND**: Browse workflows within a playbook
- ✅ **CREATE**: Create new workflows with optional phase organization
- ✅ **VIEW**: Explore workflow structure, activities, and dependencies
- ✅ **EDIT**: Update workflow details, reorder, manage activities
- ✅ **DELETE**: Remove workflows with impact warnings

**Key Point**: Workflows MAY use Phases for grouping, but Phases are optional (see Act 4).

**Next**: Maria can optionally organize workflow activities into Phases (ACT 4).

---

### Act 4: PHASES - Complete CRUDLF ⚠️ **OPTIONAL ENTITY**

**Context**: Phases are OPTIONAL groupings for activities within workflows. Maria can choose to use phases for organizing complex workflows into stages, or she can manage activities directly without phases. Not all workflows need phases.

**Pattern**: Standard CRUDLF, but with prominent "OPTIONAL" messaging throughout.

**⚠️ IMPORTANT NOTE**: Phase is an OPTIONAL entity. Workflows function perfectly without phases. Use phases only when logical grouping adds value to your workflow organization.

#### Screen: FOB-PHASES-LIST+FIND-1

From FOB-WORKFLOWS-VIEW_WORKFLOW-1, if workflow uses phases, Maria clicks [Manage Phases]. The phases list appears:

**Layout**:
- **Breadcrumb**: Playbooks > React Frontend > Workflows > Component Development > Phases
- **Header**: "Phases in Component Development workflow"
- **Optional Badge**: Prominent yellow badge: "⚠️ OPTIONAL FEATURE - Phases are not required"
- **Info Banner**:  
  "Phases are optional groupings for activities. Your workflow can function without phases. Use phases to organize activities into logical stages if it helps your methodology."
- **Top Actions**:
  - [Create New Phase] button
  - [Remove All Phases] button (converts workflow to non-phased)
  - [Reorder Phases] (drag-and-drop)
- **Phases Table**:
  - Name | Description | Activities | Order | Actions
  - Drag handles for reordering
- **Row Actions**:
  - [View] → FOB-PHASES-VIEW_PHASE
  - [Edit] → FOB-PHASES-EDIT_PHASE
  - [Delete] → FOB-PHASES-DELETE_PHASE
  - [Move Activities to Other Phase]
- **Empty State** (for workflows without phases):
  - "This workflow doesn't use phases"
  - "Activities are organized directly in the workflow"
  - "Add phases if you want to group activities into stages"
  - [Add First Phase] [Keep Without Phases] buttons

**Example Data**:
- "Foundation" | Setup and configuration | 3 Activities | Order: 1
- "Implementation" | Core development work | 5 Activities | Order: 2

---

#### Screen: FOB-PHASES-CREATE_PHASE-1

Maria clicks [Create New Phase]:

**Form**:
- **Phase Name**: Text input
  - Example: "Integration Testing"
- **Description**: Textarea
  - Example: "Integrate and test all components together"
- **Parent Workflow**: Read-only (scoped)
- **Order**: Number or "Add to end"
- **Assign Activities**: Multi-select
  - List of unassigned activities in workflow
  - Or: [Skip - Assign Later]
- **Optional Reminder**: Info box
  - "Remember: Phases are optional. You can manage activities without phase grouping."

**Actions**: [Cancel] [Create Phase]

**Success Flow**:
- Phase created in workflow
- Success: "Phase 'Integration Testing' created"
- Redirects to FOB-PHASES-VIEW_PHASE-1

---

#### Screen: FOB-PHASES-VIEW_PHASE-1

Maria views phase details:

**Layout**:
- **Header**: Phase name with "Optional grouping" badge
- **Stats**: Activities in this phase, Order in workflow
- **Activities List**:
  - All activities assigned to this phase
  - [View Activity] links → ACT 5
  - [Move to Different Phase] buttons
  - [Remove from Phase] (makes activity unassigned)
- **Phase Navigation**:
  - [Previous Phase] [Next Phase] buttons
  - Link back to workflow view

---

#### Screen: FOB-PHASES-EDIT_PHASE-1

Edit phase details, reorder, reassign activities.

**Form**: Name, Description, Order, Activity assignments

**Special Options**:
- [Merge with Another Phase]
- [Split Phase] (divide activities into two phases)
- [Dissolve Phase] (remove phase, keep activities in workflow)

---

#### Screen: FOB-PHASES-DELETE_PHASE-1

Confirmation modal:

**Impact**:
- "Activities in this phase will remain in the workflow (unassigned to any phase)"
- Shows: 5 activities will become ungrouped
- Note: "Deleting a phase does NOT delete activities"

**Actions**: [Cancel] [Delete Phase]

**Success**: Phase removed, activities remain in workflow

---

**Act 4 Summary**: Maria can optionally use phases:
- ✅ **LIST+FIND**: View phases in a workflow (if used)
- ✅ **CREATE**: Add phases to group activities
- ✅ **VIEW**: See phase organization
- ✅ **EDIT**: Reorganize phases and activities
- ✅ **DELETE**: Remove phases without losing activities

**⚠️ Key Reminder**: Phases are OPTIONAL. Workflows work perfectly without them.

**Next**: Maria manages Activities - the core work units (ACT 5).

---

### Act 5: ACTIVITIES - Complete CRUDLF

**Context**: Activities are the core work units in a methodology. Each activity represents a specific task or action to be performed. Activities have dependencies, produce artifacts, are performed by roles, and have detailed howto guides.

**Pattern**: Standard CRUDLF. Activities are the heart of the workflow execution.

#### Screen: FOB-ACTIVITIES-LIST+FIND-1

From FOB-WORKFLOWS-VIEW_WORKFLOW-1, Maria clicks [View Activities]:

**Layout**:
- **Breadcrumb**: Playbooks > React Frontend > Workflows > Component Development > Activities
- **Header**: "Activities in Component Development" (8 activities)
- **View Modes**:
  - [List View] / [Dependency Graph] / [Timeline View]
- **Top Actions**:
  - [Create New Activity]
  - [Import from Template]
  - [Bulk Edit Dependencies]
- **Filters**:
  - By Phase (if workflow uses phases)
  - By assigned Role
  - By status (Has Howto, Has Artifacts, etc.)
  - By dependencies (Blocked, Ready, Completed)
- **Activities Table**:
  - Name | Description | Phase | Role | Artifacts | Upstream | Downstream | Actions
- **Row Actions**:
  - [View] → FOB-ACTIVITIES-VIEW_ACTIVITY
  - [Edit] → FOB-ACTIVITIES-EDIT_ACTIVITY
  - [Delete] → FOB-ACTIVITIES-DELETE_ACTIVITY
  - [Add Howto] → ACT 8
  - [Link Artifacts] → ACT 6
- **Dependency Visualization**:
  - DAG showing activity flow
  - Critical path highlighted
  - Click nodes to view activity details

**Example Data**:
- "Setup Component Structure" | Phase: Foundation | Role: Developer | 1 Artifact | No upstream | 2 downstream
- "Implement Base Components" | Phase: Implementation | Role: Developer | 3 Artifacts | 1 upstream | 1 downstream

---

#### Screen: FOB-ACTIVITIES-CREATE_ACTIVITY-1

Maria clicks [Create New Activity]:

**Form**:
- **Name**: Text input
  - Example: "Design Token Integration"
- **Guidance**: Rich Markdown editor (8-row textarea)
  - Example: "## Overview\n\nIntegrate design system tokens into component library\n\n## Steps\n\n1. Review design tokens\n2. Implement token mapping..."
  - **Full Markdown Support**:
    - Headers (# ## ###), Lists, Tables, Code blocks
    - **Mermaid Diagrams**: Sequence, class, flow diagrams
    - Images, Links, Bold, Italic, Inline code
  - Placeholder shows example structure
  - **Note**: Guidance is static reference material - like a technical book chapter
- **Parent Workflow**: Read-only
- **Phase Assignment** (if workflow uses phases):
  - Dropdown: Select phase or "No phase"
  - **Note**: Phases are optional - not all workflows use them
- **Order**: Number input or auto-assigned
  - Auto-increments if blank
- **Has Dependencies**: Checkbox (informational only)
  - **IMPORTANT**: This is a documentation flag, not enforcement
  - Indicates this activity should be done after prerequisites
  - Does NOT track specific dependency relationships
  - Does NOT prevent execution
  - **Future Enhancement**: Will be replaced with actual M2M dependency tracking
- **Artifacts Section**:
  - "What does this activity produce?"
  - [Link Existing Artifacts] or [Create New Artifact]
  - Can specify multiple artifacts
- **Estimated Effort**: Optional
  - Hours or story points
- **Create Howto**: Checkbox
  - "Create detailed guide for this activity?"
  - If checked: Redirects to ACT 8 after creation

**Actions**: [Cancel] [Create Activity]

**Success Flow**:
- Activity created in workflow
- Success: "Activity 'Design Token Integration' created"
- If "Create Howto" checked: Redirects to FOB-HOWTOS-CREATE_HOWTO
- Otherwise: Redirects to FOB-ACTIVITIES-VIEW_ACTIVITY-1

---

#### Screen: FOB-ACTIVITIES-VIEW_ACTIVITY-1

Maria views activity details:

**Layout**:
- **Header**: Activity name with phase badge (if applicable)
- **Metadata**:
  - Parent workflow link
  - Assigned role
  - Phase (if applicable): "Foundation" with link
  - Created/Modified dates
- **Tabs**:

1. **Overview Tab**:
   - **Guidance**: Rendered Markdown with syntax highlighting
     - Mermaid diagrams rendered as SVG
     - Code blocks with language-specific formatting
     - Tables, images, formatted lists
   - Phase assignment (if using phases)
   - Order number in workflow
   - **Has Dependencies**: Info badge (documentation only)
   - Created/Updated timestamps
   - **Note**: View Artifacts, Roles, Howtos in separate tabs

2. **Dependencies Tab**: (Future Enhancement)
   - **Current State**: Only shows "Has Dependencies" flag
   - **Planned**: Full dependency management
     - **Upstream**: Activities that should complete first
     - **Downstream**: Activities that depend on this one
     - Dependency graph visualization
     - M2M relationship tracking
   - **Note**: Currently activities have only a boolean flag, not actual dependency relationships

3. **Artifacts Tab**:
   - List of artifacts produced by this activity
   - [View Artifact] links → ACT 6
   - [Add New Artifact] [Link Existing] buttons

4. **Howto Tab**:
   - Detailed guide for performing this activity
   - If no howto: "No detailed guide yet" with [Create Howto] button
   - If exists: Full howto content (see ACT 8)
   - [Edit Howto] button → ACT 8

5. **Work Items Tab**:
   - GitHub issues, Jira tickets linked via external MCP
   - [Create Work Item] button (opens MCP interface)
   - Status of linked items

---

#### Screen: FOB-ACTIVITIES-EDIT_ACTIVITY-1

Edit activity:

**Form**: All fields from CREATE, pre-populated

**Additional Options**:
- **Dependency Management**:
  - Drag-and-drop dependency editor
  - Visual validation (highlights circular dependencies in red)
- **Move to Different Phase**: Dropdown (if workflow uses phases)
- **Reassign Role**: Dropdown
- **Artifact Management**:
  - Add/remove artifact associations
  - [Create New Artifact] inline

**Validation**:
- Cannot create circular dependencies
- Warns if removing dependencies breaks workflow logic
- Warns if reassigning role affects other activities

**Actions**: [Cancel] [Save Changes]

---

#### Screen: FOB-ACTIVITIES-DELETE_ACTIVITY-1

Confirmation modal:

**Impact Statement**:
- "This will permanently delete the activity"
- Shows affected items:
  - ✗ 1 Howto guide
  - ⚠️ 2 Downstream activities will lose upstream dependency
  - ⚠️ 3 Artifacts may become orphaned
  - ⚠️ 5 GitHub issues will lose activity context

**Dependency Warning**:
- "2 activities depend on this one:"
  - "Implement Base Components"
  - "Component Testing"
- "Deleting will break their upstream dependencies"

**Confirmation**:
- Checkbox: "I understand the impact"
- Type activity name

**Actions**: [Cancel] [Delete Activity]

**Success**: Activity deleted, workflow updated

---

**Act 5 Summary**: Maria manages activities:
- ✅ **LIST+FIND**: Browse and filter activities with dependency visualization
- ✅ **CREATE**: Create activities with dependencies, roles, and artifacts
- ✅ **VIEW**: Explore activity details, dependencies, artifacts, and howtos
- ✅ **EDIT**: Update activity details and reorganize dependencies
- ✅ **DELETE**: Remove activities with full dependency impact warnings

**Next**: Maria defines Artifacts produced by activities (ACT 6).

---

### Act 6: ARTIFACTS - Complete CRUDLF (No More "Deliverable"!)

**Context**: Artifacts are outputs produced by activities. They represent tangible results like documents, code, designs, reports, etc. **Note**: Formerly called "Deliverable" - now consistently called "Artifact".

**Pattern**: Standard CRUDLF. Artifacts are linked to producing activities.

#### Screen: FOB-ARTIFACTS-LIST+FIND-1

From workflow or activity view, Maria navigates to Artifacts:

**Layout**:
- **Header**: "Artifacts" with count
- **Scope Selector**:
  - "All Playbooks" / "Current Playbook" / "Current Workflow"
- **Top Actions**:
  - [Create New Artifact]
  - [Import Artifacts]
- **Filters**:
  - By type (Document, Code, Design, Data, Report, etc.)
  - By producing activity
  - By workflow
  - Orphaned (no producing activity)
- **Artifacts Table**:
  - Name | Type | Description | Produced By | Workflow | Actions
- **Row Actions**:
  - [View] → FOB-ARTIFACTS-VIEW_ARTIFACT
  - [Edit] → FOB-ARTIFACTS-EDIT_ARTIFACT
  - [Delete] → FOB-ARTIFACTS-DELETE_ARTIFACT

**Example Data**:
- "Component Library" | Code | "Reusable React components" | Activity: "Build Components" | Workflow: Component Dev
- "Design Tokens" | Design | "Color, spacing, typography tokens" | Activity: "Design System Setup" | Workflow: Component Dev
- "Test Report" | Document | "Unit and integration test results" | Activity: "Run Tests" | Workflow: Testing

---

#### Screen: FOB-ARTIFACTS-CREATE_ARTIFACT-1

Create new artifact:

**Form**:
- **Name**: Text input
  - Example: "API Documentation"
- **Type**: Dropdown
  - Options: Document, Code, Design, Data, Report, Specification, Other
- **Description**: Textarea
  - Example: "Complete REST API documentation with examples"
- **Produced By**: Activity selector (required)
  - Dropdown or search for activity
  - "Which activity creates this artifact?"
- **Format/Extension**: Optional
  - Example: ".md", ".pdf", ".json"
- **Template**: Optional checkbox
  - "Use this as a template for similar artifacts"
- **External Link**: Optional URL
  - Link to actual artifact (GitHub, Figma, Google Docs, etc.)

**Actions**: [Cancel] [Create Artifact]

**Success**: Artifact created and linked to activity

---

#### Screen: FOB-ARTIFACTS-VIEW_ARTIFACT-1

View artifact details:

**Layout**:
- **Header**: Artifact name with type badge
- **Metadata**:
  - Type, Format
  - Produced by: [Activity name] with link
  - Parent workflow, playbook
  - External link (if provided)
- **Tabs**:

1. **Overview Tab**:
   - Full description
   - Producing activity details
   - Consumers: Activities that use this artifact (if any)
   - Related artifacts (similar type or workflow)

2. **Usage Tab**:
   - List of activities that reference this artifact
   - Usage context
   - Dependencies

3. **History Tab**:
   - Creation date, author
   - Modification history
   - Versions (if artifact has versions)

---

#### Screen: FOB-ARTIFACTS-EDIT_ARTIFACT-1

Edit artifact: Form with all fields from CREATE, pre-populated

**Special Options**:
- [Change Producing Activity]: Dropdown
  - Warning if changing: "This may affect workflow understanding"
- [Mark as Template]
- [Update External Link]

---

#### Screen: FOB-ARTIFACTS-DELETE_ARTIFACT-1

Confirmation modal:

**Impact**:
- "This will remove the artifact"
- Warning: "Activity 'Build Components' will no longer have this artifact listed as output"
- If other activities reference it: List shown

**Note**: "This does NOT delete the actual file/document, only the artifact metadata in Mimir"

**Actions**: [Cancel] [Delete Artifact]

---

**Act 6 Summary**: Maria manages artifacts (no more "Deliverable"!):
- ✅ **LIST+FIND**: Browse all artifacts with filtering
- ✅ **CREATE**: Define new artifacts produced by activities
- ✅ **VIEW**: See artifact details and usage
- ✅ **EDIT**: Update artifact information
- ✅ **DELETE**: Remove artifact metadata

**Terminology Note**: Always use "Artifact", never "Deliverable".

**Next**: Maria defines Roles who perform activities (ACT 7).

---

### Act 7: ROLES - Complete CRUDLF

**Context**: Roles define who performs activities. A role represents a person, team, or function responsible for executing work.

**Pattern**: Standard CRUDLF. Roles are assigned to activities.

#### Screen: FOB-ROLES-LIST+FIND-1

Maria navigates to Roles management:

**Layout**:
- **Header**: "Roles" with count
- **Scope**: All playbooks or current playbook
- **Top Actions**:
  - [Create New Role]
  - [Import from Template]
- **Roles Table**:
  - Name | Description | Activities Assigned | Playbook | Actions
- **Row Actions**: [View] [Edit] [Delete]

**Example Data**:
- "Frontend Developer" | "Implements UI components and interactions" | 12 Activities | React Frontend
- "UX Researcher" | "Conducts user research and usability testing" | 8 Activities | UX Methodology
- "Product Owner" | "Defines requirements and prioritizes work" | 5 Activities | Product Discovery

---

#### Screen: FOB-ROLES-CREATE_ROLE-1

Create role:

**Form**:
- **Name**: Text input
  - Example: "DevOps Engineer"
- **Description**: Textarea
  - Example: "Manages infrastructure, CI/CD, and deployment pipelines"
- **Responsibilities**: Rich text
  - Detailed list of role responsibilities
  - Optional but recommended
- **Skills Required**: Tags
  - Example: "Docker, Kubernetes, AWS, CI/CD"
- **Assign to Activities**: Multi-select
  - Optional: Can assign now or later
  - Shows activities in current playbook/workflow

**Actions**: [Cancel] [Create Role]

---

#### Screen: FOB-ROLES-VIEW_ROLE-1

View role details:

**Tabs**:
1. **Overview**: Description, responsibilities, skills
2. **Activities**: All activities assigned to this role
   - Grouped by workflow
   - [View Activity] links
3. **Workload**: Visual workload analysis
   - Number of activities
   - Estimated effort (if activities have effort estimates)

---

#### Screen: FOB-ROLES-EDIT_ROLE-1

Edit role: Update all fields, reassign activities

---

#### Screen: FOB-ROLES-DELETE_ROLE-1

Confirmation:

**Impact**: "12 activities will lose role assignment"

**Options**:
- [Reassign Activities to Different Role] before deleting
- [Delete and Leave Activities Unassigned]

---

**Act 7 Summary**: Maria manages roles:
- ✅ **LIST+FIND**: Browse all roles
- ✅ **CREATE**: Define new roles with responsibilities
- ✅ **VIEW**: See role details and assignments
- ✅ **EDIT**: Update role information
- ✅ **DELETE**: Remove roles with reassignment options

**Next**: Maria creates detailed Howto guides for activities (ACT 8).

---

### Act 8: HOWTOS - Complete CRUDLF

**Context**: Howtos are detailed guides for performing activities. Each activity can have one howto providing step-by-step instructions, best practices, and examples. This is 1:1 relationship with activities.

**Pattern**: Standard CRUDLF. Howtos are tightly coupled to activities (1:1).

#### Screen: FOB-HOWTOS-LIST+FIND-1

Maria navigates to Howtos:

**Layout**:
- **Header**: "Howtos" (Activity Guides)
- **Scope**: Current workflow or all workflows
- **Filters**:
  - Activities with howtos / Activities without howtos
  - By workflow, by role
- **Howtos Table**:
  - Activity Name | Howto Title | Last Updated | Completeness | Actions
  - Completeness: Has steps, best practices, examples (badges)
- **Row Actions**: [View] [Edit] [Delete]
- **Special View**:
  - "Activities Without Howtos" section
  - Shows activities that need guides
  - [Create Howto] button per activity

**Example Data**:
- Activity: "Setup Component Structure" | Howto: "Component Setup Guide" | Complete ✓
- Activity: "Implement State Management" | Howto: "Redux Integration Guide" | Missing examples ⚠️

---

#### Screen: FOB-HOWTOS-CREATE_HOWTO-1

Maria clicks [Create Howto] for an activity:

**Form**:
- **Parent Activity**: Read-only (already selected)
  - Shows: "Creating howto for: Setup Component Structure"
- **Howto Title**: Text input
  - Default: "[Activity Name] - Guide"
  - Example: "Component Structure Setup - Complete Guide"
- **Steps**: Rich text editor with numbered list
  - Example:
    1. Create /src/components directory
    2. Set up component folder structure
    3. Add index files for exports
  - Supports: Markdown, code blocks, checkboxes
- **Best Practices**: Rich text editor
  - Tips and recommendations
  - Common pitfalls to avoid
- **Examples**: Rich text with code blocks
  - Sample code, screenshots, references
- **Prerequisites**: Text area
  - What needs to be done before this activity
- **Tools Required**: List
  - Software, access, credentials needed
- **References**: URLs
  - Links to documentation, articles, videos

**Actions**: [Cancel] [Create Howto]

**Success**: Howto created and linked to activity (1:1)

---

#### Screen: FOB-HOWTOS-VIEW_HOWTO-1

View howto guide (also accessible from Activity view):

**Layout**:
- **Header**: Howto title
- **Parent Activity**: Link to FOB-ACTIVITIES-VIEW_ACTIVITY
- **Content Sections**:
  1. **Steps**: Numbered, detailed instructions
  2. **Best Practices**: Tips and recommendations
  3. **Examples**: Code samples, screenshots
  4. **Prerequisites**: What's needed first
  5. **Tools**: Required software/access
  6. **References**: External links
- **Actions**:
  - [Edit Howto]
  - [Print/Export PDF]
  - [Copy to Clipboard]
  - [Share Link]
- **Breadcrumb**: Playbooks > [Playbook] > Workflows > [Workflow] > Activities > [Activity] > Howto

---

#### Screen: FOB-HOWTOS-EDIT_HOWTO-1

Edit howto: Full rich text editing of all sections

**Auto-save**: Drafts saved automatically every 30 seconds

**Version History**: Track changes to howto over time

---

#### Screen: FOB-HOWTOS-DELETE_HOWTO-1

Confirmation:

**Impact**: "Activity 'Setup Component Structure' will no longer have a detailed guide"

**Note**: "Activity will remain, only the howto guide is deleted"

**Confirmation**: Type howto title

---

**Act 8 Summary**: Maria manages howtos:
- ✅ **LIST+FIND**: Browse activity guides, identify gaps
- ✅ **CREATE**: Write detailed step-by-step guides
- ✅ **VIEW**: Read complete activity instructions
- ✅ **EDIT**: Update and improve guides
- ✅ **DELETE**: Remove guides (activities remain)

**Key Point**: 1:1 relationship with activities - each activity has at most one howto.

---

**🎉 Acts 2-8 Complete!** All 7 core entities (Playbooks, Workflows, Phases, Activities, Artifacts, Roles, Howtos) now have full CRUDLF coverage with narrative explanations.

**Demo Playbook Available**: A Feature-Driven Development (FDD) demo playbook with 10 activities showcasing rich Markdown guidance is available via `python manage.py create_demo_fdd`. This demonstrates:
- Mermaid diagrams (class, sequence, flow)
- Code examples (Python, Bash, YAML)
- Tables and checklists
- Multi-level documentation structure

**Next**: Maria can propose improvements via PIPs (ACT 9) and manage import/export (ACT 10).

---

### Act 9: PIPs - Playbook Improvement Proposals

**Context**: As Maria uses playbooks (whether her own or downloaded from others), she discovers opportunities for improvement. PIPs (Playbook Improvement Proposals) are the mechanism for suggesting, tracking, and applying changes to playbooks.

**Key Concepts**:
- PIPs can be created manually by users or suggested by AI
- Local PIPs: Applied immediately to local playbook versions
- Submitted PIPs: Sent to original playbook author for review
- PIPs create versioned changes (e.g., v1.0 → v1.1 local)

#### Creating a PIP

**Trigger**: While using "React Frontend Development" playbook (authored by Mike), Maria notices it lacks accessibility considerations.

**Via AI Assistant (Windsurf/MCP)**:

Maria asks her AI assistant:
```
> mimir: This React playbook is great, but it doesn't mention accessibility testing. 
  I think we should add an Activity for "Accessibility Audit" after testing setup. 
  Can you help me create a PIP for this?
```

AI responds:
```
I'll help you create a Playbook Improvement Proposal (PIP).

Proposed PIP:
- Type: Extension (new Activity)
- Target Playbook: React Frontend Development v1.0 by Mike Chen
- Change: Add new Activity "Accessibility Audit"
- Position: After "Component Testing"  
- Description: "Ensure React components meet WCAG 2.1 AA standards"
- Includes:
  • Install axe-core and jest-axe
  • Add accessibility tests to component suite
  • Configure automated a11y checks in CI/CD

Shall I create this PIP in your local FOB?
```

Maria confirms: `> mimir: Yes, create the PIP`

#### Screen: FOB-PIP-CREATE (via MCP or GUI)

System creates PIP:
- **PIP ID**: PIP-42
- **Title**: "Add Accessibility Audit Activity"
- **Type**: Extension
- **Target**: React Frontend Development v1.0
- **Author**: Maria Rodriguez
- **Status**: Draft (local only)
- **Changes Preview**: Shows diff-style comparison
  - Current structure (v1.0)
  - Proposed structure (v1.1 with new activity)

**Actions Available**:
- [Apply Locally] - Creates local v1.1
- [Submit to Author] - Sends PIP to Mike for review
- [Edit PIP] - Modify proposal
- [Discard] - Delete draft

#### Action: Apply PIP Locally

Maria clicks [Apply Locally]:
- Confirmation: "This will create React Frontend Development v1.1 (local)"
- Playbook updated immediately
- Success: "PIP-42 applied. Playbook updated to v1.1 (local)"
- Version badge changes: "v1.1 (local)" indicates local modifications

**Result**: Maria now has an enhanced version with accessibility considerations.

#### Action: Submit PIP to Author

Later, Maria decides to share her improvement:
- Opens PIP-42 details
- Clicks [Submit to Author]
- Modal: "Submit PIP to Mike Chen?"
  - "This will send your proposal for review"
  - "Mike can accept, request changes, or decline"
  - Optional message to author
- Maria adds: "Great playbook! I added a11y audit based on WCAG 2.1 AA standards"
- Clicks [Submit]

**Notification Flow**:
- PIP sent to Homebase
- Mike receives notification: "Maria Rodriguez submitted PIP-42 to React Frontend Development"
- Maria sees: "PIP-42 submitted for review"

#### Screen: FOB-PIP-LIST (Manage PIPs)

Maria can view all her PIPs:
- **My Submitted PIPs**: 
  - PIP-42: Accessibility Audit (Pending Review by Mike)
  - PIP-38: State Management Patterns (Accepted - merged to v1.2)
- **Received PIPs** (for her owned playbooks):
  - PIP-55: Add Figma integration (from Alex - Pending Maria's review)
- **Local PIPs** (applied but not submitted):
  - PIP-40: Personal workflow tweaks (UX Research playbook)

**Filters**: Status (Draft, Submitted, Accepted, Declined), Playbook, Author

#### Reviewing Received PIPs (Playbook Owner View)

When Mike reviews Maria's PIP-42:

**Screen: FOB-PIP-REVIEW**:
- Shows complete PIP details
- Side-by-side diff view
- Comments/discussion thread
- Actions for owner:
  - [Accept & Merge] - Incorporates changes, publishes new version
  - [Request Changes] - Sends feedback to Maria
  - [Decline] - Rejects with reason

Mike clicks [Accept & Merge]:
- React Frontend Development updates to v1.2
- All family members notified of new version
- PIP-42 marked as "Accepted"
- Maria's contribution credited in version history

**Result**: Collaborative playbook evolution through structured improvement proposals.

#### AI-Initiated PIPs

**Context**: AI observes Maria's work patterns and proactively suggests improvements.

**Scenario**: After Maria completes several components with accessibility features, AI notices the pattern:

```
✓ Components created: Button, Card, Modal (all with focus traps, ARIA labels)
✓ Accessibility tests added to each component

I notice you're consistently adding accessibility features, but the playbook 
doesn't explicitly call for focus trapping in modals. Based on your work patterns, 
should we update the playbook to include:
  - Focus trap implementation guidelines
  - Keyboard navigation requirements  
  - ARIA attribute checklist

Would you like me to create a PIP for these additions?
```

Maria: `> mimir: Yes, great observation! Create the PIP`

AI creates PIP-43 automatically, Maria reviews and applies/submits as needed.

---

**Act 9 Summary**: Maria can evolve playbooks through PIPs:
- ✅ Create PIPs manually or via AI assistance
- ✅ Apply PIPs locally for immediate use
- ✅ Submit PIPs to original authors for community contribution
- ✅ Review and merge PIPs received on owned playbooks
- ✅ Track PIP status and version history
- ✅ AI learns from patterns and suggests improvements

**Key Benefits**: Structured change management, version control, collaborative improvement, AI-assisted evolution.

**Next**: Maria manages import/export operations (ACT 10).

---

### Act 10: IMPORT/EXPORT - Playbook Distribution

**Context**: Maria needs to share playbooks outside the Homebase sync system - for backups, offline distribution, cross-instance transfer, or client delivery.

**Key Formats**:
- **JSON**: Structured data format for programmatic use
- **MPA** (Mimir Playbook Archive): Compressed package with metadata

#### Export Playbook

**Screen: FOB-PLAYBOOKS-VIEW_PLAYBOOK-1** (from Act 2)

Maria views her "UX Research Methodology" playbook and clicks **[Export]** from top actions.

**Export Modal**:
- **Format Options**:
  - ○ JSON (.json) - Raw structured data
  - ○ Mimir Playbook Archive (.mpa) - Packaged with metadata
- **Include Options** (checkboxes):
  - ☑ All workflows and activities
  - ☑ Artifacts and roles
  - ☑ Howtos (activity guides)
  - ☑ Version history
  - ☐ PIP history (optional)
- **Security**:
  - ☐ Password protect (optional)
  - Password field (if checked)
- **Filename**: `ux-research-methodology-v2.1` (auto-generated, editable)
- [Cancel] [Export]

Maria selects **JSON format**, leaves all options checked, clicks [Export]:
- File saved: `ux-research-methodology-v2.1.json` to ~/Downloads
- Success notification: "Playbook exported successfully"
- **Use cases**:
  - Backup before major changes
  - Share with colleague via email
  - Import to another FOB instance
  - Version control (commit to git)

#### Export Scenarios

**Scenario A: Offline Distribution for Workshop**

Maria's colleague Alex needs the playbook for an offline workshop (no Homebase access):
- Maria exports as `.mpa` with password protection
- Emails file to Alex: `ux-research-v2.1.mpa`
- Alex imports to his FOB (see Import section below)

**Scenario B: Client Delivery (IP Transfer)**

After transferring ownership to Acme client, Maria exports final version:
- Exports "UX Consulting" playbook as JSON
- Delivers to client as documentation artifact
- Client can import to their own FOB instance

**Scenario C: Backup Before Experimentation**

Before applying experimental PIPs:
- Maria exports current stable version
- Tests PIPs locally
- If issues arise: deletes modified version, re-imports from backup

---

#### Import Playbook

**Screen: FOB-PLAYBOOKS-LIST+FIND-1** (from Act 2)

Maria clicks [Import from JSON] button (top actions).

**Import Modal**:
- **File Upload Area**: "Drop JSON or MPA file here or click to browse"
- Accepted formats: `.json`, `.mpa`
- [Cancel] (disabled until file selected)

**Action: Select File**

Maria selects `design-system-patterns-v1.5.json` from downloads:
- Filename appears in modal
- System validates file format
- [Import] button becomes active

**Validation Process**:

System checks:
- ✓ Valid JSON structure
- ✓ Required fields present (id, name, version, workflows, activities)
- ✓ Schema compliance (Mimir data model)
- ✓ No circular dependencies
- ✓ Referenced entities exist

**Success Path** - Valid Playbook:

Shows preview:
- **Playbook**: "Design System Patterns"
- **Version**: 1.5
- **Author**: Community Contributors
- **Contents**:
  - 3 Workflows
  - 15 Activities
  - 12 Artifacts
  - 5 Roles
  - 8 Howtos
- **Conflict Check**: "No conflicts with existing playbooks"
- Message: "This playbook will be added to your local FOB"
- [Cancel] [Import Playbook]

Maria clicks [Import Playbook]:
- Progress: "Importing playbook..."
- Playbook added to local database
- Success: "Design System Patterns v1.5 imported successfully"

**Screen: FOB-PLAYBOOKS-LIST+FIND-1** (Updated)

Imported playbook appears:
- **Design System Patterns** v1.5
- Status: Local (not synced to Homebase)
- Source: Imported from JSON
- Actions: [View] [Edit] [Export] [Delete]

---

**Error Path** - Invalid Playbook:

If validation fails:
- ✗ Error: "Invalid playbook format"
- Details: "Missing required field: 'activities'"
- OR: "Circular dependency detected in workflow 'Component Setup'"
- OR: "Schema version mismatch: File uses v2.0, FOB supports v1.5"
- [Close] [Try Another File]

**Error Path** - Conflict Detected:

If playbook with same ID exists:
- ⚠️ Warning: "Playbook 'Design System Patterns' already exists"
- **Options**:
  - ○ Skip import (keep existing)
  - ○ Replace existing (overwrites local version)
  - ○ Import as new copy (generates new ID)
- [Cancel] [Proceed]

---

**Import from MPA (Password Protected)**:

If importing `.mpa` file with password:
- Password prompt appears: "This archive is password protected"
- Password field: [____]
- [Cancel] [Unlock]

After correct password: Standard import flow continues

If wrong password: "Incorrect password. Please try again."

---

**Act 10 Summary**: Maria manages playbook distribution:
- ✅ Export playbooks as JSON or MPA
- ✅ Password-protect sensitive playbooks
- ✅ Import playbooks from files
- ✅ Validate imported data
- ✅ Handle conflicts and errors gracefully
- ✅ Distribute offline without Homebase dependency

**Use Cases Covered**:
- Backups and version control
- Offline distribution (workshops, air-gapped environments)
- Cross-instance transfer
- Client deliverables
- Emergency recovery

**Next**: Maria manages her community networks (ACT 11: Family Management).

---

### Act 11: Building Her Network (Family Management)

**Context**: Maria wants to organize her practice - a public family for UX community, a private one for her client work, and join existing communities.

#### Screen: FOB Dashboard (First Login)
Maria opens her FOB application and sees the welcome dashboard:
- Empty playbook list (no playbooks yet)
- "Browse Families" button
- "Create Family" button
- "Sync with Homebase" button

#### Screen: FOB Create Family - UX Community
Maria clicks "Create Family" and fills out the form:
- **Family Name**: "UX"
- **Description**: "User Experience methodologies and best practices"
- **Visibility**: Public (appears in browse)
- **Join Policy**: Requires Approval (Maria will review requests)
- **Category**: Design
- Clicks "Create Family"

**Result**: Maria is now the admin of the "UX" family.

#### Screen: FOB Create Family - Client Work
Maria creates a second family for her consulting clients:
- **Family Name**: "Acme, INC"
- **Description**: "UX Consulting services for Acme Corporation"
- **Visibility**: Hidden (only visible to members she manually adds)
- **Join Policy**: Invite Only
- **Category**: Private
- Clicks "Create Family"

**Result**: Maria now manages two families - one public, one hidden.

#### Screen: FOB Family Browser
Maria clicks "Browse Families" to explore existing communities. She sees:
- Search bar and category filters
- List of public families with descriptions and member counts
- "Usability" family catches her eye (Mike's community)

#### Screen: FOB Family Details - Usability
Maria clicks on "Usability" to see details:
- **Description**: "Best practices for usable software development"
- **Members**: 127 members
- **Playbooks**: 8 available playbooks (including Mike's React playbook)
- **Join Policy**: Auto-approve
- "Join Family" button

#### Action: Join Family
Maria clicks "Join Family". Because it's set to auto-approve:
- She's immediately added to the Usability family
- Notification: "You've joined the Usability family"
- She can now see available playbooks from this family

**Result**: Maria is now a member of three families - two she created, one she joined.

**Act 11 Summary**: Maria manages her professional network:
- ✅ Create families (public and hidden)
- ✅ Browse and join existing families
- ✅ Review and approve/reject join requests
- ✅ Manage family playbook submissions
- ✅ Transfer family admin rights
- ✅ Remove members (with knowledge loss consequences)

**Next**: Maria syncs playbooks with Homebase (ACT 12).

---

### Act 12: SYNC SCENARIOS - Discovering & Sharing Playbooks

**Context**: Maria downloads community playbooks from Homebase and uploads her improvements back. Sync handles clean downloads, uploads, conflicts, and version management.

#### Scenario A: Clean Download - Discovering Mike's Playbook

**Screen: FOB Sync Dashboard**

Maria clicks [Sync with Homebase] from dashboard:
- FOB connects using authentication token
- Status: "Checking for updates..."
- Lists available playbooks from her families

**Screen: FOB Available Playbooks**

Maria sees entitled playbooks:
- "React Frontend Development" (Usability family) v1.0 by Mike Chen
- 7 other playbooks from families
- Status badges: Downloaded / Not Downloaded

**Screen: FOB Playbook Preview**

Maria clicks "React Frontend Development":
- Shows structure preview (workflows, activities, artifacts)
- Author: Mike Chen
- Version history
- [Download to FOB] button

**Action: Download Playbook**

Maria clicks [Download to FOB]:
- Progress indicator
- Playbook added to local database
- Success: "React Frontend Development v1.0 downloaded"
- Now available offline with full CRUDLF access (Acts 2-8)

---

#### Scenario B: Upload with PIP - Contributing Back

**Context**: Maria applied PIP-42 locally (Act 9), enhancing React playbook with accessibility audit. She wants to contribute back.

**Screen: FOB Sync Dashboard**

Maria clicks [Sync with Homebase]:
- Analyzes local changes
- Detects: "React Frontend Development v1.1 (local) differs from v1.0 (remote)"

**Screen: FOB Sync Analysis**

Shows diff:
- Local: v1.1 with Accessibility Audit activity (PIP-42 applied)
- Remote: v1.0 (unchanged)
- Recommendation: "Upload improvements as PIP to author"
- [Generate PIP for Homebase] button

**Action: Upload PIP**

Maria clicks [Generate PIP for Homebase]:
- Creates PIP package with her changes
- Preview: "PIP-42: Add Accessibility Audit to React Frontend Development"  
- [Submit to Homebase] button

Maria submits:
- PIP uploaded to Homebase
- Notification sent to Mike (author) and family admins
- Maria sees: "PIP-42 submitted for review by Mike Chen"

Mike reviews and accepts:
- React Frontend Development updates to v1.2 on Homebase
- All family members notified
- Maria's contribution credited

---

#### Scenario C: Download Update - Conflict Resolution

**Context**: Mike accepted PIP-42 and published v1.2. Maria still has local v1.1. She syncs again.

**Screen: FOB Sync Dashboard**

Maria clicks [Sync with Homebase]:
- Detects: "React Frontend Development v1.2 available (your local: v1.1)"

**Screen: FOB Conflict Resolution**

Shows 3-way comparison:
- **Your Local v1.1**: Has PIP-42 changes
- **Remote v1.2**: Has PIP-42 merged + Mike's additional tweaks
- **Conflict Status**: No conflicts (your changes are superset of remote)

**Resolution Options**:
- ○ **Download v1.2** (recommended): Replaces local with official version
- ○ **Keep Local v1.1**: Stay on your version, opt out of updates
- ○ **Merge**: Combine local + remote changes (advanced)

Maria selects **Download v1.2**:
- Downloads official version
- Local v1.1 archived to version history
- Success: "Updated to React Frontend Development v1.2"

---

#### Scenario D: True Conflict - Divergent Changes

**Context**: Maria modified Activity 2 locally. Mike also changed Activity 2 in v1.3. Changes conflict.

**Screen: FOB Conflict Resolution (Conflict Detected)**

Shows conflicts:
- **Activity 2**: "Create Components"
  - Your change: Added accessibility checklist
  - Remote change: Restructured component architecture
  - Status: ⚠️ **CONFLICT**

**Resolution Options**:
- ○ **Accept Remote**: Use Mike's v1.3 (lose your changes)
- ○ **Keep Local**: Stay on v1.2 with your changes
- ○ **Manual Merge**: Open editor to combine both

**Actions**:
- [View Diff] - See line-by-line changes
- [Accept Remote] - Take Mike's version
- [Keep Local] - Keep your version
- [Contact Author] - Message Mike about conflict

Maria chooses [Accept Remote] (trusts Mike's architecture):
- Downloads v1.3
- Her local changes archived
- Can create new PIP later if needed

---

**Act 12 Summary**: Maria syncs playbooks with Homebase:
- ✅ Download community playbooks from families
- ✅ Preview before downloading
- ✅ Upload PIPs to contribute improvements
- ✅ Handle version updates and conflicts
- ✅ Resolve conflicts (accept, keep, merge)
- ✅ Offline resilience (downloaded playbooks work without connection)

**Key Points**:
- Sync requires Homebase connection and authentication
- Downloaded playbooks available offline with full CRUDLF
- PIPs enable structured contribution workflow
- Version control prevents data loss
- Conflict resolution preserves user choice

**Next**: Maria uses playbooks via MCP in her IDE (ACT 13).

---

### Act 13: MCP INTEGRATION - AI-Assisted Methodology Execution

**Context**: Maria works in Windsurf IDE with Mimir MCP server providing playbook context. External MCPs (GitHub, Jira) handle work items.

#### Setup: MCP Configuration

Maria's Windsurf has two MCP servers configured:
1. **Mimir MCP** (localhost:5000): Provides playbook context, activities, artifacts
2. **GitHub MCP** (external): Creates/tracks GitHub issues

FOB container runs Mimir MCP server, exposing playbook data via Model Context Protocol.

---

#### Using Active Playbook

**Screen: FOB Dashboard**

Maria activates "React Frontend Development" playbook:
- Clicks on playbook
- [Activate] button
- Success: "React Frontend Development v1.2 is now active"

**Windsurf/MCP Chat**

Maria asks her AI assistant:
```
> mimir: I'm starting a new React project. How do I set up the project structure?
```

**MCP Response** (from Mimir MCP):
```
Based on "React Frontend Development" playbook, Activity 1: Setup Project:

1. Initialize with Create React App or Vite
2. Folder structure:
   - /src/components (reusable UI)
   - /src/pages (page-level)
   - /src/hooks (custom hooks)
   - /src/state (state management)
3. Configure ESLint and Prettier  
4. Set up Jest + React Testing Library

Upstream: None
Downstream: Create Components, Implement State Management

Would you like me to create a GitHub issue to track this?
```

---

#### Creating Work Items via External MCP

Maria responds:
```
> mimir: Yes, create a GitHub issue for project setup
```

**GitHub MCP** (external server) creates issue:
- **Repo**: maria/acme-dashboard
- **Issue #47**: "Setup React project structure per React Frontend Development playbook"
- **Body**: Includes checklist from Activity 1 (context from Mimir MCP)
- **Labels**: setup, react, playbook

Link returned to Maria.

---

#### Context-Aware Guidance

After completing work, Maria asks:
```
> mimir: What's next per the React playbook?
```

**MCP Response** (coordinated):
```
Checking MIMR-47 status... (GitHub MCP) ✓ Project structure complete.

Next activity per "React Frontend Development" (Mimir MCP):
Activity 2: Create Components

Prerequisites complete ✓
Ready to start component development.

Options:
1. Show full Activity 2 details? (Mimir MCP)
2. Create GitHub issue for components? (GitHub MCP)
3. Open playbook in browser? (Mimir MCP)
```

---

#### Auto-Open Playbook in Browser

Maria: `> mimir: Open playbook in browser`

**MCP Action** (Mimir MCP):
- Sends command to open browser
- URL: `http://localhost:8000/playbooks/react-frontend-dev`
- Browser opens showing FOB-PLAYBOOKS-VIEW_PLAYBOOK-1 (Act 2)
- Activity 1 marked complete (linked to MIMR-47)
- Activity 2 highlighted as next step

---

**Act 13 Summary**: Maria uses Mimir MCP for AI-assisted methodology execution:
- ✅ Activate playbooks in FOB
- ✅ Query playbook context via AI (Windsurf/MCP)
- ✅ Get activity-specific guidance
- ✅ Create work items via external MCPs (GitHub, Jira)
- ✅ Track progress and dependencies
- ✅ Auto-open playbook details in browser

**Integration Architecture**:
- **Mimir MCP**: Playbook context, activities, artifacts (localhost:5000)
- **External MCPs**: Work item management (GitHub, Jira, GitLab, etc.)
- **AI Coordination**: Windsurf AI coordinates between MCPs for seamless workflow

**Key Benefits**:
- Playbook guidance embedded in development workflow
- No context switching between IDE and playbook docs
- Automated work item creation with playbook context
- Dependency tracking and progress visibility

**Next**: Maria configures FOB settings (ACT 14).

---

### Act 14: Settings & Preferences

**Context**: Maria needs to configure her FOB and account settings.

#### Screen: FOB Settings - Main
Maria clicks **Settings** in navigation menu:
- **Sidebar navigation**:
  - Account
  - Sync & Connection
  - Storage
  - MCP Configuration
  - Notifications
  - Privacy
  - Advanced
- **Account section** (default):
  - Profile information
  - Email: maria@uxconsulting.com
  - Full name: Maria Rodriguez
  - [Change Password] button
  - [Two-Factor Authentication] toggle
  - [Delete Account] (danger zone)

#### Screen: FOB Settings - Sync & Connection
Maria clicks **Sync & Connection**:

- **Homebase Connection**:
  - **Status**: ✓ Connected to homebase.mimir.io
  - **Account**: maria@uxconsulting.com
  - **Last sync**: 5 minutes ago
  - **Connection Details**:
    - Homebase URL: `https://homebase.mimir.io` [Edit]
    - Authentication Token: `mimir_a8f3...45678` [Show] [Copy]
    - Token created: Nov 15, 2024
  - **Actions**:
    - [Test Connection] button
    - [Regenerate Token] button (requires re-entering password)
    - [Disconnect from Homebase] button (danger action)
  
  **Note**: Only one Homebase connection is supported.

- **If Not Connected** (alternative view when disconnected):
  - **Status**: ⊝ Not connected to Homebase
  - **You are working in local-only mode**
    - You can create and manage playbooks locally
    - You cannot sync playbooks from families
    - You cannot publish playbooks to families
  - **Connect to Homebase**:
    - Homebase URL: [https://homebase.mimir.io]
    - Authentication Token: [paste your token here]
    - [Get Token from Homebase] link (opens homebase.mimir.io/account)
    - [Test Connection] button
    - [Save Connection] button

- **Sync Preferences** (only when connected to HB):
  - Auto-sync: [On/Off] toggle
  - Sync frequency: Dropdown (Manual, Every 15min, Hourly, Daily)
  - Sync on startup: [On/Off]
  - Notification for available updates: [On/Off]

- **Conflict Resolution** (only when connected to HB):
  - Default action: Dropdown (Ask me, Prefer remote, Prefer local)

#### Screen: FOB Settings - Storage
Maria clicks **Storage**:
- **Local Database**:
  - Location: /Users/maria/.mimir/data
  - Size: 2.3 GB (4 playbooks, 127 activities)
  - [Change Location] button
- **Cache**:
  - Cache size: 142 MB
  - [Clear Cache] button
- **Cleanup**:
  - Orphaned artifacts: 0
  - Old versions: 12 (keeping latest 5 per playbook)
  - [Run Cleanup] button

#### Screen: FOB Settings - MCP Configuration
Maria clicks **MCP Configuration**:
- **Mimir MCP Server Status**: ✓ Running on port 5000
- **Windsurf Integration**:
  - Connection string: `localhost:5000`
  - API key: `mcp_***********` [Show] [Regenerate]
  - [Test MCP Connection] button
- **Mimir MCP Features**:
  - Enable playbook context: [On/Off]
  - Enable PIP suggestions: [On/Off]
  - Enable AI-initiated PIPs: [On/Off]
- **External MCP Servers** (configured separately in Windsurf):
  - GitHub MCP (for work item management)
  - Jira MCP (optional)
  - GitLab MCP (optional)
  - Note: "Work item creation/tracking handled by external MCPs, not Mimir MCP"
- **Restart Mimir MCP Server** button

#### Screen: FOB Settings - Notifications
Maria clicks **Notifications**:
- **Notification Preferences**:
  - Family join requests: [On/Off]
  - Playbook updates available: [On/Off]
  - PIP submissions: [On/Off]
  - Sync conflicts: [On/Off]
  - System errors: [On/Off] (cannot be disabled)
- **Notification Method**:
  - In-app notifications: [On/Off]
  - Browser notifications: [On/Off]
  - Email notifications: [On/Off]
- **Quiet Hours**:
  - Enable: [On/Off]
  - From: 22:00
  - To: 08:00

**Act 14 Summary**: Maria configures FOB:
- ✅ Account settings (profile, password, 2FA)
- ✅ Homebase connection and sync preferences
- ✅ Storage management and cleanup
- ✅ MCP server configuration
- ✅ Notification preferences
- ✅ Privacy and advanced settings

**Next**: Maria handles errors and edge cases (ACT 15).

---

### Act 15: Error Recovery & Edge Cases

**Context**: Maria encounters various error scenarios and learns how to recover.

#### Error Scenario 1: Sync Failure

##### Screen: FOB Sync Dashboard - Error
Maria clicks "Sync with Homebase" but network is down:
- Error banner appears: ⚠️ "Sync failed: Cannot connect to Homebase"
- **Error Details** dropdown:
  - Error type: Network error
  - Homebase URL: https://homebase.mimir.io
  - Error code: CONNECTION_TIMEOUT
  - Timestamp: 2024-11-20 14:32:15
- **Recovery Actions**:
  - [Retry Sync] button
  - [Check Connection Settings] link → Settings
  - [Work Offline] button
  - [View Error Log] link

##### Action: Work Offline
Maria clicks [Work Offline]:
- Modal: "Working offline - limited functionality"
- "You can continue using local playbooks and MCP features"
- "Sync operations, downloads, and uploads are disabled until connection is restored"
- "FOB will automatically attempt reconnection"
- [Continue Offline] [Cancel]

**Result**: Maria continues working with local playbooks while offline.

#### Error Scenario 2: Permission Denied

##### Screen: FOB Playbook Editor - Permission Error
Maria tries to edit Mike's React playbook:
- Error modal: 🚫 "Permission Denied"
- "You don't have permission to edit this playbook"
- **Reason**: "This playbook is owned by Mike Chen (Usability family)"
- **Options**:
  - "You can create a local copy and modify it"
  - "Submit a PIP to suggest changes"
- **Actions**:
  - [Create Local Copy] button
  - [Submit PIP] button
  - [Cancel]

Maria clicks [Submit PIP] which opens PIP creation flow.

**Result**: Clear error messaging with actionable recovery paths.

#### Error Scenario 3: Upload Failed

##### Screen: FOB Upload to Homebase - Failed
Maria tries to upload a large playbook but it fails:
- Error toast notification: "Upload failed: File size exceeds limit"
- **Error Details**:
  - Playbook: "UX Comprehensive Guide"
  - Size: 125 MB (limit: 100 MB)
  - Reason: Embedded images too large
- **Recovery Actions**:
  - [Compress Images] button (auto-optimize)
  - [Remove Large Artifacts] button (review what to remove)
  - [Split into Multiple Playbooks] suggestion
  - [Contact Support] link

**Result**: Helpful error messages with clear resolution paths.

#### Error Scenario 4: Corrupted Playbook

##### Screen: FOB Dashboard - Playbook Error
A playbook shows error icon:
- Warning badge: ⚠️ on "Old Frontend Patterns" playbook card
- Click reveals: "Data corruption detected"
- **Details**:
  - Corrupted activities: 2 of 8
  - Last successful load: 3 days ago
  - Cause: Unknown (possibly interrupted sync)
- **Recovery Actions**:
  - [Restore from Homebase] button (if available)
  - [Restore from Local Backup] button
  - [Delete Corrupted Data] button
  - [Export Salvageable Content] button

**Result**: Maria can recover from data corruption scenarios.

#### Empty State Scenarios

##### Screen: FOB Dashboard - No Playbooks
When Maria first starts (empty state):
- Illustration: Empty box graphic
- Heading: "No playbooks yet"
- Subtext: "Get started by creating a playbook, downloading from Homebase, or importing from a file"
- **Actions**:
  - [Create Your First Playbook] button (primary)
  - [Browse Families] button
  - [Import from File] button
  - [Watch Tutorial] link

##### Screen: FOB Family Browser - No Results
Maria searches for non-existent family:
- Illustration: Magnifying glass
- Heading: "No families found matching 'blockchain'"
- Subtext: "Try adjusting your search or browse all families"
- **Suggestions**:
  - Similar families: (list of related results)
  - [Clear Filters] button
  - [Create New Family] button

**Result**: Every empty or error state provides clear guidance and next steps.

---

**Act 15 Summary**: Maria handles errors gracefully:
- ✅ Network failures with offline mode
- ✅ Permission errors with clear alternatives
- ✅ Upload failures with recovery options
- ✅ Data corruption with backup/restore
- ✅ Empty states with helpful guidance

**Key Point**: All errors provide actionable recovery paths, never dead ends.

---

## Journey Complete

Maria's journey through Acts 0-15 demonstrates the complete Mimir MVP experience:

**Core CRUDLF Entities (Acts 2-8):**
- ✅ **Playbooks**: Top-level methodologies with versioning and family publishing
- ✅ **Workflows**: Execution sequences with optional phase organization  
- ✅ **Phases**: Optional activity groupings (clearly marked as optional)
- ✅ **Activities**: Core work units with dependencies, roles, and artifacts
- ✅ **Artifacts**: Outputs produced by activities (no more "Deliverable")
- ✅ **Roles**: Definitions of who performs activities
- ✅ **Howtos**: Step-by-step activity guides (1:1 with activities)

**Supporting Features (Acts 9-15):**
- ✅ **PIPs**: Collaborative improvement proposals with versioning
- ✅ **Import/Export**: Offline distribution via JSON/MPA files
- ✅ **Family Management**: Public/private communities with admin workflows
- ✅ **Sync**: Download, upload, conflict resolution with version control
- ✅ **MCP Integration**: AI-assisted methodology execution in Windsurf
- ✅ **Settings**: Full configuration of FOB, Homebase sync, and MCP
- ✅ **Error Recovery**: Graceful handling of all failure scenarios

**Key Achievements:**
- All 7 core entities have complete CRUDLF with LIST+FIND entry points
- Consistent naming: `FOB-{ENTITY}-{OPERATION}-{VERSION}`
- Phase explicitly marked as OPTIONAL throughout
- "Artifact" terminology (not "Deliverable")
- Detailed screen specifications ready for BDD feature files
- Full sync workflow with conflict resolution
- MCP integration architecture documented
- Error recovery paths for all scenarios

Maria now has a complete, production-ready methodology management system with collaborative features, AI assistance, and offline resilience.
