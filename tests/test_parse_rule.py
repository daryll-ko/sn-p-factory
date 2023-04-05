from src.classes.Rule import Rule
from src.parsers import parse_rule

import unittest


class TestRuleParser(unittest.TestCase):
    def test_basic(self):
        expected = Rule("a", 1, 1, 0)
        self.assertEqual(parse_rule("a/a->a;0"), expected)
