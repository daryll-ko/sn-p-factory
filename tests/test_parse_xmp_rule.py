from src.classes.Rule import Rule
from src.parsers import parse_xmp_rule

import unittest


class TestXmpRuleParser(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(parse_xmp_rule("a/a->a;0"), Rule("a", 1, 1, 0))

    def test_zero_produced(self):
        self.assertEqual(parse_xmp_rule("a/a->0;0"), Rule("a", 1, 0, 0))

    def test_multiple_consumed(self):
        self.assertEqual(parse_xmp_rule("a/2a->a;0"), Rule("a", 2, 1, 0))

    def test_multiple_produced(self):
        self.assertEqual(parse_xmp_rule("a/2a->2a;0"), Rule("a", 2, 2, 0))

    def test_complex_regex(self):
        self.assertEqual(parse_xmp_rule("aU(2a)+/a->a;0"), Rule("aU(2a)+", 1, 1, 0))

    def test_nonzero_delay(self):
        self.assertEqual(parse_xmp_rule("a/a->a;1"), Rule("a", 1, 1, 1))
