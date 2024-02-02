from src.classes.Format import Format

import os


def read_dict(filename: str, format: Format) -> dict:
    """
    Reads the file with name `{filename}.{format extension}`
    and returns a dict that contains the SN P system's info.
    """
    with open(
        os.path.join(format.get_path(), f"{filename}.{format.extension}"), "r"
    ) as input_file:
        return format.str_to_dict(input_file.read())


def write_dict(d: dict, filename: str, format: Format) -> None:
    """
    Takes in a dict `d` and writes its contents to the file
    with name `{filename}.{format extension}` via `format`.
    """
    with open(
        os.path.join(format.get_path(), f"{filename}.{format.extension}"), "w"
    ) as output_file:
        output_file.write(format.dict_to_str(d))
