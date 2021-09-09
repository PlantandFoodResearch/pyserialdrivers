import serial
import logging
import argparse

from pyserialdrivers.exo.constants import Commands

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


responses = {
    Commands.Get.SERIAL: b"ABC123" + Commands.EOL,
    Commands.Get.DATA: b"21.0 12.8 0.5" + Commands.EOL,
    Commands.Get.PARA: b"1 28 37" + Commands.EOL,
    Commands.Set.WIPE: b"1.0" + Commands.EOL,
    Commands.Get.WIPE: b"0" + Commands.EOL,
}


def main():
    parser = argparse.ArgumentParser(description="A YSI EXO emulator")
    parser.add_argument("--port", help="Serial port to write", type=str, required=True)
    parser.add_argument(
        "--baudrate", help="Serial port to write", type=int, default=9600
    )
    args = parser.parse_args()
    ser = serial.Serial(port=args.port, baudrate=args.baudrate)
    while True:
        inline = ser.read_until(b"\r")
        log.info(f"Emulator received: {inline}")
        resp = responses.get(inline.strip().rstrip())
        if not resp:
            log.warning("Unknown command received!")
            resp = b"?Command" + Commands.EOL
        ser.write(resp)


if __name__ == "__main__":
    main()
