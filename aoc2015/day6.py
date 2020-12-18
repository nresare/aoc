# advent of code 2015, day 1
import re

OFFSET_PATTERN = re.compile(r"(\d+),(\d+) through (\d+),(\d+)")


def main():
    grid = Grid()
    with open("input/day6.txt", "r") as f:
        for instruction in f:
            instruction = instruction.rstrip()
            grid.apply(instruction)
    print(grid.count_lit())


class Grid(object):
    def __init__(self):
        self.rows = []
        for i in range(1000):
            column = [False] * 1000
            self.rows.append(column)

    def apply(self, instruction: str):
        match = OFFSET_PATTERN.search(instruction)
        start_x, start_y, end_x, end_y = [int(x) for x in match.groups()]
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if "turn on" in instruction:
                    self.rows[x][y] = True
                elif "turn off" in instruction:
                    self.rows[x][y] = False
                elif "toggle" in instruction:
                    self.rows[x][y] = not self.rows[x][y]

    def count_lit(self):
        return sum(sum(x) for x in self.rows)


if __name__ == "__main__":
    main()
