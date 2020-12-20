# advent of code 2015, day 7
import re
from typing import Dict

BASE_SYNTAX = re.compile(r"(.*) -> (\w+)")
OPERATION_PATTERN = re.compile(r"(\w+) (\w+) (\w+)")
NOT_PATTERN = re.compile(r"NOT (\w+)")
INT_LITERAL_PATTERN = re.compile(r"^\d+$")
WORD_LITERAL_PATTERN = re.compile(r"^\w+$")


class Gate(object):
    def __init__(self, definition: str, provider: Dict[str, "Gate"]):
        self.provider = provider
        self.definition = definition
        self.cache = None

    def _get_from_gate(self, key: str) -> int:
        gate = self.provider.get(key)
        if gate is None:
            raise ValueError(f"Found no value on wire '{key}'")
        return gate.get()

    def _resolve_operand(self, operand: str) -> int:
        # the following two lines implements 7b
        if operand == "b":
            return 46065

        match = INT_LITERAL_PATTERN.match(operand)
        if match:
            return int(operand)
        else:
            return self._get_from_gate(operand)

    def _cache(self, value: int) -> int:
        self.cache = value
        return value

    def get(self) -> int:
        if self.cache:
            return self.cache
        print(f"DEBUG getting value from definition {self.definition}")
        if " " not in self.definition:
            return self._cache(self._resolve_operand(self.definition))

        match = OPERATION_PATTERN.match(self.definition)
        if match:
            a = self._resolve_operand(match.group(1))
            b = self._resolve_operand(match.group(3))
            operator = match.group(2)
            if operator == "AND":
                return self._cache(a & b)
            elif operator == "OR":
                return self._cache(a | b)
            elif operator == "LSHIFT":
                return self._cache(a << b)
            elif operator == "RSHIFT":
                return self._cache(a >> b)
        match = NOT_PATTERN.match(self.definition)
        if match:
            a = self._resolve_operand(match.group(1))
            return self._cache(a ^ 2 ** 16 - 1)
        raise ValueError(f"failed to parse instruction {self.definition}")


def main():
    circuit: Dict[str, Gate] = {}
    with open("input/day7.txt", "r") as f:
        for line in f:
            line = line.rstrip()
            match = BASE_SYNTAX.match(line)
            if not match:
                raise ValueError(f"Don't know how to parse {line}")
            wire = match.group(2)
            definition = match.group(1)
            circuit[wire] = Gate(definition, circuit)
    if not circuit.get("a"):
        raise ValueError("wire 'a' not defined")
    print(circuit.get("a").get())


if __name__ == "__main__":
    main()
