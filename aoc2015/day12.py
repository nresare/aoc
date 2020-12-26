# advent of code 2015, day 12
from typing import IO, Iterator


def main():
    with open("input/day12.txt", "r") as f:
        print(sum(gen_numbers(f)))


OUTSIDE_NUMBER = 1
IN_NUMBER = 2
NUMBER_CHARS = "-1234567890"


def gen_numbers(file: IO) -> Iterator[int]:
    for line in file:
        yield from gen_numbers_from_line(line)


def gen_numbers_from_line(line: str) -> Iterator[int]:
    number_start = None

    state = OUTSIDE_NUMBER
    for i, c in enumerate(line):
        if state == OUTSIDE_NUMBER:
            if c in NUMBER_CHARS:
                number_start = i
                state = IN_NUMBER
        if state == IN_NUMBER:
            if c not in NUMBER_CHARS:
                yield int(line[number_start:i])
                state = OUTSIDE_NUMBER
                number_start = None
    if number_start is not None:
        yield int(line[number_start:])


if __name__ == "__main__":
    main()
