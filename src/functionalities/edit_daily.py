from datetime import date, timedelta
import pathlib
from config import Config
import argparse
from common import parse_date
from dataclasses import dataclass
from daily_types import DatedDaily
import subprocess


@dataclass
class CliEditArgs:
    daily_date: date = None

    @staticmethod
    def from_namespace(args: argparse.Namespace) -> 'CliEditArgs':
        if args.date:
            return CliEditArgs(parse_date(args.date))
        elif args.now:
            return CliEditArgs(date.today() + timedelta(days=args.now))
        else:
            return CliEditArgs(date.today())

    def apply(self, config: Config):
        try:
            DatedDaily.load(config.get_storage_dir(), self.daily_date)
        except FileNotFoundError as fe:
            print(f"Daily doesn't exist.")
            exit(1)
        except Exception as e:
            print(f'Malformed daily {self.daily_date.strftime("%Y-%m-%d")}')
            print(e)
        path = DatedDaily.as_file_path(config.get_storage_dir(), self.daily_date)
        cmd = f'nvim {path.resolve().as_posix()}'
        subprocess.run(cmd, shell=True)
