from src.classes.Format import Format

import os


def read_dict(filename: str, format: Format) -> dict:
    with open(
        os.path.join(format.path, f"{filename}.{format.extension}"), "r"
    ) as input_file:
        return format.str_to_dict(input_file.read())


def write_dict(d: dict, filename: str, format: Format) -> None:
    with open(
        os.path.join(format.path, f"{filename}.{format.extension}"), "w"
    ) as output_file:
        output_file.write(format.dict_to_str(d))
