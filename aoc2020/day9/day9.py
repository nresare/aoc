from collections import deque
from collections.abc import Iterator
from itertools import combinations
from typing import Collection, Optional


def main():
    numbers = tuple(gen_numbers("input.txt"))
    not_a_sum = find_number_not_a_sum_of_a_combination(numbers, 25)
    print("9a:", not_a_sum)
    print("9b:", find_sequence_code(numbers, not_a_sum))


def find_sequence_code(numbers: tuple[int, ...], target: int) -> int:
    def _inner(i: int) -> Optional[int]:
        sequence = [numbers[i]]
        for j in range(i + 1, len(numbers)):
            sequence.append(numbers[j])
            candidate = sum(sequence)
            if candidate == target:
                return min(sequence) + max(sequence)
            elif candidate > target:
                return None

    for n in range(len(numbers)):
        result = _inner(n)
        if result:
            return result
    raise ValueError


def find_number_not_a_sum_of_a_combination(numbers: tuple[int, ...], lookback_size: int) -> int:
    last_n = deque()
    for n in numbers[:lookback_size]:
        last_n.append(n)
    for n in numbers[lookback_size:]:
        if not is_sum_of_some_combination(last_n, n):
            return n
        last_n.popleft()
        last_n.append(n)
    print("all numbers have combinations")


def is_sum_of_some_combination(to_combine: Collection[int], number: int) -> bool:
    for combination in combinations(to_combine, 2):
        if sum(combination) == number:
            return True
    return False


def gen_numbers(filename: str) -> Iterator[int]:
    with open(filename, "r") as f:
        yield from (int(line) for line in f)


if __name__ == "__main__":
    main()
