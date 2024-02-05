import os

from dataclasses import dataclass
from typing import Callable

TEST_CASE_FOLDER = os.path.join(os.getcwd(), "data")


@dataclass
class Format:
    extension: str
    str_to_dict: Callable[[str], dict]
    dict_to_str: Callable[[dict], str]

    def get_dir_path(self):
        return os.path.join(TEST_CASE_FOLDER, self.extension)

    def get_file_path(self, filename: str):
        return os.path.join(get_dir_path(self), f"{name}.{self.extension}")
