from typing import Literal, get_args

SourceFormatString = Literal["xml", "json", "yaml"]
DestinationFormatString = Literal["json", "yaml"]
GeneratorString = Literal[
    "multiples_of",
    "increment",
    "decrement",
    "subset_sum",
    "bit_adder",
    "comparator",
    "bool_function",
    "complete_graph",
]

DESTINATION_FORMATS = list(get_args(DestinationFormatString))
SOURCE_FORMATS = list(get_args(SourceFormatString))
GENERATORS = list(get_args(GeneratorString))
