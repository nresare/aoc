# advent of code 2020 Day 5

def main():
    with open("input.txt", "r") as f:
        ids = tuple(get_id(*parse_code(x.rstrip())) for x in f)
        print("5a:", max(ids))
        print("5b:", find_free_seat(ids))


def find_free_seat(ids: tuple[int, ...]) -> int:
    id_set = set(ids)
    last_seat = get_id(127, 7)
    for i in range(get_id(127, 7)):
        if i in id_set:
            continue
        if i < 1:
            continue
        if i - 1 not in id_set:
            continue
        if i > last_seat - 1:
            continue
        if i + 1 not in id_set:
            continue
        return i
    raise ValueError("Could not find free seat")


def get_id(row: int, seat: int) -> int:
    return row * 8 + seat


def parse_code(code: str) -> tuple[int, int]:
    assert len(code) == 10
    row = 0
    for i, c in enumerate(code[:7]):
        row += 2 ** (6 - i) if c == "B" else 0
    seat = 0
    for i, c in enumerate(code[7:10]):
        seat += 2 ** (2 - i) if c == "R" else 0
    return row, seat


if __name__ == "__main__":
    main()
