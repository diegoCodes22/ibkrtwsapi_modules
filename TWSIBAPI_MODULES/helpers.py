import datetime


def has_position(positions: dict, ticker: str) -> bool:
    return True if ticker in positions.keys() else False


def formatted_date(date: datetime):
    return date.strftime("%Y%m%d-%H:%M:%S")


def one_year_ago() -> datetime:
    return datetime.datetime.now() - datetime.timedelta(days=360)


def last_open() -> datetime:
    dt = datetime.datetime.now(datetime.timezone.utc)
    dw = dt.weekday()
    dh = dt.strftime("%H:%M")
    if dh > "21:00" and dw < 5:
        return datetime.datetime.today().strftime("%Y%m%d-") + "20:58:00"
    elif dh < "14:30" or dw < 5:
        return (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d-") + "20:58:00"
    elif dw == 6:
        return (datetime.datetime.today() - datetime.timedelta(days=2)).strftime("%Y%m%d-") + "20:58:00"


def mkt_open() -> bool:
    dt = datetime.datetime.now(datetime.timezone.utc)
    return True if "14:30" < dt.strftime("%H:%M") < "21:00" and 0 <= dt.weekday() < 5 else False
