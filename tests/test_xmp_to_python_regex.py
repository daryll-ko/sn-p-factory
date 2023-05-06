import unittest

from src.classes.Rule import Rule


class TestXmpToPythonRegex(unittest.TestCase):
    def test_one(self):
        self.assertEqual(Rule.xmp_to_python_regex(r"a"), r"a")

    def test_greater_than_one(self):
        self.assertEqual(Rule.xmp_to_python_regex(r"3a"), r"a{3}")

    def test_one_with_star(self):
        self.assertEqual(Rule.xmp_to_python_regex(r"(a)*"), r"(a)*")

    def test_greater_than_one_with_star(self):
        self.assertEqual(Rule.xmp_to_python_regex(r"(2a)*"), r"(a{2})*")
