import re

PATTERN = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def main():
    with open("input.txt", "r") as f:
        print(sum(1 for x in f if is_valid(x)))


def check_password(a: int, b: int, letter: str, password: str):
    count = sum(1 for x in (a, b) if password[x-1] == letter)
    return count == 1


def is_valid(line: str) -> bool:
    match = PATTERN.match(line)
    if not match:
        raise ValueError(f"Failed to parse '{line}'")
    a, b, letter, password = match.groups()
    return check_password(int(a), int(b), letter, password)


if __name__ == "__main__":
    main()
