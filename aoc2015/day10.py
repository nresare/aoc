# advent of code 2015, day 10
from collections.abc import Iterator
from typing import Tuple


def main():
    value = "1113222113"
    for _ in range(50):
        value = look_and_say(value)
    print(len(value))


def gen_repeated_sequences(digits: str) -> Iterator[Tuple[int, str]]:
    prev = None
    prev_offset = 0
    c = None
    for i, c in enumerate(digits):
        if prev and prev != c:
            yield i - prev_offset, prev
            prev_offset = i
        prev = c
    if prev_offset < len(digits):
        yield len(digits) - prev_offset, c


def gen_numbers(digits: str) -> Iterator[str]:
    for count, character in gen_repeated_sequences(digits):
        yield str(count)
        yield character


def look_and_say(numbers: str) -> str:
    return "".join(gen_numbers(numbers))


if __name__ == "__main__":
    main()
