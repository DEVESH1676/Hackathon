# Phase 4 Context: Architectural Observability (The Nexus Blueprint)

## Objective
Implement a "Nexus Blueprint" tab in the React frontend to expose the system's inner workings through dynamic Mermaid.js diagrams and a searchable glossary. This ensures the system is understandable, debuggable, and easily extensible.

## Design Decisions

### D-01: Diagrams-as-Code (Mermaid.js)
We will use **Mermaid.js** to render the execution flow and dependency graphs. Diagrams will be defined as template strings and rendered dynamically based on the current system configuration.

### D-02: Searchable Data Dictionary (The Term Inspector)
A searchable UI component will map abstract concepts (e.g., "Centroid," "Confidence," "Multi-hop") to their:
- **Logical Definition**: What it means for the user.
- **Code Path**: The specific file and function implementing the logic.
- **Storage Path**: The DB table and column where data is persisted.

### D-03: Blueprint Source of Truth
We will create a `frontend-v2/src/config/blueprint.ts` file that acts as the "source of truth" for the architectural documentation. This allows us to update the documentation alongside code changes.

## Downstream Guidance
- **Researcher:** Investigate Mermaid.js React integration and best patterns for rendering dynamic diagrams. Map the existing v4.0 code paths for all 7 pipeline steps.
- **Planner:** Break down the UI implementation into sub-tasks: Library setup, Data structure definition, and Blueprint tab development.
