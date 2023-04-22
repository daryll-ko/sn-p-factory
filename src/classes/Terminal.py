from dataclasses import dataclass


@dataclass
class Terminal:
    id: int
    spike_times: list[int]

    def to_dict(self) -> dict[str, any]:
        return {"id": self.id, "spikeTimes": self.spike_times}

    @staticmethod
    def compress(s: str) -> list[int]:
        result = []
        if len(s.strip()) == 0:
            return result
        stream = list(map(int, s.split(",")))
        for index, bit in enumerate(stream):
            if bit == 1:
                result.append(index)
        return result

    @staticmethod
    def decompress(L: list[int]) -> str:
        characters = ["0" for _ in range(L[-1] + 1)]
        for index in L:
            characters[index] = "1"
        return ",".join(characters)
