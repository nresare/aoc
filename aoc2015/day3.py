# advent of code 2015, day 3
from collections.abc import Set
from typing import Tuple


def main():
    with open("input/day3.txt", "r") as f:
        directions: str = f.read()
        directions = directions.rstrip()
    print(count_presents(directions))


def count_presents(directions: str) -> int:
    houses: Set[Tuple[int, int]] = set()
    # the current location
    x = y = 0
    houses.add((x, y))
    for direction in directions:
        if direction == "^":
            y += 1
        elif direction == "v":
            y -= 1
        elif direction == ">":
            x += 1
        elif direction == "<":
            x -= 1
        else:
            raise ValueError(f"Unknown symbol {direction}")
        houses.add((x, y))
    return len(houses)


if __name__ == "__main__":
    main()
