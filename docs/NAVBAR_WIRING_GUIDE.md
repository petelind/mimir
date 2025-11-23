# Navbar Wiring Guide

## Purpose

This guide ensures that when a feature block is complete, we don't forget to wire it into the main navigation bar.

## Current Navbar Structure

Based on `templates/base.html`, the navbar contains:

### Active Links (Implemented)
- **Mimir** (brand/home) - `/` - Dashboard
- **Playbooks** - `/playbooks/` - Active ✅
- **PIPs** - `/pip/list/` - Active ✅
- **User Menu** - Login/Logout - Active ✅

### Placeholder Links (Coming Soon - Disabled)
- **Workflows** - `#` - Disabled (placeholder) - Icon: `fa-diagram-project`
- **Phases** - `#` - Disabled (placeholder) - Icon: `fa-layer-group`
- **Activities** - `#` - Disabled (placeholder) - Icon: `fa-list-check`
- **Artifacts** - `#` - Disabled (placeholder) - Icon: `fa-file-lines`
- **Roles** - `#` - Disabled (placeholder) - Icon: `fa-user-tag`
- **Howtos** - `#` - Disabled (placeholder) - Icon: `fa-book-open`

**Activating Placeholders:**
When implementing a feature with a placeholder:
1. Remove `disabled` class from the `<a>` tag
2. Change `href="#"` to actual route (e.g., `href="/workflows/"`)
3. Update tooltip from "Coming soon: ..." to active description
4. Ensure feature NAVBAR scenarios pass

## Feature Files with Navbar Scenarios

The following feature files have `NAVBAR` scenarios at the end to ensure navbar integration:

### 1. Playbooks (`act-2-playbooks/playbooks-list-find.feature`)

**Scenarios:**
- `PB-NAVBAR-01`: Playbooks link appears in main navigation
- `PB-NAVBAR-02`: Navigate to Playbooks from any page

**Implementation Checklist:**
- [ ] Link appears in navbar with `data-testid="nav-playbooks"`
- [ ] Icon: `fa-book-sparkles`
- [ ] Tooltip: "Browse and manage your engineering playbooks"
- [ ] Links to `/playbooks/` → `FOB-PLAYBOOKS-LIST+FIND-1`
- [ ] Active state highlighting when on Playbooks pages

### 2. PIPs (`act-9-pips/pips-manage.feature`)

**Scenarios:**
- `PIP-NAVBAR-01`: PIPs link appears in main navigation
- `PIP-NAVBAR-02`: Navigate to PIPs list from any page

**Implementation Checklist:**
- [ ] Link appears in navbar with `data-testid="nav-pips"`
- [ ] Icon: `fa-lightbulb`
- [ ] Tooltip: "Review Playbook Improvement Proposals"
- [ ] Links to `/pip/list/` → `FOB-PIPS-LIST-1`
- [ ] Shows PIPs across all playbooks (global view)
- [ ] Active state highlighting when on PIPs pages

### 3. Settings (`act-14-settings/settings.feature`)

**Implementation:**
- Settings is accessed via **Profile Menu** (not main navbar)
- Scenario `SETTINGS-01` covers navigation
- Accessed via: Profile Menu > [Settings]

## Features NOT in Main Navbar

The following features are accessed via other means and do NOT need navbar links:

- **Workflows** - Accessed via Playbook view
- **Phases** - Accessed via Workflow view  
- **Activities** - Accessed via Workflow/Phase view
- **Artifacts** - Accessed via Activity view
- **Roles** - Accessed via Playbook/Activity view
- **Howtos** - Accessed via Activity view
- **Dashboard** - Accessed via Mimir brand link (home)
- **Onboarding** - Accessed after registration
- **Authentication** - Special pages (login, register, etc.)

## Adding Navbar Scenarios to New Features

When creating a new feature that should be in the navbar:

### 1. Add Scenarios at End of Feature File

```gherkin
  # ============================================================
  # NAVBAR INTEGRATION - Wire when [Feature] block is complete
  # ============================================================
  
  Scenario: [FEATURE]-NAVBAR-01 [Feature] link appears in main navigation
    Given the [Feature] feature is fully implemented
    And Maria is authenticated in FOB
    When she views any page in FOB
    Then she sees "[Feature]" link in the main navbar
    And the link has icon "[fa-icon-name]"
    And the link has tooltip "[Helpful tooltip text]"
    
  Scenario: [FEATURE]-NAVBAR-02 Navigate to [Feature] from any page
    Given Maria is authenticated in FOB
    And she is on any page in FOB
    When she clicks "[Feature]" in the main navbar
    Then she is redirected to FOB-[FEATURE]-[PAGE]-1
    And the [Feature] nav link is highlighted as active
```

### 2. Update `templates/base.html`

```html
<li class="nav-item">
    <a class="nav-link" href="/[feature-url]/" data-testid="nav-[feature]"
       data-bs-toggle="tooltip" data-bs-placement="bottom"
       title="[Helpful tooltip text]">
        <i class="fas fa-[icon-name]"></i> [Feature]
    </a>
</li>
```

### 3. Add Integration Tests

Create `tests/integration/test_navbar_links.py` tests:

```python
def test_navbar_[feature]_link_when_authenticated():
    """Test navbar [feature] link uses correct URL."""
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    
    response = client.get('/')
    html = response.content.decode('utf-8')
    
    assert 'data-testid="nav-[feature]"' in html
    assert '/[feature-url]/' in html
```

## Best Practices

1. **Add navbar scenarios LAST** - After all other feature scenarios
2. **Use clear section headers** - `# NAVBAR INTEGRATION - Wire when...`
3. **Be specific about prerequisites** - "feature is fully implemented"
4. **Test from any page** - Navbar should work globally
5. **Include active state** - Nav link highlights when on feature pages
6. **Match existing patterns** - Icon, tooltip, `data-testid` attribute
7. **Test early** - Create navbar tests before implementation

## Icon Selection Guide

Use Font Awesome Pro icons that match the feature purpose:

- **Playbooks**: `fa-book-sparkles` - Collection of methodologies
- **PIPs**: `fa-lightbulb` - Ideas and improvements
- **Settings**: `fa-gear` or `fa-cog` - Configuration
- **Dashboard**: `fa-gauge` or `fa-chart-line` - Overview/metrics
- **Search**: `fa-magnifying-glass` - Finding content
- **Profile**: `fa-user` - User account

Browse: https://fontawesome.com/search?o=r&m=free&s=solid

## Tooltip Writing Guide

Tooltips should:
- Be concise (5-8 words)
- Use action verbs ("Browse", "Review", "Manage")
- Describe what user can do
- Match the feature's value proposition

**Good examples:**
- ✅ "Browse and manage your engineering playbooks"
- ✅ "Review Playbook Improvement Proposals"  
- ✅ "Configure your Mimir preferences"

**Bad examples:**
- ❌ "Playbooks" (not helpful)
- ❌ "Click here to see playbooks" (obvious)
- ❌ "This is where you manage all your playbooks and workflows" (too long)

## Testing Navbar Integration

### Unit Tests
Test navbar rendering in `tests/integration/test_navbar_links.py`

### Integration Tests  
Test navigation flow in feature-specific integration tests

### E2E Tests (Optional - Tier 2)
Test navbar with JavaScript/HTMX interactions using Playwright

---

**Last Updated**: 2025-11-23  
**Maintained By**: Development Team
