#  2015 day 21
import itertools
import re
from collections.abc import Iterator
from typing import NamedTuple, Tuple

ITEM_PATTERN = re.compile(r"(\w+)( \+\d)?\s+(\d+)\s+(\d+)\s+(\d+)")


class Item(NamedTuple):
    category: str
    name: str
    cost: int
    damage: int
    armor: int


# noinspection SpellCheckingInspection
SHOP = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""


def extract_items(data: str) -> Iterator[Item]:
    category = None
    for i, line in enumerate(data.split("\n")):
        if line == "":
            continue
        if ":" in line:
            category = line.split(":")[0]
            continue
        match = ITEM_PATTERN.match(line)
        if not match:
            raise ValueError(f"Could not parse line {i}: {line}")
        name, modifier, cost, damage, armor = match.groups()
        if modifier:
            name = f"{name}{modifier}"
        yield Item(category, name, int(cost), int(damage), int(armor))


class Character(object):
    def __init__(self, damage: int, armor: int, hit_points: int):
        self.damage = damage
        self.armor = armor
        self.hit_points = hit_points

    def deal_damage(self, damage: int) -> None:
        self.hit_points -= damage

    def alive(self) -> bool:
        return self.hit_points > 0


def by_cost(item: Item) -> int:
    return item.cost


def gen_ring_combinations(rings: tuple[Item]) -> Iterator[tuple[Item, ...]]:
    for first_ring in rings:
        yield first_ring,
        for second_ring in rings:
            if second_ring != first_ring:
                yield first_ring, second_ring


def gen_all_equipment_combinations(items: Tuple[Item, ...]):
    weapons = tuple(x for x in items if x.category == "Weapons")
    armor = tuple(x for x in items if x.category == "Armor")
    rings = tuple(x for x in items if x.category == "Rings")

    # only a weapon or weapon plus ring(s)
    for weapon in weapons:
        yield weapon,
        yield from (combination + (weapon,) for combination in gen_ring_combinations(rings))

    # weapon plus armor and possibly rings
    for combination in itertools.product(weapons, armor):
        yield combination
        yield from (combination + x for x in gen_ring_combinations(rings))


def main():
    initial_hp = 100
    items = tuple(extract_items(SHOP))
    most_expensive_loser = 0
    for combination in gen_all_equipment_combinations(items):
        price = sum(item.cost for item in combination)
        damage = sum(item.damage for item in combination)
        armor = sum(item.armor for item in combination)
        me = Character(damage, armor, initial_hp)
        opponent = Character(9, 2, 103)
        if not did_i_win(me, opponent):
            if price > most_expensive_loser:
                most_expensive_loser = price
                print(f"Most expensive loser {price}: ", " ".join(x.name for x in combination))


def did_i_win(me: Character, opponent: Character) -> bool:
    while True:
        opponent.deal_damage(me.damage - opponent.armor)
        if not opponent.alive():
            return True
        me.deal_damage(opponent.damage - me.armor)
        if not me.alive():
            return False


if __name__ == "__main__":
    main()
