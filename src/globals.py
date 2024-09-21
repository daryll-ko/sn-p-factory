import json

import xmltodict
import yaml

from src.classes.Format import Format

XML = Format(
    extension="xml",
    str_to_dict=lambda s: xmltodict.parse(s)["content"],
    dict_to_str=lambda d: xmltodict.unparse(d, pretty=True, newl="\n", indent=" " * 4),
)

JSON = Format(
    extension="json",
    str_to_dict=lambda s: json.loads(s),
    dict_to_str=lambda d: json.dumps(d, indent=2),
)

YAML = Format(
    extension="yaml",
    str_to_dict=lambda s: yaml.load(s, Loader=yaml.Loader),
    dict_to_str=lambda d: yaml.dump(d, sort_keys=False, indent=2),
)

LOG = Format(
    extension="log",
    str_to_dict=lambda _: {},
    dict_to_str=lambda _: "",
)

ALL_FORMATS = [XML, JSON, YAML, LOG]
