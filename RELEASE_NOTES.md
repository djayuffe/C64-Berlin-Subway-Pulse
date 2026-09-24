# Release notes — v1.2.4 Final Pulse Polish

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
