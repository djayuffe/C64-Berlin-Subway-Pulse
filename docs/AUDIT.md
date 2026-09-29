# Release audit

The release gate is `make verify`, followed by ACME assembly and PRG
inspection. `tools/verify_release.py` checks the 26-entry dispatch and timing
tables, the safe final-pulse slot, row-24 ownership, VIC register ownership,
binary assets, skip controls, and executable release helpers.

The build then verifies the `$0801` load address, BASIC `SYS 2061` token, and
non-wrapping PRG payload. `make` is the default target and produces
`build/subway.prg`.

The complete visual review is in [EFFECTS.md](EFFECTS.md). Each frame is a
native VICE capture from a deterministic `START_PART` review build.
