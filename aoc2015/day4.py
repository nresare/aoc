# advent of code 2015, day 5

import hashlib

def main():
    with open("input/day4simple.txt", "r") as f:
        data: str = f.read()
        data = data.rstrip()
    print(find_coin_serial(data))


def gen_positive_numbers():
    state = 1
    while True:
        yield state
        state += 1


def count_leading_zeroes(code: str) -> int:
    for i, c in enumerate(code):
        if c != "0":
            return i
    return len(code)


def find_coin_serial(code: str) -> int:
    for i in gen_positive_numbers():
        hex_hash = hashlib.md5(f"{code}{i}".encode("US-ASCII")).hexdigest()
        if count_leading_zeroes(hex_hash) > 5:
            return i


if __name__ == "__main__":
    main()
