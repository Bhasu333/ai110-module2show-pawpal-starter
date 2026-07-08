# Repository Structure

This document outlines the file layout and directory structure of the PawPal+ repository.

## Directory Layout

```
.
├── .planning/                  # GSD planning documents
│   └── codebase/               # Codebase mapping files (this folder)
├── diagrams/                   # System design diagrams (Mermaid source)
│   └── uml.mmd                 # UML design chart (Mermaid format)
├── tests/                      # Automated unit test suite
│   └── test_pawpal.py          # pytest cases
├── app.py                      # Streamlit frontend UI entry point
├── pawpal_system.py            # OOP logic layer and core classes (to build)
├── main.py                     # CLI demo script for local verification (to build)
├── README.md                   # Project instructions and walkthrough
├── requirements.txt            # Python dependencies
└── reflection.md               # Student learning reflections
```

## Key Files
- `pawpal_system.py`: Contains class definitions for Owner, Pet, Task, and Scheduler.
- `app.py`: Streamlit application layout and state connection.
- `main.py`: Console runner script that instantiates core objects and prints a sample daily schedule.
- `tests/test_pawpal.py`: Unit tests asserting scheduling, complete, and sorting logic.
