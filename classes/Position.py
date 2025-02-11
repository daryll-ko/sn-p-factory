from dataclasses import dataclass
from typing import Any


@dataclass
class Position:
    x: int
    y: int

    def to_dict(self) -> dict[str, Any]:
        return vars(self)
