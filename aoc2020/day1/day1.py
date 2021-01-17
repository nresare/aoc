# Advent of code 2020, day 1
from typing import Iterator, Optional


def main():
    values = sorted(gen_values("input.txt"))
    a, b = find_pair(values, 2020)
    print(a * b)


def find_pair(values: list[int], target_sum: int) -> tuple[int, int]:
    for i in range(len(values)):
        j = _inner(values, i, target_sum)
        if j:
            return values[i], values[j]
    raise ValueError("Failed to find pair in input")


def _inner(values: list[int], outer_offset: int, target_sum: int) -> Optional[int]:
    for j in range(len(values) - 1, -1, -1):
        if j <= outer_offset:
            raise ValueError("failed to find pair")
        candidate = values[outer_offset] + values[j]
        if candidate == target_sum:
            return j
        if candidate < target_sum:
            return None


def gen_values(filename: str) -> Iterator[int]:
    with open(filename, "r") as f:
        for line in f:
            yield int(line.rstrip())


if __name__ == "__main__":
    main()
