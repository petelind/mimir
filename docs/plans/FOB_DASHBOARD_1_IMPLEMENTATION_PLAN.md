# FOB-DASHBOARD-1 Implementation Plan

## Feature Overview
Implement dashboard overview with 3 sections: "My Playbooks", "Recent Activity", and "Quick Actions" as specified in `docs/features/act-0-auth/navigation.feature` Scenario NAV-01.

## Current State Assessment

### ✅ Existing Components We Can Reuse
- **Authentication System**: Fully functional with login/logout redirects to `/dashboard/`
- **Base Template**: Bootstrap 5 + Font Awesome Pro + HTMX configured with tooltips
- **Playbook Model**: Complete with author, timestamps, version tracking (`methodology/models/playbook.py`)
- **Dashboard URL Route**: `/dashboard/` already mapped to `methodology_views.dashboard`
- **Navigation**: Dashboard link exists in navbar with proper active state detection
- **Test Infrastructure**: pytest configured with integration test patterns

### ❌ Missing Components We Need to Build
- **Activity Tracking Model**: No model exists for recent activity feed
- **Dashboard View Logic**: Current view only renders stub template
- **Dashboard Template**: Needs 3 sections with proper data integration
- **Quick Actions**: No implementation for create/import/sync buttons

## Step-by-Step Implementation Plan

### Phase 1: Data Models and Activity Tracking

#### 1.1 Create Activity Model
**File**: `methodology/models/activity.py`
- Track user actions: playbook_created, playbook_updated, playbook_deleted, playbook_viewed
- Fields: user, action_type, playbook (foreign key, nullable), timestamp, description
- Model method: `get_recent_activities_for_user(user, limit=10)`
- Add to `methodology/models/__init__.py`

#### 1.2 Create Migration
```bash
python manage.py makemigrations methodology
python manage.py migrate
```

#### 1.3 Register with Admin
**File**: `methodology/admin.py`
- Register Activity model for admin visibility

### Phase 2: Dashboard View Implementation

#### 2.1 Enhance Dashboard View
**File**: `methodology/views.py` - Update `dashboard()` function
- Query 5 recent playbooks for authenticated user
- Query 10 recent activities for user
- Pass context data to template
- Add comprehensive logging per `add-logging.md`

#### 2.2 Create Activity Service
**File**: `methodology/services/activity_service.py`
- `log_activity(user, action_type, playbook=None, description=None)`
- `get_recent_playbooks(user, limit=5)`
- `get_recent_activities(user, limit=10)`
- Follow `do-write-concise-methods.md` guidelines

### Phase 3: Template Implementation

#### 3.1 Update Dashboard Template
**File**: `templates/dashboard.html`
- Replace stub content with 3-section layout
- **My Playbooks Section**: Grid of 5 recent playbooks with links
- **Recent Activity Feed**: Timeline of last 10 actions
- **Quick Actions Panel**: 3 buttons with icons and tooltips
- Use semantic `data-testid` attributes for testing
- Follow `do-semantic-versioning-on-ui-elements.md`

#### 3.2 Create Template Partials
**File**: `templates/partials/dashboard/`
- `my_playbooks.html` - Playbooks grid section
- `recent_activity.html` - Activity feed timeline  
- `quick_actions.html` - Action buttons panel

#### 3.3 Implement Quick Action Buttons
- **[+ New Playbook]**: Link to `/playbooks/playbook/create/`
- **[Import Playbook]**: Link to future import feature (disabled for now)
- **[Sync with Homebase]**: Link to future sync feature (disabled for now)
- All buttons with Font Awesome icons and Bootstrap tooltips

### Phase 4: Activity Logging Integration

#### 4.1 Update Playbook Views
**Files**: `methodology/views.py` (existing and future playbook views)
- Add activity logging for create, update, delete, view operations
- Use `activity_service.log_activity()` in relevant views

#### 4.2 Update Dashboard View
- Log activity when user accesses dashboard
- Use `activity_service.log_activity(request.user, 'dashboard_viewed')`

### Phase 5: Testing Implementation

