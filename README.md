# Project Mimir
Mimir is a foundation for self-evolving methodologies for well-defined tasks, providing a framework to capture your methodology, enable its consumption via MCP, and facilitate AI-driven evolution inspired by genetic algorithms.

# Conceptual Vision
1. The methodology is decomposed into basic units of work (Activities) fulfilling Goals, and are combined into Workflows executed by Roles (Agents and/or people), and are governed by Howtos, and are consuming and producing Deliverables.
2. This Ontology can be extended. We have an OpenAPI-compatible API + GUI to edit the Methodology, including modification of the Ontology. New types are introspected and exposed via /api/new_type/* endpoints, just like base Ontology types.
3. Methodology goes into the graph. Methodology is versioned - every modification (Activity, Howto, etc.) produces a version of the Methodology.
4. Methodology is used to formulate a Work Order(s): activity + howto + input/output Deliverables and their checklists = Work Order. Work Orders are tracked via any Task/Issue system (we expect the user environment to have an MCP for GitHub, Jira, etc.) Work Orders are self-contained and fulfilled with people and/or agents. Work Orders contain a reference to the version of the Methodology they use.
5. After completing an execution of the workflow run, Thoth AI retrospects the run and suggests edits/extensions of the Workflow - the PI (proposed improvements). The user incorporates or rejects the suggestions, explaining to Thoth AI the reasoning behind their decision, which Thoth learns. Therefore, both Thoth and methodology evolve.

# Stack
1. Neo4J as data layer.
2. FastAPI for OpenAPI talking to Methology.
3. React+Vite+Zustand+Tailwind+shadcdn for UI to edit methodology and work with PI (proposed improvements).
4. Model of choice for Maat AI (the task master), Toth AI (the improver). GPT-4o by default.
5. MCP (as container) with Maat and Toth to manage work, review the outcome, and suggest improvements.
