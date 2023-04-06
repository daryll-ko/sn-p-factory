from src.reads import read_xmp, read_json, read_yaml
from src.parsers import parse_xmp_dict, parse_dict

import os
import json
import yaml

INPUTS_PATH = os.path.join(os.path.dirname(__file__), "data")

XMP_PATH = os.path.join(INPUTS_PATH, "xmp")
JSON_PATH = os.path.join(INPUTS_PATH, "json")
YAML_PATH = os.path.join(INPUTS_PATH, "yaml")


def convert():
    success = 0
    success_filenames = []
    failure = 0
    failure_filenames = []

    for file in os.listdir(XMP_PATH):
        filename = os.path.splitext(file)[0]
        print(f"Converting ({filename})...")

        try:
            d_1 = read_xmp(filename)
            system_1 = parse_xmp_dict(d_1, filename)

            with open(
                os.path.join(JSON_PATH, f"{filename}.json"), "w"
            ) as json_output_file:
                json_output_file.write(json.dumps(system_1.to_dict(), indent=4))

            with open(
                os.path.join(YAML_PATH, f"{filename}.yaml"), "w"
            ) as yaml_output_file:
                yaml_output_file.write(
                    yaml.dump(system_1.to_dict(), sort_keys=False, indent=2)
                )

            d_2 = read_json(filename)
            system_2 = parse_dict(d_2)

            d_3 = read_yaml(filename)
            system_3 = parse_dict(d_3)

            if system_1 == system_2 == system_3:
                success += 1
                success_filenames.append(filename)
                print("Conversion successful!")
                print()
            else:
                failure += 1
                failure_filenames.append(filename)
                print("Systems don't match...")
                print()

        except Exception as ex:
            failure += 1
            failure_filenames.append(filename)
            print(f"Conversion failed: {type(ex).__name__}...")
            print()

    print(f"Successes: {success} ({round(100 * success / (success + failure), 1)}%)")
    print()
    print("\n".join(success_filenames))
    print()
    print(f"Failures: {failure} ({round(100 * failure / (success + failure), 1)}%)")
    print()
    print("\n".join(failure_filenames))


def main():
    print("hello world~")


if __name__ == "__main__":
    main()
