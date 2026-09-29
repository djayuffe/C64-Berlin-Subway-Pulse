# Release notes — v1.2.5 Complete Effect Gallery

## v1.2.5

- Added native VICE captures and descriptions for all 26 active scenes.
- Added deterministic `START_PART=0..25` review builds and a capture script.
- Fixed the documented `make` entry point so it builds instead of only printing
  help.
- Kept the v1.2.4 final-pulse safety closure unchanged.

## v1.2.4 Final Pulse Polish

## Improvements

- Added `FinalMirrorCol`.
- `fc_update` now adds mirrored far sparks on rows 6 and 18.
- `fc_update` adds a small centre heartbeat on row 11.
- No row 24 writes were added.
- No VIC control writes were added.
- No dispatch changes.

## Validation

- `python3 -S tools/verify_release.py`: PASS
- final slot remains `fc_init` / `fc_update`
- SPACE skip remains present
- `DemoReturnToReady` still uses `jmp $a474`
- `make -n help`: PASS
- `make fix-perms`: PASS
- `make -n sha256`: PASS
- Full static audit: PASS
