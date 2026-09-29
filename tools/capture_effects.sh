#!/usr/bin/env bash
# Copyright (C) 2026 Ulf Bertilsson
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p build/review docs/screenshots/effects
for index in $(seq 0 25); do
  (cd src && acme -DSTART_PART="$index" -f cbm \
    -o "../build/review/effect-${index}.prg" subway.s)
  x64sc -warp -sounddev dummy -autostartprgmode 1 \
    -autostart "build/review/effect-${index}.prg" \
    -limitcycles 6000000 \
    -exitscreenshot "docs/screenshots/effects/effect-${index}.png"
done
