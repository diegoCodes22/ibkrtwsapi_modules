from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import OrderId
from ibapi.order import Order
from ibapi.order_state import OrderState

# ------------------------------ MUST WORK ON MORE OPTIONS RIGHT NOW ITS TRASH -------------------------------------- #


def stock_lmt_order(order_id: int, action: str, quantity: int, price: float) -> Order:
    order = Order()
    order.orderId = order_id
    order.action = action
    order.totalQuantity = quantity
    order.orderType = "LMT"
    order.lmtPrice = price
    order.eTradeOnly = ''
    order.firmQuoteOnly = ''
    return order


def stock_stop_order(order_id: int, action: str, quantity: int, stop_price: float) -> Order:
    order = Order()
    order.orderId = order_id
    order.action = action
    order.totalQuantity = quantity
    order.orderType = "STP"
    order.auxPrice = stop_price
    return order


class OrderProcess(EClient, EWrapper):
    def __init__(self, contract: Contract, action: str, quantity: int, price: float):
        EClient.__init__(self, self)
        self.contract = contract
        self.action = action
        self.quantity = quantity
        self.price = price

    def nextValidId(self, orderId: int):
        self.reqContractDetails(orderId, self.contract)

    def reqContractDetails(self, reqId: int, contract: Contract):
        order = stock_lmt_order(reqId, self.action, self.quantity, self.price)
        self.placeOrder(reqId, contract, order)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"OPEN ORDER: {contract.symbol} {order.action} {orderState.status} {orderState.commission}", end="\n\n")

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float,
                    permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"ORDER STATUS: Status: {status}\nFilled: {filled}\nFill price: {avgFillPrice}\n")
        if remaining == 0:
            self.disconnect()


def place_order(CONN_VARS, contract: Contract, action: str, quantity: int, price: float):
    order_app = OrderProcess(contract, action, quantity, price)
    order_app.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    order_app.run()
