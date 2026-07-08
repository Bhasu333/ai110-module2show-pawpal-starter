# Tech Debt & Concerns

This document tracks known issues, technical debt, and architectural concerns.

## Starter Code Analysis
- **Missing Logic Layer**: The starter code contains no implementation in `pawpal_system.py`. This is our primary focus.
- **Streamlit State Reset**: Because Streamlit is stateless and reruns the entire script on every user action, we must carefully store the initialized `Owner` and `Pet` instances in `st.session_state` to prevent data loss.
- **Overlapping vs. Exact Conflicts**: The conflict detection algorithm is simplified to check for exact "HH:MM" start-time matches. Checking for duration overlaps is a potential future enhancement but is out of scope for the MVP.
