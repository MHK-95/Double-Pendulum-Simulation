from typing import List, Union, Dict
import argparse
import sys

Primitive = Union[str, bool, float, int]


def parse_args(args: List[str]) -> Dict[str, Primitive]:
    parser = argparse.ArgumentParser(args)

    return parser.parse_args(args)


def main() -> None:
    args = parse_args(sys.argv[1:])
