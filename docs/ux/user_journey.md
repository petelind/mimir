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
- **FOB displays**: "Activity 1: Setup Project" with description and guidance (static)
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

Maria clicks [Create New Playbook]. The creation wizard opens (accessed via «extends» arrow from LIST+FIND in flow diagrams):

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

Maria clicks [View] on "React Frontend Development" from the list. The detail view opens (accessed via «extends» arrow from LIST+FIND):

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

Maria clicks [Edit] on her "Product Discovery Framework" playbook. The edit form opens (accessed via «extends» arrow from VIEW or LIST+FIND):

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

Maria clicks [Delete] on an old "Test Playbook 123" she no longer needs. A confirmation modal appears (accessed via «extends» arrow from VIEW or LIST+FIND):

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
- **Description**: Rich text editor
  - Example: "Integrate design system tokens into component library"
  - Supports markdown, checklists
- **Parent Workflow**: Read-only
- **Phase Assignment** (if workflow uses phases):
  - Dropdown: Select phase or "No phase"
- **Role Assignment**: Dropdown
  - Select from existing roles or [Create New Role]
  - Example: "Frontend Developer"
- **Dependencies**:
  - **Upstream Activities**: Multi-select
    - Activities that must complete before this one
  - **Downstream Activities**: Multi-select  
    - Activities that depend on this one
  - Validation: Prevents circular dependencies
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
   - Full description
   - Assigned role with [View Role] link
   - Dependencies diagram
   - Artifacts produced (with links to ACT 6)
   - Howto guide preview (if exists)
   - Work items linked (GitHub issues via MCP)

2. **Dependencies Tab**:
   - **Upstream**: Activities that must complete first
     - Visual cards for each
     - [Add Upstream] [Remove] buttons
   - **Downstream**: Activities that depend on this one
     - Visual cards
     - [Add Downstream] [Remove] buttons
   - Dependency graph visualization

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

**Next**: Maria can propose improvements via PIPs (ACT 9) and manage import/export (ACT 10).

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

---

### Act 2.5: Family Admin Workflows

**Context**: As Maria's UX family grows, she receives join requests and playbook submissions to review.

#### Screen: FOB Family Admin Dashboard - UX Family
Maria navigates to **Families → UX → Admin Panel**:
- **Overview tab**:
  - Members: 3 (Maria + 2 auto-joins)
  - Pending join requests: 2 (badge notification)
  - Playbooks: 0 (none submitted yet)
  - Activity: Recent joins, no submissions
- **Tabs**: Overview, Members, Playbooks, Settings

#### Screen: FOB Join Requests Tab
Maria clicks **Members tab → Join Requests (2)**:
- List of pending requests:
  
**Request 1**:
  - User: Alex Thompson (alex@design.io)
  - Requested: 2 hours ago
  - Message: "Hi! I'm a UX researcher interested in joining your methodology community."
  - Actions: [Approve] [Reject] [Message]
  
**Request 2**:
  - User: Spam Bot (spam@bot.com)
  - Requested: 5 minutes ago
  - Message: "CHECK OUT MY LINKS!!!"
  - Actions: [Approve] [Reject] [Message]

#### Action: Approve Legitimate Request
Maria reviews Alex's profile:
- Clicks on Alex's name → sees profile summary
- Clicks [Approve] button

#### Modal: Confirm Approval
- "Approve Alex Thompson's join request?"
- "They will immediately get access to all family playbooks"
- [Cancel] [Confirm]

Maria confirms. Alex receives notification and is added to the family.

#### Action: Reject Spam Request
Maria clicks [Reject] on spam bot request:
- Modal: "Reject this join request?"
- Optional: "Reason for rejection" (sent to user)
- Option: "Block user from future requests"
- [Cancel] [Reject]

**Result**: Maria manages her family membership actively, maintaining quality.

#### Screen: FOB Playbook Submissions (Future Scenario)
When someone submits a playbook to Maria's family:
- **Playbooks tab → Pending Submissions (1)**:
  - Playbook: "Information Architecture Patterns" by Tom
  - Submitted: 1 day ago
  - Description, preview structure
  - Actions: [Preview Full] [Approve] [Request Changes] [Reject]

#### Action: Review Playbook Submission
Maria clicks [Preview Full]:
- Modal opens showing complete playbook structure
- Activities, Artifacts, Goals all visible
- Maria can navigate the playbook
- Bottom actions: [Approve] [Request Changes] [Reject]

Maria clicks [Approve]:
- Confirmation modal: "Approve 'Information Architecture Patterns'?"
- "This playbook will be available to all UX family members"
- [Cancel] [Confirm]

Approved. Tom receives notification, playbook activates in family.

**Result**: Family head admins have full control over membership and content quality through custom FOB screens.

---

### Act 3: First Sync - Discovering Mike's Playbook

**Context**: Maria wants to download Mike's React playbook to use in her current project. She says in her Windsurf: "Open FOB Command Center." System opens local Django web app with GUI for the local FOB.

