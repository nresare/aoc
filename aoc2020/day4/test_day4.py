from typing import Optional
from unittest import TestCase

from aoc2020.day4.day4 import validate_year, validate_height, valid_color, valid_eye_color, valid_pid


class Test(TestCase):
    def test_valid__byr(self):
        def v(value: Optional[str]):
            return validate_year(value, 1920, 2002)

        self.assertFalse(v(None))
        self.assertFalse(v("invalid"))
        self.assertTrue(v("1990"))
        self.assertFalse(v("1919"))
        self.assertTrue(v("1920"))
        self.assertTrue(v("2002"))
        self.assertFalse(v("2003"))

    def test_validate_height(self):
        self.assertFalse(validate_height(None))
        self.assertFalse(validate_height("invalid"))
        self.assertTrue(validate_height("60in"))
        self.assertFalse(validate_height("149cm"))
        self.assertTrue(validate_height("150cm"))
        self.assertTrue(validate_height("193cm"))
        self.assertFalse(validate_height("194cm"))
        self.assertFalse(validate_height("58in"))
        self.assertTrue(validate_height("59in"))
        self.assertTrue(validate_height("76in"))
        self.assertFalse(validate_height("77in"))

    def test_validate_input_examples(self):
        self.assertTrue(validate_height("60in"))
        self.assertTrue(validate_height("190cm"))
        self.assertFalse(validate_height("190in"))
        self.assertFalse(validate_height("190"))

        self.assertTrue(valid_color("#123abc"))
        self.assertFalse(valid_color("123abc"))
        self.assertFalse(valid_color("#123abz"))

        self.assertTrue(valid_eye_color("brn"))
        self.assertFalse(valid_eye_color("wat"))

        self.assertTrue(valid_pid("000000001"))
        self.assertFalse(valid_pid("0123456789"))
