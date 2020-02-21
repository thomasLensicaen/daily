from dataclasses import dataclass
import pathlib
from datetime import date, timedelta
import argparse
from common import parse_date
from config import Config
from daily_types import DatedDaily, Daily


def create_new_daily(daily_date: date):
    return DatedDaily(daily_date)


@dataclass
class CliNewArgs:
    daily_date: date = None

    @staticmethod
    def from_namespace(args: argparse.Namespace) -> 'CliNewArgs':
        if args.date:
            return CliNewArgs(parse_date(args.date))
        elif args.now:
            return CliNewArgs(date.today() + timedelta(days=args.now))
        else:
            return CliNewArgs(date.today())

    def apply(self, config: Config):
        new_dated_daily = create_new_daily(self.daily_date)
        new_dated_daily.save(config.get_storage_dir())
