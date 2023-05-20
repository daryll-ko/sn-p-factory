from typing import Callable
from dataclasses import dataclass


@dataclass
class Format:
    path: str
    extension: str
    read_function: Callable[[str], dict]
    write_function: Callable[[dict], str]
