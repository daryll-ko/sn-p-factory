import json
import os
import xmltodict
import yaml

from src.classes.Format import Format

INPUTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
FORMATS = {
    "xmp": Format(
        path=os.path.join(INPUTS_PATH, "xmp"),
        extension="xmp",
        read_function=lambda s: xmltodict.parse(s)["content"],
        write_function=lambda d: xmltodict.unparse(
            d, pretty=True, newl="\n", indent=" " * 4
        ),
    ),
    "json": Format(
        path=os.path.join(INPUTS_PATH, "json"),
        extension="json",
        read_function=lambda s: json.loads(s),
        write_function=lambda d: json.dumps(d, indent=2),
    ),
    "yaml": Format(
        path=os.path.join(INPUTS_PATH, "yaml"),
        extension="yaml",
        read_function=lambda s: yaml.load(s, Loader=yaml.Loader),
        write_function=lambda d: yaml.dump(d, sort_keys=False, indent=2),
    ),
}
