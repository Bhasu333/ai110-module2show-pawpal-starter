# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Here is the console output from running the CLI demo script `main.py`:

```
--- Unsorted Tasks ---
  18:00 on 2026-07-08 - Evening feeding (15 min) [medium] [Pending]
  08:30 on 2026-07-08 - Morning walk (30 min) [high] [Pending]
  08:30 on 2026-07-08 - Morning feeding (10 min) [high] [Pending]
  14:00 on 2026-07-08 - Brush fur (15 min) [low] [Pending]

--- Sorted Daily Schedule ---
  08:30 on 2026-07-08 - Morning walk (30 min) [high] [Pending]
  08:30 on 2026-07-08 - Morning feeding (10 min) [high] [Pending]
  14:00 on 2026-07-08 - Brush fur (15 min) [low] [Pending]
  18:00 on 2026-07-08 - Evening feeding (15 min) [medium] [Pending]

--- Conflict Warnings ---
  [CONFLICT] Warning: 'Morning feeding' and 'Morning walk' are both scheduled at 08:30!

--- Testing Task Recurrence ---
Completing 'Evening feeding' for Mochi...

--- Mochi's Updated Tasks ---
  18:00 on 2026-07-08 - Evening feeding (15 min) [medium] [Completed]
  08:30 on 2026-07-08 - Morning walk (30 min) [high] [Pending]
  18:00 on 2026-07-09 - Evening feeding (15 min) [medium] [Pending]
```

## 🧪 Testing PawPal+

We use `pytest` to assert the correctness of our scheduling constraints and behaviors. The tests cover task completion status changes, task addition tracking, chronological sorting correctness, conflict warnings, and daily task recurrence auto-spawning.

Command to run tests:
```bash
python -m pytest
```

Successful test run output:
```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\bhasw\.gemini\antigravity\playground\ionized-helix
configfile: pytest.ini
plugins: anyio-4.14.0
collected 5 items

tests\test_pawpal.py .....                                               [100%]

============================== 5 passed in 0.05s ==============================
```

**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5 stars) - Highly reliable local scheduling layer, validated through automated unit assertions.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks chronologically using string due times in "HH:MM" format. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by "pending" or "completed" status. UI also allows filtering by specific pet name. |
| Conflict handling | `Scheduler.check_conflicts()` | Identifies tasks scheduled at the same time and warns the user. |
| Recurring tasks | `Task.mark_complete()` / `Scheduler.handle_recurrence()` | Daily tasks automatically roll over to the next day (`due_date` incremented by 1 day using `timedelta`). |

## 📸 Demo Walkthrough

1. Run the app in your browser with `python -m streamlit run app.py`. Enter "Jordan" as the owner name in the sidebar.
2. In the sidebar's **Register New Pet** form, register "Mochi" (dog) and "Biscuit" (cat). They will show up in the sidebar registered list.
3. In the main panel's **Schedule Care Task** section, schedule a "Morning walk" for "Mochi" at "08:30" (duration 30 min, priority high).
4. In the same section, schedule a "Morning feeding" for "Biscuit" at "08:30". A yellow alert warning will immediately appear at the top of the planner: `⚠️ Conflict Alert: Warning: 'Morning feeding' and 'Morning walk' are both scheduled at 08:30!`.
5. Add a "Daily meds" task for "Mochi" at "09:00", setting the frequency to **Daily**.
6. View **Today's Daily Planner** to see all tasks chronologically sorted by due time.
7. Click the **Complete** button next to Mochi's "Daily meds" task. Its status changes to a checkmark (Completed), and a new pending "Daily meds" task is automatically scheduled for the next day.
8. Use the **Filter Status** or **Filter Pet** dropdown selectors to filter tasks dynamically.
