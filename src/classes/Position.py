from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def to_dict(self) -> dict[str, any]:
        return vars(self)
