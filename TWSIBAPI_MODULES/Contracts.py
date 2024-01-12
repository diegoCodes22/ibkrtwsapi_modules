from ibapi.contract import Contract


def stock(symbol: str, currency: str = "USD", exchange: str = "SMART") -> Contract:
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = currency
    contract.exchange = exchange
    return contract


def option(symbol: str, expiration: str, strike: int, opt_type: str, currency: str = "USD", exchange: str = "SMART"):
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
