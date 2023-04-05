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
