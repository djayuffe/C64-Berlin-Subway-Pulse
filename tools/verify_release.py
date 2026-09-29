#!/usr/bin/env python3
from pathlib import Path
import re, sys, hashlib

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "subway.s"
text = SRC.read_text(encoding="latin-1")
lines = text.splitlines()

def strip_comment(line: str) -> str:
    out = []
    in_str = False
    for c in line:
        if c == '"':
            in_str = not in_str
            out.append(c)
        elif c == ';' and not in_str:
            break
        else:
            out.append(c)
    return "".join(out)

def code_no_strings(line: str) -> str:
    out = []
    in_str = False
    for c in line:
        if c == '"':
            in_str = not in_str
            out.append(" ")
        elif c == ';' and not in_str:
            break
        elif in_str:
            out.append(" ")
        else:
            out.append(c)
    return "".join(out)

errors = []

def count_word(label):
    m = re.search(rf'^{label}:\n((?:\s*!word .+\n)+)', text, re.M)
    if not m:
        return None, []
    vals = []
    for line in m.group(1).splitlines():
        data = strip_comment(line)
        if "!word" in data:
            vals += [x.strip() for x in data.split("!word", 1)[1].split(",") if x.strip()]
    return len(vals), vals

def count_byte(label):
    m = re.search(rf'^{label}:?\s*!byte\s+(.+)$', text, re.M)
    if not m:
        return None, []
    vals = [x.strip() for x in strip_comment(m.group(0)).split("!byte", 1)[1].split(",") if x.strip()]
    return len(vals), vals

for lab in ["InitTbl", "UpdateTbl"]:
    c, _ = count_word(lab)
    if c != 26:
        errors.append(f"{lab}: expected 26, got {c}")

if "START_PART = 0" not in text or "lda #START_PART" not in text:
    errors.append("deterministic START_PART review selector is missing")

for lab in ["PartFramesTbl_Lo", "PartFramesTbl_Hi", "PartBorderTbl", "PartBgTbl", "CardNameLo", "CardNameHi"]:
    c, _ = count_byte(lab)
    if c != 26:
        errors.append(f"{lab}: expected 26, got {c}")

if len(re.findall(r"^CardName\d+:", text, re.M)) != 26:
    errors.append("CardName definitions: expected 26")
if len(re.findall(r"^CardSub\d+:", text, re.M)) != 0:
    errors.append("CardSub definitions must be 0")

# ACME-safe zone names and unquoted hyphen identifiers.
for n, line in enumerate(lines, 1):
    code = code_no_strings(line)
    m = re.match(r'^\s*!zone\s+(.+)$', code)
    if m:
        name = m.group(1).strip()
        if name and not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
            errors.append(f"line {n}: invalid !zone name {name!r}")
    if re.search(r'[A-Za-z_][A-Za-z0-9_]*-[A-Za-z_][A-Za-z0-9_]*', code):
        errors.append(f"line {n}: unquoted hyphenated identifier/expression residue: {code.strip()}")

# Removed crash-part must stay removed.
for banned in ["rb_init:", "rb_update:", "!zone rasterboottunnel", "rasterboot", "raster boot", "RasterBoot"]:
    if banned.lower() in text.lower():
        errors.append(f"stale removed crash-part term present: {banned}")

# Row 24 is scroller-only.  Derive the GlobalScroller block dynamically;
# hard-coded line windows break when small routines are inserted above it.
gs_start = text.find("GlobalScroller:")
gs_end = text.find("; ============================================================================", gs_start + len("GlobalScroller:"))
offset = 0
for n, line in enumerate(lines, 1):
    line_pos = offset
    offset += len(line) + 1
    if "SCREEN+24*40" in line or "COLOR+24*40" in line:
        if gs_start < 0 or gs_end < 0 or not (gs_start <= line_pos < gs_end):
            errors.append(f"line {n}: row 24 write outside global scroller")

# VIC register ownership.
allowed_contexts = ["SetupVIC:", "MegaMain_IRQ:", "MegaSplit_IRQ:", "DemoReturnToReady:"]
for reg in ["VIC_CTRL2", "VIC_CTRL1", "VIC_MEMPTR"]:
    for n, line in enumerate(lines, 1):
        if f"sta {reg}" in strip_comment(line):
            ctx = "\n".join(lines[max(0, n-30):n+8])
            if not any(label in ctx for label in allowed_contexts):
                errors.append(f"line {n}: effect/runtime writes {reg}")

# Binary assets.
for n, line in enumerate(lines, 1):
    for m in re.finditer(r'!binary\s+"([^"]+)"', strip_comment(line)):
        if not (SRC.parent / m.group(1)).exists():
            errors.append(f"line {n}: missing binary asset {m.group(1)}")

