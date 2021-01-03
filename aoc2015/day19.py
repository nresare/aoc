# advent of code 2015, day 18
import re
from collections.abc import Iterator

TRANSFORM_PATTERN = re.compile(r"^(\w+) => (\w+)$")

INPUT = (
    "ORnPBPMgArCaCaCaSiThCaCaSiThCaCaPBSiRnFArRnFArCaCaSiThCaCaSiThCaCaCaCaCaC"
    "aSiRnFYFArSiRnMgArCaSiRnPTiTiBFYPBFArSiRnCaSiRnTiRnFArSiAlArPTiBPTiRnCaSiAlArCaPTiTi"
    "BPMgYFArPTiRnFArSiRnCaCaFArRnCaFArCaSiRnSiRnMgArFYCaSiRnMgArCaCaSiThPRnFArPBCaSiRnMg"
    "ArCaCaSiThCaSiRnTiMgArFArSiThSiThCaCaSiRnMgArCaCaSiRnFArTiBPTiRnCaSiAlArCaPTiRnFArPB"
    "PBCaCaSiThCaPBSiThPRnFArSiThCaSiThCaSiThCaPTiBSiRnFYFArCaCaPRnFArPBCaCaPBSiRnTiRnFAr"
    "CaPRnFArSiRnCaCaCaSiThCaRnCaFArYCaSiRnFArBCaCaCaSiThFArPBFArCaSiRnFArRnCaCaCaFArSiRn"
    "FArTiRnPMgArF"
)


def main():
    print(find_distinct_result_count(INPUT, tuple(gen_transforms("input/day19.txt"))))


def find_distinct_result_count(start: str, transforms: tuple[tuple[str, str]]) -> int:
    distinct_results = set()
    for a, b in transforms:
        for pos in find_all(a, start):
            distinct_results.add(start[:pos] + b + start[pos + len(a):])
    return len(distinct_results)


def find_all(needle: str, haystack: str) -> Iterator[int]:
    for i in range(len(haystack)):
        if is_at_pos(needle, haystack, i):
            yield i


def is_at_pos(needle: str, haystack: str, pos: int) -> bool:
    for i in range(len(needle)):
        if haystack[pos + i] != needle[i]:
            return False
    return True


def gen_transforms(filename: str) -> Iterator[tuple[str, str]]:
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            match = TRANSFORM_PATTERN.match(line)
            if not match:
                raise ValueError(f"Could not parse line {i + 1}: {line}")
            yield match.groups()


if __name__ == "__main__":
    main()
