---
trigger: model_decision
description: When building HTML Pages, Django Templates, React Components/Views
---

# Enhanced Semantic Naming Guide for UI Components (Playwright-Optimized)

This guide provides comprehensive rules for naming HTML and UI components to ensure reliable Playwright E2E testing while maintaining LLM-friendly patterns.

---

## 1. Playwright Selector Hierarchy (MANDATORY ORDER)

**Always use selectors in this exact priority order:**

1. **`get_by_test_id(...)`** - Primary choice for complex components with proper data-testid
2. **`get_by_role(name=...)`** - Secondary choice for semantic elements with perfect aria-labels
3. **`get_by_label(...)`** - For form inputs with labels
4. **`get_by_text(...)`** - Only for static, stable content
5. **NEVER** use CSS selectors, XPath, or `locator()` with CSS

**Rationale:** `data-testid` selectors are more reliable than role-based selectors when components lack perfect accessibility attributes. Codegen naturally produces `data-testid` selectors, making them the most practical primary choice.

---

## 2. Mandatory Accessibility Attributes

**Every interactive element MUST have proper accessibility:**

```tsx
// Buttons - MUST have aria-label or descriptive text
<Button aria-label="Create new intent" data-testid="create-intent-button">
  <PlusIcon />
</Button>

// Form inputs - MUST have associated labels
<Label htmlFor="intent-name">Intent Name *</Label>
<Input 
  id="intent-name" 
  data-testid="intent-name-input"
  aria-describedby="name-error"
  required 
/>
<div id="name-error" data-testid="intent-name-error" role="alert">
  {nameError}
</div>

// Dialogs - MUST have unique accessible names
<Dialog open={open} onOpenChange={onOpenChange}>
  <DialogContent 
    aria-label="Create Intent Dialog" 
    data-testid="intent-form-dialog"
    role="dialog"
  >
    <DialogTitle>Create New Intent</DialogTitle>
  </DialogContent>
</Dialog>

// Menu items - MUST have stable text or aria-label
<DropdownMenuItem 
  onClick={onEdit} 
  data-testid="edit-intent-menuitem"
  aria-label="Edit this intent"
>
  Edit
</DropdownMenuItem>
```

---

## 3. Hierarchical data-testid Naming Convention

**Use domain-specific, hierarchical naming:**

### 3.1 Page-Level Containers
```tsx
data-testid="intents-page"
data-testid="intent-form-dialog"
data-testid="intent-details-modal"
```

### 3.2 Feature Components
```tsx
data-testid="intent-card"
data-testid="intent-list"
data-testid="intent-filters"
data-testid="intent-search"
```

### 3.3 Action Elements
```tsx
data-testid="create-intent-button"
data-testid="save-intent-button"
data-testid="cancel-intent-button"
data-testid="edit-intent-button"
data-testid="delete-intent-button"
data-testid="intent-actions-trigger"  // For dropdown menus
```

### 3.4 Form Elements
```tsx
data-testid="intent-name-input"
data-testid="intent-priority-input"
data-testid="intent-color-picker"
data-testid="intent-startag-input"
data-testid="intent-motive-textarea"
```

### 3.5 Status/Feedback Elements
```tsx
data-testid="success-message"
data-testid="error-message"
data-testid="loading-spinner"
data-testid="validation-error"
```

### 3.6 Menu Items
```tsx
data-testid="edit-intent-menuitem"
data-testid="archive-intent-menuitem"
data-testid="delete-intent-menuitem"
data-testid="duplicate-intent-menuitem"
```

---

## 4. Component State Visibility

**Make component states testable via data attributes:**

```tsx
// Loading states
<div 
  data-testid="intent-list" 
  data-state={isLoading ? "loading" : "loaded"}
  data-count={intents.length}
>

// Form validation states
<input 
  data-testid="intent-name-input"
  data-valid={isValid}
  aria-invalid={!isValid}
/>

// Button states
<button 
  data-testid="save-intent-button"
  data-state={isSubmitting ? "submitting" : "ready"}
  disabled={isSubmitting}
>
  {isSubmitting ? "Saving..." : "Save"}
</button>

// Filter states
<button 
  data-testid="active-filter-button"
  data-state={isActive ? "selected" : "unselected"}
  aria-pressed={isActive}
>
  Active
</button>
```

---

## 5. List and Card Components

**Ensure predictable structure for list items:**

```tsx
// List container
<div data-testid="intent-list" role="list">
  {intents.map(intent => (
    <IntentCard 
      key={intent.id}
      intent={intent}
      data-testid="intent-card"
      data-intent-id={intent.id}
      data-intent-startag={intent.startag}
      data-intent-priority={intent.priority}
    />
  ))}
</div>

// Individual card with identifiable attributes
<div 
  data-testid="intent-card"
  data-intent-id={intent.id}
  data-intent-startag={intent.startag}
  role="article"
  aria-label={`Intent: ${intent.name}`}
>
  <h3 data-testid="intent-card-title">{intent.name}</h3>
  <p data-testid="intent-card-startag">*{intent.startag}</p>
  
  <div data-testid="intent-card-actions">
    <Button 
      data-testid="edit-intent-button"
      aria-label={`Edit ${intent.name}`}
    >
      Edit
    </Button>
  </div>
</div>
```

