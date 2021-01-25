from unittest import TestCase

from aoc2020.day7.day7 import make_rule, Rule


class Test(TestCase):
    def test_make_rule(self):
        with self.assertRaises(ValueError):
            make_rule("")
        self.assertEqual(
            Rule("light red", ((1, "bright white"), (2, "muted yellow"))),
            make_rule("light red bags contain 1 bright white bag, 2 muted yellow bags.")
        )
