import os
import xmltodict
import json
import yaml

INPUTS_FOLDER = "inputs"

XMP_FOLDER = "xmp"
JSON_FOLDER = "json"
YAML_FOLDER = "yaml"


def read_xmp(filename: str) -> dict[str, any]:
    with open(
        os.path.join(
            os.path.dirname(__file__), INPUTS_FOLDER, XMP_FOLDER, f"{filename}.xmp"
        ),
        "r",
    ) as input_file:
        return xmltodict.parse(input_file.read())["content"]


def read_json(filename: str) -> dict[str, any]:
    with open(
        os.path.join(
            os.path.dirname(__file__), INPUTS_FOLDER, JSON_FOLDER, f"{filename}.json"
        ),
        "r",
    ) as input_file:
        return json.loads(input_file.read())


def read_yaml(filename: str) -> dict[str, any]:
    with open(
        os.path.join(
            os.path.dirname(__file__), INPUTS_FOLDER, YAML_FOLDER, f"{filename}.yaml"
        ),
        "r",
    ) as input_file:
        return yaml.load(input_file.read())
