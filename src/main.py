import os
import xmltodict

INPUT_FOLDER = "inputs"

def parse_xmp(filename: str) -> dict:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FOLDER, filename), 'r') as input_file:
        return xmltodict.parse(input_file.read())['content']

def parse_dict(d: dict):
    for k, _ in d.items():
        print(k)

dict = parse_xmp("ex1 - 3k+3 spiker.xmp")
parse_dict(dict)
