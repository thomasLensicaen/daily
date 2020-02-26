from dataclasses import dataclass
import pathlib
from datetime import date, datetime
from typing import List, Optional, Callable, Any
from common import NEW_LINE, SECTION_SEP, ELEMENT_SPLITTER


class PrintableElement:

    first_default_marker: str = None

    @classmethod
    def generate_default(cls):
        return cls.first_default_marker


class Achievable:

    achieved_marker = 'X'
    non_achieved_marker = '=>'

    def __init__(self, achieved: bool=False):
        self.achieved = achieved

    def get_achieved_marker(self) -> str:
        return self.achieved_marker if self.achieved else self.non_achieved_marker

    @classmethod
    def is_achieved(cls, achieved_marker_str: str) -> bool:
        if achieved_marker_str == cls.achieved_marker:
            return True
        elif achieved_marker_str == cls.non_achieved_marker:
            return False
        else:
            raise ValueError(f'{achieved_marker_str} is not an achieved marker')


@dataclass
class Task(Achievable):
    name: str
    description: Optional[str]= None
    achieved: bool = False

    def to_str(self):
        return self.get_achieved_marker() + ELEMENT_SPLITTER + self.name + ((ELEMENT_SPLITTER + self.description) if self.description else '')

    @staticmethod
    def from_str(line: str):
        # Case Nothing or malformed one element
        data = line.split(ELEMENT_SPLITTER)
        if line == '' or len(data) == 1:
            achieved = False
            name = ''
            description = None
        elif len(data) >= 2:
            raw_achieved_marker, name = data[0], data[1]
            if len(data) == 3:
                description = data[2]
            else:
                description = None
            achieved = Achievable.is_achieved(raw_achieved_marker)
        else:
            raise ValueError('Not parsable {data}')
        return Task(name, description, achieved)

    @staticmethod
    def get_default() -> 'Task':
        return Task('nothing', None, False)


@dataclass
class Objective(Achievable):
    to_achieve: str
    achieved: bool = False

    def to_str(self):
        return self.get_achieved_marker() + ELEMENT_SPLITTER + self.to_achieve

    @staticmethod
    def from_str(line: str) -> 'Objective':
        raw_achieved_marker, todo = line.split(ELEMENT_SPLITTER)
        achieved = Achievable.is_achieved(raw_achieved_marker)
        return Objective(todo, achieved)

    @staticmethod
    def get_default() -> 'Objective':
        return Objective('no objective')


@dataclass
class AdditionalObjective(Objective):

    @staticmethod
    def get_default() -> 'AdditionalObjective':
        return AdditionalObjective('no objective')

    @staticmethod
    def from_str(line: str) -> 'AdditionalObjective':
        raw_achieved_marker, todo = line.split(ELEMENT_SPLITTER)
        achieved = Achievable.is_achieved(raw_achieved_marker)
        return AdditionalObjective(todo, achieved)


class Section:
    SECTION_ID: str = None
    ITEM_CLASS: type = None

    def __init__(self, items: List):
        self.items = items

    def to_str(self) -> str:
        return self.SECTION_ID + NEW_LINE + NEW_LINE.join([t.to_str() for t in self.items])

    @classmethod
    def from_str(cls, raw_str) -> 'Section':
        splitted_str = raw_str.split(NEW_LINE)
        if not cls.SECTION_ID == splitted_str[0]:
            raise ValueError(f'Not expected SECTION_ID. got {splitted_str[0]}, expected {cls.SECTION_ID}')
        if len(splitted_str) > 1:
            return cls(items = [cls.ITEM_CLASS.from_str(line) for line in splitted_str[1:]])
        else:
            return cls(items=[])

    def filter(self, cond: Callable[[Achievable], bool]) -> 'Section':
        return self.__class__([item for item in self.items if cond(item)])

    def to_unachieved(self) -> 'Section':
        return self.filter(lambda a: not a.achieved)

    def copy(self, only_not_accomplished: bool = True) -> 'Section':
        items = self.filter()
        self.__class__


