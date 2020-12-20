# advent of code 2015, day 1
import re
from typing import Dict

OUTSIDE_QUOTE = 0
IN_QUOTE = 1
AFTER_FIRST_BACKSLASH = 2
IN_HEX_ESCAPE = 3


def count_encoding_surplus(line: str) -> int:
    state = OUTSIDE_QUOTE
    ignore = 0
    post_parse_count = 0
    for i, c in enumerate(line):
        if state == IN_HEX_ESCAPE:
            if ignore == 1:
                post_parse_count += 1
                state = IN_QUOTE
            else:
                ignore = 1
        elif state == OUTSIDE_QUOTE:
            if c == '"':
                state = IN_QUOTE
            else:
                raise ValueError(f"Expected \" at pos {i} in line '{line}'")
        elif state == IN_QUOTE:
            if c == '"':
                state = OUTSIDE_QUOTE
            elif c == '\\':
                state = AFTER_FIRST_BACKSLASH
            else:
                post_parse_count += 1

        elif state == AFTER_FIRST_BACKSLASH:
            if c == 'x':
                state = IN_HEX_ESCAPE
                ignore = 2
            else:
                post_parse_count += 1
                state = IN_QUOTE
    return len(line) - post_parse_count


def main():
    with open("input/day8.txt", "r") as f:
        print(sum(count_encoding_surplus(line.rstrip()) for line in f))


if __name__ == "__main__":
    main()
