from daily_types import DatedDaily
import pathlib
from typing import Iterable, List, Callable, Generator


def get_all_dailies(path_of_directory: pathlib.Path) -> Iterable[DatedDaily]:
    for daily_file in path_of_directory.iterdir():
        yield DatedDaily.load_from_file(daily_file)


def filter_daily(cond: Callable[[DatedDaily], bool], daily_gen: Iterable[DatedDaily]) -> List[DatedDaily]:
    return [daily for daily in daily_gen if cond(daily)]
