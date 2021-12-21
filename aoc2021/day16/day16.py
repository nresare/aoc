import operator
from functools import reduce
from typing import Iterable, NamedTuple, Optional

MAXIMUM = 3

MINIMUM = 2

PRODUCT = 1

SUM = 0

LITERAL_VALUE = 4


class BinaryReader(object):
    def __init__(self, binary: str):
        self.binary = binary
        self.position = 0

    def get_binary(self, binary_length: int) -> str:
        value = self.binary[self.position:self.position + binary_length]
        self.position += binary_length
        return value

    def get_int(self, binary_length: int) -> int:
        return int(self.get_binary(binary_length), 2)

    def get_literal(self) -> int:
        def gen_four_blocks():
            bits = self.get_binary(5)
            while bits[0] == '1':
                yield bits[1:]
                bits = self.get_binary(5)
            yield bits[1:]
        return int("".join(gen_four_blocks()), 2)

    def bits_left(self):
        return len(self.binary) - self.position


class Packet(NamedTuple):
    version: int
    type_id: int
    literal: Optional[int]
    children: tuple["Packet"]

    def evaluate(self) -> int:
        if self.type_id == LITERAL_VALUE:
            return self.literal
        elif self.type_id == SUM:
            return sum(child.evaluate() for child in self.children)
        elif self.type_id == PRODUCT:
            return reduce(operator.mul, (child.evaluate() for child in self.children))
        elif self.type_id == MINIMUM:
            return min(child.evaluate() for child in self.children)
        elif self.type_id == MAXIMUM:
            return max(child.evaluate() for child in self.children)
        elif self.type_id == 5:
            assert len(self.children) == 2
            return 1 if self.children[0].evaluate() > self.children[1].evaluate() else 0
        elif self.type_id == 6:
            assert len(self.children) == 2
            return 1 if self.children[0].evaluate() < self.children[1].evaluate() else 0
        elif self.type_id == 7:
            assert len(self.children) == 2
            return 1 if self.children[0].evaluate() == self.children[1].evaluate() else 0
        else:
            raise ValueError(f"unknown type_id {self.type_id}")


def parse_packet(binary: BinaryReader):
    version = binary.get_int(3)
    type_id = binary.get_int(3)
    literal = None
    children = tuple()
    if type_id == LITERAL_VALUE:
        literal = binary.get_literal()
    else:
        # any other type_id means operator
        length_type_id = binary.get_int(1)
        if length_type_id == 0:
            sub_packet_bits = binary.get_int(15)
            children = tuple(parse(BinaryReader(binary.get_binary(sub_packet_bits))))
        else:
            sub_packet_count = binary.get_int(11)
            children = tuple(parse(binary, sub_packet_count))
    return Packet(version=version, type_id=type_id, literal=literal, children=children)


def parse(binary: BinaryReader, count: int = 0) -> Iterable[Packet]:
    if count == 0:
        while binary.bits_left() > 10:
            yield parse_packet(binary)
    else:
        for _ in range(count):
            yield parse_packet(binary)


def read_to_binary(filename: str) -> BinaryReader:
    with open(filename, "r") as f:
        s = f.read().rstrip()
        return BinaryReader(hex2bin(s))


def hex2bin(hex_string: str) -> str:
    return format(int(hex_string, 16), "b").zfill(len(hex_string) * 4)


def gen_versions(packets: tuple[Packet]):
    for packet in packets:
        yield packet.version
        yield from gen_versions(packet.children)


def print_packet(packet: Packet, indent: int = 0):
    print(f"{'  ' * indent}version={packet.version} type_id={packet.type_id} literal={packet.literal}")
    for child in packet.children:
        print_packet(child, indent + 1)


def solve(filename: str):
    packet = parse_packet(read_to_binary(filename))
    # print_packet(packet)
    print(f"Versions sum: {sum(gen_versions((packet,)))}")
    print(f"Root packet evaluates to {packet.evaluate()}")


if __name__ == "__main__":
    solve("input.txt")
    # dummy()
