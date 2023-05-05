from dataclasses import dataclass
from .Rule import Rule
from .Position import Position
from .Synapse import Synapse


@dataclass
class Neuron:
    id: int
    label: str
    position: Position
    rules: list[Rule]
    spikes: int
    downtime: int
    synapses: list[Synapse]
    is_input: bool
    is_output: bool
    spike_times: list[int]

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self.id,
            "label": self.label,
            "position": self.position.to_dict(),
            "rules": [rule.to_dict() for rule in self.rules],
            "spikes": self.spikes,
            "downtime": self.downtime,
            "synapses": [synapse.to_dict() for synapse in self.synapses],
            "isInput": self.is_input,
            "isOutput": self.is_output,
            "spikeTimes": self.spike_times,
        }

    @staticmethod
    def compress_to_spike_train(s: str) -> list[int]:
        result = []
        if len(s.strip()) == 0:
            return result
        stream = list(map(int, s.split(",")))
        for index, bit in enumerate(stream):
            if bit == 1:
                result.append(index)
        return result

    @staticmethod
    def decompress_spike_train(L: list[int]) -> str:
        characters = ["0" for _ in range(L[-1] + 1)]
        for index in L:
            characters[index] = "1"
        return ",".join(characters)
