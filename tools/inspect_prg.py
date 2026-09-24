#!/usr/bin/env python3
from pathlib import Path
import sys, hashlib

ROOT = Path(__file__).resolve().parents[1]
prg = ROOT / "build" / "subway.prg"

if len(sys.argv) > 1:
    prg = Path(sys.argv[1])
    if not prg.is_absolute():
        prg = (ROOT / prg).resolve()

if not prg.exists():
    print(f"FAIL: missing PRG: {prg}")
    sys.exit(1)

data = prg.read_bytes()
errors = []

if len(data) < 16:
    errors.append(f"PRG too small: {len(data)} bytes")

load = data[0] | (data[1] << 8) if len(data) >= 2 else None
payload_len = max(0, len(data) - 2)
end_exclusive = (load + payload_len) & 0xffff if load is not None else None

if load != 0x0801:
    errors.append(f"unexpected load address ${load:04x}; expected $0801")

if payload_len <= 0:
    errors.append("empty PRG payload")

if end_exclusive is not None and end_exclusive <= load:
    errors.append(f"PRG wraps address space: load=${load:04x}, end=${end_exclusive:04x}")

# BASIC stub sanity: should at least begin in BASIC area and contain SYS token $9e early.
early = data[2:80]
if 0x9e not in early:
    errors.append("BASIC SYS token $9e not found in first 80 payload bytes")

if errors:
    print("FAIL: PRG inspection")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("PASS: PRG inspection")
print(f"file={prg}")
print(f"load=${load:04x}")
print(f"payload_bytes={payload_len}")
print(f"end_exclusive=${end_exclusive:04x}")
print("sha256=" + hashlib.sha256(data).hexdigest())
