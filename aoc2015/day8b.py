# advent of code 2015, day 1
import re
from typing import Dict

OUTSIDE_QUOTE = 0
IN_QUOTE = 1
AFTER_FIRST_BACKSLASH = 2
IN_HEX_ESCAPE = 3


def gen_encoded_string(line: str) -> int:
    for c in line:
        if c == '"':
            yield '\\"'
        elif c == '\\':
            yield '\\\\'
        else:
            yield c


def encoded_length_minus_string_length(line: str) -> int:
    return sum(len(x) for x in gen_encoded_string(line)) + 2 - len(line)


def main():
    with open("input/day8.txt", "r") as f:
        print(sum(encoded_length_minus_string_length(line.rstrip()) for line in f))


if __name__ == "__main__":
    main()
