# advent of code 2015, day 18

SIZE = 100


def main():
    b = read_board("input/day18.txt")
    for i in range(100):
        b.update()
    print(b)
    print(b.count_lit_bulbs())


class Board(object):
    def __init__(self):
        self.rows = build_rows()

    def __repr__(self):
        return "\n".join("".join("#" if x else "." for x in row) for row in self.rows)

    def update(self):
        data = build_rows(self.rows)
        for i in range(SIZE):
            for j in range(SIZE):
                count = self.count_lit_neighbours(i, j)
                if self.rows[i][j]:
                    if count not in (2, 3):
                        data[i][j] = False
                else:
                    if count == 3:
                        data[i][j] = True
        self.rows = data

    def count_lit_neighbours(self, i: int, j: int) -> int:
        i_start = i - 1 if i > 0 else i
        i_end = i + 1 if i < SIZE - 1 else i
        j_start = j - 1 if j > 0 else j
        j_end = j + 1 if j < SIZE - 1 else j

        total = 0
        for x in range(i_start, i_end + 1):
            for y in range(j_start, j_end + 1):
                if x == i and y == j:
                    continue
                total += self.rows[x][y]
        return total

    def set(self, i: int, j: int, value: bool) -> None:
        self.rows[i][j] = value

    def count_lit_bulbs(self):
        return sum(sum(1 for x in row if x) for row in self.rows)


def build_rows(previous: list[list[bool]] = None) -> list[list[bool]]:
    data: list[list[bool]] = []
    for i in range(SIZE):
        data.append([])
        for j in range(SIZE):
            data[i].append(previous[i][j] if previous else False)
    return data


def read_board(filename: str) -> Board:
    b = Board()
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            for j, c in enumerate(line):
                b.set(i, j, c == "#")
    return b


if __name__ == "__main__":
    main()
