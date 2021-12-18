from unittest import TestCase

from aoc2021.day11.day11 import gen_neighbours


class Day11Test(TestCase):

    def test_gen_neighbours(self):
        matrix = [[0] * 4 for x in range(4)]
        expected = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2))
        self.assertEquals(expected, tuple(gen_neighbours(matrix, 1, 1)))
        self.assertEquals(((0, 1), (1, 0), (1, 1)), tuple(gen_neighbours(matrix, 0, 0)))
        self.assertEquals(((2, 2), (2, 3), (3, 2)), tuple(gen_neighbours(matrix, 3, 3)))
