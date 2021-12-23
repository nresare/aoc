from typing import IO, Iterable


def dbg(to_print: str):
    print(f"DBG: {to_print}")


class Image(object):
    def __init__(self, lit: tuple[tuple[int, int], ...], inverted: bool = False):
        self.min_x = min(i[0] for i in lit)
        self.max_x = max(i[0] for i in lit)
        self.min_y = min(i[1] for i in lit)
        self.max_y = max(i[1] for i in lit)
        self.lit = frozenset(lit)
        self.inverted = inverted

    def print(self):
        def pixel(x, y):
            return "#" if (x, y) in self.lit else "."

        for i in range(self.min_x, self.max_x + 1):
            print("".join(pixel(i, j) for j in range(self.min_y, self.max_y + 1)))

    def gen_meaningful_coordinates(self):

        for i in range(self.min_x - 1, self.max_x + 2):
            for j in range(self.min_y - 1, self.max_y + 2):
                yield i, j

    def lookup_value(self, x, y) -> int:
        def value(i):
            return "1" if (i in self.lit) != self.inverted else "0"

        return int("".join(value(i) for i in gen_neighbours(x, y)), 2)

    def make_enhanced(self, enhancement: tuple[bool]) -> "Image":
        # if the first bit of enhancement is True, a pixel with all
        # dark pixels will be light, which means that the infinite
        # space of dark pixels will be flipping to light. To handle
        # this correctly, we invert the meaning of the lit tuples,
        invert = enhancement[0] and not self.inverted

        def gen_lit_coordinates():
            for x, y in self.gen_meaningful_coordinates():
                # dbg(f"Calculating output for pixel: {xy}")
                value = self.lookup_value(x, y)
                # dbg(f"value: {enhancement[value]}")
                if enhancement[value] != invert:
                    yield x, y

        return Image(tuple(gen_lit_coordinates()), inverted=invert)

    def count_lit(self) -> int:
        if self.inverted:
            raise ValueError("Infinite light pixels this time, enhance one more time!")
        return len(self.lit)


def gen_neighbours(x: int, y: int) -> Iterable[tuple[int, int]]:
    return ((i, j) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2))


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
    print(f"image size: {image.count_lit()}")
    for i in range(48):
        print("enhancing..")
        image = image.make_enhanced(enhancement)
    print(f"image size: {image.count_lit()}")


if __name__ == "__main__":
    solve()
