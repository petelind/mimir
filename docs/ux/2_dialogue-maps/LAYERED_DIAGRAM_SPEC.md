# Layered Integrated Diagram Specification

**Goal**: 87 screens organized in 4 toggle layers, readable when viewing 2-3 layers simultaneously

---

## Layer Strategy

### Layer 1: Main Success Path (Always Visible)
**Purpose**: Core journey that 90% of users follow  
**Screens**: ~28 screens  
**Visual**: Bold 3px arrows, well-spaced, clean horizontal flow

**Content**:
- Act 0: HB Register → Verify → Token → FOB Connect → Setup (5 screens)
- Act 1: First Run → Sync Prefs → MCP Config → Dashboard (4 screens)
- Act 2: Browse → View Family → Request Join → Approved (4 screens)
- Act 3: Sync → Available → Preview → Download (4 screens)
- Act 4: Open Windsurf → Load Context → Use Commands (3 screens)
- Act 5: Suggest PIP → Generate → Review → Approve (4 screens)
- Act 6: Sync Analysis → Upload PIP (2 screens)
- END marker (1 screen)

**Spacing**: 
- Horizontal: 220px between screens
- Vertical: Single row per act in swimlane
- Total width: ~3000px (fits standard ultra-wide monitors)

---

### Layer 2: Modals & Confirmations (+15 screens)
**Purpose**: Popup modals, confirmations, success/error messages  
**Visual**: Light grey (#D3D3D3), dashed border, smaller (140×70px)  
**Position**: Above or below triggering screen, 100px vertical offset

**Content**:
- Act 0: Email verified modal, Connection success modal, Error modal (3)
- Act 1: Sync preferences modal, MCP config confirmation (2)
- Act 2: Join request modal, Approval notification modal, Submit confirmation (3)
- Act 3: Validation modal, Success modal (2)
- Act 5: PIP review details modal (1)
- Act 6: Conflict resolution modal, Export options modal (2)
- Acts 8-9: Error modals (sync, permission, upload) (2)

**Visibility Rule**: Only visible when Layer 2 is enabled  
**Arrow Style**: 2px dashed to modal, then back to main flow

---

### Layer 3: MCP Processing & Internal Steps (+18 screens)
**Purpose**: Behind-the-scenes AI/MCP processing, external MCP calls  
**Visual**: Orange (#FF8C00), solid border, same size as main (160×80px)  
**Position**: Parallel to main flow, 150px vertical offset (above or below)

**Content**:
- Act 1: External MCP setup (GitHub, Jira config) (2)
- Act 4: Work item creation flows (GitHub/Jira MCPs), External MCP servers (6)
- Act 5: PIP analysis step, Generation processing (2)
- Act 7: MCP-driven playbook creation, AI structure analysis (4)
- Acts 8-9: Background processing, sync operations (4)

**Visibility Rule**: Shows when Layer 3 is enabled  
**Arrow Style**: 2px solid orange lines showing data flow

---

### Layer 4: Alternative Paths & Optional Features (+26 screens)
**Purpose**: Less common paths, optional features, admin views  
**Visual**: Same colors as main but with dashed borders  
**Position**: Below main swimlane, 120px vertical offset minimum

**Content**:
- Act 0: Login (vs Register), Admin dashboard view (2)
- Act 2: Create Family (vs Join), Admin approval workflow, Family settings (6)
- Act 3: Import JSON (vs Download from HB) (2)
- Act 6: Clean download, Conflict resolution scenarios, Export JSON (3)
- Act 7: ALL 4 creation methods (Manual, AI, Template, MCP) (11)
- Acts 8-9: Settings screens, Empty states (2)

**Visibility Rule**: Shows when Layer 4 is enabled  
**Arrow Style**: 2px dashed grey, labeled with "OR" or condition

---

## Spacing Rules (Per Visual Clarity Guidelines)

### Horizontal Spacing
- Between screens: 220px (gives 60px arrow space)
- Between alternative branches: 300px
- Between acts: 100px gap + new swimlane

### Vertical Spacing
- Main path row: Y=40 (within swimlane)
- Modal position: Y=160 or Y=-60 (100px offset from trigger)
- MCP processing: Y=160 or Y=-60 (parallel to trigger)
- Alternative paths: Y=180 (below main, within swimlane)
- Swimlane to swimlane: 20px gap

### Arrow Routing
- **Main path**: Straight horizontal, minimal waypoints
- **To modals**: Single waypoint, 90° turn
- **MCP interaction**: Curved or stepped routing
- **Alternatives**: Route below, merge back with clear waypoint
- **No more than 2 arrows** cross at any point
- **Minimum 40px** between parallel arrows

---

## Visual Hierarchy

### Line Weights
- **Main path**: 3px bold black
- **Modals**: 2px dashed grey
- **MCP**: 2px solid orange
- **Alternatives**: 2px dashed grey
- **Error paths**: 2px dashed red

### Box Sizes
- **Main screens**: 160×80px
- **Modals**: 140×70px (slightly smaller)
- **MCP**: 160×80px (same as main)
- **Alternatives**: 160×80px (same as main)

### Colors (Consistent Across Layers)
- **FOB**: Blue (#4682B4)
- **HB**: Green (#82b366)
- **Windsurf**: Purple (#9370DB)
- **MCP**: Orange (#FF8C00)
- **Modals**: Light grey (#D3D3D3)
- **Errors**: Red/Pink (#f8cecc)

---

## Layer Combinations (Readability Test)

### Layer 1 Only (Main Path)
✅ Clean, easy to follow, ~28 screens  
✅ Fits on one screen at 75% zoom  
✅ Clear start-to-end journey

### Layer 1 + Layer 2 (Main + Modals)
✅ ~43 screens total  
✅ Modals positioned to not obstruct main flow  
✅ Clear which screen triggers which modal  
✅ Still readable at 60% zoom

### Layer 1 + Layer 3 (Main + MCP)
✅ ~46 screens total  
✅ MCP boxes parallel to main, showing "what happens behind scenes"  
✅ Orange color clearly distinguishes processing  
✅ Readable at 60% zoom

### Layer 1 + Layer 2 + Layer 3 (Main + Modals + MCP)
✅ ~61 screens total  
✅ Most comprehensive view for developers  
✅ Shows UI + interactions + processing  
⚠️ Requires 50% zoom to see full flow  
✅ Still understandable with proper spacing

### All 4 Layers (Complete View)
✅ All 87 screens visible  
✅ Alternative paths clearly below main  
⚠️ Requires 40% zoom or horizontal scrolling  
✅ Each path still traceable without confusion

---

## Implementation Plan

### Phase 1: Restructure for Layers
1. Create 4 layers in Draw.io: "Main", "Modals", "MCP", "Alternatives"
2. Move current screens to appropriate layers
3. Adjust positions following spacing rules

### Phase 2: Complete Layer 1 (Main Path)
1. Verify all 28 main path screens present
2. Ensure 220px horizontal spacing
3. Test flow clarity at 75% zoom
4. Commit: "Layer 1 complete"

### Phase 3: Add Layer 2 (Modals)
1. Add 15 modal screens
2. Position 100px above/below triggers
3. Add dashed connections
4. Test Layer 1+2 readability at 60% zoom
5. Commit: "Layer 2 complete"

### Phase 4: Add Layer 3 (MCP)
1. Add 18 MCP/processing screens
2. Position parallel to main flow
3. Add orange routing arrows
4. Test Layer 1+3 readability at 60% zoom
5. Commit: "Layer 3 complete"

### Phase 5: Add Layer 4 (Alternatives)
1. Add 26 alternative path screens
2. Position below main flow in each swimlane
3. Add dashed routing with labels
4. Test all layers at 40% zoom
5. Commit: "Layer 4 complete - all 87 screens"

### Phase 6: Polish & Test
1. Run zoom out test (50%)
2. Check arrow crossings (<2 per point)
3. Verify spacing consistency
4. Add layer visibility instructions
5. Final commit: "Integrated layered diagram complete"

---

## Layer Toggle Instructions (For Diagram Users)

**In Draw.io**:
1. View → Layers (or Ctrl+Shift+L)
2. Check/uncheck layers to show/hide:
   - ☑️ Main (always recommended)
   - ☐ Modals (adds UI details)
   - ☐ MCP (adds processing details)
   - ☐ Alternatives (adds optional paths)

**Recommended Combinations**:
- **Product Manager**: Main + Alternatives (understand all possible paths)
- **UX Designer**: Main + Modals (understand all UI interactions)
- **Developer**: Main + Modals + MCP (understand full system)
- **Architecture Review**: All layers (complete system view)

---

**Status**: Specification Complete - Ready to Implement  
**Next**: Restructure existing diagram with layer support
