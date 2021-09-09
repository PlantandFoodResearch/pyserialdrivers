import sys

MICROPYTHON = False
# Protect for micropython version
if "micropython" in str(sys.implementation):
    MICROPYTHON = True
