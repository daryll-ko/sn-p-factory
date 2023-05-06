import re

from dataclasses import dataclass


@dataclass
class Rule:
    regex: str
    consumed: int
    produced: int
    delay: int

    def to_dict(self) -> dict[str, any]:
        return vars(self)

    def form_rule_xmp(self) -> str:
        return (
            f"{self.regex}/{Rule.get_symbol(self.consumed)}"
            f"->{Rule.get_symbol(self.produced)};{self.delay}"
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
            return ""
        elif value == 1:
            return "a"
        else:
            return f"{value}a"

    @staticmethod
    def get_python_regex(s: str) -> str:
        return re.sub(
            r"\\cup",
            "|",
            re.sub(
                r"\^\{\+\}",
                "+",
                re.sub(
                    r"\^\{?\*\}?",
                    "*",
                    re.sub(r"\^\{?(\d+)\}?", r"{\1}", s),
                ),
            ),
        ).replace(" ", "")
