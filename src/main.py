from src.reads import read_xmp
from src.parsers import parse_xmp_dict

import json
import yaml
import xmltodict


def main():
    filename = "3k+3"
    d = read_xmp(filename)
    system = parse_xmp_dict(d, filename)
    print(json.dumps(system.to_dict(), indent=4))
    print()
    print(xmltodict.unparse(system.to_dict_old(), pretty=True, indent="    "))
    print()
    print(yaml.dump(system.to_dict(), sort_keys=False, indent=2))


if __name__ == "__main__":
    main()
