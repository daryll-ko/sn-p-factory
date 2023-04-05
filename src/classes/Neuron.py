from dataclasses import dataclass
from .Rule import Rule


@dataclass
class Neuron:
    id: int
    label: str
    spikes: int
    rules: list[Rule]
