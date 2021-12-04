# Advent of code 2021, day 3

from collections.abc import Iterator, Callable


def solve(filename: str) -> int:
    first, second = part2(tuple(gen_binaries(filename)))
    return first * second


def part2(to_handle: tuple[str]) -> tuple[int, int]:
    values = tuple(to_handle)
    pos = 0
    while len(values) > 1:
        values = filter_on_digit(values, pos, oxygen_rating)
        if len(values) == 1:
            break
        pos += 1
    oxygen = int(values[0], 2)

    pos = 0
    values = tuple(to_handle)
    while len(values) > 1:
        values = filter_on_digit(values, pos, co2_rating)
        pos += 1
    co2 = int(values[0], 2)

    return oxygen, co2


def filter_on_digit(lines: tuple[str], pos: int, criteria: Callable[int, int, str]) -> tuple[str]:
    count = 0
    for line in lines:
        if line[pos] == "1":
            count += 1
    return tuple(line for line in lines if line[pos] == criteria(count, len(lines)))


def co2_rating(found: int, total: int) -> str:
    if found == total / 2:
        return "0"
    return "0" if found > total // 2 else "1"


def oxygen_rating(found: int, total: int) -> str:
    if found == total / 2:
        return "1"
    return "1" if found > total // 2 else "0"


def part1(values: Iterator[str]) -> tuple[int, int]:
    lines_seen = 0
    one_counts = None
    for line in values:
        lines_seen += 1
        if one_counts is None:
            one_counts = [int(x) for x in line]
            continue
        for pos, digit in enumerate(line):
            if digit == "1":
                one_counts[pos] += 1
    gamma_binary = "".join("1" if x > lines_seen // 2 else "0" for x in one_counts)
    epsilon_binary = "".join("0" if x > lines_seen // 2 else "1" for x in one_counts)

    return int(epsilon_binary, 2), int(gamma_binary, 2)


def gen_binaries(filename: str) -> Iterator[str]:
    with open(filename, "r") as f:
        for line in f:
            yield line.rstrip()


if __name__ == "__main__":
    print(solve("input.txt"))
