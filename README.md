# C64 - Berlin Trip Subway Pulse

Copyright © 2026 Ulf Bertilsson. Licensed under the
[GNU General Public License v3.0 or later](LICENSE).

A C64/ACME/VICE release of the Berlin Transit SID-techno megademo. This
version focuses on a stable final-scene pulse treatment while retaining the
original scene controls and warm-start return.

![VICE runtime capture](docs/screenshots/effects/effect-0.png)

## Requirements

- [ACME](https://sourceforge.net/projects/acme-crossass/) cross-assembler
- Python 3 for the release verifier
- [VICE](https://vice-emu.sourceforge.io/) `x64sc` for interactive playback

## Improvements

Safe final-scene polish:
- mirrored spark pairs on rows 6 and 18
- tiny centre heartbeat on row 11
- final glow rows still clear before redraw
- row 24 remains untouched except by the global scroller
- no VIC control writes
- no pointer indirection in final update

Preserved:
- SPACE skips current part/card
- Black Orbit 2 removed from final slot
- final slot uses safe `fc_init` / `fc_update`
- 26 active slots
- READY warm-start return
- verifier-first build
- PRG inspection after ACME

## Build and run

```bash
make
make run
```

`make` verifies the source, assembles `build/subway.prg`, and validates its
load address. `make run` opens that PRG in VICE. The demo starts through the
embedded BASIC loader (`SYS 2061`).

## Controls

- `SPACE` skips the active part or card.
- A normal C64 reset returns to the BASIC prompt; the demo also preserves its
  READY warm-start return path.

## Complete effect gallery

The complete 26-scene dispatch, descriptions, and native VICE captures are in
[docs/EFFECTS.md](docs/EFFECTS.md). Each scene can be reviewed deterministically
with the assembler-time `START_PART=0..25` selector.
