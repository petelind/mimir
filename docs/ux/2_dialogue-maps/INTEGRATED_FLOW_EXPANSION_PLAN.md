# Integrated Flow Expansion Plan

**Goal**: Show ALL 87 screens including modals, MCP interactions, and complete workflows

---

## Current State vs. Target

| Act | Current Screens | Total Screens | Missing |
|-----|----------------|---------------|---------|
| **Act 0** | 5 | 11 | 6 (modals, login screens) |
| **Act 1** | 4 | 8 | 4 (modals, external MCP setup) |
| **Act 2** | 6 | 12 | 6 (admin modals, approval flows) |
| **Act 3** | 6 | 8 | 2 (validation modal, success modal) |
| **Act 4** | 3 | 12 | 9 (work item creation, external MCPs) |
| **Act 5** | 4 | 6 | 2 (MCP processing steps) |
| **Act 6** | 6 | 8 | 2 (conflict details, export modal) |
| **Act 7** | 0 | 11 | 11 (all 4 creation methods) |
| **Acts 8-9** | 0 | 11 | 11 (settings pages, error modals) |

**Current**: ~34 screens  
**Target**: 87 screens  
**To Add**: 53 screens

---

## Missing Elements by Type

### Modals (Light Grey #D3D3D3, Dashed Border)
- Act 0: Connection error modal, success confirmation
- Act 1: MCP config modal, sync preference modals
- Act 2: Join request modal, approval modal, rejection modal, submission confirmation
- Act 3: Import validation modal, success modal
- Act 5: PIP review modal details
- Act 6: Conflict resolution modal, export options modal
- Acts 8-9: All error modals, empty state screens

### MCP Internal Processing (Orange #FF8C00)
- Act 4: All work item creation steps
- Act 5: PIP analysis, generation steps
- External MCP interactions (GitHub, Jira)

### Complete Workflows
- Act 2: Full admin approval workflow
- Act 4: Complete MCP command flows
- Act 7: All 4 creation methods (Manual, AI, Template, MCP)
- Acts 8-9: Settings navigation, error recovery

---

## Expansion Strategy

### Phase 1: Expand Canvas
- **Current**: 2800×2400px
- **New**: 4800×3200px (much wider for all screens)
- Increase swimlane widths to accommodate all screens horizontally

### Phase 2: Add Missing Screens Act-by-Act

#### Act 0 (Authentication & Setup)
**Add**:
1. HB-LOGIN-1 (before register)
2. HB-ADMIN-DASHBOARD-1 (admin view)
3. FOB-STARTUP-1 (FOB initialization)
4. FOB-ERROR-CONNECTION-1 (modal - light grey)
5. HB-AUTH-SUCCESS-MODAL-1 (modal - light grey)
6. FOB-ONBOARDING-SUCCESS-1 (confirmation)

**Total**: 11 screens (5 existing + 6 new)

#### Act 1 (Onboarding)
**Add**:
1. FOB-ONBOARDING-EXTERNAL-MCP-1 (GitHub/Jira setup)
2. FOB-ONBOARDING-EXTERNAL-MCP-GITHUB-1 (GitHub config)
3. FOB-ONBOARDING-PREFERENCES-MODAL-1 (modal)
4. FOB-ONBOARDING-COMPLETE-1 (final confirmation)

**Total**: 8 screens (4 existing + 4 new)

#### Act 2 (Family Management)
**Add**:
1. FOB-FAMILY-JOIN-REQUEST-MODAL-1 (modal)
2. HB-ADMIN-APPROVE-REQUEST-1 (admin approval)
3. FOB-FAMILY-JOIN-APPROVED-NOTIFICATION-1 (notification)
4. FOB-FAMILY-PLAYBOOK-SUBMIT-1 (submit playbook to family)
5. FOB-FAMILY-ADMIN-APPROVAL-MODAL-1 (modal)
6. FOB-FAMILY-SETTINGS-1 (family configuration)

**Total**: 12 screens (6 existing + 6 new)

#### Act 3 (First Sync & Download)
**Add**:
1. FOB-IMPORT-VALIDATE-MODAL-1 (validation details modal)
2. FOB-SYNC-SUCCESS-MODAL-1 (success confirmation modal)

**Total**: 8 screens (6 existing + 2 new)

#### Act 4 (MCP Usage)
**Add**:
1. WINDSURF-CHAT-PLAYBOOK-DETAIL-1 (detailed playbook view)
2. MCP-WORKITEM-CREATE-GITHUB-1 (GitHub work item - orange)
3. MCP-WORKITEM-CREATE-JIRA-1 (Jira work item - orange)
4. WINDSURF-WORKITEM-CREATED-1 (confirmation)
5. FOB-OPEN-PLAYBOOK-1 (open from MCP)
6. FOB-PLAYBOOK-DETAIL-VIEW-1 (full detail)
7. MCP-EXTERNAL-GITHUB-1 (external MCP - orange)
8. MCP-EXTERNAL-JIRA-1 (external MCP - orange)
9. WINDSURF-MCP-COMMANDS-LIST-1 (available commands)

