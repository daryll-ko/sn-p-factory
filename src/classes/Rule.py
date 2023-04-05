from dataclasses import dataclass


@dataclass
class Rule:
    regex: str
    consumed: int
    produced: int
    delay: int

    def to_dict(self) -> dict[str, any]:
        return vars(self)
