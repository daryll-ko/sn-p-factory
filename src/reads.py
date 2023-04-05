import os
import xmltodict

INPUTS_FOLDER = "inputs"
XMP_FOLDER = "xmp"


def read_xmp(filename: str) -> dict[str, any]:
    with open(
        os.path.join(
            os.path.dirname(__file__), INPUTS_FOLDER, XMP_FOLDER, f"{filename}.xmp"
        ),
        "r",
    ) as input_file:
        return xmltodict.parse(input_file.read())["content"]
