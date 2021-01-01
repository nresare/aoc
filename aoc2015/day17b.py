# advent of code 2015, day 17
from collections.abc import Iterator
from itertools import combinations


def main():
    containers = tuple(gen_containers("input/day17.txt"))
    print(run(containers))


def run(containers: tuple[int, ...]) -> int:
    for i in range(len(containers)):
        hits = hits_for_count(containers, i)
        if hits > 0:
            return hits


def hits_for_count(containers: tuple[int, ...], count: int) -> int:
    return sum(1 for x in combinations(containers, count) if sum(x) == 150)


def gen_containers(filename: str) -> Iterator[int]:
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            yield int(line)


if __name__ == "__main__":
    main()
