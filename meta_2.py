import subprocess
from pathlib import Path

for i in range(2, 10**2):
    s = "1" + "0" * (i - 2) + "1"
    file = Path("data") / "json" / "multiples_of_2.json"
    command = f"./snp.py ch {file} lit -b {s}"
    subprocess.run(command.split())
