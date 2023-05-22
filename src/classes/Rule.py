import re

from dataclasses import dataclass


@dataclass
class Rule:
    regex: str
    consumed: int
    produced: int
    delay: int

    def stringify(self, in_xmp: bool) -> str:
        return (
            f"{Rule.python_to_xmp_regex(self.regex)}"
            if in_xmp
            else f"{Rule.python_to_json_regex(self.regex)}"
            "/"
            f"{Rule.get_symbol(self.consumed, in_xmp)}"
            "->"
            if in_xmp
            else "\\to " f"{Rule.get_symbol(self.produced, in_xmp)}" ";" f"{self.delay}"
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
    def get_symbol(value: int, in_xmp: bool) -> str:
        if value == 0:
            return "0" if in_xmp else "\\lambda"
        elif value == 1:
            return "a"
        else:
            return f"{value}a" if in_xmp else f"a^{{{value}}}"

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
