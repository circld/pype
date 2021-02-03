#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse as ap
import logging
import sys

from toolz.curried import filter, identity, map


def command(cmd):
    lambda_cmd = f"lambda _: {cmd}"
    logging.debug(lambda_cmd)
    return eval(lambda_cmd)


def format_sequence(seq):
    return "\n".join(seq)


def parse_args():
    p = ap.ArgumentParser()
    group = p.add_mutually_exclusive_group()
    p.add_argument(
        "snippet",
        help=" ".join(
            (
                "Snippet of python code to execute on stdin.",
                "If the snippet is a function that takes the input as an argument, pass the `--function` flag.",
            )
        ),
    )
    group.add_argument(
        "--filter",
        action="store_true",
        help="Filter input using the snippet. The snippet must be a boolean expression.",
    )
    group.add_argument(
        "--map", action="store_true", help="Apply the snippet to each line of input."
    )
    p.add_argument(
        "--function",
        action="store_true",
        help="The snippet is a syntactically correct function and should be called on the input.",
    )
    p.add_argument(
        "--import",
        nargs="*",
        dest="modules",
        help="Make the following modules available for use in the snippet.",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase amount of logging output printed to stdout.",
    )
    return p.parse_args()


def main(args):
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(filename)s:%(funcName)s (line %(lineno)s) %(message)s",
    )

    logging.debug(args)
    input_stream = map(str.strip, sys.stdin)

    if args.modules:
        import importlib

        for m in args.modules:
            globals()[m] = importlib.import_module(m)

    snippet = args.snippet.strip()
    f = command(f"({snippet})(_)") if args.function else command(snippet)

    if args.filter:
        f = filter(f)
    if args.map:
        f = map(f)

    out = f(input_stream)
    logging.debug(out)

    format_output = identity if isinstance(out, str) else format_sequence
    sys.stdout.write(format_output(out))


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(args))
