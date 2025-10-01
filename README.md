# Project Mimir
Mimir is a foundation for self-evolving methodologies for well-defined tasks, providing a framework to capture your methodology, enable its consumption via MCP, and facilitate AI-driven evolution inspired by genetic algorithms.

# Conceptual Vision
1. The methodology is decomposed into basic units of work (Activities) fulfilling Goals, and are combined into Workflows executed by Roles (Agents and/or people), and are governed by Howtos, and are consuming and producing Deliverables.
2. This Ontology can be extended. We have an OpenAPI-compatible API + GUI to edit the Methodology, including modification of the Ontology. New types are introspected and exposed via /api/new_type/* endpoints, just like base Ontology types.
3. Methodology goes into the graph. Methodology is versioned - every modification (Activity, Howto, etc.) produces a version of the Methodology.
4. Methodology is used to formulate a Work Order(s): activity + howto + input/output Deliverables and their checklists = Work Order. Work Orders are tracked via any Task/Issue system (we expect the user environment to have an MCP for GitHub, Jira, etc.) Work Orders are created by Tyr AI, self-contained and fulfilled with people and/or agents. Work Orders contain a reference to the version of the Methodology they use.
5. After completing an execution of the workflow run, Saga AI retrospects the run and suggests edits/extensions of the Workflow - the PI (proposed improvements). The user incorporates or rejects the suggestions, explaining to Saga AI the reasoning behind their decision, which Saga learns. Therefore, both Saga and methodology evolve.

## Stack

1. Neo4J as data layer.
2. FastAPI for OpenAPI-compatible API talking to Methodology.
3. React+Vite+Zustand+Tailwind+shadcdn for UI to edit methodology and work with PI (proposed improvements).
4. Model of choice for Tyr AI (the task master), Saga AI (the improver). GPT-4o by default.
5. MCP (as container) with Tyr and Saga to manage work, review the outcome, and suggest improvements.

## Key Concepts

### Well-Defined Tasks

Mimir is designed for methodologies around well-defined, repeatable tasks such as:

- **Feature-driven software engineering** - from requirements to deployment
- **User-flow-driven UX design** - from user research to validated designs
- **BDD-style acceptance testing** - from scenarios to automated test suites

### Genetic Algorithm Inspiration

Saga AI uses a fitness function to evaluate methodology effectiveness:

- **Default fitness metric**: Number of corrections required to complete work correctly (target: zero)
- **Analysis focus**: When corrections are needed, identify root causes:
  - Is Activity X poorly defined?
  - Are upstream activities missing key outputs?
  - Do downstream activities need different inputs?
- **Evolution mechanism**: Successful methodology variations are preserved and propagated

### Activities vs Howtos

- **Activity**: The *what* with generic guidance
  - Example: "Create a screen mockup"
- **Howto**: The *how* with specific implementation details
  - Example: "Creating mockups with React and Shadcn"

### Deliverables

Deliverables are the connecting tissue between activities:

- **Definition**: Outputs from one activity that become inputs to another activity
- **Purpose**: Enable workflow composition and dependency tracking
- **Examples**: Design specifications, code modules, test cases, documentation
