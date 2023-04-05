from dataclasses import dataclass


@dataclass
class Synapse:
    start: int
    end: int
    weight: int
