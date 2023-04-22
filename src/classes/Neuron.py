from dataclasses import dataclass
from .Rule import Rule
from .Position import Position


@dataclass
class Neuron:
    id: int
    label: str
    position: Position
    rules: list[Rule]
    spikes: int
    downtime: int

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self.id,
            "label": self.label,
            "position": self.position.to_dict(),
            "rules": [rule.to_dict() for rule in self.rules],
            "spikes": self.spikes,
            "downtime": self.downtime,
        }
