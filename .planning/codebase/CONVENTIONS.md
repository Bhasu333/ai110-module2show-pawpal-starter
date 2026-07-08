# Coding Conventions

This document outlines the coding standards, naming conventions, and style rules for the PawPal+ repository.

## Python Coding Style
- **PEP 8 Guidelines**: Function and variable names use `snake_case`, and class names use `PascalCase`.
- **Dataclasses**: Use `@dataclass` from the Python `dataclasses` module to define data containers (`Task`, `Pet`) to reduce boilerplate.

## Human Student Style Rules
To match authentic student execution:
- **Variable Names**: Use short, slightly inconsistent names (e.g. `rs`, `tk_list`, `sc`, `own`, `p`) rather than overly verbose names.
- **Comments**: Casual inline notes expressing doubt or reminding of syntax (e.g., `# TODO: make sure timedelta works`, `# reminder: start tests with test_`). No redundant AI-style narration above every single line.
- **Dead Variables**: Unevenly scatter 5–9 unused variables across the files to represent natural design changes during development.
- **Error Handling**: Focused guards added where issues occur during manual runs, rather than comprehensive defensive validation upfront.
