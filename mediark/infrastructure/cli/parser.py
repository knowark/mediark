
import sys
from typing import List
from argparse import ArgumentParser, Namespace


def build_parser(argv: List[str] = None) -> Namespace:
    argv = argv or sys.argv

    parser = ArgumentParser()

    return parser.parse_args(argv)
