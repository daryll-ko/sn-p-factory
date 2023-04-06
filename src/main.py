from src.reads import read_xmp, read_json, read_yaml
from src.parsers import parse_xmp_dict, parse_dict

import os
import json
import yaml


def main():
    inputs_path = os.path.join(os.path.dirname(__file__), "data")

    xmp_path = os.path.join(inputs_path, "xmp")
    json_path = os.path.join(inputs_path, "json")
    yaml_path = os.path.join(inputs_path, "yaml")

    for file in os.listdir(xmp_path):
        filename = os.path.splitext(file)[0]

        d_1 = read_xmp(filename)
        system_1 = parse_xmp_dict(d_1, filename)

        with open(os.path.join(json_path, f"{filename}.json"), "w") as json_output_file:
            json_output_file.write(json.dumps(system_1.to_dict(), indent=4))

        with open(os.path.join(yaml_path, f"{filename}.yaml"), "w") as yaml_output_file:
            yaml_output_file.write(
                yaml.dump(system_1.to_dict(), sort_keys=False, indent=2)
            )

        d_2 = read_json(filename)
        system_2 = parse_dict(d_2)

        d_3 = read_yaml(filename)
        system_3 = parse_dict(d_3)

        print(system_1 == system_2 == system_3)


if __name__ == "__main__":
    main()
