from dataclasses import dataclass
from daily_types import TasksSection


@dataclass
class TaskList:
    tasks: TasksSection
