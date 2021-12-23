from collections import Counter, deque
from collections.abc import Iterable
from itertools import product, combinations
from re import match
from typing import NamedTuple, Optional

Triplet = tuple[int, int, int]


class Scanner(NamedTuple):
    id: int
    beacons: tuple[Triplet, ...]
    position: Optional[Triplet]


def gen_scanners(filename: str) -> Iterable[Scanner]:
    def gen_coordinates():
        for line0 in f:
            line0 = line0.rstrip()
            if line0 == "":
                return
            x, y, z = tuple(int(x) for x in line0.split(","))
            yield x, y, z

    with open(filename, "r") as f:
        for line in f:
            m = match(r"^--- scanner (\d+) ---$", line)
            if m:
                beacons = tuple(gen_coordinates())
                scanner_id = int(m.group(1))
                yield Scanner(int(m.group(1)), beacons, (0, 0, 0) if scanner_id == 0 else None)


def triplet_offset(a: tuple[int, int, int], b: tuple[int, int, int]) -> Triplet:
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def rotate_on_axis(triplet: tuple[int, int, int], axis: str, steps: int) -> Triplet:
    if steps == 0:
        return triplet
    a, b, c = triplet

    if axis == "y":
        a, b = b, a
    elif axis == "z":
        a, c = c, a

    if steps == 1:
        b, c = -c, b
    elif steps == 2:
        b, c = -b, -c
    elif steps == 3:
        b, c = c, -b

    if axis == "y":
        a, b = b, a
    elif axis == "z":
        a, c = c, a

    return a, b, c


def rotate(triplet: tuple[int, int, int], rotation: int):
    outer = rotation // 4
    if outer == 0:
        inner_axis = "y"
    elif outer == 1:
        inner_axis = "z"
        triplet = rotate_on_axis(triplet, "x", 1)
    elif outer == 2:
        inner_axis = "y"
        triplet = rotate_on_axis(triplet, "x", 2)
    elif outer == 3:
        inner_axis = "z"
        triplet = rotate_on_axis(triplet, "x", 3)
    elif outer == 4:
        inner_axis = "x"
        triplet = rotate_on_axis(triplet, "z", 1)
    elif outer == 5:
        inner_axis = "x"
        triplet = rotate_on_axis(triplet, "z", 3)
    else:
        raise ValueError()
    return rotate_on_axis(triplet, inner_axis, rotation % 4)


def analyse_scanner_pair(a: Scanner, b: Scanner, threshold: int = 12) -> Optional[Scanner]:
    for i in range(24):
        c = Counter()
        for ab, bb, in product(a.beacons, b.beacons):
            rotated = rotate(bb, i)
            offset = triplet_offset(ab, rotated)
            c[offset] += 1
        offset, how_common = c.most_common(1)[0]
        if how_common >= threshold:
            print(f"Found beacon offset for {b.id} at {offset}")
            moved = tuple(triplet_add(offset, rotate(x, i)) for x in b.beacons)
            return Scanner(b.id, moved, offset)


def gen_normalised_locations(scanners: tuple[Scanner], threshold: int = 12) -> Iterable[Scanner]:
    by_id = {s.id: s for s in scanners}
    unreached = set(s.id for s in scanners[1:])
    to_search = deque((scanners[0],))
    # since we align everyone to the first one, this one is already normalised
    yield scanners[0]
    while unreached and to_search:
        current = to_search.popleft()
        found = []
        for i in unreached:
            scanner = by_id[i]
            updated = analyse_scanner_pair(current, scanner, threshold)
            if updated is not None:
                found.append(updated)
                yield updated
        to_search += found
        for x in found:
            unreached.remove(x.id)
    if unreached:
        raise ValueError(f"failed to reach {unreached}")


def triplet_add(a: Triplet, b: Triplet) -> Triplet:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def gen_beacon_distances(updated: Iterable[Scanner]) -> Iterable[tuple[int, tuple[int, int]]]:
    for a, b in combinations(updated, 2):
        distance = sum(abs(x) for x in triplet_offset(a.position, b.position))
        yield distance, (a.id, b.id)


def solve():
    scanners = tuple(gen_scanners("input.txt"))
    updated = tuple(gen_normalised_locations(scanners, 12))

    triplets = {triplet for scanner in updated for triplet in scanner.beacons}
    print(len(triplets))

    longest_distance, between = sorted(gen_beacon_distances(updated))[-1]
    print(f"Found longest distance {longest_distance} between {between}")


if __name__ == "__main__":
    solve()
