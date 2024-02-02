from collections import Counter
from typing import Callable, Literal

from src.generators.increment import generate_increment_system
from src.generators.decrement import generate_decrement_system
from src.generators.multiples_of import generate_multiples_of_system
from src.generators.subset_sum import generate_subset_sum_system
from src.generators.bit_adder import generate_bit_adder_system
from src.generators.comparator import generate_comparator_system
from src.generators.boolean_function import generate_boolean_function_system
from src.generators.complete_graph import generate_complete_graph_system

from src.classes.Format import Format
from src.globals import XML, JSON, YAML
from src.utils import read, write
from src.parsers import parse_dict_xml, parse_dict

import argparse
import functools
import operator
import os
import time


def _convert(filename: str, from_format: Format, to_format: Format) -> None:
    d = read(filename, from_format)
    system = parse_dict_xml(d) if from_format == XML else parse_dict(d)
    d = system.to_dict_xml() if to_format == XML else system.to_dict()
    write(d, filename, to_format)


def _simulate(
    filename: str,
    type_: Literal["generating", "halting", "boolean"],
    format: Format = JSON,
    time_limit: int = 10**3,
    make_log: bool = True,
) -> int:
    system = (
        parse_dict_xml(read(filename, format))
        if format == XML
        else parse_dict(read(filename, format))
    )
    return system.simulate(filename, type_, time_limit, make_log)


def search_through_folder(format: Format, f: Callable[[str], None]) -> None:
    for file in os.listdir(format.path):
        filepath = os.path.join(format.path, file)
        if os.path.isfile(filepath):
            f(file)


total_xml_size = 0
total_json_size = 0
total_yaml_size = 0


def benchmark():
    def benchmark_size(file: str) -> None:
        global total_xml_size, total_json_size, total_yaml_size

        filename = os.path.splitext(file)[0]

        xml_size = os.path.getsize(os.path.join(XML.path, f"{filename}.xml"))
        json_size = os.path.getsize(os.path.join(JSON.path, f"{filename}.json"))
        yaml_size = os.path.getsize(os.path.join(YAML.path, f"{filename}.yaml"))

        total_xml_size += xml_size
        total_json_size += json_size
        total_yaml_size += yaml_size

        xml_to_json = round(json_size / xml_size * 100, 1)
        xml_to_yaml = round(yaml_size / xml_size * 100, 1)

        print(f"File sizes for ({filename})")
        print()
        print(f"xml: {xml_size}")
        print(f"json: {json_size} ({xml_to_json}% of xml)")
        print(f"yaml: {yaml_size} ({xml_to_yaml}% of xml)")
        print()

    search_through_folder(format=JSON, f=benchmark_size)

    total_xml_to_json = round(total_json_size / total_xml_size * 100, 1)
    total_xml_to_yaml = round(total_yaml_size / total_xml_size * 100, 1)

    print("Total file sizes")
    print()
    print(f"xml: {total_xml_size}")
    print(f"json: {total_json_size} ({total_xml_to_json}% of xml)")
    print(f"yaml: {total_yaml_size} ({total_xml_to_yaml}% of xml)")
    print()


def batch_convert(from_format: Format, to_format: Format) -> None:
    search_through_folder(
        format=from_format,
        f=lambda file: _convert(os.path.splitext(file)[0], from_format, to_format),
    )


def round_trip(filename: str, format: Format = JSON) -> None:
    system = parse_dict(read(filename, format))
    write(system.to_dict(), filename, format)


def do_multiples_of(inputs: list[int]) -> None:
    for n in inputs:
        system = generate_multiples_of_system(n)
        write(system.to_dict(), f"multiples_of({str(n).zfill(3)})")
        counter = Counter[int]()
        t1 = time.time()
        for _ in range(10**2):
            value = _simulate(f"multiples_of({str(n).zfill(3)})", type_="generating")
            counter[value] += 1
        t2 = time.time()
        print(f"n={n} took {t2-t1} seconds ({(t2-t1)/(10**3)} seconds/simulation)")
        print()
        for k, v in sorted(list(counter.items())):
            print(f"({k//n}){n} => {v}")
        print()


def do_inc_dec(inputs: list[int]) -> None:
    for v in inputs:
        system = generate_increment_system(v)
        write(system.to_dict(), f"increment({str(v).zfill(3)})", format=JSON)
        _simulate(f"increment({str(v).zfill(3)})", type_="halting")
        system = generate_decrement_system(v)
        write(system.to_dict(), f"decrement({str(v).zfill(3)})", format=JSON)
        _simulate(f"decrement({str(v).zfill(3)})", type_="halting")


def do_subset_sum(inputs: list[tuple[list[int], int]]) -> None:
    for L, s in inputs:
        system = generate_subset_sum_system(L, s)
        filename = f"subset_sum([{','.join(map(str, L))}],{s})"
        write(system.to_dict(), filename)
        time_limit = 10**2
        for _ in range(10**2):
            result = _simulate(filename, type_="halting", time_limit=time_limit)
            if result != time_limit:
                break


