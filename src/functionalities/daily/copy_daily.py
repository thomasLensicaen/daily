from datetime import date
from daily_types import DatedDaily
from config import Config

def copy_daily(config: Config, daily_date_1: date, daily_date_2: date, only_no_accomplished: bool = True) -> DatedDaily:
    daily_copyied: DatedDaily = DatedDaily.load(config.get_storage_dir(),
                                                daily_date_1).copy(only_no_accomplished=only_no_accomplished)
    daily_copyied.set_date(daily_date_2)
    return daily_copyied
