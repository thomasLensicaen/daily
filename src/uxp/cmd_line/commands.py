from dataclasses import dataclass
import pathlib
from datetime import date, timedelta
import argparse
from common import parse_date
from config import Config
import subprocess
from functionalities import create_new_daily, delete_daily
from daily_types import DatedDaily, Daily


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
        new_dated_daily = create_new_daily(config, self.daily_date)
        new_dated_daily.save(config.get_storage_dir())


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
        delete_daily(config, self.daily_date, True)


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


@dataclass
class CliListArgs:
    daily_date: date = None
    before: bool = True

    @staticmethod
    def from_namespace(args: argparse.Namespace) -> 'CliListArgs':
        if args.date:
            return CliListArgs(parse_date(args.date))
        elif args.now:
            return CliListArgs(date.today() + timedelta(days=args.now))
        else:
            return CliListArgs(date.today())

    def apply(self, config: Config):
        cmd = f'nvim {DatedDaily.load(config.get_storage_dir(), self.daily_date).get_file_path(pathlib.Path(config.get_storage_dir())).resolve().as_posix()}'
        subprocess.run(cmd, shell=True)


@dataclass
class CliShowArgs:
    daily_date: date = None
    before: bool = True

    @staticmethod
    def from_namespace(args: argparse.Namespace) -> 'CliShowArgs':
        if args.date:
            return CliShowArgs(parse_date(args.date))
        elif args.now:
            return CliShowArgs(date.today() + timedelta(days=args.now))
        else:
            return CliShowArgs(date.today())

    def apply(self, config: Config):
        try:
            DatedDaily.load(config.get_storage_dir(), self.daily_date)
        except FileNotFoundError as fe:
            print(f"Daily doesn't exist.")
            exit(1)
        except Exception as e:
            print(f'Malformed daily {self.daily_date.strftime("%Y-%m-%d")}')
            print(e)
        cmd = f'cat {DatedDaily.as_file_path(config.get_storage_dir(), self.daily_date)}'
        subprocess.run(cmd, shell=True)
