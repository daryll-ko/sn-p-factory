import os
import xmltodict
import json

INPUT_FOLDER = "inputs"

def parse_xmp(filename: str):
    with open(os.path.join(os.path.dirname(__file__), INPUT_FOLDER, filename), 'r') as input_file:
        return xmltodict.parse(input_file.read())

dict = parse_xmp("ex1 - 3k+3 spiker.xmp")
print(json.dumps(dict, indent=4))
