from typing import Any
from src.classes.Format import Format

import os


def write(d: dict[str, Any], filename: str, format: Format, simulating: bool) -> None:
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
    ) as output_file:
        output_file.write(format.write_function(d))
