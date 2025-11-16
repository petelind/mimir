---
description: Define application structure, navigation patterns, and user flows
auto_execution_mode: 1
---

# UI Guidelines Documentation Creation Workflow

This workflow guides the creation of comprehensive UI Guidelines documentation that ensures consistency across the application's React TypeScript frontend with shadcn/ui components.

## Prerequisites

1. Review existing codebase patterns and components
2. Understand the tech stack: React TypeScript, shadcn/ui, FontAwesome Pro, Tailwind CSS
3. Analyze current implementation patterns from working components
4. Identify common UI patterns and anti-patterns

## Step 1: Document Analysis and Pattern Identification

### A. Analyze Existing Components
```bash
# Find all React components
find frontend/src/components -name "*.tsx" | head -10

# Analyze common patterns in key components
grep -r "className.*container" frontend/src/components/
grep -r "data-testid" frontend/src/components/
grep -r "FontAwesome" frontend/src/components/
```

### B. Review shadcn/ui Usage
```bash
# Check which shadcn/ui components are used
grep -r "from '@/components/ui/" frontend/src/components/ | cut -d: -f2 | sort | uniq

# Review component imports patterns
grep -r "import.*@/components/ui" frontend/src/components/
```

### C. Identify Layout Patterns
- Navigation sidebar structure
- Page container patterns
- Form layouts
- List/grid layouts
- Card structures

## Step 2: Create Document Structure

Create the UI Guidelines document with these main sections:

### A. Navigation Components
- Sidebar structure and behavior
- Breadcrumb navigation system
- Navigation item patterns

### B. Page Layout Patterns
- List pages (with filters, actions, cards)
- Form pages (create/edit patterns)
- Container sizing guidelines
- Grid and spacing systems

### C. Component Guidelines
- Required imports for different page types
- shadcn/ui component usage patterns
- FontAwesome icon integration
- Data attributes for testing

### D. Error Handling and States
- Form validation patterns
- Loading states
- Empty states
- Error display patterns

## Step 3: Document Navigation Patterns

### A. Sidebar Navigation
Document the established pattern:
```tsx
<Sidebar variant="inset" collapsible="icon">
  <SidebarHeader>
    {/* Logo + App name with collapse state handling */}
  </SidebarHeader>
  <SidebarContent>
    {/* Navigation menu with grouped items */}
  </SidebarContent>
  <SidebarFooter>
    {/* User info + logout */}
  </SidebarFooter>
</Sidebar>
```

### B. Breadcrumb System
- Centralized breadcrumb management
- Route mapping patterns
- Dynamic route handling
- Icon integration

### C. Navigation Items Structure
- Icon + title patterns
- Active state handling
- URL structure

## Step 4: Document Page Layout Patterns

### A. List Pages Pattern
Document the established container structure:
```tsx
<div className="container mx-auto p-6" data-testid="page-name">
  {/* Filter and Action Bar */}
  <div className="flex items-center justify-between mb-6">
    {/* Left: Filters (ToggleGroup, search, etc.) */}
    {/* Right: Primary Actions (Create, Add, etc.) */}
  </div>
  {/* Content Grid/List */}
</div>
```

### B. Form Pages Pattern
Document form container structure:
```tsx
<div className="container mx-auto p-6 max-w-4xl">
  {/* Page Header */}
  {/* Error Display */}
  {/* Form with sections */}
  {/* Form Actions */}
</div>
```

### C. Card Structure for Lists
Document card patterns with:
- Optional image headers
- Card header with icon + title
- Card content
- Action toolbar at bottom

## Step 5: Document Component Guidelines

### A. Required Imports by Page Type
Create import checklists for:
- Form pages (Alert, Button, Input, Label, etc.)
- List pages (Card, Badge, ToggleGroup, etc.)
- Common components (FontAwesome integration)

### B. shadcn/ui Component Usage
- Proper component selection
- Styling patterns
- Variant usage
- Size guidelines

### C. FontAwesome Integration
- Icon selection patterns
- Sizing and spacing
- Color integration
- Accessibility considerations

## Step 6: Document Sizing and Spacing Guidelines

### A. Container Widths
- Full width vs constrained patterns
- Responsive breakpoints
- Mobile-first considerations

### B. Grid Layouts
- Card grid patterns
- Form field layouts
- Responsive grid behavior

### C. Spacing System
- Consistent spacing scales
- Section separation
- Component spacing
- Button group spacing

## Step 7: Document Error Handling Patterns

### A. Form Validation
- Error display patterns
- Field-level validation
- Form-level error alerts
- User feedback patterns

### B. Loading States
- Loading indicators
- Skeleton patterns
- Progress feedback

### C. Empty States
- No data patterns
- Call-to-action integration
- Helpful messaging

## Step 8: Document Screen Real Estate Optimization

### A. Header Redundancy Rules
- When to avoid page headers
- Navigation context utilization
- Efficient layout patterns

### B. Layout Efficiency
- Combining related elements
- Prioritizing content
- Mobile optimization

## Step 9: Document Accessibility Guidelines

### A. Required Attributes
- ARIA labels and roles
- Data attributes for testing
- Semantic HTML structure

### B. Interactive Elements
- Button accessibility
- Form accessibility
- Navigation accessibility

## Step 10: Create Examples and Anti-Patterns

### A. Good Examples
- Working component implementations
- Proper pattern usage
- Best practice demonstrations

### B. Anti-Patterns
- Common mistakes to avoid
- Inefficient layouts
- Accessibility violations

## Step 11: Validation and Review

### A. Cross-Reference with Existing Code
```bash
# Verify patterns match actual implementation
grep -r "container mx-auto p-6" frontend/src/components/
grep -r "data-testid" frontend/src/components/
grep -r "space-y-6" frontend/src/components/
```

### B. Test Pattern Consistency
- Check if documented patterns are actually used
- Identify deviations from patterns
- Update documentation or code as needed

### C. Review with Team
- Validate patterns with development team
- Ensure patterns support all use cases
- Get feedback on clarity and completeness

## Step 12: Maintenance and Updates

### A. Living Document Process
- Regular review schedule
- Pattern evolution tracking
- New component integration

### B. Enforcement
- Code review checklist integration
- Automated pattern checking
- Developer onboarding materials

## Output Deliverables

1. **UI Guidelines Document** (`docs/architecture/UI_guidelines.MD`)
   - Complete pattern documentation
   - Code examples and anti-patterns
   - Import checklists and component guides

2. **Pattern Validation Scripts** (optional)
   - Automated pattern checking
   - Consistency validation tools

3. **Developer Reference** (optional)
   - Quick reference guide
   - Component selection flowchart
   - Common pattern templates

## Success Criteria

- [ ] All major UI patterns documented with examples
- [ ] Import requirements clearly specified
- [ ] Accessibility guidelines included
- [ ] Error handling patterns covered
- [ ] Screen real estate optimization rules defined
- [ ] Testing attributes standardized
- [ ] Examples match actual working code
- [ ] Anti-patterns clearly identified
- [ ] Document is actionable and practical
- [ ] Patterns support the established tech stack (React TypeScript, shadcn/ui, FontAwesome Pro, Tailwind CSS)

This workflow ensures comprehensive UI Guidelines that maintain consistency across the React TypeScript frontend while leveraging the established shadcn/ui component library and FontAwesome Pro icon system.