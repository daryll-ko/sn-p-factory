from dataclasses import dataclass
from typing import Any
from .Rule import Rule
from .Position import Position
from .Record import Record


@dataclass
class Neuron:
    id: str
    position: Position
    rules: list[Rule]
    spikes: int
    is_input: bool
    input_log: list[Record]
    is_output: bool
    output_log: list[Record]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "position": self.position.to_dict(),
            "rules": [rule.stringify(in_xmp=False) for rule in self.rules],
            "spikes": self.spikes,
            "isInput": self.is_input,
            "inputLog": [record.to_dict() for record in self.input_log],
            "isOutput": self.is_output,
            "outputLog": [record.to_dict() for record in self.output_log],
        }

    @staticmethod
    def compress_log(s: str) -> list[Record]:
        result: list[Record] = []
        if len(s.strip()) == 0:
            return result
        stream = list(map(int, s.split(",")))
        for time, spikes in enumerate(stream):
            if spikes > 0:
                result.append(Record(time, spikes))
        return result

    @staticmethod
    def decompress_log(L: list[Record]) -> str:
        values = [0 for _ in range(L[-1].time + 1)]
        for log in L:
            values[log.time] = log.spikes
        return ",".join(map(str, values))
