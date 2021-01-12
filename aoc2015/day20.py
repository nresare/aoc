#  2015 day 20
import math
from collections.abc import Iterator


def main():
    target = 34_000_000
    result = find_target_number(target)
    print(
        f"house {result} gets {sum(get_divisors(result)) * 10} presents, "
        f"the lowest house to get more than {target}"
    )


def find_target_number(target: int) -> int:
    for i in range(1, target):
        if sum(get_divisors(i)) * 10 > target:
            return i
        if not i % 10_000:
            print(f"Considering {i}")


def get_divisors(number: int) -> Iterator[int]:
    for i in range(1, int(math.sqrt(number)) + 1):
        if not number % i:
            yield i
            if i ** 2 == number:
                continue
            yield int(number / i)


if __name__ == "__main__":
    main()
