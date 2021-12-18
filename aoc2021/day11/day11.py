from typing import Iterable, Set

Matrix = list[list[int, ...], ...]


def read_matrix(filename: str) -> Matrix:
    with open(filename, "r") as f:
        lines = (x.rstrip() for x in f)
        return [[int(y) for y in x] for x in lines]


def print_matrix(matrix: Matrix):
    print("\n".join(("".join(str(y) for y in x) for x in matrix)))


def is_valid(matrix: Matrix, x: int, y: int) -> bool:
    if x < 0 or y < 0:
        return False
    if x >= len(matrix) or y >= len(matrix[x]):
        return False
    return True


def gen_neighbours(matrix: Matrix, x: int, y: int) -> Iterable[tuple[int, int]]:
    def inner():
        for x0 in (x - 1, x, x + 1):
            for y0 in (y - 1, y, y + 1):
                if x0 != x or y0 != y:
                    yield x0, y0
    return (xy for xy in inner() if is_valid(matrix, xy[0], xy[1]))


def increment_neighbours(matrix, x, y):
    for x, y in gen_neighbours(matrix, x, y):
        matrix[x][y] += 1


def one_step(matrix: Matrix) -> int:
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            matrix[x][y] += 1

    flashed: Set[tuple[int, int]] = set()
    go_on = True
    while go_on:
        go_on = False
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                if matrix[x][y] > 9 and (x, y) not in flashed:
                    go_on = True
                    flashed.add((x, y))
                    # print(f"Flash at {x}, {y}")
                    increment_neighbours(matrix, x, y)

    for x, y in flashed:
        matrix[x][y] = 0
    return len(flashed)


def solve(filename: str) -> None:
    matrix = read_matrix(filename)
    n = 100
    print(f"Sum of flashes after {n} iterations: {sum(one_step(matrix) for x in range(n))}")

    matrix = read_matrix(filename)
    target = sum(len(row) for row in matrix)
    for i in range(10_000):
        if one_step(matrix) == target:
            print(f"All octopuses flashed after {i + 1} steps")
            return


if __name__ == "__main__":
    solve("input.txt")
