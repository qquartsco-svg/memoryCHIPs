#!/usr/bin/env python3
"""SHA-256 manifest generator / verifier for Memory Chip Readiness Foundation.

Usage:
    python scripts/generate_signature.py            # generate SIGNATURE.sha256
    python scripts/generate_signature.py --verify   # verify against SIGNATURE.sha256
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIG_FILE = ROOT / "SIGNATURE.sha256"

INCLUDE_GLOBS = [
    "memory_chip_readiness/**/*.py",
    "memory_chip_readiness/py.typed",
    "pyproject.toml",
    "LICENSE",
]


def _collect_files() -> list[Path]:
    files: list[Path] = []
    for pattern in INCLUDE_GLOBS:
        files.extend(ROOT.glob(pattern))
    return sorted(set(files))


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def generate() -> None:
    lines: list[str] = []
    for f in _collect_files():
        rel = f.relative_to(ROOT)
        lines.append(f"{_hash_file(f)}  {rel}")
    SIG_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Wrote {len(lines)} hashes to {SIG_FILE.name}")


def verify() -> bool:
    if not SIG_FILE.exists():
        print("[FAIL] SIGNATURE.sha256 not found", file=sys.stderr)
        return False
    ok = True
    for line in SIG_FILE.read_text(encoding="utf-8").strip().splitlines():
        expected, _, rel = line.partition("  ")
        path = ROOT / rel
        if not path.exists():
            print(f"[MISSING] {rel}")
            ok = False
            continue
        actual = _hash_file(path)
        if actual != expected:
            print(f"[MISMATCH] {rel}")
            ok = False
        else:
            print(f"[OK] {rel}")
    if ok:
        print("\nAll files verified.")
    else:
        print("\nVerification FAILED.", file=sys.stderr)
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        sys.exit(0 if verify() else 1)
    generate()
