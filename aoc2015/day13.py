# advent of code 2015, day 13
import re
from itertools import permutations
from typing import Tuple, Iterator, Dict

PATTERN = re.compile(r"^(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).$")


def main():
    happiness = dict(gen_happiness("input/day13.txt"))
    print(find_happiest_placement(happiness))


def gen_happiness(filename: str) -> Iterator[Tuple[Tuple[str, str], int]]:
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            match = PATTERN.match(line)
            if not match:
                raise ValueError(f"could not parse line {line}")
            person_a, verb, amount, person_b = match.groups()
            yield (person_a, person_b), int(amount) if verb == "gain" else -int(amount)


def gen_people(happiness: Dict[Tuple[str, str], int]) -> Iterator[str]:
    for a, b in happiness.keys():
        yield a
        yield b


def gen_pairs(people: Tuple[str, ...]) -> Iterator[Tuple[str, str]]:
    for i in range(len(people)):
        if i + 1 == len(people):
            yield people[i], people[0]
        else:
            yield people[i], people[i + 1]


def get_happiness(pair: Tuple[str, str], happiness: Dict[Tuple[str, str], int]) -> int:
    return happiness[pair] + happiness[(pair[1], pair[0])]


def find_happiest_placement(happiness: Dict[Tuple[str, str], int]) -> int:
    best = 0
    for candidate in permutations(set(gen_people(happiness))):
        current = sum(get_happiness(pair, happiness) for pair in gen_pairs(candidate))
        print(f"testing {candidate} got {current}")
        if current > best:
            best = current
    return best


if __name__ == "__main__":
    main()
