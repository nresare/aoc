from collections.abc import Iterator
from typing import Optional


def main():
    print("a:", sum(len(s) for s in gen_groups_a("input.txt")))
    print("b:", sum((len(s) for s in gen_groups_b("input.txt"))))


def gen_groups_a(filename: str) -> Iterator[set[str]]:
    group: set[str] = set()
    with open(filename, "r") as f:
        for line in (set(x.rstrip()) for x in f):
            if not line:
                yield group
                group = set()
            group |= line
    yield group


def gen_groups_b(filename: str) -> Iterator[set[str]]:
    group: Optional[set[str]] = None
    with open(filename, "r") as f:
        for line in (set(x.rstrip()) for x in f):
            if not line:
                yield group
                group = None
            elif group is None:
                # the group is empty, it means that we add all the characters in the first line
                group = line
            else:
                group &= line
    yield group


if __name__ == "__main__":
    main()
