#!/usr/bin/env python3
"""Encrypt curriculum modules 1-7 into vault/ and remove the plaintext.

One-shot build step (already run for the shipped repo; rerun only if you
rename/rewrite phase docs). Phase 0 stays plaintext — it is the entry
module. Uses the same stdlib keystream as unlock.py.
"""
import base64
import hashlib
import importlib.util
import json
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "gates"))
sys.path.insert(0, str(ROOT))
from unlock import xor  # noqa: E402  (reuse the engine's keystream)

CURRICULUM = ROOT / "curriculum"
VAULT = ROOT / "vault"


def gate_stems():
    stems = []
    for n in range(8):
        spec = importlib.util.spec_from_file_location(
            f"gate{n}", ROOT / "gates" / f"gate{n}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if getattr(mod, "NEXT_DOC", None):
            stems.append(mod.NEXT_DOC)
    return stems


def seal(stem, manifest, reseal):
    entry_file = VAULT / f"{stem}.bin"
    src = CURRICULUM / f"{stem}.md"
    if not src.exists():
        sys.exit(f"missing plaintext module: {src}")
    plain = src.read_bytes()
    key = secrets.token_bytes(32)
    entry_file.write_bytes(xor(plain, key))
    manifest[stem] = {
        "file": entry_file.name,
        "key": base64.b64encode(key).decode(),
        "sha256": hashlib.sha256(plain).hexdigest(),
    }
    src.unlink()   # plaintext NEVER stays on disk
    print(f"  {'re' if reseal else ''}sealed: {src.name} -> vault/{entry_file.name}")


def main():
    VAULT.mkdir(exist_ok=True)
    mpath = VAULT / "manifest.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    args = sys.argv[1:]

    if args and args[0] in ("--reseal", "--reseal-all"):
        # maintainer mode: plaintext docs must currently be on disk
        # (edited while decrypted); each gets a FRESH key + sha256.
        stems = gate_stems() if args[0] == "--reseal-all" else args[1:]
        for stem in stems:
            if stem not in gate_stems():
                sys.exit(f"unknown module stem: {stem}")
            seal(stem, manifest, reseal=True)
        mpath.write_text(json.dumps(manifest, indent=2))
        print(f"done: {len(stems)} module(s) resealed")
        return

    made = 0
    for stem in gate_stems():
        if (VAULT / f"{stem}.bin").exists():
            print(f"  already vaulted: {stem}   (use --reseal {stem} to update)")
            continue
        seal(stem, manifest, reseal=False)
        made += 1
    if made:
        mpath.write_text(json.dumps(manifest, indent=2))
    print(f"done: {made} module(s) newly sealed")


if __name__ == "__main__":
    main()
