from dataclasses import dataclass, field

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    due_time: str
    completed: bool = False
    frequency: str = "one-time"

    def mark_complete(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets = []

    def add_pet(self, pet: Pet):
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    @staticmethod
    def sort_by_time(tasks: list[Task]) -> list[Task]:
        pass

    @staticmethod
    def filter_tasks(tasks: list[Task], status: str) -> list[Task]:
        pass

    @staticmethod
    def check_conflicts(tasks: list[Task]) -> list[str]:
        pass

    @staticmethod
    def handle_recurrence(task: Task) -> Task:
        pass
