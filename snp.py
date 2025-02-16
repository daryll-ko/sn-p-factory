#!/usr/bin/env -S uv run

from argparse import ArgumentParser
from pathlib import Path
from random import Random
from typing import Any, Optional

from classes.FileFormat import FileFormat, str_to_format
from classes.SystemGenerator import SystemGenerator, str_to_generator
from utils.logging import tgreen, tred
from utils.parsers import parse_dict
from utils.types import DESTINATION_FORMATS, GENERATORS, SOURCE_FORMATS


def _convert(src_path: Path, dest_path: Path) -> None:
    try:
        with open(src_path, "r") as f:
            s = f.read()

        d = str_to_format(src_path.suffix).str_to_dict(s)
        s = str_to_format(dest_path.suffix).dict_to_str(d)

        with open(dest_path, "w") as f:
            f.write(s)
    except Exception as e:
        print(tred(e))
    else:
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
                _convert(src_path, dest_path)


def _generate(dest_path: Path, generator: SystemGenerator, args: Any) -> None:
    try:
        system = generator.generate(*args)

        d = system.to_dict()
        s = str_to_format(dest_path.suffix).dict_to_str(d)

        with open(dest_path, "w") as f:
            f.write(s)
    except Exception as e:
        print(tred(e))
    else:
        print(tgreen(dest_path))


def generate(args: Any) -> None:
    dest_formats = args.to if isinstance(args.to, list) else [args.to]
    generator = str_to_generator(args.generator)

    def generate_with_args(gen_args: Any) -> None:
        name = f"{args.generator}_{'_'.join(map(str, gen_args))}"
        for dest_format in dest_formats:
            dest_path = Path(args.dir) / dest_format / f"{name}.{dest_format}"
            _generate(dest_path, generator, gen_args)

    if args.random is not None:
        rand = Random(199)
        for _ in range(args.random):
            gen_args = generator.rand_args(rand)
            generate_with_args(gen_args)
    else:
        generate_with_args(args.args)


def _simulate(path: Path, _format: FileFormat) -> None:
    try:
        with open(path, "r") as f:
            s = f.read()

        d = _format.str_to_dict(s)
        sys = parse_dict(d)

        sys.simulate("generating", 100, True)
    except Exception as e:
        print(tred(e))


def simulate(args: Any):
    path = Path(args.path)
    _format = str_to_format(path.suffix)

    _simulate(path, _format)


def _check(
    path: Path, intrp: str, n: Optional[int], b: Optional[str], _format: FileFormat
) -> None:
    try:
        with open(path, "r") as f:
            s = f.read()

        d = _format.str_to_dict(s)
        sys = parse_dict(d)

        if intrp == "dis":
            assert n is not None
            for ans in sys.get_configs(n + 1, det=False, lazy=True):
                if ans.get_spike_distance() == n:
                    print(tgreen(f"{n} is accepted by the system!"))
                    return
            print(tred(f"{n} isn't accepted by the system..."))
        elif intrp == "lit":
            assert b is not None
            for ans in sys.get_configs(len(b), det=False, lazy=True):
                if ans.get_bit_string() == b:
                    print(tgreen(f"{b} is accepted by the system!"))
                    return
            print(tred(f"{b} isn't accepted by the system..."))

    except Exception as e:
        print(tred(e))


def check(args: Any):
    path = Path(args.path)
    intrp = args.interpretation

    n, b = None, None

    if intrp == "dis":
        assert args.num is not None
        n = args.num
    elif intrp == "lit":
        assert args.bit_string is not None
        b = args.bit_string

    _format = str_to_format(path.suffix)

    _check(path, intrp, n, b, _format)


def setup_checker(ch: ArgumentParser) -> None:
    ch.add_argument("path")
    ch.add_argument("interpretation", choices=["dis", "lit"])
    ch.add_argument("-n", "--num", type=int)
    ch.add_argument("-b", "--bit_string")

    ch.set_defaults(func=check)


def setup_converter(c: ArgumentParser) -> None:
    c.add_argument("name")
    c.add_argument("_from", choices=SOURCE_FORMATS)
    c.add_argument(
        "-t",
        "--to",
        choices=DESTINATION_FORMATS,
        default=DESTINATION_FORMATS,
    )
    c.add_argument("-d", "--dir", default="data")

    c.set_defaults(func=convert)


def setup_generator(g: ArgumentParser) -> None:
    g.add_argument("generator", choices=GENERATORS)

    _g = g.add_mutually_exclusive_group()
    _g.add_argument("-a", "--args", nargs="+")
    _g.add_argument("-r", "--random", type=int)

    g.add_argument(
        "-t", "--to", choices=DESTINATION_FORMATS, default=DESTINATION_FORMATS
    )
    g.add_argument("-d", "--dir", default="data")

    g.set_defaults(func=generate)


def setup_simulator(s: ArgumentParser) -> None:
    s.add_argument("path")

    s.set_defaults(func=simulate)


def setup_parser() -> ArgumentParser:
    parser = ArgumentParser(
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
    setup_simulator(s)

    ch = subparsers.add_parser(
        "check", aliases=["ch"], help="Check if a string is accepted by an SN P system."
    )
    setup_checker(ch)

    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
