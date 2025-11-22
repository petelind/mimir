---
description: Write BDD-style feature files for user interactions and journeys
auto_execution_mode: 3
---

# Feature File Creation Workflow

## Goal
Write BDD-style feature files for each page interaction and user journey using Gherkin syntax. In the screen flow (and mockups if they exist - if they do not its not a problem, as we can envision them using IA_guidelines.md) we have all Pages detailed. Now for every page we will have a .feature file detailing its behavior.

## Approach
One page is described in one .feature file. Page is deconstructed into Components (akin to React components), and each of them have one or more Scenarios detailing its behavior - think "View List of [Entities]", or "Primary button [and what happens when I click it]" etc. 

## Setup
- Create feature files **Location**: `docs/ux/features/[act]/[feature-name].feature` (create folders if they do not exist)
- Follow Gherkin syntax (Given/When/Then)

## Workflow Steps

### 1. Extract User Flows
- Review user journey, screen flow, and page specifications (if available)
- Identify sequence of actions which supposed to happen there
- Identify primary, secondary and optional actions/extensions - they all need to be covered by scenarios
- Envision start state and defaults
- Prioritize critical paths and edge cases

### 2. Write Feature Files
For each user flow, create:
- **Feature**: High-level description of functionality
- **Scenario**: Specific user interaction or use case
- **Steps**: Given/When/Then format describing the flow
- **Examples**: Data tables for scenario outlines (if applicable)

### 3. Structure Template
```gherkin
Feature: [Feature Name]
  As a [user type]
  I want to [goal]
  So that [benefit]

  Scenario: [Scenario Name]
    Given [initial context]
    When [action performed]
    Then [expected outcome]
    And [additional verification]
```

## Generic Example

```gherkin
Feature: CM Content Management
  As a content creator
  I want to create and edit content
  So that I can publish information for users

  Scenario: CM-1 User creates new content
    Given the user is on the content creation page
    When the user enters "Sample Title" in the title field
    And the user enters content in the editor
    And the user clicks the "Save" button
    Then the system displays a success message
    And the content appears in the content list

  Scenario Outline: CM-2 User validates required fields
    Given the user is on the content creation page
    When the user leaves the <field> empty
    And the user clicks "Save"
    Then the system displays "<error_message>"
    
    Examples:
      | field   | error_message           |
      | title   | Title is required       |
      | content | Content cannot be empty |
```

## Best Practices
- Make sure you follow naming convention for feature and scenario names if one was introduced in user-journey and/or screen flow (screen flow takes precedence)
- Use clear, business-readable language
- Focus on user behavior, not implementation details
- Include both happy path and error scenarios
- Keep scenarios focused and atomic
- Use scenario outlines for data-driven tests - having examples (derive from user journey) is highly desirable