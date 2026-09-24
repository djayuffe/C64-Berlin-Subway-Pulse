#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v x64sc >/dev/null 2>&1; then
  echo "error: x64sc not found in PATH" >&2
  echo "install VICE, then rerun: ./run_vice.sh" >&2
  exit 127
fi

if [ ! -f build/subway.prg ]; then
  echo "missing build/subway.prg - run ./build_release.sh first" >&2
  exit 1
fi

x64sc -autostartprgmode 1 -autostart build/subway.prg
