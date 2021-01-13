# Advent of code 2015 Day 23
import re
from collections.abc import Iterator
from typing import Optional, Callable

PATTERN = re.compile(r"(\w{3}) (\w)?(, )?([-+]\d+)?$")

Instruction = tuple[str, str, Optional[int]]


def parse(filename: str) -> Iterator[tuple[str, str, Optional[int]]]:
    with open(filename, "r") as f:
        for line in (x.rstrip() for x in f):
            match = PATTERN.match(line)
            if not match:
                raise ValueError(f"Failed to parse {line}")
            instruction, register, _, offset = match.groups()
            if not offset:
                yield instruction, register, None
            else:
                yield instruction, register, int(offset)


class Computer(object):
    def __init__(self):
        self.a: int = 0
        self.b: int = 0

    def run(self, code: tuple[Instruction]):
        position = 0
        while position < len(code):
            instruction, register, offset = code[position]
            if instruction == "hlf":
                self.change_register(register, lambda x: x // 2)
                position += 1
            elif instruction == "tpl":
                self.change_register(register, lambda x: x * 3)
                position += 1
            elif instruction == "inc":
                self.change_register(register, lambda x: x + 1)
                position += 1
            elif instruction == "jmp":
                position += offset
            elif instruction == "jie":
                if not self.get_register(register) % 2:
                    position += offset
                else:
                    position += 1

            elif instruction == "jio":
                if self.get_register(register) == 1:
                    position += offset
                else:
                    position += 1
            else:
                raise ValueError("don't know how to deal with {instruction} at {position}")

    def change_register(self, register: str, perform: Callable[[int], int]):
        assert register
        self.set_register(register, perform(self.get_register(register)))

    def get_register(self, name: str) -> int:
        if name == "a":
            return self.a
        elif name == "b":
            return self.b
        else:
            raise ValueError(f"Unknown register {name}")

    def set_register(self, name: str, value: int) -> None:
        if name == "a":
            self.a = value
        elif name == "b":
            self.b = value
        else:
            raise ValueError(f"Unknown register {name}")


def main():
    code = tuple(parse("input/day23.txt"))
    c = Computer()
    c.a = 1
    c.run(code)
    print(c.b)


if __name__ == "__main__":
    main()