def do_bit_adder(inputs: list[list[int]]) -> None:
    for L in inputs:
        system = generate_bit_adder_system(L)
        filename = f"bit_adder([{','.join(map(str, L))}])"
        write(system.to_dict(), filename)
        _simulate(filename, type_="halting")


def do_comparator(inputs: list[tuple[int, int]]) -> None:
    for a, b in inputs:
        system = generate_comparator_system(a, b)
        filename = f"comparator({a},{b})"
        write(system.to_dict(), filename)
        _simulate(filename, type_="halting")


def to_bool_list(n: int, bits: int) -> list[bool]:
    b = []
    while n > 0:
        b.append(n % 2 == 1)
        n //= 2
    while len(b) < bits:
        b.append(False)
    return b


def do_boolean_function(
    inputs: list[tuple[int, Callable[[list[bool]], bool], str]],
) -> None:
    for n, f, name in inputs:
        for i in range(1 << n):
            b = to_bool_list(i, n)
            system = generate_boolean_function_system(b, f)
            filename = (
                "boolean_function"
                f"({name}({','.join(map(lambda v: '1' if v else '0', b))}))"
            )
            write(system.to_dict(), filename)
            result = _simulate(filename, type_="boolean")
            print(f"({','.join(map(str, b))}) => {result}")
            print()


def do_complete_graph(inputs: list[int]) -> None:
    for n in inputs:
        system = generate_complete_graph_system(n)
        filename = f"complete_graph({str(n).zfill(3)})"
        write(system.to_dict(), filename)


def _main():
    round_trip(filename="even_positive_integer_generator")
    simulate("even_positive_integer_generator", type_="generating")

    multiples_of_inputs = [1, 2, 3, 4, 8, 9, 16, 27, 32, 64, 81, 100]
    do_multiples_of(multiples_of_inputs)

    inc_dec_inputs = [0, 1, 20, 30, 133, 140, 150, 165, 180, 198]
    do_inc_dec(inc_dec_inputs)

    subset_sum_inputs = [
        ([1, 2, 3], 5),
        ([1, 3, 5], 2),
        ([], 7),
        ([], 0),
        ([5], 5),
        ([9], 6),
        ([1, 2, 4, 8], 15),
    ]
    do_subset_sum(subset_sum_inputs)

    bit_adder_inputs = [
        [7, 11],
        [2, 9, 14],
        [30, 31, 32, 33],
        [],
        [1, 2, 4, 8, 16],
        [0, 0, 3, 0, 0],
    ]
    do_bit_adder(bit_adder_inputs)

    comparator_inputs = [
        (1, 6),
        (3, 3),
        (0, 5),
        (4, 2),
        (0, 0),
        (7, 4),
        (20, 23),
        (204, 133),
    ]
    do_comparator(comparator_inputs)

    boolean_function_inputs = [
        (3, lambda L: sum(L) != 2, "sum_not_2"),
        (4, lambda L: functools.reduce(operator.and_, L), "and"),
        (2, lambda L: functools.reduce(operator.xor, L), "xor"),
    ]
    do_boolean_function(boolean_function_inputs)

    complete_graph_inputs = [1, 2, 4, 8, 16, 32, 64]
    do_complete_graph(complete_graph_inputs)

    batch_convert(from_format=JSON, to_format=YAML)
    batch_convert(from_format=JSON, to_format=XML)

    benchmark()


def convert(path: str):
    if not os.path.exists(path):
        print(f"Error:\tFile at {path} doesn't exist...")
        return
    pass


def simulate(path: str):
    if not os.path.exists(path):
        print(f"Error:\tFile at {path} doesn't exist...")
        return
    if not os.path.isfile(path):
        print(f"Error:\tFile at {path} may be a directory...")


def generate(path: str, sys_type: str):
    if not os.path.exists(path):
        print(f"Error:\tFile at {path} doesn't exist...")
        return
    if not os.path.isdir(path):
        print(f"Error:\tFile at {path} isn't a directory...")
        return
    if sys_type is None:
        print(f"Error:\tNo type of system indicated...")
        return
    pass


DESCRIPTION = """
Converts, generates, and simulates Spiking Neural P (SN P) systems.

All actions take in a file path (e.g., /json/even_positive_integer_generator.json).
What happens next depends on the action specified:

    - [c]onvert: Converts {filetype} into {json,yaml} - {filetype}.
                 Note that xml is not a target filetype of the conversion.
                 If the given file path is a folder, attempts to convert each file
                 in this folder.

    - [s]imulate: Simulates the indicated system.

    - [g]enerate: Generates the requested system(s) into the indicated file path.
                  The given file path must be a folder.
                  For this action, another argument must be provided to indicate the
                  type of system to generate.
"""


def main():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "action",
        choices=["c", "g", "s"],
        help="[c]onvert, [g]enerate, or [s]imulate",
    )
    parser.add_argument(
        "path", help="path of folder or file to work on"
    )
    parser.add_argument(
        "-t", "--type", choices=["incr"], help="type of system to generate"
    )
    args = parser.parse_args()
    match args.action:
        case "c":
            convert(args.path)
        case "g":
            generate(args.path, args.type)
        case "s":
            simulate(args.path)


if __name__ == "__main__":
    main()
