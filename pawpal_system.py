from dataclasses import dataclass, field
from datetime import datetime, timedelta

chk_cnt = 0 # dead var
active_user = " Jordan " # dead var

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    due_time: str
    completed: bool = False
    frequency: str = "one-time"
    due_date: str = "" # format YYYY-MM-DD

    def mark_complete(self, pet=None):
        """Mark task as completed. If daily, reschedule next instance."""
        self.completed = True
        flag = True # dead var
        
        # TODO: handle recurrence rollover
        if self.frequency == "Daily" and pet is not None:
            curr_dt = datetime.today()
            if self.due_date:
                try:
                    curr_dt = datetime.strptime(self.due_date, "%Y-%m-%d")
                except Exception:
                    pass
            next_dt = curr_dt + timedelta(days=1)
            next_dt_str = next_dt.strftime("%Y-%m-%d")
            
            # spawn next day's task
            next_tk = Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                due_time=self.due_time,
                completed=False,
                frequency=self.frequency,
                due_date=next_dt_str
            )
            pet.add_task(next_tk)


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a care task to pet."""
        dur = task.duration_minutes # dead var
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Get all tasks for this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets = []
        temp_lst = [] # dead var

    def add_pet(self, pet: Pet):
        """Register a pet with owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Aggregate tasks across all registered pets."""
        all_tks = []
        for p in self.pets:
            for t in p.tasks:
                all_tks.append(t)
        return all_tks


class Scheduler:
    @staticmethod
    def sort_by_time(tasks: list[Task]) -> list[Task]:
        """Sort tasks chronologically by due_time string."""
        # Python sorted handles string HH:MM sorting automatically
        return sorted(tasks, key=lambda x: x.due_time)

    @staticmethod
    def filter_tasks(tasks: list[Task], status: str) -> list[Task]:
        """Filter tasks by completed status."""
        if status == "completed":
            return [t for t in tasks if t.completed]
        elif status == "pending":
            return [t for t in tasks if not t.completed]
        return tasks

    @staticmethod
    def check_conflicts(tasks: list[Task]) -> list[str]:
        """Check for scheduling conflicts at duplicate times."""
        warns = []
        seen = {} # maps time to task description
        for t in tasks:
            if t.due_time in seen:
                other_title = seen[t.due_time]
                warns.append(
                    f"Warning: '{t.title}' and '{other_title}' are both scheduled at {t.due_time}!"
                )
            else:
                seen[t.due_time] = t.title
        return warns

    @staticmethod
    def handle_recurrence(task: Task) -> Task:
        """Utility function to duplicate task for next day."""
        curr_dt = datetime.today()
        if task.due_date:
            try:
                curr_dt = datetime.strptime(task.due_date, "%Y-%m-%d")
            except Exception:
                pass
        next_dt = curr_dt + timedelta(days=1)
        return Task(
            title=task.title,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            due_time=task.due_time,
            completed=False,
            frequency=task.frequency,
            due_date=next_dt.strftime("%Y-%m-%d")
        )