#### Screen: FOB Sync Dashboard
Maria clicks "Sync with Homebase" from the dashboard. The sync operation starts:
- FOB connects to Homebase using her authentication token
- Status: "Checking for updates..."
- Homebase reports available playbooks from her families

**Note**: Sync requires active Homebase connection with valid token. If disconnected, the Sync button would be disabled with tooltip: "Connect to Homebase in Settings to enable sync."

#### Screen: FOB Available Playbooks
After sync completes, Maria sees a list of playbooks she's entitled to:
- "React Frontend Development" (Usability family) - v1.0 by Mike Chen
- 7 other playbooks from Usability family
- Status: Not downloaded

#### Screen: FOB Playbook Preview
Maria clicks on "React Frontend Development" to preview:
- Shows playbook structure (Activities, Artifacts, Goals)
- Description and author information
- Version history
- "Download to FOB" button

#### Action: FOB Download Playbook (Clean Sync - No Conflicts)
Maria clicks "Download to FOB":
- Progress indicator shows download
- Playbook is added to her local graph
- Success message: "React Frontend Development v1.0 downloaded"

**Result**: Mike's playbook is now available in Maria's FOB for offline use.

---

### Act 3.1: Upload Playbook from JSON

**Context**: Maria has a playbook exported as JSON (from another FOB instance or a backup) and wants to import it into her FOB.

#### Screen: FOB Playbooks List
Maria navigates to the Playbooks page and sees:
- List of downloaded playbooks
- "Sync with Homebase" button
- **"Upload Playbook" button** (new)

#### Action: Click Upload Playbook
Maria clicks "Upload Playbook":
- File upload modal appears

#### Modal: FOB Upload Playbook
Upload dialog shows:
- **File Upload Area**: "Drop JSON file here or click to browse"
- Accepted format: `.json` files only
- Example: `playbook_react_frontend_v1.0.json`
- **Note**: "Playbook JSON must follow Mimir schema"
- [Cancel] [Upload] (disabled until file selected)

#### Action: Select and Upload JSON File
Maria selects a JSON file from her computer:
- File name appears: `ux_research_playbook_v2.1.json`
- [Upload] button becomes active
- Maria clicks [Upload]

#### Screen: FOB Upload Validation
System validates the JSON:
- **Checking**: "Validating playbook structure..."
- Validates:
  - Required fields (id, name, description, activities, etc.)
  - Schema compliance
  - Version format
  - Dependencies

**Success Path**:
- ✓ Validation successful
- Shows preview:
  - Playbook Name: "UX Research Methodology"
  - Version: 2.1
  - Activities: 12
  - Artifacts: 8
  - Author: Maria Rodriguez
- Message: "This playbook will be added to your local FOB"
- [Cancel] [Import Playbook]

**Error Path** (if validation fails):
- ✗ Validation failed
- Error message: "Invalid playbook format: Missing required field 'activities'"
- [Close] [Try Another File]

#### Action: Import Playbook
Maria clicks [Import Playbook]:
- Progress: "Importing playbook..."
- Playbook added to local graph
- Success notification: "UX Research Methodology v2.1 imported successfully"

#### Screen: FOB Playbooks List (Updated)
Maria sees the imported playbook in her list:
- **UX Research Methodology** v2.1
- Status: Local (not synced to Homebase)
- Source: Imported from JSON
- Author: Maria Rodriguez
- Actions: [View] [Edit] [Delete] [Export]

**Result**: Maria successfully imported a playbook from JSON and can now use it locally.

---

### Act 3.5: Exploring Playbook Details

**Context**: Maria wants to explore the React playbook structure in detail before using it.

#### Screen: FOB Playbook Detail - Overview
Maria clicks on "React Frontend Development" playbook card:
- **Header**:
  - Playbook name and description
  - Version: v1.0
  - Author: Mike Chen (Usability family)
  - Status: Active
  - Actions: [Activate] [Disable] [Export] [...More]
- **Tabs**: Overview, Activities, Artifacts, Goals, History, Settings
- **Overview tab** shows:
  - Quick stats: 3 Activities, 3 Artifacts, 2 Goals
  - Workflow diagram (visual graph)
  - Recent activity timeline
  - Connected work items (0) - Links to external GitHub issues/Jira tickets if configured with external MCP

