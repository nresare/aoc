# advent of code 2015, day 5
from typing import IO, Iterator

FORBIDDEN_PAIRS = ("ab", "cd", "pq", "xy")


def main():
    with open("input/day5.txt", "r") as f:
        print(sum(1 for x in line_generator(f) if is_nice(x)))


def line_generator(file: IO) -> Iterator[str]:
    for line in file:
        yield line.rstrip()


def is_nice(code: str) -> bool:
    if count_vowels(code) < 3:
        return False
    if not has_repeated(code):
        return False
    for pair in FORBIDDEN_PAIRS:
        if pair in code:
            return False
    return True


def count_vowels(code: str) -> int:
    return sum(1 for x in code if x in "aeiou")


def has_repeated(code: str) -> bool:
    previous = None
    for c in code:
        if c == previous:
            return True
        previous = c
    return False


if __name__ == "__main__":
    main()
