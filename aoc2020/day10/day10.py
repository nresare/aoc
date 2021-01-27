from collections import Counter
from collections.abc import Iterator


def get_steps(numbers: tuple[int]):
    counter: Counter[int] = Counter()
    previous = 0
    for number in sorted(numbers):
        counter[number - previous] += 1
        previous = number
    # special rule for the last step, always 3
    counter[3] += 1
    return counter


def number_of_combinations(numbers: tuple[int, ...]) -> int:
    count_at_position = {max(numbers): 1}
    for i in range(max(numbers) - 1, -1, -1):
        total = 0
        for j in range(i + 1, i + 4):
            if j in numbers:
                total += count_at_position[j] if j in count_at_position else 0
        count_at_position[i] = total
    return count_at_position[0]


def main():
    numbers = tuple(gen_numbers("input.txt"))
    step_counts: dict[int, int] = get_steps(numbers)
    print("10a:", step_counts[1] * step_counts[3])
    print("10b:", number_of_combinations(numbers))


def gen_numbers(filename: str) -> Iterator[int]:
    with open(filename, "r") as f:
        yield from (int(line) for line in f)


if __name__ == "__main__":
    main()
