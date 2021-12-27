from collections import defaultdict
from re import match
from typing import NamedTuple, Iterable, Optional

Range = tuple[int, int]
Triplet = tuple[int, int, int]

# I got some help this time as well, from https://www.youtube.com/watch?v=zGS_-vC9UAQ


class Action(NamedTuple):
    on: bool
    x: Range
    y: Range
    z: Range


def gen_input(filename: str) -> Iterable[Action]:
    with open(filename, "r") as f:
        for line in f:
            parts = line.rstrip().split(" ")
            m = match(r"x=([\-\d]+)\.\.([\-\d]+),y=([\-\d]+)\.\.([\-\d]+),z=([\-\d]+)\.\.([\-\d]+)$", parts[1])
            if m is None:
                raise ValueError
            ints = tuple(int(i) for i in m.groups())
            yield Action(parts[0] == "on", (ints[0], ints[1]), (ints[2], ints[3]), (ints[4], ints[5]))


def gen_cubes(action: Action) -> Iterable[Triplet]:
    for x in range(min(action.x), max(action.x) + 1):
        for y in range(min(action.y), max(action.y) + 1):
            for z in range(min(action.z), max(action.z) + 1):
                yield x, y, z


def is_close(action: Action) -> bool:
    if max(action.x) < -50 or min(action.x) > 50:
        return False
    if max(action.y) < -50 or min(action.y) > 50:
        return False
    if max(action.z) < -50 or min(action.z) > 50:
        return False
    return True


def solve_part1(filename):
    cubes: set[Triplet] = set()
    for i, action in enumerate(gen_input(filename)):
        if not is_close(action):
            continue
        s = {c for c in gen_cubes(action)}
        if action.on:
            cubes |= s
        else:
            cubes -= s
        print(f"after action {i}: {len(cubes)}")
    return len(cubes)


def solve_part2(filename: str) -> int:
    counts = defaultdict(int)
    for action in gen_input(filename):

        to_add = defaultdict(int)

        for other in counts:
            overlap = overlap_cube(action, other)
            if overlap:
                # If we were counting other before, we count it in the other direction
                # in the overlap cube, to compensate for the double counting
                to_add[overlap] -= counts[other]

        if action.on:
            to_add[action] += 1

        for c in to_add:
            counts[c] += to_add[c]

    return sum(size(cube) * counts[cube] for cube in counts)


def overlap_cube(a: Action, b: Action) -> Optional[Action]:
    x = one_d_case(a.x, b.x)
    y = one_d_case(a.y, b.y)
    z = one_d_case(a.z, b.z)
    if range_size(x) == 0 or range_size(y) == 0 or range_size(z) == 0:
        return None
    return Action(a.on, one_d_case(a.x, b.x), one_d_case(a.y, b.y), one_d_case(a.z, b.z))


def one_d_case(first: Range, second: Range) -> Range:
    return max(min(first), min(second)), min(max(first), max(second))


def size(a: Action) -> int:
    return (a.x[1] - a.x[0] + 1) * (a.y[1] - a.y[0] + 1) * (a.z[1] - a.z[0] + 1)


def range_size(r: Range) -> int:
    return max(0, r[1] - r[0] + 1)


if __name__ == "__main__":
    # print(solve_part1("sample0.txt"))
    print(solve_part2("input.txt"))
