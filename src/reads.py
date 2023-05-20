from src.globals import FORMATS

import os


def read(filename: str, format: str) -> dict[str, any]:
    format_data = FORMATS[format]
    with open(
        os.path.join(format_data.path, f"{filename}.{format_data.extension}"), "r"
    ) as input_file:
        return format_data.read_function(input_file.read())
