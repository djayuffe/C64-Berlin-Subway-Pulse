#!/usr/bin/env python3
from pathlib import Path
import hashlib

root = Path(".")
for p in sorted(root.rglob("*")):
    if p.is_file() and p.name != "SHA256SUMS.txt":
        print(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p}")
