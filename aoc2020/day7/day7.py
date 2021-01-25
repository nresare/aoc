# advent of code 2020 day 7
import re
from collections import defaultdict
from collections.abc import Iterator
from typing import NamedTuple, DefaultDict

OUTER_PATTERN = re.compile(r"([\w\s]+) bags contain (.+)$")
INNER_PATTERN = re.compile(r"(\d+) ([\w\s]+) bags*.?$")


class Rule(NamedTuple):
    name: str
    payload: tuple[tuple[int, str], ...]


def main():
    inner_to_outer: DefaultDict[str, list[str]] = defaultdict(list)
    name_to_rule: dict[str, Rule] = {}
    for rule in gen_rules("input.txt"):
        name_to_rule[rule.name] = rule
        for payload in rule.payload:
            inner_to_outer[payload[1]].append(rule.name)
    print("7a:", len(set(gen_tree_nodes(inner_to_outer, "shiny gold"))))
    print("7b:", count_bags_inside(name_to_rule, "shiny gold") - 1)


def count_bags_inside(name_to_rule: dict[str, Rule], name: str) -> int:
    rule = name_to_rule[name]
    return sum(count_bags_inside(name_to_rule, x[1]) * x[0] for x in rule.payload) + 1
    # return total


def gen_tree_nodes(inner_to_outer: dict[str, list[str]], name: str):
    outers = inner_to_outer.get(name)
    if not outers:
        return
    for outer in outers:
        yield outer
        yield from gen_tree_nodes(inner_to_outer, outer)


def make_rule(data: str) -> Rule:
    match = OUTER_PATTERN.match(data)
    if not match:
        raise ValueError(f"failed to parse line {data}")
    return Rule(match.group(1), tuple(gen_payload(match.group(2))))


def gen_payload(data: str) -> Iterator[tuple[int, str]]:
    if data == "no other bags.":
        return
    for item in data.split(", "):
        match = INNER_PATTERN.match(item)
        if not match:
            raise ValueError(f"Failed to parse item {data}")
        yield int(match.group(1)), match.group(2)


def gen_rules(filename: str) -> Iterator[Rule]:
    with open(filename, "r") as f:
        yield from (make_rule(x.rstrip()) for x in f)


if __name__ == "__main__":
    main()
