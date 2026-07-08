from pawpal_system import Owner, Pet, Task, Scheduler

# reminder: pytest functions must start with test_ to be auto-discovered

def test_task_completion():
    # Verify that calling mark_complete changes completed status
    t = Task("Feed cat", 17, "high", "08:15")
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_task_addition():
    # Verify that adding a task to Pet increases task count
    p = Pet("Luna", "cat")
    assert len(p.tasks) == 0
    t1 = Task("Play time", 23, "low", "15:00")
    p.add_task(t1)
    assert len(p.tasks) == 1
    assert p.tasks[0].title == "Play time"


def test_task_sorting_chronological():
    # Verify tasks are returned in chronological order
    t1 = Task("Night walk", 45, "medium", "21:30")
    t2 = Task("Breakfast", 15, "high", "07:00")
    t3 = Task("Midday nap check", 10, "low", "13:00")
    
    sorted_lst = Scheduler.sort_by_time([t1, t2, t3])
    assert sorted_lst[0].due_time == "07:00"
    assert sorted_lst[1].due_time == "13:00"
    assert sorted_lst[2].due_time == "21:30"


def test_recurrence_daily_reschedules():
    # Confirm that marking a daily task complete creates a new task for the following day
    p = Pet("Max", "dog")
    t = Task("Daily meds", 5, "high", "09:00", frequency="Daily", due_date="2026-07-08")
    p.add_task(t)
    
    # Complete the task
    t.mark_complete(p)
    
    assert len(p.tasks) == 2
    assert p.tasks[0].completed is True
    
    # Next day task checks
    new_t = p.tasks[1]
    assert new_t.title == "Daily meds"
    assert new_t.completed is False
    assert new_t.due_date == "2026-07-09"
    assert new_t.due_time == "09:00"


def test_conflict_detection_flagging():
    # Verify that the Scheduler flags duplicate times
    t1 = Task("Grooming", 50, "medium", "10:30")
    t2 = Task("Vet consult", 60, "high", "10:30")
    t3 = Task("Dinner", 20, "low", "18:00")
    
    warns = Scheduler.check_conflicts([t1, t2, t3])
    assert len(warns) == 1
    assert "10:30" in warns[0]
