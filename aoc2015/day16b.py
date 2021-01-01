# advent of code 2015, day 16
import re
from typing import Dict, Iterator, Tuple, NamedTuple

BASE_PATTERN = re.compile(r"^Sue (\d+): (.*)$")


class Memories(NamedTuple):
    sue: int
    memories: Dict[str, int]


def main():
    sue_memories = tuple(gen_memories("input/day16.txt"))
    for fact in gen_facts("input/day16facts.txt"):
        sue_memories = tuple(x for x in sue_memories if should_remain(fact, x.memories))
    print(sue_memories)


def should_remain(fact: Tuple[str, int], memories: Dict[str, int]) -> bool:
    key, value = fact
    if key in ("cats", "trees"):
        if key in memories and memories[key] <= value:
            return False
    elif key in ("pomeranians", "goldfish"):
        if key in memories and memories[key] >= value:
            return False
    elif key in memories and memories[key] != value:
        return False
    return True


def gen_memories(filename: str) -> Iterator[Memories]:
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            m = BASE_PATTERN.match(line)
            if not m:
                raise ValueError(f"Could not parse line {line}")
            yield Memories(int(m.group(1)), dict(gen_kvs(m.group(2))))


def gen_kvs(pairs: str) -> Iterator[Tuple[str, int]]:
    for pair in pairs.split(", "):
        key, value = pair.split(": ")
        yield key, int(value)


def gen_facts(filename: str) -> Iterator[Tuple[str, int]]:
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            key, value = line.split(": ")
            yield key, int(value)


if __name__ == "__main__":
    main()
