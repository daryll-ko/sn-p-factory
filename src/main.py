from src.reads import read_xmp, read_json, read_yaml
from src.parsers import parse_xmp_dict, parse_dict

import json
import yaml
import xmltodict


def main():
    filename = "3k+3"

    d_xmp = read_xmp(filename)
    system_xmp = parse_xmp_dict(d_xmp, filename)
    print(xmltodict.unparse(system_xmp.to_dict_old(), pretty=True, indent=" " * 4))
    print()

    d_json = read_json(filename)
    system_json = parse_dict(d_json)
    print(json.dumps(system_json.to_dict(), indent=4))
    print()

    d_yaml = read_yaml(filename)
    system_yaml = parse_dict(d_yaml)
    print(yaml.dump(system_yaml.to_dict(), sort_keys=False, indent=2))
    print()


if __name__ == "__main__":
    main()
