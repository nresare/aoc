# advent of code 2020, day 3
from typing import Iterator


def main():
    matrix = tuple(gen_input_rows("input.txt"))
    line_lengths = set(len(x) for x in matrix)
    # verify that all lines are of the same length
    assert len(line_lengths) == 1
    line_length = next(iter(line_lengths))
    print("a:", count(gen_values(matrix, line_length, (3, 1))))
    total = 1
    for path in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        total *= count(gen_values(matrix, line_length, path))
    print("b:", total)


def count(booleans: Iterator[bool]) -> int:
    return sum(1 for i in booleans if i)


def gen_values(matrix: [tuple, [tuple[bool, ...], ...]], line_length: int, path: tuple[int, int]) -> Iterator[bool]:
    right, down = path
    x = 0
    y = 0
    for y in range(0, len(matrix), down):
        value = matrix[y][x % line_length]
        yield value
        x += right


def gen_input_rows(filename: str) -> Iterator[tuple[bool, ...]]:
    with open(filename, "r") as f:
        for line in (x.rstrip() for x in f):
            yield tuple(x == "#" for x in line)


if __name__ == "__main__":
    main()
