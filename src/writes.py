from src.globals import FORMATS

import os


def write(d: dict[str, any], filename: str, format: str, simulating: bool) -> None:
    format_data = FORMATS[format]
    if simulating:
        directory_path = os.path.join(
            format_data.path, "|".join(filename.split("|")[:-1])
        )
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        with open(
            os.path.join(directory_path, f"{filename}.{format_data.extension}"), "w"
        ) as output_file:
            output_file.write(format_data.write_function(d))
