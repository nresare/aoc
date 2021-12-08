from collections import Counter
from typing import Iterator, NamedTuple, Sized

ALL_SEGMENTS = "abcdefg"


class Display(NamedTuple):
    configuration: tuple[str, ...]
    digits: tuple[str, ...]


SEGMENTS = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


def a_maps_to(configuration: tuple[str, ...]) -> str:
    one = next(x for x in configuration if len(x) == 2)
    seven = next(x for x in configuration if len(x) == 3)
    # the one in 7 that is not in 1 is 'a'
    difference = [x for x in seven if x not in one]
    if len(difference) != 1:
        raise ValueError(f"invalid configuration: {configuration}")
    return difference[0]

# the two in 4 not in 1 are b and d
# the missing ones in 9, 6, 0 are e, c, d


# if we calculate the ones missing from the ones with one missing,
#   the one in this set that also exist in 4 and not in 1 is 'd'

def gen_missing_in_690(configuration: tuple[str, ...]) -> Iterator[tuple[str, str]]:
    for x in configuration:
        if len(x) != 6:
            continue
        for l in ALL_SEGMENTS:
            if l not in x:
                yield l, x


def find_2(configuration: tuple[str, ...], f_segment: str) -> str:
    for x in configuration:
        if len(x) != 5:
            continue
        if f_segment not in x:
            return x


def find_segment_b(digit_2: str, segment_f: str) -> str:
    for s in ALL_SEGMENTS:
        if s not in digit_2 and s != segment_f:
            return s


def build_translation(configuration: tuple[str, ...]) -> dict[str, str]:
    digits = {
        1: next(x for x in configuration if len(x) == 2),
        7: next(x for x in configuration if len(x) == 3),
        4: next(x for x in configuration if len(x) == 4),
        8: next(x for x in configuration if len(x) == 7),
    }
    mapping = {"a": a_maps_to(configuration)}

    in_4_but_not_1 = tuple(x for x in digits[4] if x not in digits[1])
    missing_in_690 = tuple(gen_missing_in_690(configuration))

    # looking at the missing segments in 6, 9 and 0
    for missing, digit in missing_in_690:
        if missing in in_4_but_not_1:
            mapping["d"] = missing
            digits[0] = digit
        elif missing in digits[1]:
            mapping["c"] = missing
            digits[6] = digit
        else:
            mapping["e"] = missing
            digits[9] = digit

    # We know which segment of 1 that is also part of 6 (segment c)
    # the other one is segment f
    mapping["f"] = next(x for x in digits[1] if x != mapping["c"])

    # of the 5 segment digits, the one where segment f is missing
    # is 2. The other missing segment is b
    digits[2] = find_2(configuration, mapping["f"])

    # the segment missing from 2 that is not segment f, is segment b
    mapping["b"] = find_segment_b(digits[2], mapping["f"])

    mapping["g"] = next(x for x in ALL_SEGMENTS if x not in mapping.values())

    # for num, code in sorted(digits.items()):
    #     print(f"{num}: {code}")
    #
    # print("Mappings:")
    # for before, after in sorted(mapping.items()):
    #     print(f"{before}: {after}")
    return {v: k for k, v in mapping.items()}


def solve_part1(filename: str) -> int:
    return sum(gen_digits_with_unique_lengths(gen_displays(filename)))


def gen_digits_with_unique_lengths(gen: Iterator[Display]) -> Iterator[int]:
    for display in gen:
        yield sum(1 for x in display.digits if len(x) in (2, 3, 4, 7))


def gen_displays(filename: str) -> Iterator[Display]:
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            split_by_pipes = line.split(" | ")
            configs = tuple("".join(sorted(x)) for x in split_by_pipes[0].split(" "))
            digits = tuple("".join(sorted(x)) for x in split_by_pipes[1].split(" "))
            yield Display(configs, digits)


def print_stats():
    c = Counter()
    segments: Sized
    for num, segments in SEGMENTS.items():
        c[len(segments)] += 1
        # print(f"{num} {len(segments)}")
    for i in sorted(c):
        print(f"{i}: {c[i]}")


def parse_digits(translation: dict[str, str], digits: tuple[str, ...]) -> int:
    def inner():
        for d in digits:
            translated = "".join(sorted(translation[c] for c in d))
            # print(f"{translated} maps to {SEGMENTS[translated]}")
            yield SEGMENTS[translated]
    s = "".join(str(inner()))
    return int("".join(str(x) for x in inner()), 10)


def solve_part2(filename: str) -> Iterator[int]:
    for display in gen_displays(filename):
        translation = build_translation(display.configuration)
        value = parse_digits(translation, display.digits)
        print(f"{display.digits}: {value}")
        yield value


if __name__ == "__main__":
    # print_stats()
    # print(solve_part1("input.txt"))
    print(sum(solve_part2("input.txt")))
