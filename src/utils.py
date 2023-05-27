from typing import Any
from src.classes.Format import Format
from src.globals import JSON

import os


def read(filename: str, format: Format = JSON) -> dict[str, Any]:
    with open(
        os.path.join(format.path, f"{filename}.{format.extension}"), "r"
    ) as input_file:
        return format.read_function(input_file.read())


def write(d: dict[str, Any], filename: str, format: Format = JSON) -> None:
    with open(
        os.path.join(format.path, f"{filename}.{format.extension}"), "w"
    ) as output_file:
        output_file.write(format.write_function(d))
