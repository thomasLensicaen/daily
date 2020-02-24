from datetime import date
from daily_types import DatedDaily


def create_new_daily(daily_date: date) -> DatedDaily:
    return DatedDaily(daily_date)

