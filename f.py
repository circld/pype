#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from toolz.curried import *


def command(args):
    return lambda _: eval(" ".join(map(str.strip, args)))


def format_sequence(seq):
    return "\n".join(seq)


def identity(e):
    return e


if __name__ == "__main__":
    input_stream = map(str.strip, sys.stdin)
    f = command(sys.argv[1:])
    out = f(input_stream)
    format_output = identity if isinstance(out, str) else format_sequence
    sys.stdout.write(format_output(out))
