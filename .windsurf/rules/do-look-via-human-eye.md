---
trigger: model_decision
description: When drawing a diagram in Draw.io or Mermaid check if it looks OK to human eye.
---

---
trigger: model_decision
description: When drawing a diagram in Draw.io or Mermaid check if it looks OK to human eye.
---

Render the diagram the way human eye will look on it. Check for visual perception hindrances:

## Layout and Spacing Issues
1. **Overlapping components** - ensure all elements are clearly separated
2. **Too crowded layout** - components bunched too tight together so it's hard to understand what is what
3. **Text over arrows** covers them completely
4. **Inconsistent spacing** - maintain uniform gaps between similar elements
5. **Poor alignment** - elements should align to a grid or consistent baseline

## Flow and Navigation Clarity
6. **Arrow direction confusion** - ensure flow direction is immediately obvious
7. **Missing or unclear connection points** - arrows should clearly connect specific elements
8. **Crossing arrows** - minimize line crossings that create visual confusion
9. **Inconsistent arrow styles** - use consistent styling for similar types of connections
10. **Flow loops** - ensure circular flows are visually clear and don't create confusion
11. **Arrow bunching** - avoid multiple arrows entering/exiting the same side of an element
12. **Parallel arrow overlap** - stagger parallel arrows with different routing paths
13. **Decision point congestion** - space decision diamonds wider to accommodate multiple exit paths
14. **Phase transition crowding** - use dedicated routing lanes between major workflow phases
15. **Connector spacing** - maintain minimum 40px gaps between parallel arrow segments
16. **Junction points** - avoid more than 3 arrows meeting at any single point
17. **Routing diversity** - use different path shapes (straight, curved, stepped) to distinguish flows
18. **Error flow separation** - route error/retry flows away from primary success paths
19. **Label collision** - ensure arrow labels don't overlap with other elements or arrows
20. **Multi-level routing** - use different vertical levels for crossing flows to maintain clarity

## Visual Hierarchy and Grouping
21. **Lack of visual grouping** - related elements should be visually grouped together
22. **Inconsistent element sizing** - similar elements should have similar sizes
23. **Poor color contrast** - ensure sufficient contrast between elements and backgrounds
24. **Missing visual hierarchy** - important elements should be visually prominent

## Legend and Documentation
25. **Missing or incomplete legend** - all visual elements must be explained
26. **Legend placement** - legend should be easily visible and not interfere with main content
27. **Unclear symbols** - all shapes, colors, and symbols must be intuitive or explained
28. **Text readability** - ensure all text is large enough and has sufficient contrast

## Technical Considerations for Draw.io
29. **Canvas size** - ensure diagram fits well within standard page sizes
30. **Export compatibility** - verify diagram renders correctly when exported
31. **Element IDs** - use meaningful IDs for programmatic access if needed
32. **Layer organization** - use layers to organize complex diagrams
33. **Connection anchor points** - use specific anchor points rather than automatic connections
34. **Waypoint management** - add manual waypoints to control arrow routing paths
35. **Arrow style hierarchy** - use different stroke weights (1px, 2px, 3px) for different flow importance
36. **Color coding consistency** - maintain consistent color schemes for different flow types
37. **Curved vs orthogonal** - choose appropriate line styles based on diagram complexity
38. **Arrow head sizing** - ensure arrow heads are proportional to line thickness
39. **Flow grouping** - visually group related flows using similar colors or styles
40. **Spacing multipliers** - use grid-based spacing (20px, 40px, 60px) for consistent arrow separation

## Validation Steps
Before finalizing any diagram:
1. **Zoom out test** - diagram should be understandable at 50% zoom
2. **Fresh eyes test** - can someone unfamiliar understand the flow immediately?
3. **Print test** - would this be readable if printed in black and white?
4. **Tablet test** - is it readable on smaller screens?
5. **Arrow clarity test** - can you trace each flow path without confusion?
6. **Intersection test** - verify no critical information is lost at arrow crossings

## Specific to UX Flow Diagrams
41. **Decision points clarity** - decision diamonds should have clear Yes/No paths
42. **Error flow visibility** - error paths should be visually distinct (e.g., red, dashed)
43. **Modal/form relationships** - clear connection between triggers and UI components
44. **Screen transitions** - obvious navigation between different screens/pages
45. **Phase separation** - distinct visual boundaries between workflow phases
46. **User journey continuity** - primary user path should be visually prominent and easy to follow
47. **Component hierarchy** - pages > forms > buttons > modals should have clear visual weight differences
48. **State transitions** - clear indication of what triggers each state change