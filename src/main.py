from src.reads import read_xmp, read_json, read_yaml
from src.writes import write_json, write_yaml
from src.parsers import parse_dict_xmp, parse_dict

import os


INPUTS_PATH = os.path.join(os.path.dirname(__file__), "data")

XMP_PATH = os.path.join(INPUTS_PATH, "xmp")
JSON_PATH = os.path.join(INPUTS_PATH, "json")
YAML_PATH = os.path.join(INPUTS_PATH, "yaml")


def convert():
    success_count = 0
    success_filenames = []
    failure_count = 0
    failure_filenames = []

    for file in os.listdir(XMP_PATH):
        filename = os.path.splitext(file)[0]
        print(f"Converting ({filename})...")
        print()

        try:
            dict_xmp = read_xmp(filename)
            system_xmp = parse_dict_xmp(dict_xmp, filename)

            dict_new = system_xmp.to_dict()

            write_json(dict_new, filename)
            write_yaml(dict_new, filename)

            dict_json = read_json(filename)
            system_json = parse_dict(dict_json)

            dict_yaml = read_yaml(filename)
            system_yaml = parse_dict(dict_yaml)

            if system_xmp == system_json == system_yaml:
                success_count += 1
                success_filenames.append(filename)
                print("Conversion successful!")
                print()
            else:
                failure_count += 1
                failure_filenames.append(filename)
                print("Systems don't match...")
                print()
                print(f"xmp: {system_xmp}")
                print()
                print(f"json: {system_json}")
                print()
                print(f"yaml: {system_yaml}")
                print()

        except Exception as ex:
            failure_count += 1
            failure_filenames.append(filename)
            print(f"Conversion failed: [{type(ex).__name__} - {ex}]...")
            print()

    print(
        f"Successes: {success_count} of {success_count + failure_count}"
        " "
        f"({round(100 * success_count / (success_count + failure_count), 1)}%)"
    )
    print()
    print("\n".join(success_filenames))
    print()
    print(
        f"Failures: {failure_count} of {success_count + failure_count}"
        " "
        f"({round(100 * failure_count / (success_count + failure_count), 1)}%)"
    )
    print()
    print("\n".join(failure_filenames))
    print()


def benchmark():
    total_xmp_size = 0
    total_json_size = 0
    total_yaml_size = 0

    for file in os.listdir(JSON_PATH):
        filename = os.path.splitext(file)[0]

        xmp_size = os.path.getsize(os.path.join(XMP_PATH, f"{filename}.xmp"))
        json_size = os.path.getsize(os.path.join(JSON_PATH, f"{filename}.json"))
        yaml_size = os.path.getsize(os.path.join(YAML_PATH, f"{filename}.yaml"))

        total_xmp_size += xmp_size
        total_json_size += json_size
        total_yaml_size += yaml_size

        xmp_to_json = round(json_size / xmp_size * 100, 1)
        xmp_to_yaml = round(yaml_size / xmp_size * 100, 1)

        print(f"File sizes for ({filename})")
        print()
        print(f"xmp: {xmp_size}")
        print(f"json: {json_size} ({xmp_to_json}% of xmp)")
        print(f"yaml: {yaml_size} ({xmp_to_yaml}% of xmp)")
        print()

    total_xmp_to_json = round(total_json_size / total_xmp_size * 100, 1)
    total_xmp_to_yaml = round(total_yaml_size / total_xmp_size * 100, 1)

    print("Total file sizes")
    print()
    print(f"xmp: {total_xmp_size}")
    print(f"json: {total_json_size} ({total_xmp_to_json}% of xmp)")
    print(f"yaml: {total_yaml_size} ({total_xmp_to_yaml}% of xmp)")
    print()


def main():
    convert()
    print("- " * 39 + "-")
    print()
    benchmark()


if __name__ == "__main__":
    main()
