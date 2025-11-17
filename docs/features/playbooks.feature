# Feature: PB - Playbook Management
# Icon: fa-book-sparkles
# Prefix: PB (Playbooks)
#
# Feature Specification:
# Alex Chen (Software Engineering Team Lead) wants to browse, create, and manage
# engineering playbooks in their FOB instance so they can standardize practices
# across their team and evolve them based on retrospectives and PIPs.
#
# Context: Engineering teams need living documentation of their practices that can
# be queried by AI assistants and updated based on feedback. The playbook system
# provides a UI for managing these playbooks before they're fully implemented with
# backend persistence.
#
# Affected Components:
# - New: /playbooks/ routes and views
# - Modified: templates/base.html (navbar)
# - Modified: templates/methodology/index.html (home page links)
# - New: templates/playbooks/*.html (list, detail, form, 404)
#
# Available Resources:
# - Bootstrap 5.3.8 for UI components
# - Font Awesome Pro (kit 600fa45ed9.js) for icons
# - Django templates with base.html layout
# - @login_required decorator for auth
#
# What We're Building:
# - Playbook list view (card grid with search/filter)
# - Playbook detail view (read-only display)
# - Playbook add form (tabbed, full page)
# - Playbook edit form (same as add, pre-filled)
# - 404 handling for non-existent playbooks

