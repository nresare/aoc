import re
from collections.abc import Iterator
from typing import Optional

REQUIRED_FIELDS = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
HEIGHT_PATTERN = re.compile(r"(\d+)(in|cm)")
COLOR_PATTERN = re.compile(r"#[0-9a-f]{6}$")


def main():
    print("4a:", sum(1 for i in gen_passports("input.txt") if valid(i)))
    print("4b:", sum(1 for i in gen_passports("input.txt") if valid_second_part(i)))


def valid(passport: dict[str, str]) -> bool:
    for field in REQUIRED_FIELDS:
        if field not in passport:
            return False
    return True


def valid_second_part(passport: dict[str, str]) -> bool:
    if not validate_year(passport.get("byr"), 1920, 2002):
        return False
    if not validate_year(passport.get("iyr"), 2010, 2020):
        return False
    if not validate_year(passport.get("eyr"), 2020, 2030):
        return False
    if not validate_height(passport.get("hgt")):
        return False
    if not valid_color(passport.get("hcl")):
        return False
    if not valid_eye_color(passport.get("ecl")):
        return False
    if not valid_pid(passport.get("pid")):
        return False
    return True


def valid_pid(pid: Optional[str]) -> bool:
    if not pid:
        return False
    return re.match(r"\d{9}$", pid) is not None


def valid_eye_color(color: Optional[str]) -> bool:
    return color in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def valid_color(color: Optional[str]):
    if not color:
        return False
    return COLOR_PATTERN.match(color) is not None


def validate_height(height: Optional[str]) -> bool:
    if not height:
        return False
    match = HEIGHT_PATTERN.match(height)
    if not match:
        return False
    numeric_height = int(match.group(1))
    if match.group(2) == "cm":
        if not 150 <= numeric_height <= 193:
            return False
    elif match.group(2) == "in":
        if not 59 <= numeric_height <= 76:
            return False
    else:
        return False

    return True


def validate_year(birth_year: Optional[int], low: int, high: int) -> bool:
    if not birth_year:
        return False
    try:
        birth_year_number = int(birth_year)
    except ValueError:
        return False
    if low > birth_year_number:
        return False
    if birth_year_number > high:
        return False
    return True


def gen_passports(filename: str) -> Iterator[dict[str, str]]:
    current: dict[str, str] = {}
    for i in gen_keys(filename):
        if i:
            current[i[0]] = i[1]
        else:
            yield current
            current = {}
    yield current


def gen_keys(filename: str) -> Iterator[Optional[tuple[str, str]]]:
    with open(filename, "r") as f:
        for line in (line.rstrip() for line in f):
            if line == "":
                yield None
            else:
                for item in line.split(" "):
                    key, value = item.split(":")
                    yield key, value


if __name__ == "__main__":
    main()
