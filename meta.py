import subprocess
from pathlib import Path

for i in range(10**2):
    file = Path("data") / "json" / "multiples_of_2.json"
    command = f"./snp.py ch {file} dis -n {i}"
    subprocess.run(command.split())
