from typing import IO, Iterable


def dbg(to_print: str):
    print(f"DBG: {to_print}")


class Image(object):
    def __init__(self, lit: tuple[tuple[int, int], ...], generation: int = 0):
        self.min_x = min(i[0] for i in lit)
        self.max_x = max(i[0] for i in lit)
        self.min_y = min(i[1] for i in lit)
        self.max_y = max(i[1] for i in lit)
        self.lit = frozenset(lit)
        self.generation = generation

    def print(self):
        def pixel(x, y):
            return "#" if (x, y) in self.lit else "."

        for i in range(self.min_x, self.max_x + 1):
            print("".join(pixel(i, j) for j in range(self.min_y, self.max_y + 1)))

    def gen_meaningful_coordinates(self):
        border = 10 - (3 * self.generation)
        dbg(f"border: {border}")
        # dbg(f"border box {self.min_x - border}, {self.max_x + 1 + border}, {self.min_y - border}, {self.max_y + 1 + border}")
        for i in range(0 - border, 101 + border):
            for j in range(0 - border, 101 + border):
                yield i, j

        # for i in range(self.min_x - border, self.max_x + 1 + border):
        #     for j in range(self.min_y - border, self.max_y + 1 + border):
        #         yield i, j

    def lookup_value(self, xy) -> int:
        neighbours = tuple(gen_neighbours(xy))
        # print_neighbours(neighbours, self.lit)
        binstring = "".join("1" if x in self.lit else "0" for x in gen_neighbours(xy))
        # dbg(f"binstring: {binstring}, value {int(binstring, 2)}")
        return int(binstring, 2)

    def make_enhanced(self, enhancement: tuple[bool]) -> "Image":

        def gen_lit_coordinates():
            for xy in self.gen_meaningful_coordinates():
                # dbg(f"Calculating output for pixel: {xy}")
                value = self.lookup_value(xy)
                # dbg(f"value: {enhancement[value]}")
                if enhancement[value]:
                    yield xy

        return Image(tuple(gen_lit_coordinates()), generation=self.generation + 1)

    def count_lit(self) -> int:
        return len(self.lit)


def print_neighbours(neighbours: tuple[tuple[int, int], ...], lit: frozenset[tuple[int, int]]):
    for i in range(3):
        dbg(" ".join("#" if neighbours[i * 3 + j] in lit else "." for j in range(3)))


def gen_neighbours(xy: tuple[int, int]) -> Iterable[tuple[int, int]]:
    x, y = xy
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            yield i, j


def parse_input(filename: str) -> tuple[tuple[bool, ...], Image]:
    def gen_image_rows(lines: IO) -> Iterable[tuple[int, int]]:
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == "#":
                    yield i, j
            yield tuple(True if c == "#" else False for c in line.rstrip())

    def gen_enhancement(lines: IO) -> Iterable[bool]:
        for line in lines:
            line = line.rstrip()
            if line == "":
                return
            yield from (True if c == "#" else False for c in line)

    with open(filename, "r") as f:
        return tuple(gen_enhancement(f)), Image(tuple(gen_image_rows(f)))


def solve():
    enhancement, image = parse_input("input.txt")
    for i in range(2):
        print("enhancing..")
        image = image.make_enhanced(enhancement)
    image.print()
    print(f"image size: {image.count_lit()}")


if __name__ == "__main__":
    solve()
