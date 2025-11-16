---
description: Create visual mockups and wireframes for UI design
auto_execution_mode: 3
---

# Mockup Creation Workflow

## Goal
Create visual mockups and wireframes for a specific screen using Draw.io. The idea is that we will have:
a) mockup detailing what do we have on the screen, and
b) scenario(s) describing screen behavior

## Prerequisites
- Screen/page identified for mockup creation
- User journey map completed (from workflow 1)
- Information architecture defined (from workflow 2)

## Screen Selection
**Required Input**: Specify the target screen/page/scenario for mockup creation
- If not provided, ask: "Which screen/page/scenario should we create mockups for?"
- Examples: Login screen, TODAY 1.1, Library.feature.

## Tools & Standards
- **Primary Tool**: Draw.io (for consistency with other workflows)
- **Fidelity Levels**: Low-fi wireframes → Mid-fi mockups → High-fi prototypes
- **Responsive Design**: Mobile-first, then tablet and desktop variants
- **Component Annotation**: Label reusable vs custom components

## Output Artifacts

### Primary Deliverable
**Artifact**: Screen Mockups and Wireframes for [Screen Name]
**Tool**: Draw.io
**Location**: `docs/ux/mockups/[screen-name]/`
**Files**:
- `wireframe.drawio` - Low-fidelity wireframe using Draw.io
- `mockup.drawio` - High-fidelity mockup using Draw.io
- `annotations.md` - Design annotations and specifications

### Supporting Deliverables
1. **Component Usage Map**
   - Location: `docs/ux/mockups/[screen-name]/components.md`
   - Content: List of components used in the screen

2. **Interaction Specifications**
   - Location: `docs/ux/mockups/[screen-name]/interactions.md`
   - Content: Detailed interaction behaviors and states

3. **Responsive Breakpoints**
   - Location: `docs/ux/mockups/[screen-name]/responsive.md`
   - Content: Mobile, tablet, and desktop variations, micro-interactions

## Definition of Done
- [ ] Low-fidelity wireframe created in Draw.io for the screen
- [ ] Mobile mockup created with proper component annotations
- [ ] Desktop mockup created with responsive considerations
- [ ] All interactive elements clearly labeled
- [ ] Component reusability documented
- [ ] Accessibility considerations noted
- [ ] Design system consistency verified
- [ ] Stakeholder review completed and approved

## Workflow Steps

### Step 1: Create Low-Fidelity Wireframe
- Open Draw.io and create new diagram
- Use basic shapes to layout screen structure
- Focus on content hierarchy and information architecture
- Annotate key functional areas

### Step 2: Develop Mobile Mockup
- Create detailed mobile-first design
- Apply visual design system elements
- Label all interactive components
- Include realistic content where possible

### Step 3: Create Desktop Mockup
- Adapt mobile design for larger screens
- Optimize layout for desktop interactions
- Ensure responsive design principles
- Document layout differences from mobile

### Step 4: Document Components and Interactions
- Create component annotation document
- Specify interaction behaviors
- Note accessibility requirements
- Prepare developer handoff notes