**Total**: 12 screens (3 existing + 9 new)

#### Act 5 (Creating PIPs)
**Add**:
1. MCP-PIP-ANALYZE-1 (analysis step - orange)
2. FOB-PIP-REVIEW-MODAL-1 (detailed review modal)

**Total**: 6 screens (4 existing + 2 new)

#### Act 6 (Sync Scenarios)
**Add**:
1. FOB-SYNC-CONFLICT-MODAL-1 (conflict details modal)
2. FOB-PLAYBOOK-EXPORT-MODAL-1 (export options modal)

**Total**: 8 screens (6 existing + 2 new)

#### Act 7 (Create Playbooks) - NEW SWIMLANE
**Add ALL 11 screens**:
1. FOB-CREATE-PLAYBOOK-1 (dashboard entry)
2. FOB-PLAYBOOK-WIZARD-BASIC-1 (wizard step 1)
3. FOB-PLAYBOOK-EDITOR-1 (editor)
4. FOB-PLAYBOOK-WIZARD-PUBLISH-1 (wizard step 3)
5. FOB-IMPORT-NOTES-1 (import from notes)
6. FOB-AI-STRUCTURE-1 (AI analysis)
7. FOB-UPLOAD-HOMEBASE-1 (upload progress)
8. FOB-TEMPLATE-SELECT-1 (template selection)
9. FOB-MEMBER-MANAGEMENT-1 (hidden family members)
10. WINDSURF-CREATE-PLAYBOOK-1 (MCP creation)
11. MCP-PLAYBOOK-CREATED-1 (MCP confirmation)

**Total**: 11 screens (all new)

#### Acts 8-9 (Settings & Errors) - NEW SWIMLANE(S)
**Add ALL 11 screens**:
1. FOB-SETTINGS-MAIN-1 (settings hub)
2. FOB-SETTINGS-SYNC-1 (sync settings)
3. FOB-SETTINGS-STORAGE-1 (storage)
4. FOB-SETTINGS-MCP-1 (MCP config)
5. FOB-SETTINGS-NOTIFICATIONS-1 (notifications)
6. FOB-SYNC-ERROR-1 (sync error modal)
7. FOB-PERMISSION-ERROR-1 (permission error modal)
8. FOB-UPLOAD-ERROR-1 (upload error modal)
9. FOB-CORRUPTION-ERROR-1 (corruption error)
10. FOB-EMPTY-PLAYBOOKS-1 (empty state)
11. FOB-EMPTY-SEARCH-1 (no results)

**Total**: 11 screens (all new)

---

## Visual Design Updates

### Color Coding
- **Modals**: Light grey (#D3D3D3) with dashed border
- **MCP Processing**: Orange (#FF8C00) solid
- **External MCPs**: Orange (#FF8C00) with dashed border
- **Error Screens**: Red/Pink (#f8cecc)
- **Empty States**: Blue with lighter shade
- **Settings**: Blue standard

### Box Sizes
- **Standard Screen**: 160×80px
- **Modal**: 140×70px (slightly smaller)
- **MCP Processing**: 160×80px
- **Expanded for details**: Up to 180×100px when needed

### Layout
- Increase canvas to 4800px wide
- Each swimlane can be 800-1200px wide
- Use horizontal scrolling in Draw.io
- Group related screens with proximity
- Use vertical branches for alternatives

---

## Implementation Order

1. ✅ Expand canvas size
2. ⏳ Act 0: Add 6 missing screens + modals
3. ⏳ Act 1: Add 4 missing screens + external MCP
4. ⏳ Act 2: Add 6 missing screens + admin workflow
5. ⏳ Act 3: Add 2 modals
6. ⏳ Act 4: Add 9 MCP/work item screens
7. ⏳ Act 5: Add 2 processing screens
8. ⏳ Act 6: Add 2 modals
9. ⏳ Act 7: Add NEW swimlane with 11 screens
10. ⏳ Acts 8-9: Add NEW swimlane with 11 screens
11. ⏳ Update connections and flow arrows
12. ⏳ Add annotations for clarity
13. ⏳ Test and commit

---

## Success Criteria

✅ All 87 screens visible in integrated diagram  
✅ Modals clearly distinguished (light grey, dashed)  
✅ MCP interactions shown (orange)  
✅ All alternative paths visible  
✅ Error scenarios included  
✅ Settings accessible from main flow  
✅ Complete picture of Maria's journey  

---

**Status**: Planning Complete - Ready to Implement  
**Next**: Start expanding canvas and adding Act 0 missing screens
