from unittest import TestCase

from aoc2020.day5.day5 import parse_code, get_id


class Test(TestCase):
    # noinspection SpellCheckingInspection
    def test_parse_code(self):
        self.assertEqual((44, 5), parse_code("FBFBBFFRLR"))
        self.assertEqual((70, 7), parse_code("BFFFBBFRRR"))
        self.assertEqual((14, 7), parse_code("FFFBBBFRRR"))
        self.assertEqual((102, 4), parse_code("BBFFBBFRLL"))

    def test_set_get_id(self):
        self.assertEqual(357, get_id(44, 5))
