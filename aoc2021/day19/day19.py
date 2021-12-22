from collections import Counter, deque, defaultdict
from collections.abc import Iterable
from itertools import product
from re import match
from typing import NamedTuple

Triplet = tuple[int, int, int]


class Scanner(NamedTuple):
    beacons: tuple[Triplet, ...]
    id: int


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
                yield Scanner(beacons, int(m.group(1)))


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


class Result(NamedTuple):
    reference: int
    target: int
    offset: Triplet
    rotation: int


def analyse_scanner_pair(a: Scanner, b: Scanner, threshold: int = 12) -> Result:
    for i in range(24):
        c = Counter()
        for ab, bb, in product(a.beacons, b.beacons):
            rotated = rotate(bb, i)
            offset = triplet_offset(ab, rotated)
            c[offset] += 1
        offset, how_common = c.most_common(1)[0]
        if how_common >= threshold:
            return Result(a.id, b.id, offset, i)


def gen_scanner_locations(scanners: tuple[Scanner], threshold: int = 12) -> Result:
    unreached = set(scanners[1:])
    to_search = deque((scanners[0],))
    while unreached and to_search:
        current = to_search.popleft()
        found = []
        for scanner in unreached:
            result = analyse_scanner_pair(current, scanner, threshold)
            if result is not None:
                found.append(scanner)
                yield result
        to_search += found
        unreached = unreached.difference(found)
    if unreached:
        raise ValueError(f"failed to reach {unreached}")


def translate(triplet: Triplet, offset: Triplet, rotation) -> Triplet:
    x, y, z = rotate(triplet, rotation)
    return x + offset[0], y + offset[1], z + offset[2]


def convert(beacons: Iterable[Triplet], offset: Triplet, rotation: int) -> Iterable[Triplet]:
    for beacon in beacons:
        yield translate(beacon, offset, rotation)


def triplet_add(a: Triplet, b: Triplet) -> Triplet:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def gen_converted_beacons(beacons: tuple[Triplet], path: tuple[Result, ...]):
    beacon_offset = 0, 0, 0
    for i in range(len(path)):
        result = path[i]
        beacons = convert(beacons, result.offset, result.rotation)
        to_add_to_offset = result.offset
        if i > 0:
            to_rotate = path[i - 1].rotation
            to_add_to_offset = rotate(to_add_to_offset, to_rotate)
        beacon_offset = triplet_add(beacon_offset, to_add_to_offset)
    print(f"beacon_offset: {beacon_offset}")
    yield from beacons


def walk(current: int, by_reference: dict[int, Result], scanners: dict[int, Scanner], path: tuple[Result, ...] = ()):
    targets = by_reference.get(current, ())
    print(f"visiting {current}, path: {path}")
    yield from gen_converted_beacons(scanners[current].beacons, path)
    for i in targets:
        yield from walk(i.target, by_reference, scanners, path=path + (i,))


def solve():
    scanners = tuple(gen_scanners("sample.txt"))
    results = tuple(gen_scanner_locations(scanners, 12))

    scanners_by_id = {s.id: s for s in scanners}
    by_reference = defaultdict[int, Result](list)
    for i in results:
        by_reference[i.reference].append(i)

    normalised_beacons = set(walk(0, by_reference, scanners_by_id))

    for triplet in sorted(normalised_beacons):
        print(triplet)
    print(len(normalised_beacons))


if __name__ == "__main__":
    solve()
