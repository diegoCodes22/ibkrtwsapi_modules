from typing import List


class NoSecDef(Exception):
    def __init__(self):
        super().__init__("No security definition found.")


class ConnError(Exception):
    def __init__(self):
        super().__init__("Couldn't connect to TWS.")


class InvalidPeriod(ValueError):
    def __init__(self, period, valid_periods: List[str]):
        super().__init__(f"Invalid period format, your period: {period}, options are {valid_periods}")


class EndDateFormatError(ValueError):
    def __init__(self, date: str):
        super().__init__(f"End date format is incorrect.\n Your format: {date}, correct format: %Y%m%d %H:%M:%S "
                         f"(YYYYMMDD HH:MM:SS)")


class HistoricalDataError(Exception):
    def __init__(self, message: str = ""):
        self.message = f"Could not retrieve historical data.\n{message}"
        super().__init__(self.message)


def exceptions_factory(error_code: int) -> None:
    """
    Factory function to raise exceptions based on error codes returned from TWS or IBGateway.
    :param error_code: TWS or IBGateway error code
    :return: None if error code doesn't match any exception
    """
    if error_code == 502:
        raise ConnError
    elif error_code == 200:
        raise NoSecDef
    else:
        pass
