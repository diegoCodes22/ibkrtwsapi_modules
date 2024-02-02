from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import TickAttrib, TickerId, BarData
from ibapi.ticktype import TickType
from typing import List
from TWSIBAPI_MODULES.exceptions_handler import exceptions_factory


class CurrentPrice(EClient, EWrapper):
    def __init__(self, contract: Contract):
        EClient.__init__(self, self)
        self.current_price: float = 0.0
        self.contract: Contract = contract

    def nextValidId(self, orderId: int) -> None:
        self.reqMarketDataType(2)
        self.reqMktData(orderId, self.contract, "", False, False, [])

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib) -> None:
        if tickType == 4:
            self.current_price = price
            self.disconnect()

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        exceptions_factory(errorCode)



def reqCurrentPrice(CONN_VARS: list, contract: Contract) -> float:
    """
    :param CONN_VARS: Connection variables to connect to TWS or IBGateway
    :param contract: ibapi Contract object
    :return: Returns current (last) price for the specified contract
    """
    cp = CurrentPrice(contract=contract)
    cp.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    cp.run()
    return cp.current_price


# ------------------------------------------------------------------------------------ #
class HistoricalDataStream(EClient, EWrapper):
    def __init__(self, contract: Contract, bar_size: str, duration: str, end_date: str = "",
                 what_to_show: str = "TRADES", use_rth: int = 1):
        """
        :param contract: ibapi Contract object
        :param end_date: Request's end date and time, must be in format %Y%m%d %H:%M:%S an empty string represents current date
        :param duration: The amount of time to go back from the request's end_date
        :param bar_size: Size of bars to be returned
        :param what_to_show: Type of data to retrieve, see ibapi docs Historical Data Types
        :param use_rth: 0 to fetch data outside of Regular Trading Hours, 1 to use RTH
        """
        EClient.__init__(self, self)
        self.contract: Contract = contract
        self.end_date: str = end_date
        self.duration: str = duration
        self.bar_size: str = bar_size
        self.what_to_show: str = what_to_show
        self.use_rth: int = use_rth
        self.data_stream: List[BarData] = []

    def historicalData(self, reqId: int, bar: BarData):
        self.data_stream.append(bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        self.disconnect()

    def nextValidId(self, orderId: int):
        self.reqHistoricalData(orderId, self.contract, self.end_date, self.duration, self.bar_size, self.what_to_show,
                               self.use_rth, 1, False, [])

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        if errorCode == 502:
            exceptions_factory(errorCode)


def reqHistoricalDataStream(CONN_VARS: list, contract: Contract, duration: str, bar_size: str, end_date: str = "",
                            what_to_show: str = "TRADES", use_rth: int = 1) -> List[BarData]:
    """
    :param CONN_VARS: Connection variables to connect to TWS or IBGateway
    :param contract: ibapi Contract object
    :param end_date: Request's end date and time, must be in format %Y%m%d %H:%M:%S, an empty string represents current
     date
    :param duration: The amount of time to go back from the request's end_date
    :param bar_size: Size of bars to be returned
    :param what_to_show: Type of data to retrieve, see ibapi docs Historical Data Types
    :param use_rth: 0 to fetch data outside of Regular Trading Hours, 1 to use RTH
    :return: Returns a list containing BarData objects of the specified bar size for the given duration
    """
    hds = HistoricalDataStream(contract=contract, duration=duration, bar_size=bar_size, end_date=end_date,
                               what_to_show=what_to_show, use_rth=use_rth)
    hds.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    hds.run()
    return hds.data_stream


def reqBarAtDate(CONN_VARS: list, contract: Contract, date: str) -> BarData:
    """
    :param CONN_VARS: Connection variables to connect to TWS or IBGateway
    :param contract: ibapi Contract object
    :param date: Date and time of the requested bar, must be in format %Y%m%d %H:%M:%S, an empty string represents current
     date
    :return: Returns a BarData object
    """
    data = HistoricalDataStream(contract=contract, duration="1 D", bar_size="1 day", end_date=date)
    data.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    data.run()
    return data.data_stream[0]


def reqAllTimeHigh(CONN_VARS: list, contract: Contract) -> float:
    """
    :param CONN_VARS: Connection variables to connect to TWS or IBGateway
    :param contract: ibapi Contract object
    :return: Returns all-time high of the last 5 years.
    """
    data = HistoricalDataStream(contract=contract, duration="5 Y", bar_size="1 month")
    data.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    data.run()
    return max([bar.high for bar in data.data_stream])


def reqAllTimeLow(CONN_VARS: list, contract: Contract) -> float:
    """
    :param CONN_VARS: Connection variables to connect to TWS or IBGateway
    :param contract: ibapi Contract object
    :return: Returns all-time low of the last 5 years.
    """
    data = HistoricalDataStream(contract=contract, duration="5 Y", bar_size="1 month")
    data.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    data.run()
    return min([bar.low for bar in data.data_stream])

