import unittest

from src.classes.Rule import Rule


class TestJsonToPythonRegex(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(Rule.json_to_python_regex(r""), r"")

    def test_basic(self):
        self.assertEqual(Rule.json_to_python_regex(r"a"), r"a")

    def test_exponent(self):
        self.assertEqual(Rule.json_to_python_regex(r"a^{2}"), r"a{2}")

    def test_exponent_no_braces(self):
        self.assertEqual(Rule.json_to_python_regex(r"a^2"), r"a{2}")

    def test_plus(self):
        self.assertEqual(Rule.json_to_python_regex(r"a^{+}"), r"a+")

    def test_plus_no_braces(self):
        self.assertEqual(Rule.json_to_python_regex(r"a^+"), r"a+")

    def test_star(self):
        self.assertEqual(Rule.json_to_python_regex(r"a^{*}"), r"a*")

    def test_star_no_braces(self):
        self.assertEqual(Rule.json_to_python_regex(r"a^*"), r"a*")

    def test_union(self):
        self.assertEqual(Rule.json_to_python_regex(r"a \cup a"), r"a|a")

    def test_complex(self):
        self.assertEqual(
            Rule.json_to_python_regex(r"(a^{2} \cup a^{3})^{+} \cup a^{*}"),
            r"(a{2}|a{3})+|a*",
        )

    def test_complex_no_braces(self):
        self.assertEqual(
            Rule.json_to_python_regex(r"(a^2 \cup a^3)^+ \cup a^*"), r"(a{2}|a{3})+|a*"
        )
