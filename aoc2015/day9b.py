# advent of code 2015, day 9
import re
from itertools import permutations
from typing import Dict, Tuple, Set, Iterator, Sequence

DISTANCE_PATTERN = re.compile(r"^(\w+) to (\w+) = (\d+)$")


def gen_pairs(cities: Sequence[str]) -> Iterator[Tuple[str, str]]:
    prev = None
    for city in cities:
        if prev:
            yield prev, city
        prev = city


def main():
    distances: Dict[Tuple[str, str], int] = {}
    cities: Set[str] = set()
    with open("input/day9.txt", "r") as f:
        for line in f:
            match = DISTANCE_PATTERN.match(line.rstrip())
            if not match:
                raise ValueError(f"could not parse line {line}")
            a = match.group(1)
            b = match.group(2)
            distance = int(match.group(3))
            cities.add(a)
            cities.add(b)
            distances[_to_key(a, b)] = distance

    for city_pair, distance in distances.items():
        print(city_pair, distance)

    largest = 0
    for i, city_tuple in enumerate(permutations(cities)):

        total = sum(distances[_to_key(a, b)] for a, b in gen_pairs(city_tuple))
        if total > largest:
            largest = total
        if not i % 100:
            print(f"checking permutation {i}: {total}")
    print(f"largest: {largest}")


def _to_key(a: str, b: str) -> Tuple[str, str]:
    if a < b:
        return a, b
    else:
        return b, a


if __name__ == "__main__":
    main()
