import heapq
import sys
from timeit import default_timer
from typing import Iterable, Set, Dict

Matrix = tuple[tuple[int, ...], ...]
Node = tuple[int, int]


def gen_tiled_row(row: tuple[int], repetitions: int, row_iteration: int):
    for i in range(repetitions):
        for j in range(len(row)):
            yield ((row[j] + i + row_iteration - 1) % 9) + 1


def read_matrix(filename: str, tiled: int) -> Matrix:
    with open(filename, "r") as f:
        tile = tuple(tuple(int(c) for c in line.rstrip()) for line in f)
        if tiled == 1:
            return tile
        else:
            def gen_tiled():
                for i in range(tiled):
                    for row in tile:
                        yield tuple(gen_tiled_row(row, tiled, i))
            return tuple(gen_tiled())


def gen_nodes(matrix: Matrix) -> Iterable[Node]:
    for i, row in enumerate(matrix):
        for j in range(len(row)):
            yield i, j


def gen_neighbours(matrix: Matrix, node: Node) -> Iterable[Node]:
    if node[0] > 0:
        yield node[0] - 1, node[1]
    if node[1] > 0:
        yield node[0], node[1] - 1
    if node[0] < len(matrix) - 1:
        yield node[0] + 1, node[1]
    if node[1] < len(matrix[node[0]]) - 1:
        yield node[0], node[1] + 1


def calculate_least_risk_to_get_anywhere(matrix: Matrix, start: Node) -> Dict[Node, int]:
    unvisited_nodes: Set[Node] = set(gen_nodes(matrix))
    best_path: Dict[Node, int] = dict((x, sys.maxsize) for x in unvisited_nodes)
    # previous_node: Dict[Node, Node] = {}

    best_path[start] = 0
    queue = []
    heapq.heappush(queue, (0, start))

    while queue:
        _, current = heapq.heappop(queue)
        for neighbour in gen_neighbours(matrix, current):
            cost = matrix[neighbour[0]][neighbour[1]] + best_path[current]
            if cost < best_path[neighbour]:
                heapq.heappush(queue, (cost, neighbour))
                best_path[neighbour] = cost
                # previous_node[neighbour] = current
        unvisited_nodes.remove(current)

    return best_path


def print_matrix(matrix: Matrix):
    for row in matrix:
        print("".join(str(i) for i in row))


def solve(filename: str):
    matrix = read_matrix(filename, 5)
    # print_matrix(matrix)
    before = default_timer()
    lowest_risk = calculate_least_risk_to_get_anywhere(matrix, (0, 0))
    after = default_timer()
    print(f"time taken {after - before}s")
    end_node = len(matrix) - 1, len(matrix[-1]) - 1
    print(f"Lowest cost to get to lower right corner: {lowest_risk[end_node]}")


if __name__ == "__main__":
    solve("input.txt")
