# Integrations

This document tracks external integrations, APIs, and services utilized by the system.

## External Services
- **None**: PawPal+ is a self-contained local Python application. It does not integrate with any external databases, authentication providers, or third-party web services.

## Local Interfaces
- **Streamlit Interface**: The frontend `app.py` directly communicates with the local OOP backend classes in `pawpal_system.py`.
- **pytest Runner**: The test suite in `tests/test_pawpal.py` directly imports and asserts behaviors in `pawpal_system.py`.
