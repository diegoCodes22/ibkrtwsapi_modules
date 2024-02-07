from ibapi.contract import Contract


def stock(symbol: str, currency: str = "USD", exchange: str = "SMART") -> Contract:
    """
    :param symbol: Stock symbol to create contract for
    :param currency: Currency to be used, default is "USD"
    :param exchange: Exchange to be used, default is "SMART". Read more on SMART routing in the IB API documentation
    :return: Contract object for the stock
    """
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = currency
    contract.exchange = exchange
    return contract


def option(symbol: str, expiration: str, strike: int, opt_type: str, currency: str = "USD", exchange: str = "SMART"):
    """

    :param symbol: Symbol of the underlying stock
    :param expiration: Option contract expiration date
    :param strike: Option contract strike price
    :param opt_type: Option type, "C" for call, "P" for put
    :param currency: Currency to be used, default is "USD"
    :param exchange: Exchange to be used, default is "SMART". Read more on SMART routing in the IB API documentation
    :return: Contract object for the option of the specified underlying stock
    """
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "OPT"
    contract.currency = currency
    contract.exchange = exchange
    contract.strike = strike
    contract.lastTradeDateOrContractMonth = expiration
    contract.right = opt_type
    contract.multiplier = 100
    return contract
