#!/usr/bin/env python3
import re
from datetime import datetime


UBUNTU_TIMESTAMP_PATTERN = re.compile(r"\w{3} \d+ \d\d:\d\d:\d\d")
DATE_PATTERN = "%Y %b %d %H:%M:%S"


def get_date(line: str) -> datetime:
    match = UBUNTU_TIMESTAMP_PATTERN.match(line)
    if not match:
        raise ValueError("couldn't find date")
    return datetime.strptime("2020 " + match.group(), DATE_PATTERN)


def main():
    with open("/tmp/input.txt", "r") as f:
        previous = None
        for line in f:
            line = line.rstrip()

            current = get_date(line)
            if previous:
                print(f"delta: {current - previous} {line}")
            previous = current


if __name__ == "__main__":
    main()
