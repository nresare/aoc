from re import match
from typing import NamedTuple, IO, Iterable

Paper = tuple[tuple[bool, ...]]


class FileContents(NamedTuple):
    coordinates: tuple[tuple[int, int], ...]
    folds: tuple[tuple[str, int], ...]


def read_file(filename: str) -> FileContents:
    def coords(file: IO) -> Iterable[tuple[int, int]]:
        for line in file:
            line = line.rstrip()
            if line == "":
                return
            ints = tuple(int(x) for x in line.split(","))
            yield ints[0], ints[1]

    def folds(file: IO) -> Iterable[tuple[str, int]]:
        for line in file:
            line = line.rstrip()
            m = match(r"fold along ([xy])=(\d+)", line)
            yield m.group(1), int(m.group(2))

    with open(filename, "r") as f:
        contents = FileContents(
            coordinates=(tuple(coords(f))),
            folds=(tuple(folds(f)))
        )
        return contents


def print_coordinates(coordinates: Iterable[tuple[int, int]]) -> None:
    coordinates = tuple(coordinates)
    max_y = max(i[0] for i in coordinates)
    max_x = max(i[1] for i in coordinates)

    rows = [[False] * (max_y + 1) for _ in range(max_x + 1)]

    for x, y in coordinates:
        rows[y][x] = True

    for row in rows:
        print("".join("#" if x else "." for x in row))


def fold(coordinates: Iterable[tuple[int, int]], direction: str, at: int) -> Iterable[tuple[int, int]]:
    if direction == "y":
        for x, y in coordinates:
            if y > at:
                y = at + at - y
            yield x, y
    if direction == "x":
        for x, y in coordinates:
            if x > at:
                x = at + at - x
            yield x, y


def part_1(c: FileContents) -> int:
    direction, at = c.folds[0]
    coordinates = fold(c.coordinates, direction, at)
    return len(set(coordinates))


def solve(filename: str):
    c = read_file(filename)

    print(f"Part 1 solution: {part_1(c)}")

    coordinates = c.coordinates
    for direction, at in c.folds:
        coordinates = fold(coordinates, direction, at)

    print_coordinates(coordinates)


if __name__ == "__main__":
    solve("input.txt")
