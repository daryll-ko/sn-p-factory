from dataclasses import dataclass


@dataclass
class Rule:
    regex: str
    consumed: int
    produced: int
    delay: int

    def to_dict(self) -> dict[str, any]:
        return vars(self)

    @staticmethod
    def form_symbol(value: int) -> str:
        if value == 0:
            return ""
        elif value == 1:
            return "a"
        else:
            return f"{value}a"

    def form_rule_old(self) -> str:
        return f"{self.regex}/{Rule.form_symbol(self.consumed)}->{Rule.form_symbol(self.produced)};{self.delay}"
