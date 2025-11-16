---
description: Map user journeys and dialogue flows to UI pages and state transitions with visual flow diagrams
auto_execution_mode: 3
---

# Dialogue Map Design Workflow

## Goal

Create comprehensive visual dialogue maps showing user journeys through UI pages, components, and interactions. Produces both simplified screen flows and detailed extended flows with all UI elements and decision points.

## Prerequisites

- Target user personas identified
- Current journey/demo flow identified for mapping

## Input Required

**Current Journey/Screen**: Specify which user journey or screen interaction you're mapping if there is more than one (e.g., "User Onboarding", "Checkout Process", "Dashboard Navigation")
**Existing implementation**: 
a) Check frontend/ and api/ for the current implementation. If they exist - ask user if you want existing implementation captured as part of the exerise.
b) check docs/features/ for the for the current understanding captured as .features. If they exist - ask user if you want existing implementation captured as part of the exerise, and what takes precedence - user journey, feature files, or existing implementation? (Default order of importance: implementation (most important) -> feature files -> user journey)


## Output Artifacts

### Primary Deliverables

**Artifact**: Extended Screen Flow Diagram, as a separate   
**Location**: `docs/ux/2_dialogue-maps/[journey-name]/screen-flow.drawio`  
**Description**: Detailed flow including components, forms, modals, and interactions


### Supporting Deliverables

1. **User Journey Map**
   - Location: `docs/ux/1_journey/user_journey.md`
   - Content: Step-by-step user experience documentation. Thats what we need to cover

2. **Component Inventory**
   - Location: `frontend/src/components`
   - Content: All forms, modals, and components we created so far



## Visual Design Standards

### Screen Flow Diagram Elements
- **Green Rectangles**: Pages/Screens (main destinations)
- **Bold Arrows**: Primary navigation paths (main flow)
- **Regular Arrows**: Secondary navigation paths
- **Labels**: Clear page names and navigation actions

### Extended Flow Diagram Elements
- **Green Rectangles**: Pages/Screens
- **Grey Diamonds**: Forms and Components
- **Light Grey Vertical Rectangles**: Modals/Confirmations/Dialogs
- **Dark Blue Rectangles**: Primary Action Buttons
- **Regular Arrows**: Navigation/Flow connections
- **Bold Arrows**: Primary user paths
- **Decision Points**: Diamond shapes for conditional flows

### Legend Requirements
- Each diagram must include a legend explaining all visual elements
- Legend should be LLM-readable with clear shape and color descriptions
- Include flow direction indicators and interaction types

## Definition of Done

- [ ] Screen Flow diagram created with green pages and navigation arrows
- [ ] Extended Flow diagram created with all UI elements (forms, modals, buttons)
- [ ] Both diagrams include comprehensive LLM-readable legends
- [ ] Main user paths clearly marked with bold arrows
- [ ] All decision points and conditional flows documented
- [ ] Component inventory lists all identified UI elements
- [ ] System responses defined for all user actions
- [ ] Error states and recovery paths identified
- [ ] Success and failure scenarios documented
- [ ] State transitions clearly defined
- [ ] UI page connections established
- [ ] Flow diagram created in Draw.io
- [ ] Validation criteria established
- [ ] Stakeholder review completed

## Workflow Steps

### Step 1: Define Journey Scope

- Identify journey start and end points
- Define primary user goals and motivations
- Document user context and prerequisites

### Step 2: Map User Actions

- List all possible user actions in sequence
- Identify decision points and branching
- Document user inputs and choices
- Plan for edge cases and variations

### Step 3: Define System Responses

- Specify system feedback for each action
- Design confirmation and error messages
- Plan loading states and transitions
- Define data validation responses

### Step 4: Reconcile against existing artifacts
- Read ALL feature files in the docs/features
- Introspect components and pages in frontend/src
- Reconcile features against screens against user flow
- Report inconsistencies to user and resolve them, one by one

### Step 5: Capture reconciled flow as a Flow Diagram

- Build visual flow in Draw.io
- Show all paths and decision points
- Include error and recovery flows
- Indicate page transitions and states

### Step 5: Document Dialogue Scripts

- Write detailed interaction descriptions inside the diagrams
- Include all user-facing text and messages
- Specify tone and voice guidelines

### Step 6: Validate and Refine

- Review flow with the user
- Refine based on feedback

## Dialogue Flow Components

### User Actions

- **Input Actions**: Form submissions, data entry
- **Navigation Actions**: Page transitions, menu selections
- **Selection Actions**: Choices, preferences, configurations
- **Confirmation Actions**: Approvals, cancellations, saves

### System Responses

- **Feedback Messages**: Success, error, validations, warning notifications
- **State Changes**: Page updates, data refreshes
- **Navigation**: Redirects, modal displays
- **Data Presentation**: Results, confirmations, summaries

### Decision Points

- **Conditional Logic**: If/then scenarios based on user data
- **Branching Paths**: Different flows for different user types
- **Error Handling**: Recovery paths for failed actions
- **Validation Gates**: Requirements before proceeding

## Page and State Mapping

### UI Page Connections

- Map each dialogue step to specific UI pages
- Define page-to-page transitions
- Identify shared components across pages
- Plan for responsive and mobile considerations

### State Management

- Document application state changes
- Define data persistence requirements
- Plan for session management
- Consider offline scenarios

## Content and Messaging

### User-Facing Text

- Instructional text and guidance
- Error messages and help text
- Success confirmations and feedback
- Call-to-action buttons and labels

### Tone and Voice

- Consistent brand voice throughout
- Appropriate tone for context
- Clear and accessible language
- Internationalization considerations

## Error Handling and Recovery

### Error Scenarios

- Input validation failures
- Network connectivity issues
- Server errors and timeouts
- Permission and authorization errors

### Recovery Paths

- Clear error messaging
- Actionable next steps
- Alternative pathways
- Help and support options

## Success Metrics and Validation

### Measurable Outcomes

- Task completion rates
- Time to complete journey
- Error rates and recovery success
- User satisfaction scores

### Validation Methods

- User testing with prototypes
- Stakeholder walkthrough sessions
- Technical feasibility review
- Accessibility compliance check

## Implementation Considerations

### Technical Requirements

- API endpoints and data needs
- Authentication and authorization
- Performance and loading considerations
- Browser and device compatibility

### Design System Integration

- Component usage and consistency
- Visual design alignment
- Interaction pattern compliance
- Accessibility standard adherence

## Documentation Standards

### Flow Diagram Elements

- Clear start and end points
- Decision diamonds for choices
- Process rectangles for actions
- Connector arrows with labels
- Error path indicators

### Script Documentation

- Step-by-step action descriptions
- User goals and motivations
- System feedback and responses
- Alternative paths and variations

When creating diagram, follow .windsurf/rules/do-diagrams-element-by-element.md