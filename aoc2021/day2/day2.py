# Advent of code 2021, day 1
from typing import Tuple, Iterator


def solve(filename: str) -> int:
    depth, horizontal = find_position_part2(gen_input(filename))
    return depth * horizontal


def find_position_part1(moves: Iterator[Tuple[str, int]]) -> Tuple[int, int]:
    depth = 0
    horizontal = 0
    for action, magnitude in moves:
        if action == "forward":
            horizontal += magnitude
        elif action == "down":
            depth += magnitude
        elif action == "up":
            depth -= magnitude
    return horizontal, depth


def find_position_part2(moves: Iterator[Tuple[str, int]]) -> Tuple[int, int]:
    aim = depth = horizontal = 0
    for action, magnitude in moves:
        if action == "forward":
            horizontal += magnitude
            depth += aim * magnitude
        elif action == "down":
            aim += magnitude
        elif action == "up":
            aim -= magnitude
    return horizontal, depth


def gen_input(filename: str) -> Iterator[Tuple[str, int]]:
    with open(filename, "r") as f:
        for line in f:
            parts = line.split(" ")
            yield parts[0], int(parts[1])


if __name__ == "__main__":
    print(solve("input.txt"))
