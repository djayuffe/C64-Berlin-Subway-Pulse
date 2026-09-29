#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python3 -S tools/verify_release.py

if ! command -v acme >/dev/null 2>&1; then
  echo "error: acme assembler not found in PATH" >&2
  echo "expected command: acme -f cbm -o build/subway.prg src/subway.s" >&2
  exit 127
fi

mkdir -p build
cd src
acme -f cbm -o ../build/subway.prg subway.s
cd ..
python3 -S tools/inspect_prg.py build/subway.prg
echo "built: build/subway.prg"
