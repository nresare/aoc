# Advent of code 2020, day 8
import re
from collections.abc import Iterator
from copy import copy
from typing import NamedTuple

PATTERN = re.compile(r"([a-z]{3}) ([-+]\d+)$")


class Instruction(NamedTuple):
    operation: str
    parameter: int


def main():
    code = list(gen_instructions("input.txt"))
    print("8a:", find_value_in_the_end(code)[0])
    print("8b:", find_value_after_fixed_execution(code))


def find_value_in_the_end(code: list[Instruction, ...]) -> tuple[int, bool]:
    """
    Returns the value of the accumulator and true if it exited successfully, else false if there was an infinite loop"
    """
    visited: set[int] = set()
    position = 0
    accumulator = 0
    while position < len(code):
        if position in visited:
            return accumulator, False
        visited.add(position)

        instruction, parameter = code[position]
        if instruction == "acc":
            accumulator += parameter
            position += 1
        elif instruction == "jmp":
            position += parameter
        elif instruction == "nop":
            position += 1
        else:
            raise ValueError(f"unknown instruction {instruction}")
    return accumulator, True


def find_value_after_fixed_execution(code: list[Instruction]) -> int:
    for i in range(len(code)):
        if code[i].operation not in ("jmp", "nop"):
            continue
        code_copy = copy(code)
        if code[i].operation == "jmp":
            code_copy[i] = Instruction("nop", code[i].parameter)
        else:
            code_copy[i] = Instruction("jmp", code[i].parameter)
        result, success = find_value_in_the_end(code_copy)
        if success:
            print(f"found successful fix, at line {i}")
            return result


def gen_instructions(filename: str) -> Iterator[Instruction]:
    with open(filename, "r") as f:
        for line in (x.rstrip() for x in f):
            match = PATTERN.match(line)
            if not match:
                raise ValueError
            instruction, parameter = match.groups()
            yield Instruction(instruction, int(parameter))


if __name__ == "__main__":
    main()