# v1.2.4 final pulse polish guards.
for required in ["FinalMirrorCol:", "sta SCREEN+6*40,y", "sta SCREEN+18*40,y", "sta COLOR+6*40,y", "sta COLOR+18*40,y", "sta SCREEN+11*40+18", "sta SCREEN+11*40+21"]:
    if required not in text:
        errors.append(f"missing v1.2.4 final pulse polish requirement: {required}")
fc_start = text.find("fc_update:")
fc_end = text.find("FinalClosureTitle:", fc_start)
fc_body = text[fc_start:fc_end] if fc_start >= 0 and fc_end > fc_start else ""
for forbidden in ["SCREEN+24*40", "COLOR+24*40", "VIC_CTRL1", "VIC_CTRL2", "VIC_MEMPTR", "(TXTP)"]:
    if forbidden in fc_body:
        errors.append(f"fc_update contains forbidden pattern: {forbidden}")

# v1.2.3 polish guards.
if ".fc_clear:" not in text:
    errors.append("fc_update must clear final glow rows before redraw")
if "sta SCREEN+7*40,x\n        sta SCREEN+17*40,x" not in text:
    errors.append("fc_update must redraw only safe rows 7 and 17")
if "sta COLOR+11*40,x" not in text:
    errors.append("DemoEyeCandy/final title colour row 11 sparkle missing")

# Keyboard/skip controls regression checks.
if "cmp #$20                ; SPACE -> skip current part / finish current card" not in text:
    errors.append("SPACE must be documented/implemented as skip, not pause")
if "jsr SkipPart" not in text:
    errors.append("ReadKeys must call SkipPart on SPACE")
if "SkipPart:" not in text:
    errors.append("missing SkipPart routine")
if "jmp BeginTransition" not in text:
    errors.append("SkipPart must jump to BeginTransition for running parts")
if "jmp $a474" not in text:
    errors.append("DemoReturnToReady must jump to BASIC warm start, not RTS back into demo loop")
if "SPACE -> toggle pause" in text:
    errors.append("stale SPACE pause behavior remains")

# Final slot crash guard: black orbit ii must not be used as final closure.
_, init_vals_guard = count_word("InitTbl")
_, upd_vals_guard = count_word("UpdateTbl")
if init_vals_guard and init_vals_guard[-1] != "fc_init":
    errors.append(f"final InitTbl slot must be fc_init, got {init_vals_guard[-1]}")
if upd_vals_guard and upd_vals_guard[-1] != "fc_update":
    errors.append(f"final UpdateTbl slot must be fc_update, got {upd_vals_guard[-1]}")
for required in ["fc_init:", "fc_update:", "FinalClosureTitle:", "FinalClosureColors:", "FinalClosureChars:"]:
    if required not in text:
        errors.append(f"missing safe final closure symbol: {required}")
if "CardName25: !scr \"black orbit" in text:
    errors.append("CardName25 must not be black orbit")

# Known data-load/store regression checks.
if "lda NfxGoldBorder,x\n        lda #$00" in text:
    errors.append("gt_update loads NfxGoldBorder,x but discards it before storing")
if "lda NfxGoldBorder,x\n        sta partBorder" not in text:
    errors.append("gt_update must store NfxGoldBorder,x to partBorder")

# Release workflow files and executable bits.
required_files = ["Makefile", "build_release.sh", "run_vice.sh", "build_and_run.sh", "tools/verify_release.py", "tools/inspect_prg.py", "tools/print_sha256.py"]
for rel in required_files:
    p = ROOT / rel
    if not p.exists():
        errors.append(f"missing release workflow file: {rel}")

for rel in ["build_release.sh", "run_vice.sh", "build_and_run.sh", "tools/verify_release.py", "tools/inspect_prg.py", "tools/print_sha256.py"]:
    p = ROOT / rel
    if p.exists() and not (p.stat().st_mode & 0o111):
        errors.append(f"not executable: {rel}")

mf = ROOT / "Makefile"
if mf.exists():
    mf_text = mf.read_text(encoding="utf-8")
    for needle in ["help:", "test: verify", "verify:", "build: verify", "inspect:", "release-check: verify inspect", "fix-perms:", "run:", "clean:", "distclean:", "sha256:"]:
        if needle not in mf_text:
            errors.append(f"Makefile missing target/dependency: {needle}")

if errors:
    print("FAIL: release verification")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("PASS: release verification")
print("source_sha256=" + hashlib.sha256(SRC.read_bytes()).hexdigest())
