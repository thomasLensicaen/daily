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
        cmd = f'nvim {DatedDaily.load(config.get_storage_dir(), self.daily_date).get_file_path(pathlib.Path(config.get_storage_dir())).resolve().as_posix()}'
        subprocess.run(cmd, shell=True)
