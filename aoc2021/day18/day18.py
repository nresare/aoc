import functools
from copy import deepcopy
from itertools import permutations
from typing import Iterable, Optional

BEFORE = 1
IN_EXPRESSION = 2


class Node(object):
    def __init__(
            self,
            left: Optional["Node"] = None,
            right: Optional["Node"] = None,
            value: Optional[int] = None
    ):
        if value and (left or right):
            raise ValueError
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return str(self.value)
        return f"[{self.left}, {self.right}]"


def gen_pair(expression: str) -> Iterable[str]:
    depth = 0
    state = BEFORE
    start = 0
    for i, c in enumerate(expression):
        if c == " ":
            continue
        if state == BEFORE:
            if c != "[":
                raise ValueError()
            state = IN_EXPRESSION
            start = i + 1
        elif state == IN_EXPRESSION:
            if c == "[":
                depth += 1
            elif depth > 0 and c == "]":
                depth -= 1
            elif depth < 1:
                if c == ",":
                    yield expression[start:i]
                    start = i + 1
                elif c == "]":
                    yield expression[start:i]


def parse(expression: str) -> Node:
    l, r = gen_pair(expression)
    return Node(
        Node(value=int(l)) if l.isdigit() else parse(l),
        Node(value=int(r)) if r.isdigit() else parse(r)
    )


def explode(node: Node) -> bool:
    return Exploder().traverse(node)


class Exploder(object):
    def __init__(self):
        self.prev = None
        self.to_move_forward = None
        self.dirty = False

    def traverse(self, node: Node, depth=0):
        if node is None:
            return False
        if node.value is not None:
            if self.to_move_forward is not None:
                node.value += self.to_move_forward
                self.to_move_forward = None
            self.prev = node
        if not self.dirty and node.value is None and depth > 3:
            if self.prev:
                self.prev.value += node.left.value
            self.to_move_forward = node.right.value
            node.value = 0
            node.left = None
            node.right = None
            self.dirty = True
            return self.dirty
        self.traverse(node.left, depth + 1)
        self.traverse(node.right, depth + 1)
        return self.dirty


def split(node: Node):
    if node is None:
        return False
    if node.value is not None and node.value > 9:
        do_split(node)
        return True
    return split(node.left) or split(node.right)


def do_split(node: Node):
    node.left = Node(value=node.value // 2)
    node.right = Node(value=node.value // 2 + node.value % 2)
    node.value = None


def reduce(node: Node):
    while explode(node) or split(node):
        pass


def add(left: Node, right: Node) -> Node:
    n = Node(deepcopy(left), deepcopy(right))
    reduce(n)
    # print(f"Sum: {n}")
    return n


def gen_nodes(filename: str) -> Iterable[Node]:
    with open(filename, "r") as f:
        for line in f:
            yield parse(line.rstrip())


def magnitude(node: Node) -> int:
    if node.value is not None:
        return node.value
    return sum((3 * magnitude(node.left), 2 * magnitude(node.right)))


def solve_part1(filename: str) -> int:
    return magnitude(functools.reduce(add, gen_nodes(filename)))


def solve_part2(filename: str) -> int:
    numbers = tuple(gen_nodes(filename))
    sums = ((magnitude(add(*x)), x) for x in permutations(numbers, 2))
    return sorted(sums, key=lambda x: x[0])[-1][0]


if __name__ == "__main__":
    print(solve_part2("input.txt"))
