import sys
from collections.abc import Iterable
from typing import NamedTuple, Optional

Coords = tuple[int, int]


class TargetArea(NamedTuple):
    x_min: int
    x_max: int
    y_min: int
    y_max: int


def generate_sequence(x_velocity: int, y_velocity: int) -> Iterable[Coords]:
    x = y = 0
    while True:
        x += x_velocity
        y += y_velocity
        if x_velocity < 0:
            x_velocity += 1
        elif x_velocity > 0:
            x_velocity -= 1
        y_velocity -= 1
        yield x, y


def hits_target(target: TargetArea, x_velocity: int, y_velocity: int) -> Optional[int]:
    highest = -sys.maxsize
    for x, y in generate_sequence(x_velocity, y_velocity):
        if y > highest:
            highest = y
        # print(f"got {x},{y}")
        if x > target.x_max or y < target.y_min:
            return None
        if target.x_min <= x <= target.x_max and target.y_min <= y <= target.y_max:
            return highest
    return None


def solve():
    target = TargetArea(29, 73, -248, -194)
    # target = TargetArea(20, 30, -10, -5)
    highest = -sys.maxsize
    valid = []
    for x in range(0, 74):
        for y in range(-248, 1000):
            maybe_height = hits_target(target, x, y)
            if maybe_height is not None:
                # print(f"{x}, {y}: {maybe_height}")
                valid.append((x, y))
                if maybe_height > highest:
                    highest = maybe_height
    print(f"highest height: {highest}")
    print(f"number of distinct velocity pairs: {len(valid)}")
    for x, y in sorted(valid):
        print(f"{x}, {y}")


def dummy():
    target = TargetArea(20, 30, -10, -5)
    print(f"hits_target: {hits_target(target, 6, 0)}")


if __name__ == "__main__":
    solve()
    # dummy()
