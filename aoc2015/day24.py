import sys
from collections import deque
from collections.abc import Iterator
from typing import Iterable


def gen_weights(filename: str) -> Iterator[int]:
    with open(filename, "r") as f:
        for line in f:
            yield int(line)


Sizes = tuple[int, ...]


def main():
    weights = tuple(gen_weights("input/day24.txt"))
    if len(set(weights)) < len(weights):
        raise ValueError("This algo assumes unique sizes")
    if sum(weights) % 3:
        raise ValueError("weights is not evenly divisible into 3 equal sizes")
    target = sum(weights) // 3
    print("shortest combinations: ")
    cg = CombinationGenerator(target, weights)
    smallest = sys.maxsize
    print(min(get_qe(x) for x in cg.gen_combinations()))


def get_qe(sizes: Sizes) -> int:
    result = 1
    for size in sizes:
        result *= size
    return result


class CombinationGenerator(object):
    def __init__(self, target_sum: int, weights: Iterable[int]):
        self.weights = sorted(weights)
        self.target_sum = target_sum
        self.shortest_length = 0
        self.to_visit: deque[Sizes] = deque()

    def gen_combinations(self) -> Iterator[Sizes]:
        for weight in self.weights:
            if weight < self.target_sum:
                self.to_visit.appendleft((weight,))
        while self.to_visit:
            yield from self._inner()

    def _inner(self) -> Iterator[Sizes]:
        base = self.to_visit.pop()
        so_far = sum(base)
        for weight in self.weights:
            if weight > base[-1]:
                # only add numbers that are smaller than the currently last added
                break
            elif weight == base[-1]:
                # Don't add the same weight twice
                continue
            if so_far + weight > self.target_sum:
                break
            elif so_far + weight < self.target_sum:
                # since we are only interested in the shortest ones, as soon as we find something
                # we stop appending to to_visit
                if not self.shortest_length:
                    self.to_visit.appendleft(base + (weight,))
            elif so_far + weight == self.target_sum:
                if not self.shortest_length:
                    self.shortest_length = len(base) + 1
                if len(base) + 1 == self.shortest_length:
                    yield base + (weight,)


if __name__ == "__main__":
    main()
