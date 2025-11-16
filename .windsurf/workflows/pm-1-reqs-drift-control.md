---
description: Requirements drift control and synchronization analysis between UX artifacts
---

# Requirements Drift Control Workflow

## Goal

Identify and resolve synchronization issues between dialogue maps, demo scenarios, feature files, and mockups to ensure all UX artifacts are aligned and consistent.

## Prerequisites

- Both starting artifacts exist:
  - Demo scenario exists: docs/ux/demo-flow.md
  - Dialogue map exists (`docs/ux/dialogue-maps/`)
- At least one of the following artifacts exists:
  - Feature files (`docs/ux/feature-files/`)
  - Mockups (`docs/ux/mockups/`)

## Input Required

**Analysis Scope**: Specify which artifacts to analyze (e.g., "User Onboarding Journey", "Complete Application", "Specific Feature Set")

## Output Artifacts

### Primary Deliverable

**Artifact**: Requirements Drift Analysis Report  
**Location**: `docs/ux/drift-analysis/`  
**Files**:
- `drift-state.md` - Comprehensive drift analysis table
- `analysis-summary.md` - Executive summary of findings
- `resolution-plan.md` - Recommended resolution actions

### Supporting Deliverables

1. **Gap Analysis Matrix**
   - Location: `docs/ux/drift-analysis/gap-matrix.md`
   - Content: Cross-reference matrix of all artifacts

2. **Synchronization Checklist**
   - Location: `docs/ux/drift-analysis/sync-checklist.md`
   - Content: Step-by-step resolution tasks

## Definition of Done

- [ ] All scenarios cross-referenced with dialogue maps
- [ ] All dialogue map screens verified against mockups
- [ ] All feature files validated against existing mockups
- [ ] Drift analysis table created with unique suggestion IDs
- [ ] User choice column provided for each suggestion
- [ ] Resolution recommendations documented
- [ ] Executive summary completed
- [ ] Stakeholder review scheduled

## Workflow Steps

### Step 1: Inventory Existing Artifacts

- Scan `docs/ux/dialogue-maps/` for existing dialogue flows
- Review `docs/ux/feature-files/` for BDD scenarios
- Check `docs/ux/mockups/` for screen designs
- Identify demo scenarios or user stories
- Document artifact coverage and completeness

### Step 2: Cross-Reference Scenarios with Dialogue Maps

- Extract user journeys from scenarios/stories
- Map each journey step to dialogue map flows
- Identify missing dialogue map coverage
- Flag inconsistencies between scenarios and flows
- Document gaps and misalignments

### Step 3: Validate Dialogue Maps Against Mockups

- Review each dialogue map screen/page reference
- Verify corresponding mockup exists in `docs/ux/mockups/`
- Check mockup completeness and fidelity
- Identify missing or outdated mockups
- Flag design inconsistencies

### Step 4: Validate Feature Files Against Mockups

- Parse Gherkin scenarios for UI interactions
- Map each interaction to specific mockup elements
- Verify mockups support all feature file actions
- Identify missing UI components or states
- Check for testability gaps

### Step 5: Generate Drift Analysis Table

Create comprehensive table in `drift-state.md` with columns:
- **Item ID**: Unique identifier (e.g., DM001, MK002, FF003)
- **Artifact Type**: Dialogue Map, Mockup, Feature File, Scenario
- **Item Description**: What was checked
- **Status**: ✅ Synced, ⚠️ Minor Drift, ❌ Major Gap, 🔍 Needs Review
- **Issue Description**: Detailed description of drift/gap
- **Suggestion ID**: Unique action identifier (e.g., UNI001, PF002)
- **Recommended Action**: Specific resolution steps
- **User Choice**: [PENDING] - for user to fill in their decision

### Step 6: Create Resolution Plan

- Prioritize suggestions by impact and effort
- Group related suggestions into logical work packages
- Estimate effort for each resolution action
- Recommend implementation sequence
- Prepare execution checklist

## Drift Analysis Categories

### Dialogue Map Drifts

- **Missing Flows**: Scenarios not covered by dialogue maps
- **Orphaned Flows**: Dialogue maps without corresponding scenarios
- **Flow Inconsistencies**: Logic mismatches between scenarios and flows
- **State Misalignments**: Different state definitions across artifacts

### Mockup Drifts

- **Missing Mockups**: Dialogue map screens without mockups
- **Outdated Mockups**: Mockups not reflecting current dialogue flows
- **Incomplete Mockups**: Missing UI elements referenced in flows
- **Design Inconsistencies**: Visual conflicts between related mockups

### Feature File Drifts

- **Untestable Scenarios**: Feature files referencing non-existent UI elements
- **Missing Test Coverage**: Mockup features without corresponding tests
- **Interaction Gaps**: UI interactions not covered by feature files
- **Data Mismatches**: Test data inconsistent with mockup designs

## Suggestion ID Conventions

### Prefix Categories

- **UNI**: Universal/Cross-cutting issues
- **DM**: Dialogue Map specific
- **MK**: Mockup specific  
- **FF**: Feature File specific
- **SC**: Scenario specific
- **PF**: Process/Flow issues
- **UI**: User Interface issues
- **DT**: Data/Content issues

### Example Suggestions

- **UNI001**: Create missing cross-reference documentation
- **DM002**: Update dialogue flow to match scenario requirements
- **MK003**: Create mockup for missing screen in dialogue map
- **FF004**: Add feature file coverage for new UI interaction
- **PF005**: Align user flow sequence across all artifacts

## Quality Assurance

### Validation Criteria

- All scenarios have corresponding dialogue map coverage
- All dialogue map screens have mockup representations
- All feature files can be executed against existing mockups
- No orphaned artifacts without clear purpose
- Consistent terminology and naming across artifacts

### Review Process

- Technical review of analysis completeness
- Stakeholder validation of identified gaps
- User acceptance of recommended actions
- Implementation feasibility assessment

## Implementation Guidelines

### Resolution Prioritization

1. **Critical Gaps**: Missing core functionality or user flows
2. **Major Drifts**: Significant inconsistencies affecting user experience
3. **Minor Drifts**: Small misalignments or outdated content
4. **Enhancements**: Opportunities for improvement

### Execution Approach

- Address critical gaps first
- Group related suggestions for efficient execution
- Maintain artifact synchronization during updates
- Validate changes against all affected artifacts
- Update drift analysis table as issues are resolved

## Continuous Monitoring

### Drift Prevention

- Regular synchronization checks during development
- Automated validation where possible
- Clear ownership of artifact maintenance
- Change management processes for UX updates

### Success Metrics

- Percentage of scenarios with complete dialogue map coverage
- Percentage of dialogue maps with corresponding mockups
- Percentage of feature files executable against mockups
- Time to resolve identified drifts
- Frequency of drift occurrences