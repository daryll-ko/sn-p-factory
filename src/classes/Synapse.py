from dataclasses import dataclass


@dataclass
class Synapse:
    to: int
    weight: int

    def to_dict(self) -> dict[str, any]:
        return vars(self)
