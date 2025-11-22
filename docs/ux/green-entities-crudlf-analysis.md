# Green Entities CRUDLF Analysis

## Domain Model Green Objects (Playbook Structure)

From the Domain Model diagram, we have **7 green entities**:

1. **Workflow** - Top-level container for organized activities
2. **Phase** - Organizational grouping within workflow
3. **Activity** - Individual actionable step  
4. **Artifact** - Output/deliverable produced by activities
5. **Goal** - Target outcomes achieved by workflows
6. **Howto** - Detailed instructions/guides for activities
7. **Role** - Performer/responsible party for activities

## CRUDLF Requirements

For each entity, we need:
- **C**reate - Add new instance
- **R**ead - View details
- **U**pdate - Edit existing
- **D**elete - Remove instance
- **L**ist - View all instances
- **F**ind - Search/filter instances

## Current MVP Coverage

### ✅ COVERED via MCP
All 7 green entities have MCP tool coverage:
- `@create_[entity]`
- `@get_[entity]_details` 
- `@update_[entity]`
- `@delete_[entity]`
- `@list_[entities]`
- `@find_[entities]`

### ⚠️ MISSING FOB Pages

#### Current FOB Pages (Generic):
- `FOB-CREATE-PLAYBOOK-1` - Creates entire playbook
- `FOB-WIZARD-BASIC-1` - Wizard for basic playbook setup
- `FOB-EDITOR-1` - General playbook editor
- `FOB-DETAIL-1` - Playbook overview/detail
- `FOB-PLAYBOOK-PREVIEW-1` - Preview before publishing

**Problem:** These are all **playbook-level** pages. No entity-specific CRUDLF pages.

## Missing FOB Pages by Entity

### 1. Workflow
- ❌ FOB-WORKFLOW-LIST
- ❌ FOB-WORKFLOW-CREATE  
- ❌ FOB-WORKFLOW-EDIT
- ❌ FOB-WORKFLOW-DETAIL
- ❌ FOB-WORKFLOW-DELETE (modal/confirmation)

### 2. Phase
- ❌ FOB-PHASE-LIST
- ❌ FOB-PHASE-CREATE
- ❌ FOB-PHASE-EDIT
- ❌ FOB-PHASE-DETAIL
- ❌ FOB-PHASE-DELETE (modal/confirmation)

### 3. Activity
- ❌ FOB-ACTIVITY-LIST
- ❌ FOB-ACTIVITY-CREATE
- ❌ FOB-ACTIVITY-EDIT
- ❌ FOB-ACTIVITY-DETAIL
- ❌ FOB-ACTIVITY-DELETE (modal/confirmation)

### 4. Artifact
- ❌ FOB-ARTIFACT-LIST
- ❌ FOB-ARTIFACT-CREATE
- ❌ FOB-ARTIFACT-EDIT
- ❌ FOB-ARTIFACT-DETAIL
- ❌ FOB-ARTIFACT-DELETE (modal/confirmation)

### 5. Goal
- ❌ FOB-GOAL-LIST
- ❌ FOB-GOAL-CREATE
- ❌ FOB-GOAL-EDIT
- ❌ FOB-GOAL-DETAIL
- ❌ FOB-GOAL-DELETE (modal/confirmation)

### 6. Howto
- ❌ FOB-HOWTO-LIST
- ❌ FOB-HOWTO-CREATE
- ❌ FOB-HOWTO-EDIT
- ❌ FOB-HOWTO-DETAIL
- ❌ FOB-HOWTO-DELETE (modal/confirmation)

### 7. Role
- ❌ FOB-ROLE-LIST
- ❌ FOB-ROLE-CREATE
- ❌ FOB-ROLE-EDIT
- ❌ FOB-ROLE-DETAIL
- ❌ FOB-ROLE-DELETE (modal/confirmation)

## Summary

**Total Missing Pages: 35**
- 7 entities × 5 pages each = 35 pages

**Note:** Some pages could be combined:
- List + Create on same page (common pattern)
- Detail + Edit combined view with edit mode toggle
- Delete as modal confirmation overlay

**Realistic Page Count:** ~20-25 pages if we combine intelligently.

## Recommendation

Create consolidated pages:
1. **FOB-WORKFLOW-MANAGE** (List + Create + Search)
2. **FOB-WORKFLOW-VIEW** (Detail + Edit + Delete)
3. Same pattern for all 7 entities = **14 pages minimum**

Plus entity-specific considerations:
- Workflow → Phase relationship views
- Activity → Artifact/Goal relationship views  
- Activity → Howto linkage views
- Role assignment views

**Estimated total:** 20-22 pages needed for full CRUDLF coverage.
