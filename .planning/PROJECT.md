# Project: PawPal+

## What This Is
A modular, object-oriented pet care task planner that helps owners schedule and manage daily tasks (feedings, walks, medications) across multiple pets. The project involves system design using UML, building a backend OOP logic layer, writing scheduler algorithms (sorting, filtering, conflicts, recurrence), writing automated tests, and integrating the logic into a Streamlit UI.

## Core Value
A clean, OOP-driven pet care scheduling system that handles task organization, sorting, recurrence, and conflict warnings robustly.

## Requirements

### Validated
(None yet - starting project design phase)

### Active
- [ ] **UML-01**: Design Mermaid UML diagrams for system architecture (draft and final) showing classes, methods, and relations.
- [ ] **OOP-01**: Implement core classes (Owner, Pet, Task, Scheduler) in `pawpal_system.py` using object-oriented principles.
- [ ] **ALGO-01**: Implement scheduling algorithms (task sorting, status/pet filtering, conflict warnings, recurring task automation).
- [ ] **CLI-01**: Create a standalone testing script `main.py` demonstrating system operations in the terminal and document CLI output in README.md.
- [ ] **UI-01**: Wire the Streamlit `app.py` frontend to the logic layer classes, leveraging session state for memory persistence.
- [ ] **TEST-01**: Create a pytest suite in `tests/test_pawpal.py` verifying system constraints and logic.
- [ ] **DOC-01**: Complete all reflection prompts in `reflection.md` and build a professional user manual in `README.md`.

## Context
- Python OOP, dataclasses, Streamlit state, pytest.
- Authentic human student coding style (abbreviated variable names, casual comments, dead variables).

## Constraints
- **Tech Stack**: Python 3, Streamlit, pytest.
- **Commit Pattern**: Commits at milestones to show gradual development.

## Key Decisions
| Decision | Rationale | Outcome |
|----------|-----------|---------|
| CLI-First | Build and verify logic in terminal before wiring to Streamlit to isolate issues. | — Pending |

---
*Last updated: 2026-07-08 after GSD initialization*
