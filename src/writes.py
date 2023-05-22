from typing import Any
from src.classes.Format import Format
from src.classes.TestName import TestName

import os


def write(
    d: dict[str, Any], testname: TestName, format: Format, simulating: bool
) -> None:
    filename = testname.make_filename()
    if simulating:
        directory_path = os.path.join(format.path, testname.name)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        with open(
            os.path.join(directory_path, f"{filename}.{format.extension}"), "w"
        ) as output_file:
            output_file.write(format.write_function(d))
    else:
        with open(
            os.path.join(format.path, f"{filename}.{format.extension}"), "w"
        ) as output_file:
            output_file.write(format.write_function(d))
