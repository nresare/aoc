# advent of code 2015, day 18
import re
import string
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
    transforms = tuple(gen_transforms("input/day19.txt"))
    for a, b in transforms:
        if sum(1 for c in a if c in string.ascii_uppercase) != 1 and a != "e":
            raise ValueError(f"transform start {a} does not contain exactly one uppercase letter")
        validate_transform_target(b)

    # Now that we know that our transforms conform to this very specific set of requirements,
    # we know that we can calculate the number of transforms needed with this trick:
    y_count = sum(1 for x in find_all("Y", INPUT))

    upper_count = sum(1 for x in INPUT if x in string.ascii_uppercase)
    rn_count = sum(1 for x in find_all("Rn", INPUT))
    ar_count = sum(1 for x in find_all("Ar", INPUT))

    print(upper_count - rn_count - ar_count - (2 * y_count) - 1)


def find_all(needle: str, haystack: str) -> Iterator[int]:
    for i in range(len(haystack)):
        if is_at_pos(needle, haystack, i):
            yield i


def is_at_pos(needle: str, haystack: str, pos: int) -> bool:
    for i in range(len(needle)):
        if haystack[pos + i] != needle[i]:
            return False
    return True


def validate_transform_target(transform_target: str) -> None:
    if sum(1 for c in transform_target if c in string.ascii_uppercase) == 2:
        # first case, outputs two tokens
        return
    match = re.match(r"[A-Z][a-z]?Rn(.*)Ar$", transform_target)
    if match:
        in_parenthesis = match.group(1)
        if sum(1 for c in in_parenthesis if c in string.ascii_uppercase) == 1:
            # the [token]Rn[token]Ar construct
            return
        match = re.match(r"([A-Z][a-z]?Y){1,2}([A-Z][a-z]?)?$", in_parenthesis)
        if match:
            # the [token]Rn[token]Y[token]Ar construct
            return

    raise ValueError(f"This transform target doesn't conform: {transform_target}")


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
