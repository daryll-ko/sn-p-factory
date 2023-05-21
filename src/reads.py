from src.classes.Format import Format

import os


def read(filename: str, format: Format) -> dict[str, any]:
    with open(
        os.path.join(format.path, f"{filename}.{format.extension}"), "r"
    ) as input_file:
        return format.read_function(input_file.read())
