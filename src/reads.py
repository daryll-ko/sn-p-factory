from typing import Any
from src.classes.Format import Format

import os


def read(filename: str, format: Format, simulating: bool) -> dict[str, Any]:
    if simulating:
        directory_path = os.path.join(format.path, filename.split("[")[0])
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
    with open(
        os.path.join(
            directory_path if simulating else format.path,
            f"{filename}.{format.extension}",
        ),
        "w",
    ) as input_file:
        return format.read_function(input_file.read())
