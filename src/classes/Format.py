from typing import Callable
from dataclasses import dataclass


@dataclass
class Format:
    path: str
    extension: str
    str_to_dict: Callable[[str], dict]
    dict_to_str: Callable[[dict], str]
