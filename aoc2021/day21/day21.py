from functools import cache
from typing import Iterable

# I had some help with my thinking from this one  https://www.youtube.com/watch?v=tEPgMuqZZGE


class DeterministicDie(object):
    def __init__(self):
        self.counter = -1

    def __next__(self):
        return sum((
            self.single(),
            self.single(),
            self.single()
        ))

    def single(self) -> int:
        self.counter += 1
        return self.counter % 100 + 1

    def count(self):
        return self.counter + 1


class Player(object):
    def __init__(self, position):
        self.position = position
        self.points = 0

    def move(self, die: DeterministicDie):
        self.position = forward(self.position, next(die))
        self.points += self.position


def forward(current: int, steps: int) -> int:
    return ((current - 1) + steps) % 10 + 1


# returns the lowest count when there is a winner
def play(players: tuple[Player, ...], die: DeterministicDie):
    while True:
        for player in players:
            player.move(die)
            if player.points >= 1000:
                return min(x.points for x in players)


def solve(first_position: int, second_position: int):
    players = (
        Player(first_position),
        Player(second_position)
    )
    die = DeterministicDie()
    lowest_points = play(players, die)
    print(f"The die has been thrown {die.count()} times")
    print(f"The player with least points had {lowest_points} points")
    print(f"Result: {die.count() * lowest_points}")


throw_counts = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}


def backwards(position: int, steps: int):
    return (position - 1 - steps) % 10 + 1


@cache
def combinations(position: int, score: int, turn: int, start_position: int) -> int:
    def inner(s: int):
        for throw in throw_counts:
            c = combinations(backwards(position, throw), s, turn - 1, start_position)
            yield throw_counts[throw] * c

    if turn == 0:
        return 1 if (score == 0 and position == start_position) else 0

    new_score = score - position
    if new_score >= 21:
        return 0

    return sum(inner(new_score))


def gen_end_state_counts(start_pos_1: int, start_pos_2: int, flipped: bool) -> Iterable[int]:
    for win_position in range(1, 11):
        for win_score in range(21, 31):
            for turn in range(3, 11):
                for lose_position in range(1, 11):
                    for lose_score in range(3, 21):
                        flipped_turn = turn - 1 if flipped else turn
                        s0 = combinations(win_position, win_score, turn, start_pos_1)
                        s1 = combinations(lose_position, lose_score, flipped_turn, start_pos_2)
                        yield s0 * s1


def solve_part2(first, second):
    print(sum(gen_end_state_counts(first, second, True)))
    print(sum(gen_end_state_counts(second, first, False)))


if __name__ == "__main__":
    solve(4, 3)
    solve_part2(4, 8)
