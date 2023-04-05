from dataclasses import dataclass


@dataclass
class Synapse:
    start: int
    end: int
    weight: int

    def to_dict(self) -> dict[str, any]:
        return {"from": self.start, "to": self.end, "weight": self.weight}
