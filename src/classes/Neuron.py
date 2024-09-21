from dataclasses import dataclass
from typing import Any, Literal, Union

from .Position import Position
from .Rule import Rule


@dataclass
class Neuron:
    id: str
    type_: Literal["regular", "input", "output"]
    position: Position
    rules: list[Rule]
    content: Union[int, list[int]]

    def to_dict(self) -> dict[str, Any]:
        d = {
            "id": self.id,
            "type": self.type_,
            "position": self.position.to_dict(),
            "content": self.content
            if isinstance(self.content, int)
            else "".join(map(str, self.content)),
        }
        if self.type_ == "regular":
            d["rules"] = [rule.stringify(in_xml=False) for rule in self.rules]
        return d
