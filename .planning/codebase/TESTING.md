# Testing Patterns

This document describes the testing practices and patterns for PawPal+.

## Test Framework
- **pytest**: The primary framework for unit testing.
- **Location**: All tests reside in `tests/test_pawpal.py`.

## Test Execution
Tests can be executed in the terminal using:
```bash
python -m pytest
```

## Testing Focus Areas
1. **Core Data Flow**: Verify that adding a task to a `Pet` increases its task list size, and changing task completion flags updates the status correctly.
2. **Sorting Logic**: Ensure tasks are returned chronologically by due time ("HH:MM" format).
3. **Conflict Detection**: Verify that overlapping or duplicate task times are flagged by the Scheduler.
4. **Recurrence Logic**: Confirm that daily task completions auto-generate tasks for the next day.
