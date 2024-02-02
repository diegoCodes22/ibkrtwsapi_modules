class NoSecDef(Exception):
    def __init__(self):
        super().__init__("No security definition found.")


class ConnError(Exception):
    def __init__(self):
        super().__init__("Couldn't connect to TWS.")
