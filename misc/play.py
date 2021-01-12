from abc import ABC

class Character(object):
    def __init__(self, hit_points: int, mana: int = 0, damage: int = 0):
        self.hit_points = hit_points
        self.mana = mana
        self.damage = damage
        self.armor = 0

    def pay(self, cost: int) -> bool:
        if cost > self.mana:
            return True
        return False

    def deal_damage(self, damage: int):
        self.hit_points -= damage

    def is_alive(self):
        return self.hit_points > 0

    def increase_mana(self, count: int):
        self.mana += count


class Spell(ABC):
    def __init__(self, cost: int, duration: int = 0, instant: bool = False):
        self.cost = cost
        self.duration = duration
        self.instant = instant

    def deplete(self) -> bool:
        """
        Remove one from the duration counter. Return True if spell
        has expired, else False
        """
        self.duration -= 1
        return not self.duration

    def modify_damage(self, initial_damage: int) -> int:
        return initial_damage

    def apply(self, opponent: Character, player: Character) -> None:
        pass


class MagicMissile(Spell):
    def __init__(self):
        Spell.__init__(self, 53, instant=True)

    def apply(self, opponent: Character, player: Character):
        opponent.deal_damage(4)


TYPES = (MagicMissile,)

if __name__ == "__main__":
    for t in TYPES:
        mm = t()

