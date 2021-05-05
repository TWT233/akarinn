import datetime
from typing import Union


def pcr_today() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(hours=5)


def get_real_which_day(which_day: Union[datetime.date, str]) -> Union[datetime.date, None]:
    if isinstance(which_day, str):
        if which_day == 'today':
            return pcr_today()
        else:
            return None
    else:
        return which_day