class TasksSection(Section):
    SECTION_ID = 'TASKS'
    ITEM_CLASS = Task


class ObjectiveSection(Section):
    SECTION_ID = 'OBJECTIVES'
    ITEM_CLASS = Objective


class AdditionalObjectiveSection(Section):
    SECTION_ID = 'ADDITIONAL OBJECTIVES'
    ITEM_CLASS = AdditionalObjective


@dataclass
class Daily:
    task_section: TasksSection
    objective_section: ObjectiveSection
    additional_objective_section: AdditionalObjectiveSection

    def to_str(self) -> str:
        tasks_str = self.task_section.to_str()
        objs_str = self.objective_section.to_str()
        add_objs_str = self.additional_objective_section.to_str()
        return SECTION_SEP.join([tasks_str, objs_str, add_objs_str]) + NEW_LINE

    @classmethod
    def from_str(cls, raw: str) -> 'Daily':
        tasks_str, objs_str, add_objs_str = raw.split(SECTION_SEP)
        return Daily(TasksSection.from_str(tasks_str),
                     ObjectiveSection.from_str(objs_str),
                     AdditionalObjectiveSection.from_str(add_objs_str[:-1]))

    @staticmethod
    def get_default():
        return Daily(TasksSection([Task.get_default()]),
                     ObjectiveSection([Objective.get_default()]),
                     AdditionalObjectiveSection([AdditionalObjective.get_default()]))

    def copy(self, only_not_accomplished: bool):
        self.task_section.
        self.task_section


class DatedDaily:

    FILE_FORMAT = "%Y_%m_%d"
    DISPLAY_FORMAT = "%Y-%m-%d"

    def __init__(self, daily_date: date, daily: Daily = None):
        self.daily_date = daily_date
        self.daily: Daily = daily if daily else Daily.get_default()

    @classmethod
    def get_file_pattern(cls, daily_date):
        return f"daily_{daily_date.strftime(cls.FILE_FORMAT)}"

    def get_file_path(self, storage_dir: pathlib.Path):
        return self.as_file_path(storage_dir, self.daily_date)

    @classmethod
    def get_daily_date_from_name(cls, name: str) -> date:
        return datetime.strptime(name.replace('daily_', ''), cls.FILE_FORMAT).date()

    @classmethod
    def as_file_path(cls, work_dir: pathlib.Path, daily_date: date) -> pathlib.Path:
        return work_dir / cls.get_file_pattern(daily_date)

    def save(self, storage_dir: pathlib.Path):
        if self.as_file_path(storage_dir, self.daily_date).exists():
            raise Exception(f'Daily for date {self.daily_date.strftime(self.DISPLAY_FORMAT)} already exists')
        with open(self.as_file_path(storage_dir, self.daily_date), 'w') as fd:
            fd.write(self.daily.to_str())

    @classmethod
    def load(cls, storage_dir: pathlib.Path, daily_date: date) -> 'DatedDaily':
        if not cls.as_file_path(storage_dir, daily_date).exists():
            raise FileNotFoundError(f'Daily for date {daily_date.strftime(cls.DISPLAY_FORMAT)} doesn\'t exists')
        with open(cls.as_file_path(storage_dir, daily_date), 'r') as fd:
            return DatedDaily(daily_date, Daily.from_str(fd.read()))

    def set_date(self, daily_date: date):
        self.daily_date = daily_date

    def copy(self, only_no_accomplished: bool) -> 'DatedDaily':
        new_daily: Daily = self.daily.copy(only_no_accomplished)
        return new_daily

    @classmethod
    def load_from_file(cls, path: pathlib.Path) -> 'DatedDaily':
        daily_date = cls.get_daily_date_from_name(path.name)
        with open(path, 'r') as f:
            daily = Daily.from_str(f.read())
        return DatedDaily(daily_date, daily)
