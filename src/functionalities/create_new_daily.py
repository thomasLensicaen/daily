from dataclasses import dataclass
import pathlib
from datetime import date, timedelta
import argparse
from common import parse_date
from config import Config
from daily_types import DatedDaily, Daily


def create_new_daily( config: Config, daily_date: date):
    return DatedDaily(daily_date).save(config.get_storage_dir())

