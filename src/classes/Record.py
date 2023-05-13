from dataclasses import dataclass


@dataclass
class Record:
    time: int
    spikes: int

    def to_dict(self) -> dict[str, any]:
        return vars(self)
