#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./build_release.sh
./run_vice.sh
