from unittest import TestCase

from aoc2020.day1.day1 import _inner


class Test(TestCase):
    def test__inner(self):
        self.assertEqual(_inner([1, 2, 3, 4, 5], 1, 5), 2)
