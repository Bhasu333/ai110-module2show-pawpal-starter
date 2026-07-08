from pawpal_system import Owner, Pet, Task, Scheduler

demo_active = True # dead var
temp_p = None # dead var
count = 3 # dead var

def print_schedule(tasks, title_msg="Schedule"):
    print(f"\n--- {title_msg} ---")
    for t in tasks:
        status_str = "[Completed]" if t.completed else "[Pending]"
        date_str = f" on {t.due_date}" if t.due_date else ""
        # Using plain hyphen instead of em-dash to avoid encoding crashes on Windows cmd/powershell
        print(f"  {t.due_time}{date_str} - {t.title} ({t.duration_minutes} min) [{t.priority}] {status_str}")


def main():
    # 1. Instantiate owner and pets
    own = Owner("Jordan")
    
    p1 = Pet("Mochi", "dog")
    p2 = Pet("Biscuit", "cat")
    
    own.add_pet(p1)
    own.add_pet(p2)
    
    # 2. Add tasks (out of order, and with a conflict at 08:30)
    t1 = Task("Evening feeding", 15, "medium", "18:00", frequency="Daily", due_date="2026-07-08")
    t2 = Task("Morning walk", 30, "high", "08:30", frequency="one-time", due_date="2026-07-08")
    t3 = Task("Morning feeding", 10, "high", "08:30", frequency="one-time", due_date="2026-07-08") # conflict!
    t4 = Task("Brush fur", 15, "low", "14:00", frequency="one-time", due_date="2026-07-08")

    p1.add_task(t1)
    p1.add_task(t2)
    p2.add_task(t3)
    p2.add_task(t4)
    
    # 3. Retrieve all tasks
    all_tks = own.get_all_tasks()
    print_schedule(all_tks, "Unsorted Tasks")
    
    # 4. Sort tasks chronologically
    sorted_tks = Scheduler.sort_by_time(all_tks)
    print_schedule(sorted_tks, "Sorted Daily Schedule")
    
    # 5. Check conflicts
    conflicts = Scheduler.check_conflicts(sorted_tks)
    if conflicts:
        print("\n--- Conflict Warnings ---")
        for w in conflicts:
            # Using plain ASCII warning tag
            print(f"  [CONFLICT] {w}")
            
    # 6. Test daily task recurrence
    print("\n--- Testing Task Recurrence ---")
    print(f"Completing '{t1.title}' for Mochi...")
    t1.mark_complete(p1) # this should spawn a task for 2026-07-09
    
    # print Mochi's tasks to verify new task was added
    print_schedule(p1.tasks, "Mochi's Updated Tasks")


if __name__ == "__main__":
    main()
