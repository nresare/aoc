# advent of code 2015, day 15
import re
from typing import Tuple, Iterator, NamedTuple

PATTERN = re.compile(
    r"^(\w+): capacity ([-]*\d+), durability ([-]*\d+), flavor ([-]*\d+), texture ([-]*\d+), calories ([-]*\d+)$"
)
Aspects = Tuple[int, int, int, int, int]


class Ingredient(NamedTuple):
    name: str
    aspects: Aspects


def main():
    ingredients = tuple(gen_ingredients("input/day15.txt"))
    print(max(gen_all_scores(ingredients)))
    # for i in gen_possible_proportions(100, 4):
    #     print(i)


def gen_all_scores(ingredients: Tuple[Ingredient]) -> Iterator[int]:
    for proportions in gen_possible_proportions(100, len(ingredients)):
        if get_calories(proportions, ingredients) != 500:
            continue
        yield get_score(proportions, ingredients)


def get_calories(proportions: Tuple[int, ...], ingredients: Tuple[Ingredient, ...]) -> int:
    total = 0
    for i, amount in enumerate(proportions):
        total += ingredients[i].aspects[4] * amount
    return total


def get_score(proportions: Tuple[int, ...], ingredients: Tuple[Ingredient, ...]) -> int:
    total = None
    for aspect in range(4):
        per_aspect = 0
        for i, amount in enumerate(proportions):
            if not amount:
                continue
            ingredient = ingredients[i]
            per_aspect += ingredient.aspects[aspect] * amount
        if per_aspect < 0:
            return 0
        if total is None:
            total = per_aspect
        else:
            total *= per_aspect
    return total


def gen_ingredients(filename: str) -> Iterator[Ingredient]:
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            m = PATTERN.match(line)
            if not m:
                raise ValueError(f"Could not parse line {line}")
            # noinspection PyTypeChecker
            ingredients: Aspects = tuple(int(x) for x in m.groups()[1:])
            yield Ingredient(m.group(1), ingredients)


def gen_possible_proportions(what_to_divide: int, number_of_ingredients: int) -> Iterator[Tuple[int, ...]]:
    if number_of_ingredients == 1:
        yield what_to_divide,
        return
    for i in range(0, what_to_divide + 1):
        for item in gen_possible_proportions(what_to_divide - i, number_of_ingredients - 1):
            yield tuple((i,) + item)


if __name__ == "__main__":
    main()
