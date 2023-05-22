from dataclasses import dataclass
from typing import Optional


@dataclass
class TestName:
    name: str
    inputs: Optional[list[int]] = None
    time: Optional[int] = None

    def make_filename(self) -> str:
        inputs_part = (
            f"({','.join(map(str, self.inputs))})" if self.inputs is not None else ""
        )
        time_part = f"[{str(self.time).zfill(3)}]" if self.time else ""
        return f"{self.name}{inputs_part}{time_part}"
