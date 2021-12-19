import itertools
from collections import defaultdict
from typing import Iterable


def gen_edges(filename: str) -> Iterable[tuple[str, str]]:
    with open(filename, "r") as f:
        for line in f:
            segments = line.rstrip().split("-")
            if len(segments) != 2:
                ValueError("invalid line")
            yield segments[0], segments[1]


Graph = dict[str, tuple[str]]


def build_graph(edges: Iterable[tuple[str, str]]) -> Graph:
    vertices = defaultdict(list[str])
    for edge in edges:
        vertices[edge[0]].append(edge[1])
        vertices[edge[1]].append(edge[0])
    return dict((k, tuple(sorted(v))) for k, v in vertices.items())


def print_graph(graph: Graph):
    for item in graph.items():
        print(f"from '{item[0]}' I can visit {', '.join(item[1])}")


def gen_paths(graph: Graph, cur: str, end: str, path: tuple[str, ...], rule):
    for target in graph[cur]:
        if target == end:
            yield path + (target, )
        elif not rule(path, target):
            yield from gen_paths(graph, target, end, path + (target,), rule)


def find_all_paths(graph: Graph, start: str, end: str, rule):
    paths = tuple(sorted(set(gen_paths(graph, start, end, (start,), rule))))
    print(f"graph has {len(paths)} paths")


def forbidden_part1(path: tuple[str, ...], cur: str) -> bool:
    return cur.islower() and cur in path


def forbidden_part2(path: tuple[str, ...], cur: str) -> bool:
    if cur == "start" and len(path) > 1:
        return True
    if not cur.islower():
        return False
    lowers = tuple(x for x in itertools.chain(path, (cur,)) if x.islower())
    if len(set(lowers)) < len(lowers) - 1:
        return True
    return False


if __name__ == "__main__":
    g = build_graph(gen_edges("input.txt"))
    find_all_paths(g, "start", "end", forbidden_part1)
    find_all_paths(g, "start", "end", forbidden_part2)
