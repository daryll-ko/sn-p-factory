from collections import Counter
from typing import Callable

from src.classes.Format import Format
from src.generators.increment import generate_increment_system
from src.generators.decrement import generate_decrement_system
from src.generators.boolean_triple_sum_not_2 import (
    generate_boolean_triple_sum_not_2_system,
)
from src.generators.multiples_of import generate_multiples_of_system
from src.globals import XML, JSON, YAML
from src.utils import read, write
from src.parsers import parse_dict_xml, parse_dict

import os
import time


def convert(
    filename: str, from_format: Format, to_format: Format, simulating: bool
) -> None:
    d = read(filename, from_format, simulating)
    system = parse_dict_xml(d) if from_format == XML else parse_dict(d)
    d = system.to_dict_xml() if to_format == XML else system.to_dict()
    write(d, filename, to_format, simulating)


def simulate(filename: str, format: Format, verbose: bool) -> int:
    system = (
        parse_dict_xml(read(filename, format, simulating=False))
        if format == XML
        else parse_dict(read(filename, format, simulating=False))
    )
    return system.simulate(filename, format, verbose)


def search_through_folder(
    format: Format, outer_f: Callable[[str], None], inner_f: Callable[[str], None]
) -> None:
    for file in os.listdir(format.path):
        filepath = os.path.join(format.path, file)
        if os.path.isfile(filepath):
            outer_f(file)
        else:
            for inner_file in os.listdir(filepath):
                inner_f(inner_file)


total_xml_size = 0
total_json_size = 0
total_yaml_size = 0


def benchmark():
    def benchmark_file(file: str, inside_folder: bool) -> None:
        global total_xml_size, total_json_size, total_yaml_size

        folder_name = os.path.splitext(file)[0].split("[")[0]
        filename = os.path.splitext(file)[0]

        xml_size = os.path.getsize(
            os.path.join(XML.path, folder_name, f"{filename}.xml")
            if inside_folder
            else os.path.join(XML.path, f"{filename}.xml")
        )
        json_size = os.path.getsize(
            os.path.join(JSON.path, folder_name, f"{filename}.json")
            if inside_folder
            else os.path.join(JSON.path, f"{filename}.json")
        )
        yaml_size = os.path.getsize(
            os.path.join(YAML.path, folder_name, f"{filename}.yaml")
            if inside_folder
            else os.path.join(YAML.path, f"{filename}.yaml")
        )

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

    search_through_folder(
        format=JSON,
        outer_f=lambda file: benchmark_file(file, inside_folder=False),
        inner_f=lambda file: benchmark_file(file, inside_folder=True),
    )

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
        outer_f=lambda file: convert(
            os.path.splitext(file)[0], from_format, to_format, simulating=False
        ),
        inner_f=lambda inner_file: convert(
            os.path.splitext(inner_file)[0], from_format, to_format, simulating=True
        ),
    )


def round_trip(filename: str, format: Format, simulating: bool) -> None:
    system = parse_dict(read(filename, format, simulating))
    write(
        system.to_dict(),
        filename,
        format,
        simulating,
    )


def do_multiples_of(initial_values: list[int]) -> None:
    for n in initial_values:
        system = generate_multiples_of_system(n)
        write(
            system.to_dict(),
            f"multiples_of({str(n).zfill(3)})",
            format=JSON,
            simulating=False,
        )
        counter = Counter[int]()
        t1 = time.time()
        for _ in range(10**3):
            value = simulate(
                f"multiples_of({str(n).zfill(3)})", format=JSON, verbose=False
            )
            counter[value] += 1
        t2 = time.time()
        print(f"n={n} took {t2-t1} seconds ({(t2-t1)/(10**3)} seconds/simulation)")
        print()
        for k, v in sorted(list(counter.items())):
            print(f"({k//n}){n} => {v}")
        print()


def do_inc_dec(initial_values: list[int]) -> None:
    for v in initial_values:
        system = generate_increment_system(v)
        write(
            system.to_dict(),
            f"increment({str(v).zfill(3)})",
            format=JSON,
            simulating=False,
        )
        simulate(f"increment({str(v).zfill(3)})", format=JSON, verbose=True)
        system = generate_decrement_system(v)
        write(
            system.to_dict(),
            f"decrement({str(v).zfill(3)})",
            format=JSON,
            simulating=False,
        )
        simulate(f"decrement({str(v).zfill(3)})", format=JSON, verbose=True)


def do_boolean_triple_sum_not_2() -> None:
    for b1 in range(2):
        for b2 in range(2):
            for b3 in range(2):
                system = generate_boolean_triple_sum_not_2_system(b1, b2, b3)
                write(
                    system.to_dict(),
                    f"boolean_triple_sum_not_2({b1},{b2},{b3})",
                    format=JSON,
                    simulating=False,
                )
                result = (
                    1
                    if simulate(
                        f"boolean_triple_sum_not_2({b1},{b2},{b3})",
                        format=JSON,
                        verbose=False,
                    )
                    else 0
                )
                print(f"({b1},{b2},{b3}) => {result}")
                print()


def main():
    pass

    # --- TO DO ---
    # - split snapshots to A/B parts
    # - add SAT & Subset-Sum test cases

    # round_trip(filename="positive_integer_generator", format=JSON, simulating=False)

    # simulate("positive_integer_generator", format=JSON, verbose=True)
    # simulate("even_positive_integer_generator", format=JSON, verbose=True)

    # multiples_of_initial_values = [1, 2, 3, 4, 8, 9, 16, 27, 32, 64, 81, 100]
    # do_multiples_of(multiples_of_initial_values)

    # inc_dec_initial_values = [0, 1, 20, 30, 133, 140, 150, 165, 180, 198]
    # do_inc_dec(inc_dec_initial_values)

    # do_boolean_triple_sum_not_2()

    # batch_convert(from_format=JSON, to_format=YAML)
    # batch_convert(from_format=JSON, to_format=XML)

    # benchmark()


if __name__ == "__main__":
    main()
