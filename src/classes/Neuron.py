from dataclasses import dataclass
from typing import Any, Literal, Union
from .Rule import Rule
from .Position import Position
from .Record import Record


@dataclass
class Neuron:
    id: str
    type_: Literal["regular", "input", "output"]
    position: Position
    rules: list[Rule]
    content: Union[int, list[int]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type_,
            "position": self.position.to_dict(),
            "rules": [rule.stringify(in_xml=False) for rule in self.rules],
            "content": self.content
            if isinstance(self.content, int)
            else ",".join(map(str, self.content)),
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
