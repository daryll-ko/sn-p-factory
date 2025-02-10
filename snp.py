#!/usr/bin/env -S uv run

import argparse
import functools
import operator
import os
import time
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Literal, Optional

from classes.FileFormat import FileFormat, str_to_format
from globals import DEST_FORMATS, GENERATORS, SRC_FORMATS
from src.classes.Format import Format
from src.generators.bit_adder import generate_bit_adder_system
from src.generators.boolean_function import generate_boolean_function_system
from src.generators.comparator import generate_comparator_system
from src.generators.complete_graph import generate_complete_graph_system
from src.generators.decrement import generate_decrement_system
from src.generators.increment import generate_increment_system
from src.generators.multiples_of import generate_multiples_of_system
from src.generators.subset_sum import generate_subset_sum_system
from src.globals import ALL_FORMATS, JSON, XML, YAML
from src.parsers import parse_dict, parse_dict_xml
from utils.logging import tgreen, tred


def _simulate(
    filename: str,
    type_: Literal["generating", "halting", "boolean"],
    format: Format = JSON,
    time_limit: int = 10**3,
    make_log: bool = True,
) -> int:
    system = (
        parse_dict_xml(read_dict(filename, format))
        if format == XML
        else parse_dict(read_dict(filename, format))
    )
    return system.simulate(filename, type_, time_limit, make_log)


def round_trip(filename: str, format: Format = JSON) -> None:
    system = parse_dict(read_dict(filename, format))
    write_dict(system.to_dict(), filename, format)


def do_multiples_of(inputs: list[int]) -> None:
    for n in inputs:
        system = generate_multiples_of_system(n)
        write_dict(system.to_dict(), f"multiples_of({str(n).zfill(3)})", JSON)
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
        write_dict(system.to_dict(), f"increment({str(v).zfill(3)})", format=JSON)
        _simulate(f"increment({str(v).zfill(3)})", type_="halting")
        system = generate_decrement_system(v)
        write_dict(system.to_dict(), f"decrement({str(v).zfill(3)})", format=JSON)
        _simulate(f"decrement({str(v).zfill(3)})", type_="halting")


def do_subset_sum(inputs: list[tuple[list[int], int]]) -> None:
    for L, s in inputs:
        system = generate_subset_sum_system(L, s)
        filename = f"subset_sum([{','.join(map(str, L))}],{s})"
        write_dict(system.to_dict(), filename, JSON)
        time_limit = 10**2
        for _ in range(10**2):
            result = _simulate(filename, type_="halting", time_limit=time_limit)
            if result != time_limit:
                break


def do_bit_adder(inputs: list[list[int]]) -> None:
    for L in inputs:
        system = generate_bit_adder_system(L)
        filename = f"bit_adder([{','.join(map(str, L))}])"
        write_dict(system.to_dict(), filename, JSON)
        _simulate(filename, type_="halting")


def do_comparator(inputs: list[tuple[int, int]]) -> None:
    for a, b in inputs:
        system = generate_comparator_system(a, b)
        filename = f"comparator({a},{b})"
        write_dict(system.to_dict(), filename, JSON)
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
            write_dict(system.to_dict(), filename, JSON)
            result = _simulate(filename, type_="boolean")
            print(f"({','.join(map(str, b))}) => {result}")
            print()


def do_complete_graph(inputs: list[int]) -> None:
    for n in inputs:
        system = generate_complete_graph_system(n)
        filename = f"complete_graph({str(n).zfill(3)})"
        write_dict(system.to_dict(), filename, JSON)


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

    benchmark()


def _convert(
    src_path: Path, dest_path: Path, src_format: FileFormat, dest_format: FileFormat
) -> None:
    try:
        with open(src_path, "r") as f:
            s = f.read()
    except Exception as e:
        print(tred(e))
        return

    d = src_format.str_to_dict(s)
    s = dest_format.dict_to_str(d)

    try:
        with open(dest_path, "w") as f:
            f.write(s)
    except Exception as e:
        print(tred(e))
        return

    print(tgreen(f"{src_path} --> {dest_path}"))


def convert(args: Any) -> None:
    src_format = args._from
    src_paths = Path(args.dir).glob(f"**/*{args.name}*.{src_format}")
    dest_formats = args.to if isinstance(args.to, list) else [args.to]

    for src_path in src_paths:
        for dest_format in dest_formats:
            if dest_format != src_format:
                dest_path = (
                    Path(args.dir) / dest_format / f"{src_path.stem}.{dest_format}"
                )
                _convert(
                    src_path,
                    dest_path,
                    str_to_format(args._from),
                    str_to_format(dest_format),
                )


def simulate(path: str):
    if not os.path.exists(path):
        print(f"Error:\t{path} doesn't exist...")
        return
    if not os.path.isfile(path):
        print(f"Error:\t{path} isn't a file...")
        return


def generate(args: Any) -> None: ...


def setup_converter(c: ArgumentParser) -> None:
    c.add_argument("name")
    c.add_argument("_from", choices=SRC_FORMATS)
    c.add_argument("-t", "--to", choices=DEST_FORMATS, default=DEST_FORMATS)
    c.add_argument("-d", "--dir", default="systems")

    c.set_defaults(func=convert)


def setup_generator(g: ArgumentParser) -> None:
    g.add_argument("generator", choices=GENERATORS)
    g.add_argument("-t", "--to", choices=DEST_FORMATS, default=DEST_FORMATS)
    g.add_argument("-d", "--dir", default="systems")
    g.set_defaults(func=generate)


def setup_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="snp.py",
        description="Utilities for working with Spiking Neural P (SN P) systems.",
    )
    subparsers = parser.add_subparsers(required=True)

    c = subparsers.add_parser("convert", aliases=["c"], help="Convert an SN P system.")
    setup_converter(c)

    g = subparsers.add_parser(
        "generate", aliases=["g"], help="Generate an SN P system."
    )
    setup_generator(g)

    s = subparsers.add_parser(
        "simulate", aliases=["s"], help="Simulate an SN P system."
    )
    s.add_argument("file")
    s.set_defaults(func=simulate)

    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
