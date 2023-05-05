from src.globals import XMP_PATH, JSON_PATH, YAML_PATH

import os
import xmltodict
import json
import yaml


def read_xmp(filename: str) -> dict[str, any]:
    with open(
        os.path.join(XMP_PATH, f"{filename}.xmp"),
        "r",
    ) as input_file:
        return xmltodict.parse(input_file.read())["content"]


def read_json(filename: str) -> dict[str, any]:
    with open(
        os.path.join(JSON_PATH, f"{filename}.json"),
        "r",
    ) as input_file:
        return json.loads(input_file.read())


def read_yaml(filename: str) -> dict[str, any]:
    with open(
        os.path.join(YAML_PATH, f"{filename}.yaml"),
        "r",
    ) as input_file:
        return yaml.load(input_file.read(), Loader=yaml.Loader)
