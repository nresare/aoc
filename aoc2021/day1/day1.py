# Advent of code 2021, day 1

from typing import Iterator


def count_increments(depths: Iterator[int]) -> int:
    previous = 0
    count = 0
    for depth in depths:
        if depth > previous:
            count += 1
        previous = depth
    return count - 1


def gen_sliding_window_sums(depths: Iterator[int]) -> Iterator[int]:
    first = 0
    second = 0

    for depth in depths:
        if depth and first and second:
            yield sum((depth, first, second))
        second = first
        first = depth


def gen_values(filename: str) -> Iterator[int]:
    with open(filename, "r") as f:
        for line in f:
            yield int(line)


if __name__ == "__main__":
    # print(count_increments(gen_values("input.txt")))
    print(count_increments(gen_sliding_window_sums(gen_values("input.txt"))))

