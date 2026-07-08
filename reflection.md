# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design organizes pet care routines into four core classes. I included `Task` to represent individual pet activities (like feedings, walks, medications), `Pet` to group a list of tasks for a specific pet, `Owner` to coordinate multiple pets under one person, and `Scheduler` to act as the logical engine that organizes and checks tasks. The `Task` class holds descriptive data and handles completions, the `Pet` class manages its own metadata and task additions, the `Owner` class coordinates pets and aggregates all tasks, and the `Scheduler` implements sorting, filtering, conflict alerts, and recurrence algorithms.

**b. Design changes**

Yes, my design changed slightly during implementation. Originally, I did not include the `due_date` attribute in the `Task` class. However, during the coding phase, I realized that to implement the daily recurrence logic correctly, I needed a way to increment the calendar date by one day using `datetime.timedelta`. Therefore, I added `due_date` to `Task` and updated `mark_complete()` to accept a `pet` parameter so it could automatically append the rolled-over task back to the pet's tasks list.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers three primary constraints: pet ownership (tasks must be assigned to specific pets), task completion status, and chronological due times. I decided that chronological time-based ordering was the most critical constraint because a pet owner needs a sequential daily roadmap to follow throughout the day.

**b. Tradeoffs**

One tradeoff my scheduler makes is that conflict detection only flags exact start-time collisions (e.g. two tasks scheduled at "08:30") rather than calculating task overlaps based on duration (e.g. walking a dog for 30 minutes at 08:30 overlapping with feeding a cat at 08:45). This is reasonable because for simple daily pet care tasks, a basic warning for exact start times is lightweight and sufficient to alert an owner of immediate bottlenecks without overcomplicating the algorithm.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to help brainstorm class attributes, write the Mermaid class diagram, and suggest template structures for the CLI demo script. Prompts asking "suggest a clear, readable way to format this schedule output for the terminal" and asking for `timedelta` examples were the most helpful.

**b. Judgment and verification**

I did not accept the AI's suggestion to use an external cron job library for task recurrence. I evaluated that a simple, self-contained Python approach using `datetime.timedelta` to auto-spawn the next day's task directly in the pet's list was far cleaner and avoided unnecessary external dependencies.

---

## 4. Testing and Verification

**a. What you tested**

I tested core task addition (increasing task counts), completion status flags, chronological sorting correctness, conflict flagging, and daily recurrence auto-spawning. These tests were important to ensure the data models and scheduler rules were perfectly correct before connecting them to the Streamlit UI.

**b. Confidence**

I am highly confident (5/5 stars) in the scheduler's reliability because all 5 unit tests pass successfully in pytest. If I had more time, I would write tests checking for invalid string formats in `due_time` (e.g. "noon") and negative integer durations.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the CLI-first workflow. Writing the logic in `pawpal_system.py` and verifying it with `main.py` and `pytest` first made wiring up the Streamlit UI in `app.py` incredibly fast and bug-free.

**b. What you would improve**

If I had another iteration, I would implement duration-based overlap warnings to make conflict detection more comprehensive for tasks that run long.

**c. Key takeaway**

An important takeaway is that designing the UML blueprint upfront prevents architectural confusion later, and that using separate AI chat sessions for design, code, and testing keeps the context clean and helps avoid logic bugs.

