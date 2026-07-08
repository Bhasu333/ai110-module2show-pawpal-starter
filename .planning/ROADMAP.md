# Roadmap: PawPal+

## Overview
This roadmap outlines our progression from UML design to CLI-first Python implementation, algorithm writing, automated testing, and finally Streamlit integration and documentation.

## Phases
- [ ] **Phase 1: System Design** - Brainstorm classes, draft the Mermaid UML diagram (`diagrams/uml_draft.mmd`), create code skeletons in `pawpal_system.py`, and complete Section 1 of `reflection.md`.
- [ ] **Phase 2: Core Implementation & CLI** - Fully implement logic layer classes and algorithms (sorting, filtering, conflicts, recurrence), build a verification script `main.py`, run automated tests in `tests/test_pawpal.py`, and make Commit 2.
- [ ] **Phase 3: Streamlit UI Integration & Finalize** - Import logic into `app.py`, integrate session state memory, display warnings and schedules in UI, finalize UML, complete `reflection.md` and `README.md`, make final commit, and push.

## Phase Details

### Phase 1: System Design
**Goal**: Design the OOP architecture and write code skeletons.
**Depends on**: Nothing (cloned starter)
**Requirements**: UML-01, UML-03, OOP-05 (skeleton)
**Success Criteria**:
  1. Mermaid UML draft diagram `diagrams/uml_draft.mmd` created.
  2. Classes, attributes, and methods defined in a skeleton structure in `pawpal_system.py`.
  3. `reflection.md` section 1a completed.
**Plans**: 1 plan

Plans:
- [ ] 01-01: Draft UML class diagram and scaffold the pawpal_system.py skeleton.

### Phase 2: Core Implementation & CLI
**Goal**: Implement the models, scheduling algorithms, CLI demo script, and unit tests.
**Depends on**: Phase 1
**Requirements**: OOP-01, OOP-02, OOP-03, OOP-04, OOP-05, ALGO-01, ALGO-02, ALGO-03, ALGO-04, CLI-01, CLI-02, TEST-01, TEST-02, TEST-03
**Success Criteria**:
  1. Classes in `pawpal_system.py` fully implemented.
  2. Sorting, filtering, conflict warnings, and recurrence logic implemented and verified.
  3. Standalone demo script `main.py` successfully runs and outputs the daily schedule.
  4. Unit tests pass with `pytest`.
**Plans**: 1 plan

Plans:
- [ ] 02-01: Complete OOP model implementations, scheduler algorithms, main.py runner, and test suite.

### Phase 3: Streamlit UI Integration & Finalize
**Goal**: Bind backend logic to frontend Streamlit UI, finalize documentation, and push.
**Depends on**: Phase 2
**Requirements**: UML-02, UI-01, UI-02, UI-03, UI-04, DOC-01, DOC-02
**Success Criteria**:
  1. Streamlit `app.py` successfully reads and writes `st.session_state.owner`.
  2. Forms in UI correctly invoke logic layer methods and render updated schedules and warnings.
  3. Final UML diagram `diagrams/uml_final.mmd` updated.
  4. `README.md` and `reflection.md` fully completed.
**Plans**: 1 plan

Plans:
- [ ] 03-01: Wire Streamlit frontend, finalize documentation, and push to GitHub.

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. System Design | 0/1 | Not started | - |
| 2. Core & CLI | 0/1 | Not started | - |
| 3. UI & Finalize | 0/1 | Not started | - |
