# Advent of code 2021, day 5
from typing import Iterator


class Coord(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


def make_coords(s: str) -> Coord:
    segments = s.split(",")
    return Coord(int(segments[0]), int(segments[1]))


def gen_lines(filename: str) -> Iterator[tuple[Coord]]:
    with open(filename, "r") as f:
        for line in f:
            segments = line.split(" -> ")
            yield make_coords(segments[0]), make_coords(segments[1])


class Board(object):
    def __init__(self):
        self.board = []

    def mark(self, x, y):
        while x >= len(self.board):
            self.board.append([])
        while y >= len(self.board[x]):
            self.board[x].append(0)
        self.board[x][y] += 1

    def __str__(self):
        return "\n".join(" ".join(str(x) for x in row) for row in self.board)

    def count_more_than(self, value) -> int:
        count = 0
        for row in self.board:
            for item in row:
                if item > value:
                    count += 1
        return count


def mark_45_line(a: Coord, b: Coord, board: Board):
    if a.x == b.x or a.y == b.y:
        return

    x_increasing = b.x > a.x
    y_increasing = b.y > a.y

    length = max(a.x, b.x) - min(a.x, b.x)

    for i in range(length + 1):
        if x_increasing:
            if y_increasing:
                board.mark(a.x + i, a.y + i)
            else:
                board.mark(a.x + i, a.y - i)
        else:
            if y_increasing:
                board.mark(a.x - i, a.y + i)
            else:
                board.mark(a.x - i, a.y - i)


def solve(filename: str) -> None:
    board = Board()
    for line in gen_lines(filename):

        a = line[0]
        b = line[1]

        if a.x == b.x:
            for y in range(min(a.y, b.y), max(a.y, b.y) + 1):
                board.mark(a.x, y)
        elif a.y == b.y:
            for x in range(min(a.x, b.x), max(a.x, b.x) + 1):
                board.mark(x, a.y)

    # print(board)
    print(f"overlapping, only counting horizontal and vertical lines: {board.count_more_than(1)}")

    for line in gen_lines(filename):
        mark_45_line(line[0], line[1], board)

    print(board)
    print(f"overlapping, all lines: {board.count_more_than(1)}")


if __name__ == "__main__":
    solve("input.txt")
    # lab()
