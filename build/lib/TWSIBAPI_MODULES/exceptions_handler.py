from typing import List


class NoSecDef(Exception):
    def __init__(self):
        super().__init__("No security definition found.")


class ConnError(Exception):
    def __init__(self):
        super().__init__("Couldn't connect to TWS.")


class InvalidPeriod(ValueError):
    def __init__(self, valid_periods: List[str]):
        super().__init__(f"Invalid period suffix, options are {valid_periods}")


class EndDateFormatError(ValueError):
    def __init__(self, date: str):
        super().__init__(f"End date format is incorrect.\n Your format: {date}, correct format: %Y%m%d %H:%M:%S "
                         "(YYYYMMDD HH:MM:SS)")


def exceptions_factory(error_code: int) -> None:
    if error_code == 502:
        raise ConnError
    elif error_code == 200:
        raise NoSecDef
    else:
        pass
