import datetime
from datetime import datetime, timedelta
from pytz import timezone
from time import sleep


def has_position(positions: dict, ticker: str) -> bool:
    return True if ticker in positions.keys() else False


def formatted_date(date: datetime):
    return date.strftime("%Y%m%d-%H:%M:%S")


def one_year_ago() -> datetime:
    return datetime.datetime.now() - datetime.timedelta(days=360)


def last_open() -> str:
    dt = datetime.datetime.now(datetime.timezone.utc)
    dw = dt.weekday()
    dh = dt.strftime("%H:%M")
    if dh > "21:00" and dw < 5:
        return datetime.today().strftime("%Y%m%d-") + "20:58:00"
    elif dh < "14:30" or dw < 5:
        return (datetime.today() - timedelta(days=1)).strftime("%Y%m%d-") + "20:58:00"
    elif dw == 6:
        return (datetime.today() - timedelta(days=2)).strftime("%Y%m%d-") + "20:58:00"


def mkt_is_open() -> bool:
    """
    Function to check if the market is open.
    :return: True if the market is open, False if it is closed.
    """
    dt = datetime.datetime.now(datetime.timezone.utc)
    return True if "09:29" < dt.strftime("%H:%M") < "16:00" and 0 <= dt.weekday() < 5 else False


def sleep_one_bar(bar_size: str) -> None:
    """
    Function to sleep until the next bar is formed.
    """
    ct = datetime.now(timezone("US/Eastern"))
    size, unit = bar_size.split(" ")
    if unit == "min" or unit == "mins":
        start = (ct.minute // size) * size
        next_bar = ct.replace(minute=start, second=0, microsecond=0) + timedelta(minutes=size)
    elif unit == "hour" or unit == "hours":
        start = (ct.hour // size) * size
        next_bar = ct.replace(hour=start, minute=0, second=0, microsecond=0) + timedelta(hours=size)
    elif unit == "day":
        start = (ct.day // size) * size
        next_bar = ct.replace(day=start, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=size)
    else:
        raise NotImplemented(f"Bar size {bar_size} not implemented, missing implementation for week and month.")
        
    insec = (next_bar - ct).total_seconds()
    if insec > 0:
        sleep(insec)
