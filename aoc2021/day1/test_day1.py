from unittest import TestCase

from aoc2021.day1.day1 import count_increments


class Test(TestCase):
    def test_count_increments(self):
        self.assertEqual(7, count_increments([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]))
