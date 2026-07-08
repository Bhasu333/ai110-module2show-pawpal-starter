# Requirements: PawPal+

**Defined:** 2026-07-08
**Core Value:** A clean, OOP-driven pet care scheduling system that handles task organization, sorting, recurrence, and conflict warnings robustly.

## v1 Requirements

### System Design & UML
- [ ] **UML-01**: Draft class diagram saved to `diagrams/uml_draft.mmd` with Owner, Pet, Task, Scheduler.
- [ ] **UML-02**: Final class diagram reflecting final implementation saved to `diagrams/uml_final.mmd`.
- [ ] **UML-03**: Diagram illustrates correct class relationships (composition/association).

### OOP Core Logic Layer
- [ ] **OOP-01**: `Task` class holds description, due time/date, status, frequency, and completion methods.
- [ ] **OOP-02**: `Pet` class holds name, species, tasks list, and methods to add/list tasks.
- [ ] **OOP-03**: `Owner` class holds name, pets list, and methods to manage pets.
- [ ] **OOP-04**: `Scheduler` class retrieves, organizes, or manages tasks across multiple pets.
- [ ] **OOP-05**: Code implemented cleanly in `pawpal_system.py`.

### Scheduling Algorithms
- [ ] **ALGO-01**: Implement chronological sorting of tasks by due time ("HH:MM" string format).
- [ ] **ALGO-02**: Implement task filtering (e.g. by pet name or completion status).
- [ ] **ALGO-03**: Implement automatic recurrence execution (rescheduling daily/weekly tasks for future date).
- [ ] **ALGO-04**: Implement task conflict detection (time overlap or exact match) flagging warning messages.

### CLI verification
- [ ] **CLI-01**: `main.py` demo script instantiates classes, adds tasks, and prints schedule.
- [ ] **CLI-02**: Output of `main.py` pasted in `README.md` as fenced code block.

### UI Integration
- [ ] **UI-01**: `app.py` imports `pawpal_system.py` logic layer.
- [ ] **UI-02**: Session state used in `app.py` to persist `Owner` data.
- [ ] **UI-03**: UI actions (adding pet, scheduling task, rendering list) wired to logic methods.
- [ ] **UI-04**: UI displays sorted schedules and conflict warning messages.

### Testing & Reflections
- [ ] **TEST-01**: `tests/test_pawpal.py` contains tests for task completion and task additions.
- [ ] **TEST-02**: `tests/test_pawpal.py` contains tests for sorting, filtering, conflicts, or recurrence.
- [ ] **TEST-03**: All unit tests pass in local environment.
- [ ] **DOC-01**: `README.md` updated with Smarter Scheduling table, test output logs, and walkthrough.
- [ ] **DOC-02**: `reflection.md` answered with design choices, tradeoffs, and AI strategy details.

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| UML-01      | Phase 1 | Pending |
| UML-02      | Phase 3 | Pending |
| UML-03      | Phase 1 | Pending |
| OOP-01      | Phase 2 | Pending |
| OOP-02      | Phase 2 | Pending |
| OOP-03      | Phase 2 | Pending |
| OOP-04      | Phase 2 | Pending |
| OOP-05      | Phase 2 | Pending |
| ALGO-01     | Phase 2 | Pending |
| ALGO-02     | Phase 2 | Pending |
| ALGO-03     | Phase 2 | Pending |
| ALGO-04     | Phase 2 | Pending |
| CLI-01      | Phase 2 | Pending |
| CLI-02      | Phase 2 | Pending |
| UI-01       | Phase 3 | Pending |
| UI-02       | Phase 3 | Pending |
| UI-03       | Phase 3 | Pending |
| UI-04       | Phase 3 | Pending |
| TEST-01     | Phase 2 | Pending |
| TEST-02     | Phase 2 | Pending |
| TEST-03     | Phase 2 | Pending |
| DOC-01      | Phase 3 | Pending |
| DOC-02      | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 23 total
- Mapped to phases: 23
- Unmapped: 0 ✓

---
*Last updated: 2026-07-08 after GSD initialization*
