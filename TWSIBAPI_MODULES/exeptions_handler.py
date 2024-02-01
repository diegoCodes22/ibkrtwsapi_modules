class NoSecDef(Exception):
    print("No security definition could be found")
    exit(200)


class ConnError(Exception):
    print("Couldn't connect to TWS.")
    exit(502)
