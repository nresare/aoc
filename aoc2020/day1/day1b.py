# Advent of code 2020, day 1
from itertools import product
from typing import Iterator, Optional


def main():
    values = gen_values("input.txt")
    a, b, c = find_sequence(list(values), 2020)
    print(a * b * c)


def find_sequence(values: list[int], target_sum: int) -> tuple[int, int, int]:
    for a, b, c in product(values, values, values):
        if a == b or a == c or b == c:
            continue
        if a + b + c == target_sum:
            return a, b, c


def gen_values(filename: str) -> Iterator[int]:
    with open(filename, "r") as f:
        for line in f:
            yield int(line.rstrip())


if __name__ == "__main__":
    main()
