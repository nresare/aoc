from unittest import TestCase

from aoc2020.day2.day2 import check_password
from aoc2020.day2.day2b import check_password as check_password_b


class Test(TestCase):
    def test_check_password(self):
        self.assertTrue(check_password(1, 3, "a", "abcde"))
        self.assertFalse(check_password(1, 2, "a", "aaa"))

    def test_check_2b_password(self):
        self.assertTrue(check_password_b(1, 3, "a", "abcde"))
        self.assertFalse(check_password_b(1, 3, "a", "bbcde"))
        self.assertFalse(check_password_b(1, 3, "a", "abade"))
        self.assertTrue(check_password_b(1, 3, "a", "cbade"))
