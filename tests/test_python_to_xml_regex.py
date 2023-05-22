import unittest

from src.classes.Rule import Rule


class TestPythonToXmpRegex(unittest.TestCase):
    def test_one(self):
        self.assertEqual(Rule.python_to_xml_regex(r"^a$"), r"a")

    def test_greater_than_one(self):
        self.assertEqual(Rule.python_to_xml_regex(r"^a{3}$"), r"3a")

    def test_one_with_star(self):
        self.assertEqual(Rule.python_to_xml_regex(r"^(a)*$"), r"(a)*")

    def test_greater_than_one_with_star(self):
        self.assertEqual(Rule.python_to_xml_regex(r"^(a{2})*$"), r"(2a)*")