#### 5.1 Unit Tests
**File**: `tests/unit/test_activity_model.py`
- Test Activity model creation and methods
- Test activity service functions

**File**: `tests/unit/test_activity_service.py`  
- Test `log_activity()` function
- Test `get_recent_playbooks()` and `get_recent_activities()`

#### 5.2 Integration Tests
**File**: `tests/integration/test_dashboard_view.py`
- `test_dashboard_displays_sections()` - Main acceptance test
- `test_my_playbooks_section_shows_recent_playbooks()`
- `test_recent_activity_section_shows_user_actions()`
- `test_quick_action_buttons_visible_and_functional()`
- Test with real data, no mocking per `do-not-mock-in-integration-tests.md`

#### 5.3 Activity Logging Tests
**File**: `tests/integration/test_activity_logging.py`
- Test activity creation on playbook actions
- Test dashboard view logging
- Verify activity feed updates correctly

### Phase 6: Edge Cases and Error Handling

#### 6.1 Handle Empty States
- No playbooks: Show "Create your first playbook" message
- No activities: Show "No recent activity" message
- Proper error handling for database queries

#### 6.2 Performance Considerations  
- Efficient database queries with `select_related()`
- Limit queries to specified counts (5 playbooks, 10 activities)
- Add database indexes if needed

### Phase 7: Documentation and Cleanup

#### 7.1 Update Documentation
- Update `docs/architecture/SAO.md` with Activity model details
- Add Activity model to system documentation

#### 7.2 Code Quality
- Ensure all methods have proper docstrings per `do-docstring-format.md`
- Follow `do-write-concise-methods.md` for service methods
- Add comprehensive logging per `add-logging.md`

## Implementation Order

1. **Data Models** → Activity model and migration
2. **Services** → Activity service with logging functions  
3. **View Logic** → Enhanced dashboard view with data queries
4. **Templates** → Dashboard template with 3 sections
5. **Integration** → Activity logging in existing views
6. **Testing** → Comprehensive unit and integration tests
7. **Polish** → Error handling, performance, documentation

## Testing Strategy

### Acceptance Criteria Coverage
- ✅ Dashboard displays all 3 sections
- ✅ Recent playbooks show correctly (5 most recent)
- ✅ Activity feed displays recent actions (10 most recent)
- ✅ Quick action buttons are visible and functional

### Test Execution
```bash
# Run all dashboard tests
pytest tests/ -k dashboard -v

# Run with coverage
pytest tests/ -k dashboard --cov=methodology --cov-report=html

# Continuous testing per do-continuous-testing.md
pytest tests/ --lf --tb=short
```

## Dependencies and Risks

### Dependencies
- Playbook model (✅ exists)
- Authentication system (✅ exists)  
- Bootstrap + Font Awesome (✅ exists)
- pytest test framework (✅ exists)

### Risks and Mitigations
- **Risk**: Activity model may impact performance
  **Mitigation**: Limit queries, add indexes, monitor query counts
- **Risk**: Complex template logic
  **Mitigation**: Use template partials, keep logic in services
- **Risk**: Test data management
  **Mitigation**: Use pytest fixtures, follow `do-test-fixture-data-management.md`

## Success Metrics

1. **Functional**: All acceptance criteria pass
2. **Performance**: Dashboard loads in <200ms with 1000+ activities
3. **Coverage**: >90% test coverage for new code
4. **Quality**: No linting issues, proper documentation
5. **Integration**: Seamless with existing authentication and navigation

## Next Steps

After completing this implementation:
1. User can view comprehensive dashboard on login
2. Activity tracking provides audit trail for all user actions  
3. Foundation for future features (import, sync, global search)
4. Template patterns established for other dashboard-style pages

This plan follows all established workflows and rules:
- `do-test-first.md` - Tests before implementation
- `do-write-concise-methods.md` - Clean service methods
- `do-add-todos-for-incomplete-items.md` - Task tracking
- `do-continuous-testing.md` - Test-driven development
- `add-logging.md` - Comprehensive logging
