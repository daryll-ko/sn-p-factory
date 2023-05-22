from dataclasses import dataclass
from typing import Any


@dataclass
class Synapse:
    from_: str
    to: str
    weight: int

    def to_dict(self) -> dict[str, Any]:
        return {"from": self.from_, "to": self.to, "weight": self.weight}
