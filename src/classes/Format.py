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
        return os.path.join(self.get_dir_path(), f"{filename}.{self.extension}")

    def read_dict(self, filename: str) -> dict:
        """
        Reads the file with name `{filename}.{extension}`
        and returns a dict that contains the SN P system's info.
        """
        with open(self.get_file_path(filename), "r") as input_file:
            return self.str_to_dict(input_file.read())

    def write_dict(self, d: dict, filename: str) -> None:
        """
        Takes in a dict `d` and writes its contents to the file
        with name `{filename}.{extension}`.
        """
        with open(self.get_file_path(filename), "w") as output_file:
            output_file.write(self.dict_to_str(d))
