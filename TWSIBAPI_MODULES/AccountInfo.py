from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from typing import Tuple


class AccountInfo(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.account = {}
        self.positions = {}

    def nextValidId(self, orderId: int) -> None:
        self.reqAccountUpdates(True, "")

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str) -> None:
        if key in ["AccountCode", "ExcessLiquidity", "NetLiquidation", "FullInitMarginReq", "FullMaintMarginReq",
                   "GrossPositionValue", "BuyingPower", "UnrealizedPnL", "OptionMarketValue", "Cryptocurrency",
                   "FuturesPNL", "FxCashBalance"] and val != 0.0:
            self.account[key] = val

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str) -> None:
        self.positions[contract.symbol] = {"Contract": contract, "Position": position, "MarketPrice": marketPrice,
                                           "MarketValue": marketValue, "AverageCost": averageCost,
                                           "UnrealizedPNL": unrealizedPNL}

    def accountDownloadEnd(self, accountName: str):
        self.reqAccountUpdates(False, "")
        self.disconnect()


def reqAccountInfo(CONN_VARS: list, info_type: str = "All") -> dict or Tuple[dict, dict]:
    ai = AccountInfo()
    ai.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    ai.run()
    if info_type == "All":
        return ai.account, ai.positions
    elif info_type == "Pos":
        return ai.positions
    elif info_type == "Acc":
        return ai.account