---

## 6. Form Components Best Practices

**Structure forms for reliable testing:**

```tsx
<form 
  role="form" 
  aria-label="Intent creation form"
  data-testid="intent-form"
  onSubmit={handleSubmit}
>
  <fieldset data-testid="intent-basic-fields">
    <legend>Basic Information</legend>
    
    <div data-testid="intent-name-field">
      <Label htmlFor="intent-name">Name *</Label>
      <Input 
        id="intent-name"
        data-testid="intent-name-input"
        required
        aria-describedby="name-error"
      />
      <div id="name-error" data-testid="intent-name-error" role="alert">
        {nameError}
      </div>
    </div>
  </fieldset>
  
  <div data-testid="intent-form-actions">
    <Button 
      type="button"
      onClick={onCancel}
      data-testid="cancel-intent-button"
    >
      Cancel
    </Button>
    <Button 
      type="submit"
      data-testid="save-intent-button"
      data-state={isSubmitting ? "submitting" : "ready"}
    >
      Save
    </Button>
  </div>
</form>
```

---

## 7. Portal Components (Dialogs, Dropdowns)

**Handle Radix/shadcn portals correctly:**

```tsx
// Dialog - renders to document.body
<Dialog open={open} onOpenChange={onOpenChange}>
  <DialogTrigger asChild>
    <Button data-testid="open-dialog-button">Open</Button>
  </DialogTrigger>
  <DialogContent 
    aria-label="Intent Form Dialog"
    data-testid="intent-form-dialog"
  >
    {/* Dialog content */}
  </DialogContent>
</Dialog>

// Dropdown - also renders to document.body
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button 
      aria-label="More actions" 
      data-testid="intent-actions-trigger"
    >
      <MoreHorizontal />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent data-testid="intent-actions-menu">
    <DropdownMenuItem data-testid="edit-intent-menuitem">
      Edit
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

**Playwright Testing Note:** Always query portals from `page`, not from container elements:
```python
# ✅ Correct - query from page
dialog = page.get_by_test_id("intent-form-dialog")

# ❌ Wrong - portals aren't inside containers
dialog = container.get_by_test_id("intent-form-dialog")
```

---

## 8. Animation Control for Testing

**Disable animations in test environments:**

```css
/* Global test environment styles */
[data-testid] *, 
[data-testid] *::before, 
[data-testid] *::after {
  transition-duration: 1ms !important;
  animation-duration: 1ms !important;
  animation-iteration-count: 1 !important;
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 9. Component Documentation Template

**Document testability features for each component:**

```tsx
/**
 * IntentCard Component
 * 
 * @testability
 * - data-testid="intent-card" - Component identification
 * - data-intent-id={intent.id} - Specific intent targeting
 * - data-intent-startag={intent.startag} - Startag-based selection
 * - aria-label provides accessible description
 * - All buttons have individual data-testid attributes
 * 
 * @playwright-selectors
 * Primary: page.get_by_test_id("intent-card")
 * Specific: page.get_by_test_id("intent-card").filter(has_text="DEEPWORK")
 * Actions: page.get_by_test_id("edit-intent-button")
 * 
 * @accessibility
 * - role="article" for screen readers
 * - aria-label describes the intent
 * - All interactive elements have accessible names
 */
export function IntentCard({ intent }: IntentCardProps) {
  return (
    <div 
      data-testid="intent-card"
      data-intent-id={intent.id}
      data-intent-startag={intent.startag}
      role="article"
      aria-label={`Intent: ${intent.name}`}
    >
      {/* Component implementation */}
    </div>
  );
}
```

---

## 10. Anti-Patterns to Avoid

### ❌ Bad Practices
```tsx
// Generic names
<div id="main" className="container">
<button className="btn btn-primary">

// Fragile selectors in tests
page.locator('.btn-primary').click()
page.locator('div:nth-child(2)').click()

// Missing accessibility
<button><Icon /></button>  // No aria-label
<input />  // No label

// Unstable text content
<button>Save ({count})</button>  // Dynamic text breaks tests
```

### ✅ Good Practices
```tsx
// Semantic, descriptive names
<main data-testid="intents-page" role="main">
<button data-testid="create-intent-button" aria-label="Create new intent">

// Reliable selectors in tests
page.get_by_test_id("create-intent-button")
page.get_by_test_id("intent-card").filter(has_text="DEEPWORK")

// Proper accessibility
<button aria-label="Create new intent">
  <PlusIcon />
</button>

// Stable content with separate indicators
<button data-testid="save-button" data-count={count}>
  Save
</button>
<span data-testid="save-count">({count})</span>
```

---

## 11. Testing Validation Checklist

Before committing any component, verify:

- [ ] All interactive elements have `aria-label` or descriptive text
- [ ] All form inputs have associated `<Label>` elements
- [ ] All dialogs have unique accessible names
- [ ] All components have appropriate `data-testid` attributes
- [ ] Component states are visible via data attributes
- [ ] No CSS animations interfere with testing
- [ ] Portal components can be queried from `page` level
- [ ] List items have predictable structure and identifiers
- [ ] Form validation errors are accessible and testable

---

This enhanced guide ensures your UI components are both accessible and highly testable with Playwright, reducing E2E test flakiness and improving maintainability.
