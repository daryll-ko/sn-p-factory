from dataclasses import dataclass
from typing import Optional


@dataclass
class TestName:
    name: str
    time: Optional[int] = None

    def make_filename(self) -> str:
        time_part = f"[{str(self.time).zfill(3)}]" if self.time else ""
        return f"{self.name}{time_part}"
