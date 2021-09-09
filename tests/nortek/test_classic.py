import pytest
from pyserialdrivers.nortek.constants import Commands
from pyserialdrivers.nortek.classic import Classic


def test_classic(patch_serial):
    patch_serial.responses.update({
        b""
    })
    nortek = Classic("COM9")
    pass
