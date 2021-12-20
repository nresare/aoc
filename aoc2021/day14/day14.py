from collections import Counter
from itertools import tee
from timeit import default_timer
from typing import NamedTuple, Iterable, IO


class Input(NamedTuple):
    start: str
    rules: dict[tuple[str, str], str]


def get_input(filename: str) -> Input:
    def gen_rules(file: IO) -> Iterable[tuple[tuple[str, str], str]]:
        for line in file:
            line = line.rstrip()
            parts = line.split(" -> ")
            yield tuple(parts[0]), parts[1]

    with open(filename, "r") as f:
        start = next(f).rstrip()
        next(f)
        return Input(start=start, rules=dict(gen_rules(f)))


def pairwise(iterable):
    # copied from https://docs.python.org/3.9/library/itertools.html
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Solver(object):
    def __init__(self, rules: dict[tuple[str, str], str]):
        self.rules = rules
        self.memo: dict[tuple[tuple[str, str], int], Counter] = {}

    def count_pair(self, pair: tuple[str, str], depth: int) -> Counter:
        memoized = self.memo.get((pair, depth))
        if memoized:
            return memoized
        counter = Counter()
        subst = self.rules.get(pair)
        if depth == 0 or subst is None:
            counter[pair[0]] += 1
        else:
            counter += self.count_pair((pair[0], subst), depth - 1)
            counter += self.count_pair((subst, pair[1]), depth - 1)
        self.memo[(pair, depth)] = counter
        return counter

    def solve(self, start: str, steps: int) -> int:
        c = Counter()
        for a, b in pairwise(start):
            c += self.count_pair((a, b), steps)
        c[start[-1]] += 1
        print(f"After running the memo has size {len(self.memo)}")
        frequencies = c.most_common(len(c))
        return frequencies[0][1] - frequencies[-1][1]


def solve(filename: str):
    i = get_input(filename)
    before = default_timer()
    s = Solver(i.rules)
    counts = s.solve(i.start, 40)
    after = default_timer()

    print(counts)
    print(f"Time taken {after - before}s")


if __name__ == "__main__":
    solve("input.txt")
