from dataclasses import dataclass
from typing import Any


@dataclass
class Record:
    time: int
    spikes: int

    def to_dict(self) -> dict[str, Any]:
        return vars(self)