@core @ui-prototype
Feature: PB - Engineering Playbook Management

  Background:
    Given Alex Chen is logged in as "admin" with password "admin"
    And the following playbooks exist in the system:
      | ID        | Name                      | Family        | Type        | Status | Author                    |
      | AGILE-01  | Agile Development         | Development   | Methodology | Active | Ken Schwaber & Jeff Sutherland |
      | SCRUM-01  | Scrum Framework           | Development   | Framework   | Active | Scrum Alliance            |
      | TDD-01    | Test-Driven Development   | Testing       | Practice    | Active | Kent Beck                 |
      | DEVOPS-01 | DevOps Practices          | Operations    | Practice    | Active | DevOps Institute          |
      | DDD-01    | Domain-Driven Design      | Architecture  | Methodology | Active | Eric Evans                |
      | LEAN-01   | Lean Software Development | Development   | Methodology | Draft  | Mary & Tom Poppendieck    |

  # ═══════════════════════════════════════════════════════════════════
  # Scenario Group 1: Browse and Search Playbooks
  # ═══════════════════════════════════════════════════════════════════

  @search
  Scenario: PB-1.1 View all playbooks in card grid layout
    Given Alex is on the home page at "/"
    When Alex clicks the "Playbooks" link in the navigation bar
    Then Alex should be redirected to "/playbooks/"
    And Alex should see the page title "Playbooks"
    And Alex should see a search bar with placeholder "Search playbooks..."
    And Alex should see a family filter dropdown showing "All Families"
    And Alex should see an "Add Playbook" button with icon "fa-plus"
    And Alex should see 6 playbook cards in a grid layout
    And each card should display:
      | Field       | Example Value            |
      | ID badge    | AGILE-01                |
      | Name        | Agile Development       |
      | Type badge  | Methodology             |
      | Status      | Active (green badge)    |
      | Description | First 120 characters... |
      | Family      | Development             |
      | Author      | Ken Schwaber & Jeff...  |

  @search
  Scenario: PB-1.2 Search playbooks by name
    Given Alex is on the playbooks list page at "/playbooks/"
    When Alex enters "Test" into the search bar
    Then Alex should see only 1 playbook card
    And the card should be for playbook "TDD-01"
    And the card title should highlight "Test" in "Test-Driven Development"

  @search @filter
  Scenario: PB-1.3 Filter playbooks by family
    Given Alex is on the playbooks list page at "/playbooks/"
    When Alex selects "Testing" from the family filter dropdown
    Then Alex should see only 1 playbook card
    And the card should be for playbook "TDD-01"
    And the filter dropdown should display "Testing" as selected

  @search
  Scenario: PB-1.4 Search with no results shows empty state
    Given Alex is on the playbooks list page at "/playbooks/"
    When Alex enters "NonExistentPlaybook" into the search bar
    Then Alex should see an empty state message:
      """
      No playbooks found matching your criteria.
      Try adjusting your search or filter.
      """
    And Alex should see a "Clear Filters" button with icon "fa-times-circle"

  # ═══════════════════════════════════════════════════════════════════
  # Scenario Group 2: View Playbook Details
  # ═══════════════════════════════════════════════════════════════════

  @detail-view
  Scenario: PB-2.1 View playbook details
    Given Alex is on the playbooks list page at "/playbooks/"
    When Alex clicks on the card for playbook "AGILE-01"
    Then Alex should be redirected to "/playbooks/AGILE-01/"
    And Alex should see breadcrumbs: "Home > Playbooks > Agile Development"
    And Alex should see the playbook ID badge "AGILE-01"
    And Alex should see the playbook name "Agile Development"
    And Alex should see the full description:
      """
      Iterative and incremental approach to software development emphasizing
      flexibility and customer collaboration.
      """
    And Alex should see a metadata section displaying:
      | Field      | Value                      |
      | Type       | Methodology                |
      | Family     | Development                |
      | Status     | Active (green badge)       |
      | Version    | 2.1                        |
      | Author     | Ken Schwaber & Jeff Sutherland |
      | Created    | 2024-01-15                 |
      | Updated    | 2024-11-10                 |
    And Alex should see action buttons:
      | Button Text | Icon       | Tooltip                          |
      | Edit        | fa-edit    | Edit this playbook               |
      | Back        | fa-arrow-left | Return to playbook list       |

  @detail-view @error
  Scenario: PB-2.2 View non-existent playbook shows 404
    Given Alex is logged in
    When Alex navigates to "/playbooks/NONEXISTENT-99/"
    Then Alex should see a 404 error page
    And Alex should see the message "Playbook Not Found"
    And Alex should see the playbook ID "NONEXISTENT-99" in the error message
    And Alex should see a "Back to Playbooks" button with icon "fa-list"

  # ═══════════════════════════════════════════════════════════════════
  # Scenario Group 3: Create New Playbook
  # ═══════════════════════════════════════════════════════════════════

  @create @form
  Scenario: PB-3.1 Open add playbook form
    Given Alex is on the playbooks list page at "/playbooks/"
    When Alex clicks the "Add Playbook" button
    Then Alex should be redirected to "/playbooks/add/"
    And Alex should see the page title "Add Playbook"
    And Alex should see a tabbed form with 4 tabs:
      | Tab Number | Tab Title      | Icon               |
      | 1          | Basic Info     | fa-info-circle     |
      | 2          | Classification | fa-tags            |
      | 3          | Metadata       | fa-file-alt        |
      | 4          | Relationships  | fa-project-diagram |
    And the "Basic Info" tab should be active
    And Alex should see form fields:
      | Field       | Type     | Required | Placeholder              |
      | ID          | text     | Yes      | e.g., AGILE-01           |
      | Name        | text     | Yes      | e.g., Agile Development  |
      | Description | textarea | Yes      | Describe the playbook... |
    And Alex should see action buttons at the bottom:
      | Button Text | Icon       | Tooltip                          | State    |
      | Cancel      | fa-times   | Discard changes and go back      | Enabled  |
      | Save        | fa-save    | Fill in required fields (ID, Name, Description) | Disabled |

  @create @form @navigation
  Scenario: PB-3.2 Navigate between form tabs
    Given Alex is on the add playbook form at "/playbooks/add/"
    And the "Basic Info" tab is active
    When Alex clicks the "Classification" tab
    Then the "Classification" tab should become active
    And the "Basic Info" tab should become inactive
    And Alex should see form fields:
      | Field  | Type   | Required | Options                               |
      | Family | select | No       | Development, Testing, Operations, Architecture, Design |
      | Type   | select | No       | Methodology, Framework, Practice      |
      | Status | select | No       | Draft, Active, Archived, Deprecated   |

  @create @form @validation
  Scenario: PB-3.3 Save button enables when required fields are filled
    Given Alex is on the add playbook form at "/playbooks/add/"
    And the "Save" button is disabled
    When Alex enters "KANBAN-01" into the "ID" field
    Then the "Save" button should remain disabled
    When Alex enters "Kanban Method" into the "Name" field
    Then the "Save" button should remain disabled
    When Alex enters "Visual workflow management system" into the "Description" field
    Then the "Save" button should become enabled
    And the "Save" button tooltip should change to "Save playbook"

  @create @form
  Scenario: PB-3.4 Submit new playbook form (prototype - shows success message)
    Given Alex is on the add playbook form at "/playbooks/add/"
    And Alex has filled in all required fields:
      | Field       | Value                              |
      | ID          | KANBAN-01                          |
      | Name        | Kanban Method                      |
      | Description | Visual workflow management system  |
    And Alex has selected:
      | Field  | Value       |
      | Family | Operations  |
      | Type   | Practice    |
      | Status | Active      |
    When Alex clicks the "Save" button
    Then a success message modal should appear:
      """
      Playbook Created (Prototype Mode)
      In production, playbook "KANBAN-01 - Kanban Method" would be saved.
      """
    And the modal should have an "OK" button with icon "fa-check"

  @create @form @cancel
  Scenario: PB-3.5 Cancel adding playbook shows confirmation
    Given Alex is on the add playbook form at "/playbooks/add/"
    And Alex has entered "KANBAN-01" into the "ID" field
    When Alex clicks the "Cancel" button
    Then a confirmation modal should appear:
      """
      Discard changes?
      You have unsaved changes. Are you sure you want to discard them?
      """
    And the modal should have buttons:
      | Button Text    | Icon       | Action                          |
      | Stay on Page   | fa-times   | Close modal, stay on form       |
      | Discard Changes| fa-check   | Go back to playbooks list       |

  # ═══════════════════════════════════════════════════════════════════
  # Scenario Group 4: Edit Existing Playbook
  # ═══════════════════════════════════════════════════════════════════

  @edit @form
  Scenario: PB-4.1 Open edit playbook form
    Given Alex is on the playbook detail page for "AGILE-01"
    When Alex clicks the "Edit" button
    Then Alex should be redirected to "/playbooks/AGILE-01/edit/"
    And Alex should see the page title "Edit Playbook: Agile Development"
    And Alex should see the same tabbed form as the add form
    And the form fields should be pre-filled with:
      | Field       | Value                                           |
      | ID          | AGILE-01                                        |
      | Name        | Agile Development                               |
      | Description | Iterative and incremental approach to software development emphasizing flexibility and customer collaboration. |
      | Family      | Development (selected)                          |
      | Type        | Methodology (selected)                          |
      | Status      | Active (selected)                               |
    And the "Save" button should be enabled with tooltip "Save changes to playbook"

  @edit @form
  Scenario: PB-4.2 Edit playbook and save (prototype - shows success message)
    Given Alex is on the edit form at "/playbooks/AGILE-01/edit/"
    When Alex changes the "Version" field from "2.1" to "2.2"
    And Alex adds " Updated for 2025." to the end of the description
    And Alex clicks the "Save" button
    Then a success message modal should appear:
      """
      Playbook Updated (Prototype Mode)
      In production, changes to "AGILE-01 - Agile Development" would be saved.
      """
    And the modal should have an "OK" button with icon "fa-check"

  @edit @form @error
  Scenario: PB-4.3 Edit non-existent playbook shows 404
    Given Alex is logged in
    When Alex navigates to "/playbooks/NONEXISTENT-99/edit/"
    Then Alex should see a 404 error page
    And Alex should see the message "Playbook Not Found"

  # ═══════════════════════════════════════════════════════════════════
  # Scenario Group 5: Navigation and Integration
  # ═══════════════════════════════════════════════════════════════════

  @navigation
  Scenario: PB-5.1 Access playbooks from home page
    Given Alex is on the home page at "/"
    When Alex clicks the "Explore Playbooks" button in the hero section
    Then Alex should be redirected to "/playbooks/"
    And Alex should see the playbooks list page

  @navigation
  Scenario: PB-5.2 Access playbooks from navbar
    Given Alex is on any page in the application
    When Alex clicks the "Playbooks" link in the navigation bar
    Then Alex should be redirected to "/playbooks/"
    And the "Playbooks" nav link should be highlighted as active

  @navigation @breadcrumbs
  Scenario: PB-5.3 Navigate using breadcrumbs
    Given Alex is on the playbook detail page for "AGILE-01"
    And Alex sees breadcrumbs: "Home > Playbooks > Agile Development"
    When Alex clicks "Playbooks" in the breadcrumbs
    Then Alex should be redirected to "/playbooks/"
    And Alex should see the playbooks list page

  # ═══════════════════════════════════════════════════════════════════
  # Scenario Group 6: Responsive Design and UI Polish
  # ═══════════════════════════════════════════════════════════════════

  @ui @tooltips
  Scenario: PB-6.1 All action buttons have tooltips
    Given Alex is on the playbooks list page at "/playbooks/"
    When Alex hovers over the "Add Playbook" button
    Then Alex should see a tooltip: "Create a new playbook"
    When Alex hovers over the search bar
    Then Alex should see a tooltip: "Search by playbook name or description"

  @ui @icons
  Scenario: PB-6.2 All buttons and links have Font Awesome Pro icons
    Given Alex is on any playbooks page
    Then every action button should have a Font Awesome icon
    And the icon should be semantically appropriate for the action
    And the following icons should be used:
      | Action         | Icon               |
      | Add Playbook   | fa-plus            |
      | Edit           | fa-edit            |
      | Back/Return    | fa-arrow-left      |
      | Search         | fa-search          |
      | Filter         | fa-filter          |
      | Save           | fa-save            |
      | Cancel         | fa-times           |
      | Playbooks Nav  | fa-book-sparkles   |

  @ui @responsive
  Scenario: PB-6.3 Card grid is responsive
    Given Alex is on the playbooks list page at "/playbooks/"
    When Alex resizes the browser to mobile width (< 768px)
    Then the cards should stack in a single column
    When Alex resizes the browser to tablet width (768px - 1024px)
    Then the cards should display in 2 columns
    When Alex resizes the browser to desktop width (> 1024px)
    Then the cards should display in 3 columns
