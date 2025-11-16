---
description: Write BDD-style feature files for user interactions and journeys
---

# Feature File Creation Workflow

## Goal
Write BDD-style feature files for each page interaction and user journey using Gherkin syntax.

## Setup
- Create feature files **Location**: `docs/ux/feature-files/[feature-name].feature` directory
- Use `.feature` file extension
- Follow Gherkin syntax (Given/When/Then)

## Workflow Steps

### 1. Extract User Flows
- Review user journey maps and page specifications
- Identify key user interactions and workflows
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
Feature: Content Management
  As a content creator
  I want to create and edit content
  So that I can publish information for users

  Scenario: User creates new content
    Given the user is on the content creation page
    When the user enters "Sample Title" in the title field
    And the user enters content in the editor
    And the user clicks the "Save" button
    Then the system displays a success message
    And the content appears in the content list

  Scenario Outline: User validates required fields
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
- Use clear, business-readable language
- Focus on user behavior, not implementation details
- Include both happy path and error scenarios
- Keep scenarios focused and atomic
- Use scenario outlines for data-driven tests  
