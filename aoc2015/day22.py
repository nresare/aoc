# advent of code 2015 day 21
import itertools
import sys
from abc import ABC
from collections.abc import Iterable, Iterator
from copy import copy
from enum import Enum
from typing import Type


class Character(object):
    def __init__(self, hit_points: int, mana: int = 0, damage: int = 0):
        self.hit_points = hit_points
        self.mana = mana
        self.damage = damage
        self.armor = 0

    def pay(self, cost: int) -> bool:
        if cost > self.mana:
            return True
        self.mana -= cost
        return False

    def deal_damage(self, damage: int):
        self.hit_points -= damage

    def is_alive(self):
        return self.hit_points > 0

    def increase_mana(self, count: int):
        self.mana += count


class Spell(ABC):
    def __init__(self, duration: int = 0, instant: bool = False):
        self.duration = duration
        self.instant = instant

    def deplete(self) -> bool:
        """
        Remove one from the duration counter. Return True if spell
        has expired, else False
        """
        self.duration -= 1
        log(f"{type(self).__name__} timer is now {self.duration}")
        return not self.duration

    def modify_damage(self, initial_damage: int) -> int:
        return initial_damage

    def apply(self, opponent: Character, player: Character) -> None:
        pass


class MagicMissile(Spell):
    cost = 53

    def __init__(self):
        Spell.__init__(self, instant=True)

    def apply(self, opponent: Character, player: Character):
        log(f"MagicMissile deals 4 damage")
        opponent.deal_damage(4)


class Drain(Spell):
    cost = 73

    def __init__(self):
        Spell.__init__(self, instant=True)

    def apply(self, opponent: Character, player: Character):
        opponent.deal_damage(2)
        player.deal_damage(-2)


class Shield(Spell):
    cost = 113

    def __init__(self):
        Spell.__init__(self, duration=6)

    def modify_damage(self, initial_damage: int) -> int:
        damage = initial_damage - 7
        return 1 if damage < 1 else damage


class Poison(Spell):
    cost = 173

    def __init__(self):
        Spell.__init__(self, duration=6)

    def apply(self, opponent: Character, player: Character) -> None:
        log(f"Poison deals 3 damage")
        opponent.deal_damage(3)


class Recharge(Spell):
    cost = 229

    def __init__(self):
        Spell.__init__(self, duration=5)

    def apply(self, opponent: Character, player: Character) -> None:
        log(f"Recharge provides 101 mana, it's timer is now {self.duration-1}")
        player.increase_mana(101)


RECIPES = (
    MagicMissile,
    Drain,
    Shield,
    Poison,
    Recharge
)


def gen_winners(
        player: Character,
        opponent: Character,
        not_more_than: int,
        previous: tuple[Type[Spell], ...] = (),
        cost: int = 0,
) -> Iterator[tuple[Type[Spell], ...]]:
    for recipe in RECIPES:
        if cost + recipe.cost > not_more_than:
            continue
        candidate = previous + (recipe,)
        outcome = play(copy(player), copy(opponent), candidate)
        if outcome == Outcome.WIN:
            yield candidate
        elif outcome == Outcome.OUT_OF_SPELLS:
            yield from gen_winners(player, opponent, not_more_than, candidate, cost + recipe.cost)


def test():
    # assert play(
    #     Character(10, mana=250),
    #     Character(13, damage=8),
    #     (Poison, MagicMissile)
    # )
    # assert play(
    #     Character(10, mana=250),
    #     Character(14, damage=8),
    #     (Recharge, Shield, Drain, Poison, MagicMissile)
    # )
    assert play(
        Character(50, mana=500),
        Character(58, damage=9),
        (Poison, MagicMissile, Recharge, Poison, Shield, Recharge, Poison, Drain, MagicMissile)
    )
    print(sum(x.cost for x in (Poison, MagicMissile, Recharge, Poison, Shield, Recharge, Poison, Drain, MagicMissile)))


def main():
    cheapest_seen = sys.maxsize
    player = Character(50, mana=500)
    opponent = Character(58, damage=9)
    for i in itertools.count(0, 100):
        print(f"Trying to find a winner lower than {i}")
        for winner in gen_winners(player, opponent, i):
            candidate = sum(i.cost for i in winner)
            if candidate < cheapest_seen:
                cheapest_seen = candidate
                print(f"Found one with price {cheapest_seen}: ", " ".join(x.__name__ for x in winner))
        if cheapest_seen != sys.maxsize:
            return cheapest_seen


class Outcome(Enum):
    WIN = 1
    LOSS = 2
    OUT_OF_SPELLS = 3


def log(data: str) -> None:
    pass
    # print(data)


def play(player: Character, opponent: Character, spells: Iterable[Type[Spell], ...]) -> Outcome:
    spell_iterator = iter(spells)

    active_spells: list[Spell] = []
    while True:
        # player's turn
        log("-- Player turn --")
        log(f"Player has {player.hit_points} hit points, {player.mana} mana")
        log(f"Boss has {opponent.hit_points} hit points")

        apply_effects(active_spells, opponent, player)
        if not opponent.is_alive():
            return Outcome.WIN
        try:
            recipe = next(spell_iterator)
        except StopIteration:
            return Outcome.OUT_OF_SPELLS

        log(f"Player casts {recipe.__name__}")
        for spell in active_spells:
            # we can't cast a spell identical to an already active spell
            if isinstance(spell, recipe):
                return Outcome.LOSS
        spell = recipe()
        if player.pay(spell.cost):
            return Outcome.LOSS

        if spell.instant:
            spell.apply(opponent, player)
            if not opponent.is_alive():
                return Outcome.WIN
        else:
            active_spells.append(spell)

        log("")
        # opponent's turn
        log("-- Boss turn --")
        log(f"Player has {player.hit_points} hit points, {player.mana} mana")
        log(f"Boss has {opponent.hit_points} hit points")
        apply_effects(active_spells, opponent, player)
        if not opponent.is_alive():
            log("Boss is dead, win!")
            return Outcome.WIN

        damage = opponent.damage
        for spell in active_spells:
            damage = spell.modify_damage(damage)
        log(f"Boss attacks for {damage} damage")
        player.deal_damage(damage)
        if not player.is_alive():
            log("Player is dead, loss")
            return Outcome.LOSS
        log("")


def apply_effects(active_spells: list[Spell], opponent: Character, player: Character) -> None:
    to_delete: list[Spell] = []
    for spell in active_spells:
        spell.apply(opponent, player)
        if spell.deplete():
            to_delete.append(spell)
    for spell in to_delete:
        active_spells.remove(spell)


if __name__ == "__main__":
    print(main())
