# Berlin Trip Subway release helper
# Requires: python3, ACME assembler, VICE x64sc

.DEFAULT_GOAL := all

.PHONY: help all test verify build inspect run clean distclean sha256 release-check fix-perms

help:
	@echo "Berlin Trip Subway build targets:"
	@echo "  make verify        - run source/release verifier"
	@echo "  make test          - alias for verify"
	@echo "  make               - verify, build PRG with ACME, inspect PRG"
	@echo "  make inspect       - inspect build/subway.prg load/start sanity"
	@echo "  make run           - run built PRG in VICE x64sc"
	@echo "  make clean         - remove build/subway.prg"
	@echo "  make distclean     - remove build directory"
	@echo "  make sha256        - print checksums"
	@echo "  make release-check - verify + inspect existing PRG"
	@echo "  make fix-perms     - restore executable bits on helper scripts"

all: build

test: verify

verify:
	python3 -S tools/verify_release.py

build: verify
	@command -v acme >/dev/null 2>&1 || { echo "error: acme assembler not found in PATH" >&2; exit 127; }
	mkdir -p build
	cd src && acme -f cbm -o ../build/subway.prg subway.s
	python3 -S tools/inspect_prg.py build/subway.prg
	@echo "built: build/subway.prg"

inspect:
	python3 -S tools/inspect_prg.py build/subway.prg

release-check: verify inspect

fix-perms:
	chmod +x build_release.sh run_vice.sh build_and_run.sh tools/verify_release.py tools/inspect_prg.py tools/print_sha256.py

run:
	@command -v x64sc >/dev/null 2>&1 || { echo "error: x64sc not found in PATH" >&2; exit 127; }
	@test -f build/subway.prg || { echo "missing build/subway.prg - run make build first" >&2; exit 1; }
	x64sc -autostartprgmode 1 -autostart build/subway.prg

clean:
	rm -f build/subway.prg

distclean: clean
	rm -rf build

sha256:
	python3 -S tools/print_sha256.py
