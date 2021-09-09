
class Commands:
    class Get:
        DATETIME = b"RC"
        SERIAL = b"ID"

    class Set:
        DATETIME = b"SC"
        SLEEP = b"PD"

    EOL = b"\r"
    BREAK = b"@@@@@@K1W%!Q"  # Technically needs a 100ms pause between @s and rest
    ACK = b"\x06\x06"
    NACK = b"\x15\x15"
