# Screen Flow Diagram Update Needed

**File**: `screen-flow.drawio`  
**Tab**: "MVP Flow - Local FOB"  
**Section**: ACT 5 - Activities

---

## ⚠️ **Updates Required**

The following changes need to be made to the ACT 5 (Activities) section in the MVP Flow diagram:

### **1. Activity Form Fields**

#### **REMOVE**
- "Description" field with plain textarea

#### **ADD**
- **"Guidance"** field (8-row textarea)
- Markdown icon indicator
- Tooltip: "Supports Markdown: headers, lists, tables, code blocks, Mermaid diagrams"
- Placeholder text: "## Overview\n\n## Steps\n\n## Example"

### **2. Activity View Screen**

#### **UPDATE**
- Change "Description" label to **"Guidance"**
- Show Markdown rendering indicator (Markdown logo)
- Add note: "Rendered from Markdown with Mermaid support"
- Visual: Show formatted text instead of plain text

### **3. Has Dependencies Field**

#### **ADD CLARIFICATION**
- Keep checkbox but add note: **(Documentation Only)**
- Tooltip: "Indicates prerequisites exist - does not enforce"
- Visual indicator: Different color or dashed border
- Note box: "Future: Will become actual dependency tracking"

### **4. Phase Assignment**

#### **ADD NOTE**
- Dropdown label: "Phase (Optional)"
- Add info icon: "Phases are optional - not all workflows use them"

### **5. Order Field**

#### **ADD CLARIFICATION**
- Show "Auto-assigned if blank"
- Default value indicator

---

## 📋 **Specific Screen Updates**

### **FOB-ACTIVITIES-CREATE**

```
┌─────────────────────────────────────────┐
│ Create Activity                         │
├─────────────────────────────────────────┤
│ Name: [________________]                │
│                                         │
│ Guidance: 📝 Markdown supported         │
│ ┌─────────────────────────────────────┐ │
│ │ ## Overview                         │ │
│ │                                     │ │
│ │ ## Steps                            │ │
│ │                                     │ │
│ │ ## Example                          │ │
│ │                                     │ │
│ │ ```mermaid                          │ │
│ │ graph LR                            │ │
│ │ ```                                 │ │
│ └─────────────────────────────────────┘ │
│ ℹ️ Supports: Headers, Lists, Tables,   │
│    Code blocks, Mermaid diagrams        │
│                                         │
│ Phase: [Select...▼] (Optional)         │
│                                         │
│ Order: [__] (auto-assigned if blank)   │
│                                         │
│ ☐ Has Dependencies                     │
│   (Documentation only - future: M2M)   │
│                                         │
│ [Cancel] [Create Activity]             │
└─────────────────────────────────────────┘
```

### **FOB-ACTIVITIES-VIEW**

```
┌─────────────────────────────────────────┐
│ ← Back   [Edit] [Delete]                │
├─────────────────────────────────────────┤
│ Build Domain Model                       │
│ Phase: Modeling | Order: #1             │
│ ⚠️ Has Dependencies (doc only)          │
├─────────────────────────────────────────┤
│ Guidance 📝 (Rendered from Markdown)    │
├─────────────────────────────────────────┤
│                                         │
│ ## Overview                             │
│                                         │
│ Build an overall domain model...        │
│                                         │
│ ## Steps                                │
│                                         │
│ 1. Identify Major Domain Objects       │
│ 2. Create Class Diagram                │
│                                         │
│ ## Example                              │
│                                         │
│ ┌───────────────────────┐              │
│ │   Mermaid Diagram     │              │
│ │   (rendered as SVG)   │              │
│ └───────────────────────┘              │
│                                         │
│ ## Deliverables                         │
│                                         │
│ - Domain model diagram                  │
│ - Class definitions                     │
│                                         │
├─────────────────────────────────────────┤
│ 📅 Created: 2 days ago                  │
│ 📝 Updated: 1 day ago                   │
└─────────────────────────────────────────┘
```

---

## 🎨 **Visual Styling Notes**

### **Markdown Field Indicator**
- Use icon: 📝 or <i class="fa-brands fa-markdown">
- Background color: Light gray (#f8f9fa)
- Border: Dashed for "editable" state
- Font: Monospace for textarea

### **Rendered Guidance**
- Background: White
- Headers: Bold, larger font
- Code blocks: Gray background (#f8f9fa), monospace
- Mermaid diagrams: Centered, bordered
- Tables: Striped rows, bordered

### **Has Dependencies Badge**
- Current: Orange/yellow "⚠️ Has Dependencies"
- Add subtitle: "(Documentation only)"
- Or: Dashed border around checkbox
- Tooltip on hover explaining limitation

---

## 🔗 **Reference Implementation**

See actual implementation in:
- `templates/activities/create.html` (form)
- `templates/activities/detail.html` (rendered view)
- `docs/features/ACTIVITY_GUIDANCE_IMPLEMENTATION.md` (full spec)

---

## ✅ **Checklist for Diagram Update**

- [ ] Open `screen-flow.drawio` in draw.io editor
- [ ] Navigate to "MVP Flow - Local FOB" tab
- [ ] Locate ACT 5: Activities section
- [ ] Update CREATE form: Description → Guidance (8 rows)
- [ ] Add Markdown icon and tooltip
- [ ] Update VIEW screen: Show rendered Markdown example
- [ ] Add "Documentation only" note to Has Dependencies
- [ ] Add "(Optional)" label to Phase dropdown
- [ ] Add "auto-assigned" note to Order field
- [ ] Update visual styling to match implementation
- [ ] Save and commit diagram
- [ ] Delete this instruction file

---

**Note**: This file should be deleted after the diagram is updated.
