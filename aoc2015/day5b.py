# advent of code 2015, day 5
from typing import IO, Iterator, Tuple, Dict


def main():
    with open("input/day5.txt", "r") as f:
        print(sum(1 for x in line_generator(f) if is_nice(x)))


def line_generator(file: IO) -> Iterator[str]:
    for line in file:
        yield line.rstrip()


def is_nice(code: str) -> bool:
    if not has_repeating_pairs(code):
        return False
    if not second_rule(code):
        return False
    return True


def second_rule(code: str) -> bool:
    for i, char in enumerate(code):
        if i + 2 >= len(code):
            return False
        if code[i+2] == char:
            return True
    return False


def has_repeating_pairs(code: str) -> bool:
    positions: Dict[str, int] = {}
    for pos, pair in all_pairs(code):
        if pair in positions:
            if pos - positions[pair] > 1:
                return True
        else:
            positions[pair] = pos
    return False


def all_pairs(code: str) -> Iterator[Tuple[int, str]]:
    for i in range(len(code)):
        if i >= len(code) - 1:
            return
        yield i, code[i:i+2]


if __name__ == "__main__":
    main()
