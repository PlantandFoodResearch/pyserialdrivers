"""Helper file to generate python code from CSV of params"""
import logging
import sys
import csv
import typing
from pathlib import Path


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("constant_generator")

csv_path = Path(__file__).parent / "ysiexo_paramcodes.csv"
out_path = (
    Path(__file__).parent.parent
    / "src"
    / "pyserialdrivers"
    / "exo"
    / "_gen_constants.py"
)

_pre_amble = """\
# -*- coding: utf-8 -*-
# Auto-generated file. Do not modify!
from enum import Enum, unique
"""

_param_codes = """
@unique
class ParamCodes(Enum):
    @property
    def unit(self) -> str:
        return ParamUnits[self.name].value

    @property
    def name(self) -> str:
        return ParamNames[self.name].value

"""

_param_units = """
class ParamUnits(Enum):
"""

_param_names = """
class ParamNames(Enum):
"""


def main():
    if not csv_path.exists():
        log.error(f"Expected CSV does not exist: {csv_path}")
        raise FileNotFoundError()
    params = {}
    with open(csv_path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            param = {row[3]: {"name_long": row[0], "unit": row[1], "code": row[2]}}
            params.update(param)

    # Write output
    write_constants(params)


def write_constants(params: typing.Dict) -> None:
    param_codes = []
    param_units = []
    param_names = []
    # Prepare output
    for key, value in params.items():
        param_codes.append((key, int(value["code"])))
        param_units.append((key, str(value["unit"])))
        param_names.append((key, str(value["name_long"])))
    with open(out_path, "w", encoding="utf-8") as out_file:
        out_file.write(_pre_amble)

        out_file.write("\n")
        out_file.write(_param_units)
        for param in param_units:
            out_file.write(f'    {param[0]} = "{param[1]}"\n')

        out_file.write("\n")
        out_file.write(_param_names)
        for param in param_names:
            out_file.write(f'    {param[0]} = "{param[1]}"\n')

        out_file.write("\n")
        out_file.write(_param_codes)
        for param in param_codes:
            out_file.write(f"    {param[0]} = {param[1]}\n")


if __name__ == "__main__":
    # try:
    main()
# except BaseException as _:
#     sys.exit(-1)
