import pathlib
from typing import Optional
from datetime import datetime, date

DEFAULT_WD_PATH = pathlib.Path.home() / '.daily'
DEFAULT_STORAGE_PATH = DEFAULT_WD_PATH / 'dailies'
DEFAULT_CONFIG_NAME = 'config.json'
DEFAULT_CONFIG_PATH = DEFAULT_WD_PATH / DEFAULT_CONFIG_NAME
DEFAULT_BACKUP = DEFAULT_WD_PATH / 'backup'
ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()

NEW_LINE: str = '\n'
SECTION_SEP: str = NEW_LINE + '-' * 10 + NEW_LINE
ELEMENT_SPLITTER: str = '\t'


def parse_date(str_date) -> Optional[date]:
    if str_date is not None:
        return datetime.strptime(str_date, "%Y-%m-%d")
    return None



