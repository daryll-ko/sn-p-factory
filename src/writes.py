from src.globals import XMP_PATH, JSON_PATH, YAML_PATH

import os
import xmltodict
import json
import yaml


def write_xmp(d: dict[str, any], filename: str):
    with open(os.path.join(XMP_PATH, f"{filename}.xmp"), "w") as xmp_output_file:
        xmp_output_file.write(
            xmltodict.unparse(d, pretty=True, newl="\n", indent=" " * 4)
        )


def write_json(d: dict[str, any], filename: str, simulating: bool):
    if simulating:
        directory_path = os.path.join(JSON_PATH, "|".join(filename.split("|")[:-1]))
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        with open(
            os.path.join(directory_path, f"{filename}.json"), "w"
        ) as json_output_file:
            json_output_file.write(json.dumps(d, indent=2))
    else:
        with open(os.path.join(JSON_PATH, f"{filename}.json"), "w") as json_output_file:
            json_output_file.write(json.dumps(d, indent=2))


def write_yaml(d: dict[str, any], filename: str):
    with open(os.path.join(YAML_PATH, f"{filename}.yaml"), "w") as yaml_output_file:
        yaml_output_file.write(yaml.dump(d, sort_keys=False, indent=2))
