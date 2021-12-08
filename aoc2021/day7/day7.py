from typing import Callable


def gen_positions(filename: str) -> tuple[int, ...]:
    with open(filename, "r") as f:
        return tuple(int(x) for x in f.read().split(","))


def solve(positions: tuple[int, ...], cost: Callable[[int], int]):
    in_order = sorted(positions)
    first = in_order[0]
    last = in_order[-1]

    results = ((i, cost_for_position(i, positions, cost)) for i in range(first, last + 1))

    print("Best solution is {}".format(sorted(results, key=lambda x: x[1])[0]))
    # for item in sorted(results, key=lambda x: x[1]):
    #     print(item)


def cost_for_position(target: int, positions: tuple[int, ...], cost: Callable[[int], int]) -> int:
    return sum(cost(abs(x-target)) for x in positions)


def cost_for_distance(distance: int) -> int:
    return sum(range(1, distance + 1))


if __name__ == "__main__":
    solve(gen_positions("input.txt"), lambda x: x)

    solve(gen_positions("input.txt"), cost_for_distance)

