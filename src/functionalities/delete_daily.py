from datetime import date, timedelta
import pathlib
from config import Config
import argparse
from common import parse_date
from dataclasses import dataclass
from daily_types import DatedDaily
import subprocess


@dataclass
class CliDeleteArgs:
    daily_date: date = None

    @staticmethod
    def from_namespace(args: argparse.Namespace) -> 'CliDeleteArgs':
        if args.date:
            return CliDeleteArgs(parse_date(args.date))
        elif args.now:
            return CliDeleteArgs(date.today() + timedelta(days=args.now))
        else:
            return CliDeleteArgs(date.today())

    def apply(self, config: Config):
        print(DatedDaily.load(config.get_storage_dir(), self.daily_date))
        cmd = f'rm -i {DatedDaily.load(config.get_storage_dir(), self.daily_date).get_file_path(pathlib.Path(config.get_storage_dir())).resolve().as_posix()}'
        subprocess.run(cmd, shell=True)
