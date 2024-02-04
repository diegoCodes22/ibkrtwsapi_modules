from exceptions_handler import InvalidPeriod, EndDateFormatError
from datetime import datetime


class Configurations:
    def __init__(self, host: str = "127.0.0.1", port: int = 7497, client_id: int = 0):
        self.CONN_VARS = [host, port, client_id]

    @staticmethod
    def check_periods(duration: str) -> None:
        valid_periods = ['S', 'D', 'W', 'M', 'Y']
        if duration.split(" ")[1] not in valid_periods:
            raise InvalidPeriod(valid_periods)

    @staticmethod
    def check_end_date_format(date: str) -> None:
        try:
            datetime.strptime(date, "%Y%m%d %H:%M:%S")
        except ValueError:
            raise EndDateFormatError(date)
