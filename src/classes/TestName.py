from dataclasses import dataclass
from typing import Optional


@dataclass
class TestName:
    name: str
    time: Optional[int] = None

    def make_filename(self) -> str:
        name_part = self.name.replace(" ", "_")
        time_part = f"[{str(self.time).zfill(3)}]" if self.time else ""
        return f"{name_part}{time_part}"
