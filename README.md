# pyserialdrivers

[![Continuous Integration](https://github.com/pfrnz/pyserialdrivers/actions/workflows/ci.yml/badge.svg)](https://github.com/pfrnz/pyserialdrivers/actions/workflows/ci.yml) [![Python 3.6.2](https://img.shields.io/badge/python-3.6.2-blue.svg)](https://www.python.org/downloads/release/python-362/) [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

A collection of OOB serial drivers for interacting with predominantly environmental sensors

## Installation
```bash
pip install <git_url>
pip install pyserialdrivers
```

# Hardware Supported

## YSI EXO
This library provides a minimal middle layer for realtime interfacing with YSI EXO sensors.

### Use & Example

```python

from pyserialdrivers import exo
from pyserialdrivers.exo.constants import ParamCodes

exo = exo.serial.DCPSerial("COM10")
values = exo.values
print(values)
# [Temperature: 2.5 °C, Battery: 3.7 V, Turbidity: 5.0 NTU]
temp = exo.get(ParamCodes.TEMP_C)
temp.value  # 2.5
temp.param.unit  # °C
temp.param.description  # Temperature
```