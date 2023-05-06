import unittest

from src.classes.Rule import Rule


class TestPythonToJsonRegex(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(Rule.python_to_json_regex(r""), r"")

    def test_basic(self):
        self.assertEqual(Rule.python_to_json_regex(r"a"), r"a")

    def test_exponent(self):
        self.assertEqual(Rule.python_to_json_regex(r"a{2}"), r"a^{2}")

    def test_exponent_multiple_digits(self):
        self.assertEqual(Rule.python_to_json_regex(r"a{123}"), r"a^{123}")

    def test_plus(self):
        self.assertEqual(Rule.python_to_json_regex(r"a+"), r"a^{+}")

    def test_star(self):
        self.assertEqual(Rule.python_to_json_regex(r"a*"), r"a^{*}")

    def test_union(self):
        self.assertEqual(Rule.python_to_json_regex(r"a|a"), r"a \cup a")

    def test_complex(self):
        self.assertEqual(
            Rule.python_to_json_regex(r"(a{2}|a{3})+|a*"),
            r"(a^{2} \cup a^{3})^{+} \cup a^{*}",
        )
