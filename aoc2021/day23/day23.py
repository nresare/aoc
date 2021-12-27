from typing import Iterable


VALID_LOCATIONS = (
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
    (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11),
    (2, 3), (2, 5), (2, 7), (2, 9),
    (3, 3), (3, 5), (3, 7), (3, 9),
)

CANT_STOP = (
    (1, 3), (1, 5), (1, 7), (1, 9),
)

TARGET_POSITIONS = {
    "A": ((2, 3), (3, 3)),
    "B": ((2, 5), (3, 5)),
    "C": ((2, 7), (3, 7)),
    "D": ((2, 9), (3, 9))
}

Pair = tuple[int, int]
Piece = tuple[str, Pair]
State = tuple[Piece, ...]


def print_state(state: State):
    m = {s[1]: s[0] for s in state}

    def pixel(i, j):
        if (i, j) in m:
            return m[(i, j)]
        if (i, j) in VALID_LOCATIONS:
            return "."
        else:
            return "#"

    for x in range(5):
        print("".join(pixel(x, y) for y in range(13)))


def solve():
    state = parse("sample.txt")
    # for i in gen_valid_moves(state):
    #     print(i)
    print_state(state)
    piece, pair = next(gen_valid_moves(state))
    state = new_state(state, piece, pair)
    print_state(state)
    state = new_state(state, piece, pair)
    print_state(state)


def new_state(state: State, piece: Piece, new: Pair) -> State:
    def inner():
        for p in state:
            if p == piece:
                yield p[0], new
            else:
                yield p
    return tuple(inner())


def gen_valid_moves(state: tuple[Piece, ...]) -> tuple[Piece, Pair]:
    taken = {s[1] for s in state}
    for s in state:
        if s[1] in CANT_STOP:
            x, y = s[1]
            for candidate in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if candidate in VALID_LOCATIONS and candidate not in taken:
                    yield s, candidate
            return

    for s in state:
        x, y = s[1]
        for candidate in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if candidate in VALID_LOCATIONS and candidate not in taken:
                yield s, candidate


def parse(filename: str) -> tuple[Piece, ...]:
    def inner() -> Iterable[tuple[str, tuple[int, int]]]:
        with open(filename, "r") as f:
            for i, line in enumerate(f):
                for j, c in enumerate(line):
                    if c in "ABCD":
                        yield c, (i, j)
    return tuple(inner())


if __name__ == "__main__":
    solve()
