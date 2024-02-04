from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import OrderId, TickerId
from ibapi.order import Order
from ibapi.order_state import OrderState
from TWSIBAPI_MODULES.exceptions_handler import exceptions_factory
from typing import Tuple
from threading import Thread, Event
from time import perf_counter, sleep


# def lmt_order(order_id: int, action: str, quantity: int, price: float) -> Order:
#     order = Order()
#     order.orderId = order_id
#     order.action = action
#     order.totalQuantity = quantity
#     order.orderType = "LMT"
#     order.lmtPrice = price
#     order.eTradeOnly = ''
#     order.firmQuoteOnly = ''
#     return order


class OrderProcess(EClient, EWrapper):
    def __init__(self, contract: Contract, order: Order):
        EClient.__init__(self, self)
        self.contract = contract
        self.order = order
        self.fill = 0.
        self.commission = 0.

    def nextValidId(self, orderId: int):
        self.reqContractDetails(orderId, self.contract)

    def reqContractDetails(self, reqId: int, contract: Contract):
        self.placeOrder(reqId, contract, self.order)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        self.commission = orderState.commission
        print(f"OPEN ORDER: {contract.symbol} {order.action} {orderState.status}")

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float,
                    permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        event = Event()
        init_time = perf_counter()
        thread = Thread(target=self.cancel_conditions, args=(orderId, event, init_time))
        thread.start()

        if filled > 0:
            event.set()
            print(f"ORDER STATUS: Status: {status}\nFilled: {filled}\nFill price: {avgFillPrice}\n")
        if remaining == 0:
            self.fill = avgFillPrice
            self.disconnect()

    def cancelOpenOrder(self, orderId: OrderId):
        self.cancelOrder(orderId)
        self.disconnect()

    def cancel_conditions(self, order_id: int, event: Event, init_time: float, max_time: float = 3) -> None:
        while not event.is_set():
            if (perf_counter() - init_time) / 60 > max_time:
                self.cancelOpenOrder(order_id)
                break
            else:
                sleep(10)

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        exceptions_factory(errorCode)


def place_order(CONN_VARS, contract: Contract, order: Order) -> Tuple[float, float]:
    order_app = OrderProcess(contract, order)
    order_app.connect(CONN_VARS[0], CONN_VARS[1], CONN_VARS[2])
    order_app.run()
    return order_app.fill, order_app.commission
