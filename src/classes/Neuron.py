from dataclasses import dataclass
from .Rule import Rule


@dataclass
class Neuron:
    id: int
    label: str
    position: tuple[int, int]
    rules: list[Rule]
    spikes: int
    downtime: int

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self.id,
            "label": self.label,
            "position": {
                "x": self.position[0],
                "y": self.position[1],
            },
            "rules": [rule.to_dict() for rule in self.rules],
            "spikes": self.spikes,
            "downtime": self.downtime,
        }
