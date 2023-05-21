import re

from dataclasses import dataclass
from typing import Any


@dataclass
class Rule:
    regex: str
    consumed: int
    produced: int
    delay: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "regex": Rule.python_to_json_regex(self.regex),
            "consumed": self.consumed,
            "produced": self.produced,
            "delay": self.delay,
        }

    def form_rule_xmp(self) -> str:
        return (
            f"{Rule.python_to_xmp_regex(self.regex)}"
            "/"
            f"{Rule.get_symbol(self.consumed)}"
            "->"
            f"{Rule.get_symbol(self.produced)}"
            ";"
            f"{self.delay}"
        )

    @staticmethod
    def get_value(symbol: str) -> int:
        if symbol == "0":
            return 0
        elif symbol == "a":
            return 1
        else:
            return int(symbol.replace("a", ""))

    @staticmethod
    def get_symbol(value: int) -> str:
        if value == 0:
            return "0"
        elif value == 1:
            return "a"
        else:
            return f"{value}a"

    @staticmethod
    def json_to_python_regex(s: str) -> str:
        substituted = re.sub(
            r"\\cup",
            "|",
            re.sub(
                r"\^\{?\+\}?",
                "+",
                re.sub(
                    r"\^\{?\*\}?",
                    "*",
                    re.sub(r"\^\{?(\d+)\}?", r"{\1}", s),
                ),
            ),
        ).replace(" ", "")
        return f"^{substituted}$"

    @staticmethod
    def python_to_json_regex(s: str) -> str:
        return re.sub(
            r"\|",
            r" \\cup ",
            re.sub(
                r"\+",
                r"^{+}",
                re.sub(r"\*", r"^{*}", re.sub(r"\{(\d+)\}", r"^{\1}", s[1:-1])),
            ),
        )

    @staticmethod
    def xmp_to_python_regex(s: str) -> str:
        substituted = re.sub(r"(\d+)a", r"a{\1}", s)
        return f"^{substituted}$"

    @staticmethod
    def python_to_xmp_regex(s: str) -> str:
        return re.sub(r"a\{(\d+)\}", r"\1a", s[1:-1])
