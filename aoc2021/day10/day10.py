from collections.abc import Iterable
from collections import deque
from typing import Optional

PAIRS = {
    "{": "}",
    "(": ")",
    "[": "]",
    "<": ">",
}
LEFTS = set(PAIRS.keys())
RIGHTS = set(PAIRS.values())

CORRUPTION_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

COMPLETION_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

def gen_lines(filename: str) -> Iterable[str]:
    with open(filename, "r") as f:
        for line in f:
            yield line.rstrip()


def solve_part1(line: str) -> int:
    stack = deque()
    for i, c in enumerate(line):
        if c in LEFTS:
            stack.append(c)
        else:
            if c not in RIGHTS:
                raise ValueError(f"Found illegal character '{c}'")
            matching = PAIRS.get(stack.pop())
            if matching != c:
                # print(f"String {line} is corrupted at position {i}, expected {matching} but found {c}")
                return CORRUPTION_POINTS[c]
    return 0


def find_completion(line: str) -> Optional[str]:
    stack = deque()
    for i, c in enumerate(line):
        if c in LEFTS:
            stack.append(c)
        else:
            if c not in RIGHTS:
                raise ValueError(f"Found illegal character '{c}'")
            matching = PAIRS.get(stack.pop())
            if matching != c:
                return None
    return "".join(PAIRS[x] for x in reversed(stack))


def score_completion(completion: str) -> int:
    total = 0
    for c in completion:
        total *= 5
        total += COMPLETION_POINTS[c]
    return total


def solve(filename: str) -> None:
    print("Corruption score: {}".format(sum(solve_part1(x) for x in gen_lines(filename))))
    completions = (find_completion(x) for x in gen_lines(filename))
    scores = [score_completion(x) for x in completions if x is not None]
    if len(scores) % 2 != 1:
        raise ValueError("Expected odd number of scores")
    print("Completion score: {}".format(sorted(scores)[len(scores) // 2]))


if __name__ == "__main__":
    solve("input.txt")
