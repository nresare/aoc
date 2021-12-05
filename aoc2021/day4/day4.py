import re
from typing import Iterator, IO

Board = tuple[tuple[int, ...], ...]


def gen_boards(f: IO) -> Iterator[Board]:
    current = []
    for line in f:
        line = line.rstrip()
        if line == "":
            if len(current) > 0:
                yield tuple(current)
                current = []
        else:
            current.append(tuple(int(x) for x in re.split(r"\s+", line) if len(x) > 0))
    yield tuple(current)


def calculate_score(board: Board, drawn_so_far: tuple[int, ...]) -> int:
    non_drawn_sum = 0
    for column in board:
        for item in column:
            if item not in drawn_so_far:
                non_drawn_sum += item
    return non_drawn_sum * drawn_so_far[-1]


def mark(board: Board, numbers: tuple[int, ...]) -> tuple[int, int]:
    """
    Takes a board and a tuple of drawn numbers,
    returns the number of drawn numbers before bingo and score
    """
    for i in range(5, len(numbers) + 1):
        drawn_so_far = numbers[:i]
        if has_bingo(board, drawn_so_far):
            return i, calculate_score(board, drawn_so_far)
    return len(numbers), 0


def has_bingo(board: Board, numbers: tuple[int, ...]) -> bool:
    for row in board:
        if line_has_bingo(row, numbers):
            return True
    for i in range(len(board)):
        column = tuple(board[x][i] for x in range(len(board[0])))
        if line_has_bingo(column, numbers):
            return True
    return False


def line_has_bingo(row: tuple[int, ...], numbers: tuple[int, ...]) -> bool:
    for item in row:
        if item not in numbers:
            return False
    return True


def solve(filename: str) -> None:
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            numbers = tuple(int(x) for x in line.split(","))

            results = sorted(mark(board, numbers) for board in gen_boards(f))
            print(f"winner after {results[0][0]} rounds: {results[0][1]}")
            print(f"loser after {results[-1][0]} rounds: {results[-1][1]}")


if __name__ == "__main__":
    solve("input.txt")
