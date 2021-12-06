
DAYS_A = 80
DAYS_B = 256


def parse(filename: str) -> tuple[int]:
    with open(filename, "r") as f:
        return tuple(int(x) for x in f.read().split(","))


def solve(fish: tuple[int]):
    ages = [0] * 9

    for f in fish:
        ages[f] += 1

    for i in range(DAYS_A):
        progress_one(ages)

    print(f"After {DAYS_A} days: {sum(ages)}")

    for i in range(DAYS_B - DAYS_A):
        progress_one(ages)

    print(f"After {DAYS_B} days: {sum(ages)}")


def progress_one(ages: list[int]) -> None:
    at_zero = ages[0]
    for i in range(8):
        ages[i] = ages[i+1]
    ages[6] += at_zero
    ages[8] = at_zero


if __name__ == "__main__":
    solve(parse("input.txt"))