#### Screen: FOB Playbook Detail - Activities Tab
Maria clicks **Activities tab**:
- List of all activities in sequence:
  1. ✓ Setup Project (Completed in MIMR-47)
  2. Create Components → (Next step)
  3. Implement State Management → (Blocked by #2)
- Each activity card shows:
  - Name and description
  - Upstream/downstream dependencies
  - Status indicators
  - [View Details] button

#### Screen: FOB Activity Detail Modal
Maria clicks [View Details] on "Create Components":
- Modal opens showing full activity information:
  - **Description**: Detailed steps for component creation
  - **Checklist**: 
    - [ ] Set up component folder structure
    - [ ] Create base component templates
    - [ ] Add prop validation
    - [ ] Write component tests
  - **Upstream**: Setup Project
  - **Downstream**: Implement State Management
  - **Artifacts**: Component Library (linked)
  - **Related work items**: (empty) - Note: Links to external work items (GitHub issues, Jira tickets) if configured
  - Actions: [Create Work Item via MCP] [Close]

#### Screen: FOB Playbook Detail - History Tab
Maria clicks **History tab**:
- Version history timeline:
  - **v1.0** (current) - 2 weeks ago by Mike Chen
    - Initial release
    - 3 activities, 3 artifacts, 2 goals
  - **v0.9** (draft) - 3 weeks ago by Mike Chen
    - Pre-release testing
- Each version shows:
  - [View This Version] button
  - [Compare with Current] button

#### Screen: FOB Version Comparison
Maria clicks [Compare with Current] on v0.9:
- Split view showing differences:
  - Left: v0.9
  - Right: v1.0 (current)
  - Highlighting:
    - Added items (green)
    - Removed items (red)
    - Modified items (yellow)
  - Diff viewer for activity descriptions

**Result**: Maria has complete visibility into playbook structure, can drill into any element, and track version changes.

---

### Act 4: Working with MCP - Using the Playbook

**Context**: Maria is starting a new React project for a client and wants to use Mike's playbook as guidance.

#### Screen: FOB Playbook Activation
Maria opens her FOB dashboard and sees her downloaded playbooks:
- Clicks on "React Frontend Development"
- Clicks "Activate Playbook" button
- Confirmation: "React Frontend Development is now active"

After activation, her local MCP server (running in the FOB container) knows about the active playbook and will use it by default when Maria asks questions about activities, artifacts, goals, etc.

#### Interface: Windsurf/MCP Chat
Maria opens Windsurf IDE where MCP (Model Context Protocol) is configured to connect to her FOB container's MCP server. She types in the Windsurf Cascade chat:

```
> mimir: I'm starting a new React project. How do I set up the project structure?
```

#### MCP Response
The AI, now aware of the active playbook, responds with guidance from Mike's playbook:

```
Based on the "React Frontend Development" playbook, Activity 1: Setup Project:

1. Initialize project with Create React App or Vite
2. Set up folder structure:
   - /src/components (reusable UI components)
   - /src/pages (page-level components)
   - /src/hooks (custom hooks)
   - /src/state (state management)
3. Configure ESLint and Prettier
4. Set up testing environment (Jest + React Testing Library)

Upstream dependencies: None
Downstream activities: Create Components, Implement State Management

Would you like me to create a GitHub issue to track this setup work?
```

#### Action: Create Work Item via External MCP
Maria responds:

```
> mimir: Yes, create a GitHub issue for project setup
```

**Note**: Work item management is handled by **external 3rd party MCP servers** (GitHub MCP, Jira MCP, GitLab MCP, etc.), NOT Mimir's MCP server. Mimir's MCP provides playbook context and guidance, while external MCPs handle actual work item creation and tracking.

#### External GitHub MCP Creates Work Item
GitHub MCP server (configured in Maria's Windsurf alongside Mimir MCP) uses GitHub API to create an issue:
- **Repo**: maria/acme-dashboard
- **Issue #47**: "Setup React project structure per React Frontend Development playbook"
- **Body**: Includes checklist from the playbook Activity (context provided by Mimir MCP)
- **Labels**: setup, react, playbook
- Link returned to Maria

#### Interface: Windsurf/MCP - Continuing Work
Later that day, after completing some work, Maria asks her AI (which coordinates between Mimir MCP for playbook context and GitHub MCP for work item data):

```
> mimir: Let's pick up MIMR-47 - assess the codebase and identify what's next per React Frontend Development playbook? What do we do next?
```

#### MCP Response - Context-Aware Guidance
```
Checking MIMR-47 status... (querying GitHub MCP) Project structure is set up.

According to "React Frontend Development" playbook (from Mimir MCP), next activity is:
Activity 2: Create Components

Current status: Ready to start component development
Downstream activities: Implement State Management, Add Testing

Would you like me to:
1. Show the full Component Creation activity details? (from Mimir MCP)
2. Create a new issue for component development? (via GitHub MCP)
3. Open the playbook in the web interface to see the full workflow? (via Mimir MCP)
```

#### Action: Navigate to Playbook Detail
Maria wants to see the complete workflow:

```
> mimir: Open the playbook in the web interface to see the full workflow
```

#### Screen: FOB Playbook Detail (Auto-Opened)
MCP sends a command to open Maria's browser:
- URL: `http://localhost:8000/playbooks/react-frontend-dev/workflow`
- Browser opens to FOB web GUI showing the complete workflow diagram
- Activity 1 "Setup Project" is marked complete (linked to MIMR-47)
- Activity 2 "Create Components" is highlighted as next step
- Full dependency graph visible

#### Interface: Windsurf/MCP - AI-Initiated PIP
After Maria completes several components and commits the work, the AI observes patterns:

```
✓ MIMR-47 completed: Project setup done
✓ Components created: Button, Card, Modal
✓ Committed to main branch

I notice you're creating modals but the playbook doesn't mention accessibility considerations for focus trapping in modals. Based on your work patterns, I think we should update the "Create Components" activity to include accessibility guidelines.

Would you like me to submit a PIP to add:
- Focus trap implementation for modals
- Keyboard navigation guidelines
- ARIA attribute checklist

This would go in "React Frontend Development" playbook, Activity 2: Create Components.
```

#### Action: Approve AI PIP Submission
Maria responds:

```
> mimir: Yes, great idea! Submit the PIP for accessibility in components
```

#### Screen: FOB PIP Created Notification
FOB GUI shows notification:
- "AI submitted PIP: Add Accessibility Guidelines to Component Creation"
- "Status: Draft (local only)"
- "Review and approve to apply locally"

**Result**: Maria is following Mike's playbook methodology with AI assistance that learns from her work patterns and proactively suggests improvements.

---

### Act 5: Evolving Playbooks - Creating PIPs

**Context**: While using Mike's playbook, Maria notices it could be improved with accessibility considerations.

#### Interface: Windsurf/MCP - Suggesting Improvement
Maria continues working in Windsurf and has an insight. She asks her MCP-connected AI assistant:

```
> mimir: This playbook is great, but it doesn't mention accessibility testing. 
  I think we should add an Activity for "Accessibility Audit" after the testing setup. 
  Can you help me create a PIP for this?
```

#### MCP Response - PIP Creation Assistance
```
I'll help you create a Playbook Improvement Proposal (PIP). 

Proposed PIP:
- Type: Extension (new Activity)
- Activity Name: "Accessibility Audit"
- Description: "Ensure React components meet WCAG 2.1 AA standards"
- Position: After "Set up testing environment"
- Upstream: Activity "Setup Project" 
- Downstream: Activity "Create Components"
- Includes: 
  - Install axe-core and jest-axe
  - Add accessibility tests to component test suite
  - Configure automated a11y checks in CI/CD

Shall I create this PIP in your local FOB?
```

#### Action: Create PIP
Maria confirms:

```
> mimir: Yes, create the PIP
```

#### Screen: FOB PIP Created Notification
FOB GUI shows a notification:
- "New PIP created: Add Accessibility Audit activity"
- "Status: Draft (local only)"
- "View PIP" link

#### Screen: FOB PIP Review Interface
Maria clicks "View PIP" and sees the PIP details:
- Shows the proposed changes in a diff-like view
- Original playbook structure vs. proposed structure
- Fields for rationale and implementation notes
- Actions: "Approve", "Edit", "Reject"

#### Action: Approve PIP Locally
Maria reviews the PIP and thinks it's good:
- Clicks "Approve" button
- Modal: "This PIP is approved locally. Your FOB now uses version 1.1 (local). To contribute back to the original playbook, sync with Homebase."
- The playbook version updates to v1.1 (local) in her FOB

**Result**: Maria has an improved version of the playbook locally, ready to share back with Mike and the community.

---

### Act 6: Sharing knowledge (Sync Scenarios) - Upload, Updates, and Conflicts

**Context**: Maria's workflow involves several sync operations, each demonstrating different scenarios.

#### Scenario A: Clean Upload with PIP Generation

**Context**: Maria wants to contribute her accessibility improvement back to Mike's playbook.

##### Screen: FOB Sync Dashboard
Maria clicks "Sync with Homebase":
- FOB connects to Homebase using her authentication token
- Analyzes local changes
- Detects: "React Frontend Development v1.1 (local) differs from v1.0 (remote)"

##### Screen: FOB Sync Analysis
System shows:
- **Local version**: v1.1 with Accessibility Audit activity
- **Remote version**: v1.0 (unchanged)
- **Recommendation**: "Upload your improvements as a PIP"
- Button: "Generate PIP for Homebase"

##### Action: Upload PIP
Maria clicks "Generate PIP for Homebase":
- System creates a PIP package with her changes
- Shows preview: "PIP: Add Accessibility Audit to React Frontend Development"
- "Submit to Homebase" button

Maria clicks "Submit to Homebase":
- PIP uploaded successfully
- Notification sent to Mike (original author) and Usability family admins
- Message: "Your PIP has been submitted for review"

**Result**: Mike will receive a notification about Maria's proposed improvement.

---

#### Scenario B: Clean Download - No Conflicts

**Context**: A week later, Maria checks for updates to other playbooks.

##### Screen: FOB Sync Dashboard
Maria initiates another sync:
- FOB connects to Homebase
- Checks all her entitled playbooks
- Finds: "UX Research Methods v2.3 available (not downloaded)"

##### Screen: FOB Available Updates
Maria sees:
- New playbook available from Usability family
- No conflicts with local playbooks
- "Download" button

##### Action: Simple Download
Maria clicks "Download":
- Progress bar shows download
- Success: "UX Research Methods v2.3 downloaded"
- No conflicts, no decisions needed

**Result**: New playbook added to Maria's FOB seamlessly.

---

#### Scenario C: Conflict Resolution - Remote Wins

**Context**: Meanwhile, Mike approved Maria's PIP and released React Frontend Development v1.2. Maria also made local changes to v1.1.

##### Screen: FOB Sync Dashboard - Conflict Detected
Maria syncs again:
- FOB detects: "React Frontend Development - Version conflict"
- Local: v1.1 (with Maria's local changes)
- Remote: v1.2 (Mike released an update incorporating Maria's PIP + his own changes)

##### Screen: FOB Conflict Resolution Interface
System shows the conflict:
- **Local version**: v1.1 (Maria's local experimental changes)
- **Remote version**: v1.2 (official release with Maria's PIP + Mike's updates)
- **Changes**:
  - Local: Maria added a "Performance Optimization" activity (not yet submitted)
  - Remote: Mike incorporated Maria's Accessibility PIP + added "Error Boundary Patterns"

##### Modal: Conflict Resolution Options
Message: "Conflict detected. Choose how to proceed:"
- Option 1: **Keep Remote** (recommended) - "Overwrite local with v1.2, losing your uncommitted changes"
- Option 2: **Keep Local** - "Stay on v1.1, don't download updates"
- Warning: "No automatic merging available yet"

##### Action: Choose Remote Version
Maria decides the official version is more valuable:
- Selects "Keep Remote"
- Confirms in confirmation modal
- Her Performance Optimization work is saved as a draft PIP for later submission

##### Result: Version Updated
- Local playbook updated to v1.2 (matches remote)
- Maria's uncommitted changes saved as draft PIP
- Notification: "You can review your draft PIP and submit it when ready"

**Result**: Maria now has the latest official version and can resubmit her additional improvements later.

---

#### Scenario D: Download Playbook as JSON (Export)

**Context**: Maria wants to backup her locally created playbook or share it with a colleague who doesn't have Homebase access.

##### Screen: FOB Playbook Detail - Author View
Maria views one of her authored playbooks:
- **UX Research Methodology** v2.1
- Author: Maria Rodriguez (Local)
- **Note**: Download button is only visible if:
  - User is the original author, OR
  - Playbook is locally created (meaning user is author)

##### Action: Click Download/Export
Maria clicks the [Export] button in the playbook actions menu:
- **Icon**: Download icon (fa-download)
- **Tooltip**: "Download this playbook as JSON file for backup or sharing"

##### Modal: FOB Export Playbook
Export dialog shows:
- **Playbook**: UX Research Methodology v2.1
- **Export Options**:
  - ☑ Include version history
  - ☑ Include metadata (author, timestamps)
  - ☐ Include local PIPs (if any)
- **File Format**: JSON
- **Filename**: `ux_research_methodology_v2.1.json` (editable)
- [Cancel] [Download JSON]

##### Action: Download JSON
Maria clicks [Download JSON]:
- Browser downloads file: `ux_research_methodology_v2.1.json`
- Success notification: "Playbook exported successfully"
- File size shown: ~45 KB

##### Downloaded JSON Structure (Example)
```json
{
  "schema_version": "1.0",
  "playbook": {
    "id": "ux-research-methodology",
    "name": "UX Research Methodology",
    "version": "2.1",
    "description": "Comprehensive guide to UX research...",
    "author": {
      "name": "Maria Rodriguez",
      "email": "maria@uxconsulting.com"
    },
    "created_at": "2024-11-15T10:30:00Z",
    "updated_at": "2024-11-20T14:22:00Z",
    "activities": [
      {
        "id": "define-research-questions",
        "name": "Define Research Questions",
        "description": "...",
        "upstream_dependencies": [],
        "downstream_dependencies": ["recruit-participants"]
      }
    ],
    "artifacts": [...],
    "goals": [...]
  }
}
```

##### Use Cases for Exported JSON:
1. **Backup**: Save local copy before making major changes
2. **Share offline**: Send to colleague via email/file share
3. **Import to another FOB**: Colleague can import using Act 3.1 Upload feature
4. **Version control**: Store in Git repository
5. **Migration**: Move playbook to different FOB instance

##### Permissions Note:
**Download button NOT visible** if:
- User is not the author
- Playbook is synced from Homebase (authored by someone else)
- User only has read access to the playbook

**Download button IS visible** if:
- User is the original author
- Playbook was created locally by this user
- Playbook was imported from JSON by this user (becomes author)

**Result**: Maria has a portable JSON backup of her playbook that can be imported into any FOB instance.

---

### Act 7: Creating Original Content - Multiple Playbooks

**Context**: Maria wants to create her own playbooks for different purposes: personal goals, community sharing, and client work.

#### Playbook 1: Private Personal Playbook

**Context**: Maria wants to track her personal career goals privately.

##### Screen: FOB Create Playbook - Home Dashboard
Maria clicks "Create New Playbook" from FOB dashboard.

##### Screen: FOB Playbook Creation Wizard - Step 1: Basic Info
Maria fills out:
- **Name**: "My Goals"
- **Description**: "Personal and professional development goals for 2024"
- **Category**: Personal
- Click "Next"

##### Screen: FOB Playbook Editor
Maria builds her playbook structure:
- Adds Goals: "Learn Three.js", "Speak at UX conference", "Publish case study"
- Adds Activities: "Weekly learning blocks", "Draft talk proposal", "Document project"
- Links them together in sequence

##### Screen: FOB Playbook Creation - Step 2: Publishing
Maria chooses visibility:
- **Visibility**: Private (only visible to me)
- **Location**: Local FOB only (not uploaded to Homebase)
- Click "Create Playbook"

**Result**: Maria has a private playbook for personal use, never shared with anyone.

---

#### Playbook 2: Family Playbook from Notes

**Context**: Maria has extensive notes about UX methodologies she wants to formalize and share with her UX family.

##### Screen: FOB Create Playbook - Import from Notes
Maria clicks "Create New Playbook" → "Import from Notes"

##### Screen: FOB Note Import Interface
Maria pastes her markdown notes containing:
- User research techniques
- Wireframing approaches
- Usability testing procedures
- Design system documentation

##### Screen: FOB AI-Assisted Structure
System analyzes her notes and suggests structure:
- Detected Activities: 12 activities
- Detected Artifacts: 8 artifacts
- Detected Goals: 5 goals
- Shows preview of extracted structure
- "Review and Edit" button

##### Action: Review and Finalize
Maria reviews the auto-generated structure:
- Adjusts some activity dependencies
- Adds missing links
- Enriches descriptions

##### Screen: FOB Playbook Creation - Publishing
Maria configures:
- **Name**: "UX"
- **Description**: "Comprehensive UX methodology from research to validation"
- **Visibility**: Family - "UX" (her public family)
- **Location**: Upload to Homebase
- Clicks "Create and Publish"

##### Screen: FOB Upload to Homebase
- Progress: "Uploading playbook to Homebase..."
- Success: "Playbook published to UX family"
- Notification sent to all UX family members
- Maria retains ownership as family admin

**Result**: Maria's UX playbook is now available to all members of her UX family community.

---

#### Playbook 3: Hidden Family - Client Playbook

**Context**: Maria wants to create a customized UX consulting playbook specifically for her Acme, INC client work.

##### Screen: FOB Create Playbook - Professional Template
Maria starts with:
- **Template**: "Consulting Project" (pre-built structure)
- **Name**: "UX Consulting"
- **Description**: "Tailored UX consulting methodology for enterprise clients"

##### Screen: FOB Playbook Editor - Customization
Maria customizes the template:
- Adds Activities specific to enterprise constraints
- Includes Artifacts: "Stakeholder Report", "Executive Summary", "ROI Analysis"
- Adds client-specific Goals and compliance requirements
- Structures delivery phases and milestones

##### Screen: FOB Playbook Creation - Publishing (Hidden Family)
Maria configures:
- **Visibility**: Family - "Acme, INC" (her hidden family)
- **Access**: Only members manually added by Maria
- **Confidentiality**: Marked as "Client Confidential"
- Clicks "Create and Publish"

##### Screen: FOB Manual Member Management
After creation, Maria manages the hidden family:
- Goes to "Acme, INC" family settings
- Manually adds her team members:
  - sarah@uxconsulting.com
  - james@uxconsulting.com
- They receive email invitations
- Playbook only visible after they accept and join

**Result**: Maria has a confidential playbook shared only with her specific consulting team for Acme client work.

---

#### Playbook 4: MCP-Driven Playbook Creation

**Context**: Maria wants to quickly create a playbook for design system documentation using MCP commands.

##### Interface: Windsurf/MCP - Create Playbook via Chat
Maria uses MCP to create a new playbook without opening the GUI:

```
> mimir: Create a new playbook called "Design System Management" with these activities:
  1. Establish design tokens
  2. Create component library
  3. Document usage guidelines
  4. Maintain versioning
  Make it private, keep it local only.
```

##### MCP Response - Playbook Created
```
✓ Created playbook: "Design System Management"
✓ Added 4 activities with dependencies
✓ Visibility: Private (local only)
✓ Status: Active on your FOB

Playbook ID: ds-mgmt-001
You can view it in FOB GUI or continue editing via MCP.

Would you like me to add artifacts or goals to this playbook?
```

##### Action: Add Content via MCP
Maria continues:

```
> mimir: Add artifact "Token Library" to activity 1, and goal "Consistent UI across products"
```

**Result**: Maria created a complete playbook structure via MCP without touching the GUI.

---

#### Playbook Lifecycle Management

**Context**: Maria wants to manage her growing collection of playbooks - some need to be temporarily disabled, others are outdated.

##### Screen: FOB Playbook Library
Maria opens her playbook library and sees all her playbooks with status indicators:
- React Frontend Development (Active, Downloaded)
- UX (Active, Owned)
- UX Consulting (Active, Owned)
- My Goals (Active, Private)
- Design System Management (Active, Private)
- Old Frontend Patterns v1 (Active, Downloaded - outdated)

##### Action: Disable Outdated Playbook
Maria right-clicks "Old Frontend Patterns v1":
- Select "Disable Playbook"
- Confirmation: "This playbook will remain in your FOB but won't appear in searches or MCP suggestions. You can re-enable it later."
- Clicks "Disable"

**Result**: Playbook is hidden from UI but remains in local graph. Can be re-enabled anytime.

##### Action: Delete Personal Experiment
Maria has a test playbook "Test Playbook 123" she no longer needs:
- Selects "Test Playbook 123"
- Clicks "Delete"
- Warning: "This will permanently remove the playbook from your FOB. This cannot be undone."
- Confirms deletion

**Result**: Playbook completely removed from local graph.

---

#### Playbook Authorship Transfer

**Context**: Maria created a comprehensive design system playbook for Acme. The project is ending, and Acme wants to own the playbook IP.

##### Screen: FOB Playbook Settings
Maria opens "UX Consulting" playbook settings:
- Current Owner: Maria Rodriguez
- Family: Acme, INC (hidden)
- Clicks "Transfer Ownership"

##### Screen: FOB Transfer Ownership Dialog
Maria sees the transfer interface:
- **Transfer to**: sarah@uxconsulting.com (Acme's design lead)
- **Transfer type**: Full ownership (cannot be reversed)
- Warning: "You will lose all admin rights to this playbook. The new owner can modify, delete, or restrict your access."
- Acknowledgment checkbox: "I understand this is like selling the playbook - ownership transfers completely"
- Clicks "Transfer Ownership"

##### Action: Confirm Transfer
Confirmation modal:
- "Are you sure you want to transfer 'UX Consulting' to sarah@uxconsulting.com?"
- "You will no longer be able to edit or manage this playbook"
- Maria confirms

##### Screen: HB Ownership Transfer Notification
Sarah receives notification:
- "Maria Rodriguez has transferred ownership of 'UX Consulting' playbook to you"
- "Accept Transfer" button

Sarah accepts, and the playbook ownership updates on Homebase.

**Result**: Sarah now owns the playbook. Maria can still use it (she's in the family) but cannot edit or manage it. This simulates "selling" IP to the client.

---

#### Offline Distribution Mode

**Context**: Maria's colleague Alex doesn't have Homebase access but needs Maria's UX playbook for an offline workshop.

##### Screen: FOB Playbook Export
Maria selects her "UX" playbook:
- Clicks "Export" → "Dump to File"
- Modal shows export options:
  - **Format**: Mimir Playbook Archive (.mpa)
  - **Include**: Full playbook with all activities, artifacts, goals
  - **Encryption**: Optional password protection
  - **Save location**: Browse for folder

##### Action: Create Playbook Dump
Maria exports:
- Filename: `ux-methodology-v1.2.mpa`
- No password (Alex is trusted)
- Saved to ~/Downloads/

Maria emails the .mpa file to Alex.

##### Screen: FOB Import from Dump (Alex's FOB)
Alex receives the file and opens his FOB:
- Clicks "Import" → "Load from Dump"
- Selects `ux-methodology-v1.2.mpa`
- Import wizard shows:
  - Playbook: "UX" v1.2
  - Author: Maria Rodriguez
  - Activities: 12, Artifacts: 8, Goals: 5
  - "Import to FOB" button

Alex clicks import, and the playbook is added to his local FOB (offline, no Homebase connection needed).

**Result**: Playbooks can be distributed via file dumps for offline/air-gapped environments.

---

#### Family Dynamics: Member Removal Consequences

**Context**: Maria's UX family has grown. One member, Tom, contributed valuable playbooks but violated community guidelines. Maria must remove him.

##### Screen: FOB Family Management - UX Family
Maria opens her UX family admin panel:
- Members: 24 members
- Playbooks: 6 playbooks (3 by Maria, 2 by Tom, 1 by others)
- Sees Tom's profile with "Remove from Family" button

##### Screen: FOB Member Removal Warning
Maria clicks "Remove Tom":
- Warning modal appears:
  - "Tom has contributed 2 playbooks to this family:"
    - "Interaction Design Patterns"
    - "User Testing Framework"
  - "When you remove Tom, his playbooks will be recalled from the family"
  - "All family members will lose access on their next sync"
  - "This action cannot be undone - you'll lose this knowledge unless Tom rejoins"
  - Checkbox: "I understand we're losing Tom's contributed playbooks"

##### Action: Confirm Removal
Maria confirms the removal.

##### Screen: HB Family Playbook Recall
On Homebase, Tom's playbooks are marked:
- Status: "Recalled by author (removed from family)"
- Family members will see update on next sync

##### Screen: FOB Sync - Forced Removal (Other Members)
When other UX family members sync:
- Notification: "2 playbooks have been removed by their authors:"
  - "Interaction Design Patterns" (by Tom)
  - "User Testing Framework" (by Tom)
- "These playbooks will be deleted from your FOB"
- Confirmation required to proceed with sync

**Result**: Removing a member means losing their intellectual contributions. The family pays the price of knowledge loss. This creates strong incentive to resolve conflicts rather than kick people out.

---

#### Family Admin Advanced Management

**Context**: Maria's UX family continues to grow. She needs to delegate some responsibilities and prepare for scaling.

##### Screen: FOB Family Settings - UX Family
Maria opens advanced family settings:
- Current admin: Maria Rodriguez
- Members: 24
- Pending join requests: 3
- Active playbooks: 4 (after Tom's removal)

##### Action: Transfer Admin Role
Maria decides to make Sarah a co-admin:
- Clicks "Transfer Admin Rights"
- Selects sarah@uxconsulting.com
- Options:
  - **Transfer Type**: Make co-admin (Maria retains admin) OR Full transfer (Maria loses admin)
  - Maria selects: "Full Transfer" (she's focusing on client work)
- Confirmation: "You will no longer have admin rights. Sarah will control all family settings, memberships, and playbook approvals."

Maria confirms. Sarah becomes the UX family admin.

##### Action: Deactivate Family (Hypothetical Scenario)
If Maria were to deactivate the family (she didn't, but the feature exists):
- "Deactivate Family" button in danger zone
- Warning: "Family will be hidden from all listings. All family playbooks will be force-removed from member FOBs on next sync. Members keep their memberships but family becomes dormant."
- Use case: Temporary pause or sunset of the community

**Result**: Full lifecycle management capabilities for family admins - delegate, transfer, or wind down families as needed.

---

### Act 8: Settings & Preferences

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

**Result**: Maria has full control over FOB behavior and preferences.

---

### Act 9: Error Recovery & Edge Cases

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

## Journey Complete

Maria's journey demonstrates the full Mimir experience:

✅ **Authenticated** - Logged into both HB and FOB systems with proper authentication flows  
✅ **Navigated** - Used persistent top nav, sidebar, notification center, and global search  
✅ **Onboarded** - Registered and set up FOB container with MCP integration  
✅ **Networked** - Created families (public and hidden) and joined existing communities  
✅ **Administered Families** - Reviewed join requests, approved members, managed playbook submissions through custom FOB screens  
✅ **Discovered** - Found and downloaded community playbooks with HB Django Admin approval workflow  
✅ **Explored** - Drilled into playbook details (activities, artifacts, goals), viewed version history, compared versions  
✅ **Used** - Worked with playbooks via Mimir MCP in Windsurf; created and tracked work items via external 3rd party MCPs (GitHub, Jira, etc.)  
✅ **Navigated Playbooks** - Used MCP to auto-open playbook details in web interface  
✅ **Contributed** - Created PIPs (user-initiated and AI-initiated) and shared improvements  
✅ **Synced** - Handled clean downloads, uploads, and conflicts with version management  
✅ **Created** - Built playbooks via GUI and MCP with varying visibility levels  
✅ **Managed Lifecycle** - Enabled, disabled, and deleted playbooks  
✅ **Transferred Ownership** - "Sold" playbook IP to client via authorship transfer  
✅ **Distributed Offline** - Exported/imported playbooks as .mpa dumps for air-gapped environments  
✅ **Configured** - Set up sync preferences, storage, MCP settings, notifications  
✅ **Recovered from Errors** - Handled network failures, permission errors, upload failures, data corruption  

Maria experienced critical scenarios:
- **Admin approval**: Mike's playbook went through Homebase admin review before publication
- **AI collaboration**: AI proactively suggested PIPs based on Maria's work patterns
- **Knowledge loss**: Removing Tom from the family resulted in losing his 2 contributed playbooks
- **Ownership economics**: Transferred "UX Consulting" playbook to client, simulating IP sale
- **Offline resilience**: Distributed playbooks via file dumps without Homebase dependency

Maria now manages:
- 2 private personal playbooks (My Goals, Design System Management)
- 1 public family playbook (UX community) - admin transferred to Sarah
- 1 transferred playbook (UX Consulting - now owned by Acme's Sarah)
- Multiple downloaded community playbooks (some active, some disabled)

She actively participates in the Usability family, transferred leadership of her UX family to Sarah, and continues contributing to the community's collective knowledge while understanding the real consequences of family dynamics and knowledge ownership.
