from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import TickAttrib, TickerId, BarData
from ibapi.ticktype import TickType
from typing import List


class CurrentPrice(EClient, EWrapper):
    def __init__(self, contract: Contract):
        EClient.__init__(self, self)
        self.current_price: float = 0.0
        self.contract: Contract = contract

    def nextValidId(self, orderId: int) -> None:
        self.reqMarketDataType(2)
        self.reqMktData(orderId, self.contract, "", False, False, [])

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib) -> None:
        if tickType == 9:
            self.current_price = price
            self.disconnect()


def reqCurrentPrice(CONN_VARS: list, contract: Contract) -> float:
    cp = CurrentPrice(contract=contract)
    cp.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    cp.run()
    return cp.current_price


# ------------------------------------------------------------------------------------ #
class HistoricalDataStream(EClient, EWrapper):
    def __init__(self, contract: Contract, duration: str, bar_size: str, end_date: str = "",
                 what_to_show: str = "TRADES", use_rth: int = 1):
        # End date format: "20200601 12:00:00" %Y%m%d %H:%M:%S
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


def reqHistoricalDataStream(CONN_VARS: list, contract: Contract, duration: str, bar_size: str, end_date: str = "",
                            what_to_show: str = "TRADES", use_rth: int = 1) -> List[BarData]:
    hds = HistoricalDataStream(contract=contract, duration=duration, bar_size=bar_size, end_date=end_date,
                               what_to_show=what_to_show, use_rth=use_rth)
    hds.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    hds.run()
    return hds.data_stream


def reqBarAtDate(CONN_VARS: list, contract: Contract, date: str) -> BarData:
    data = HistoricalDataStream(contract=contract, duration="1 D", bar_size="1 day", end_date=date)
    data.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    data.run()
    return data.data_stream[0]


def reqAllTimeHigh(CONN_VARS: list, contract: Contract) -> float:
    data = HistoricalDataStream(contract=contract, duration="5 Y", bar_size="1 month")
    data.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    data.run()
    return max([bar.high for bar in data.data_stream])


def reqAllTimeLow(CONN_VARS: list, contract: Contract) -> float:
    data = HistoricalDataStream(contract=contract, duration="5 Y", bar_size="1 month")
    data.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    data.run()
    return min([bar.low for bar in data.data_stream])
