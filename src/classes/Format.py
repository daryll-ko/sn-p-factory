import os

from dataclasses import dataclass
from typing import Callable

from src.globals import TEST_CASE_FOLDER


@dataclass
class Format:
    extension: str
    str_to_dict: Callable[[str], dict]
    dict_to_str: Callable[[dict], str]

    def get_path(self):
        return os.path.join(TEST_CASE_FOLDER, self.extension)
