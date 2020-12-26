# advent of code 2015, day 14
import re
from typing import Iterator

PATTERN = re.compile(r"^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$")


class Reindeer(object):
    def __init__(self, line):
        match = PATTERN.match(line)
        if not match:
            raise ValueError(f"Could not parse {line}")
        self.name = match.group(1)
        self.speed = int(match.group(2))
        self.endurance = int(match.group(3))
        self.rest = int(match.group(4))
        self.star_count = 0

    def distance_at_time(self, duration: int) -> int:
        return sum(self.gen_distances(duration))

    def gen_distances(self, duration: int) -> Iterator[int]:
        while duration > 0:
            if duration > self.endurance:
                duration -= self.endurance
                yield self.endurance * self.speed
                duration -= self.rest
            else:
                yield self.speed * duration
                duration = 0

    def award(self):
        self.star_count += 1


def main():
    reindeers = tuple(gen_reindeers("input/day14.txt"))
    for i in range(1, 2503 + 1):
        results = tuple((x, x.distance_at_time(i)) for x in reindeers)
        best = max(x[1] for x in results)
        for reindeer, result in results:
            if result == best:
                reindeer.award()

    for r in reindeers:
        print(f"{r.name} {r.star_count}")
    print(max(r.star_count for r in reindeers))

def gen_reindeers(filename: str) -> Iterator[Reindeer]:
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            yield Reindeer(line)


if __name__ == "__main__":
    main()
