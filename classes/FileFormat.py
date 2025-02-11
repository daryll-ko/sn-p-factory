import json
from typing import Protocol

import xmltodict
import yaml


class FileFormat(Protocol):
    def str_to_dict(self, s: str) -> dict: ...
    def dict_to_str(self, d: dict) -> str: ...


class XML:
    def str_to_dict(self, s: str) -> dict:
        return xmltodict.parse(s)["content"]

    def dict_to_str(self, d: dict) -> str:
        return xmltodict.unparse(d, pretty=True, newl="\n", indent=" " * 4)


class JSON:
    def str_to_dict(self, s: str) -> dict:
        return json.loads(s)

    def dict_to_str(self, d: dict) -> str:
        return json.dumps(d, indent=2)


class YAML:
    def str_to_dict(self, s: str) -> dict:
        return yaml.load(s, Loader=yaml.Loader)

    def dict_to_str(self, d: dict) -> str:
        return yaml.dump(d, sort_keys=False, indent=2)


def str_to_format(s: str) -> FileFormat:
    match s:
        case ".xml":
            return XML()
        case ".json":
            return JSON()
        case ".yaml":
            return YAML()
        case _:
            raise Exception(":(")
