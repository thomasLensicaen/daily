from daily_types import DatedDaily
import pathlib
from typing import Iterable, List, Callable


def get_all_dailies(path_of_directory: pathlib.Path):
    for daily in path_of_directory.iterdir():
        yield DatedDaily.get_daily_date_from_name(daily.name)


def filter_daily(cond: Callable[[DatedDaily], bool], daily_gen: Iterable[DatedDaily]) -> List[DatedDaily]:
    return [daily for daily in daily_gen if cond(daily)]
