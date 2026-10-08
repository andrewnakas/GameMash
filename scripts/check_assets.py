#!/usr/bin/env python3
"""Asset licence gate. Every file under assets/ must match exactly one [[asset]] entry
in assets/MANIFEST.toml with an allowed licence, and no retail game data may appear anywhere."""
import fnmatch
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ALLOWED = {"CC0", "original", "OFL-1.1"}
# Containers and archives that only come from retail games.
RETAIL = {".xex", ".xbe", ".iso", ".pak", ".bsa", ".ba2", ".esm", ".esp", ".ff", ".iwd", ".big", ".rpf", ".ytd", ".ydr", ".wad", ".z64", ".n64", ".sfc", ".gba", ".nds", ".psarc", ".sdat"}
SKIP_DIRS = {".git", "target", "dist", "node_modules"}

entries = tomllib.loads((ASSETS / "MANIFEST.toml").read_text())["asset"]
errors, warnings = [], []
for e in entries:
    if e["license"] not in ALLOWED and not e.get("replace"):
        errors.append(f"{e['what']}: licence {e['license']} is not in {sorted(ALLOWED)}")
    elif e.get("replace"):
        warnings.append(f"{e['what']} ({e['license']}) is marked for replacement")

for f in sorted(p for p in ASSETS.rglob("*") if p.is_file()):
    rel = f.relative_to(ASSETS).as_posix()
    if rel in ("MANIFEST.toml", "CREDITS.md") or f.name == ".DS_Store":
        continue
    hits = [e for e in entries if any(fnmatch.fnmatchcase(rel, g) for g in e["files"])]
    if len(hits) != 1:
        errors.append(f"assets/{rel}: matched by {len(hits)} manifest entries (need exactly 1)")

for f in ROOT.rglob("*"):
    if f.is_file() and f.suffix.lower() in RETAIL and not SKIP_DIRS & set(f.relative_to(ROOT).parts):
        errors.append(f"{f.relative_to(ROOT)}: retail game data extension {f.suffix}")

for w in warnings:
    print(f"::warning::{w}")
for e in errors:
    print(f"::error::{e}")
print(f"check_assets: {len(entries)} entries, {len(errors)} errors, {len(warnings)} to replace")
sys.exit(1 if errors else 0)
