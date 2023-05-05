import os
import xmltodict
import json
import yaml

INPUTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

XMP_PATH = os.path.join(INPUTS_PATH, "xmp")
JSON_PATH = os.path.join(INPUTS_PATH, "json")
YAML_PATH = os.path.join(INPUTS_PATH, "yaml")


def write_xmp(dict: dict[str, any], filename: str):
    with open(os.path.join(XMP_PATH, f"{filename}.xmp"), "w") as xmp_output_file:
        xmp_output_file.write(
            xmltodict.unparse(dict, pretty=True, newl="\n", indent=" " * 4)
        )


def write_json(dict: dict[str, any], filename: str):
    with open(os.path.join(JSON_PATH, f"{filename}.json"), "w") as json_output_file:
        json_output_file.write(json.dumps(dict, indent=2))


def write_yaml(dict: dict[str, any], filename: str):
    with open(os.path.join(YAML_PATH, f"{filename}.yaml"), "w") as yaml_output_file:
        yaml_output_file.write(yaml.dump(dict, sort_keys=False, indent=2))
