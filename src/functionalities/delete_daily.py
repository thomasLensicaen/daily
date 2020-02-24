from datetime import date
import pathlib
from config import Config
from daily_types import DatedDaily
import subprocess
import shutil


def delete_daily(config: Config, daily_date: date, interactive_shell=True):
    if interactive_shell:
        cmd = f'rm -i {DatedDaily.load(config.get_storage_dir(), daily_date).get_file_path(pathlib.Path(config.get_storage_dir())).resolve().as_posix()}'
        subprocess.run(cmd, shell=True)
    else:
        shutil.move(DatedDaily.as_file_path(config.get_storage_dir(), daily_date), config.bkp)


