# advent of code 2015, day 17
from collections.abc import Iterator
from itertools import combinations


def main():
    containers = tuple(gen_containers("input/day17.txt"))
    print(sum(1 for x in gen_matches(containers) if sum(x) == 150))


def gen_matches(containers: tuple[int, ...]) -> Iterator[tuple[int, ...]]:
    for i in range(len(containers)):
        yield from combinations(containers, i)


def gen_containers(filename: str) -> Iterator[int]:
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            yield int(line)


if __name__ == "__main__":
    main()
