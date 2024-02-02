class NoSecDef(Exception):
    def __init__(self):
        super().__init__("No security definition found.")


class ConnError(Exception):
    def __init__(self):
        super().__init__("Couldn't connect to TWS.")


def exceptions_factory(error_code: int) -> None:
    if error_code == 502:
        raise ConnError
    elif error_code == 200:
        raise NoSecDef
    else:
        pass
