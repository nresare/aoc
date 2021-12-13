import operator
from collections import Counter
from functools import reduce
from typing import Iterator, Optional

HeightMap = tuple[tuple[int, ...], ...]


def build_height_map(filename: str) -> HeightMap:
    with open(filename, "r") as f:
        return tuple(tuple(int(c) for c in line.rstrip()) for line in f)


def valid_coordinate(x: int, y: int, height_map: HeightMap) -> Optional[int]:
    if x < 0 or y < 0:
        return False
    if x >= len(height_map) or y >= len(height_map[x]):
        return False
    return True


def gen_coordinates(height_map: HeightMap) -> Iterator[tuple[int, int]]:
    for i, row in enumerate(height_map):
        for j in range(len(row)):
            yield i, j


def gen_neighbours(height_map: HeightMap, x: int, y: int) -> Iterator[tuple[int, int]]:
    for xy in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
        if valid_coordinate(xy[0], xy[1], height_map):
            yield xy


def is_low_point(xy: tuple[int, int], height_map: HeightMap) -> Optional[tuple[int, int]]:
    value = height_map[xy[0]][xy[1]]
    for neighbour in gen_neighbours(height_map, xy[0], xy[1]):
        if height_map[neighbour[0]][neighbour[1]] <= value:
            return None
    return xy


def to_string(item: int, x: int, y: int, low_points: set[tuple[int, int]]):
    return str(item) if (x, y) not in low_points else f"\u001b[31m{item}\u001b[0m"


def print_map(height_map: HeightMap, low_points: set[tuple[int, int]]) -> None:
    for x, row in enumerate(height_map):
        print("".join(to_string(item, x, y, low_points) for y, item in enumerate(row)))


def solve_part1(filename: str):
    height_map = build_height_map(filename)
    low_points = set(x for x in (is_low_point(xy, height_map) for xy in gen_coordinates(height_map)) if x is not None)
    print_map(height_map, low_points)
    print(sum(height_map[xy[0]][xy[1]] + 1 for xy in low_points))
    # print(sum(x + 1 for x in low_points if x is not None))


def expand_area(height_map: HeightMap, visited: list[list[int]], xy: tuple[int, int], i: int):
    x, y = xy
    if visited[x][y] != 0:
        # someone was already here
        return
    if height_map[x][y] == 9:
        # nines are never part of an area
        return
    visited[x][y] = i
    for neighbour in gen_neighbours(height_map, x, y):
        expand_area(height_map, visited, neighbour, i)


def solve_part2(filename: str):
    height_map = build_height_map(filename)
    low_points = set(x for x in (is_low_point(xy, height_map) for xy in gen_coordinates(height_map)) if x is not None)
    visited = [[0] * len(height_map[0]) for _ in range(len(height_map))]
    for i, (x, y) in enumerate(low_points):
        expand_area(height_map, visited, (x, y), i+1)

    c = Counter()
    for row in visited:
        for item in row:
            c[item] += 1

    print(reduce(operator.mul, (sorted(c.values(), reverse=True)[1:4])))


if __name__ == "__main__":
    solve_part2("input.txt")
