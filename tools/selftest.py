#!/usr/bin/env python3
"""Self-test for the gate/unlock machinery.

Runs in a THROWAWAY COPY of the repo (never touches real progress).
Scenarios: fresh status, unpassed-stub, order-lock, full 0->7 pass chain,
certificate, reset, tamper (int/float/function), resync, leak warning,
manifest integrity. Exit 0 + "SELFTEST OK" on success.
"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = Path(tempfile.mkdtemp(prefix="ptz-selftest-"))
REPO = TMP / "repo"

sys.path.insert(0, str(ROOT / "gates"))

FUNC_SNIPPETS = {
    (1, "q12"): """
def _ans(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True
""",
    (2, "q12"): """
def _ans(n):
    import math
    return n * (math.log(n) + math.log(math.log(n)) - 1)
""",
    (3, "q12"): """
def _ans(x):
    import math
    s = bytearray(b"\\x01" * (int(x) + 1))
    s[0] = s[1] = 0
    for i in range(2, int(x) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return sum(math.log(i) for i in range(2, int(x) + 1) if s[i])
""",
    (4, "q10"): """
def _ans(coeffs, R):
    import numpy as np
    return int((np.abs(np.roots(coeffs)) < R).sum())
""",
    (5, "q10"): """
def _ans(x):
    import math
    s = bytearray(b"\\x01" * (int(x) + 1))
    s[0] = s[1] = 0
    for i in range(2, int(x) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    tot = 0.0
    for q in range(2, int(x) + 1):
        if s[q]:
            pk = float(q)
            while pk <= x:
                tot += math.log(q)
                pk *= q
    return tot
""",
    (6, "q10"): """
def _ans(t):
    k = len(t)
    primes = [p for p in range(2, k + 1)
              if all(p % d for d in range(2, int(p ** 0.5) + 1))]
    return all(len({x % p for x in t}) < p for p in primes)
""",
    (7, "q10"): """
def _ans(n):
    def isp(m):
        if m < 2:
            return False
        d = 2
        while d * d <= m:
            if m % d == 0:
                return False
            d += 1
        return True
    c, m = 0, 1
    while True:
        m += 1
        if isp(m):
            c += 1
            if c == n:
                return m
""",
}

FAILURES = []


def ok(cond, label):
    tag = "PASS" if cond else "FAIL"
    print(f"  [{tag}] {label}")
    if not cond:
        FAILURES.append(label)


def gate_mod(n):
    spec = importlib.util.spec_from_file_location(
        f"gate{n}", ROOT / "gates" / f"gate{n}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def correct_answers_source(n):
    gate = gate_mod(n)
    kb = gate.keybook()
    snippets, entries = [], []
    for q in gate.questions():
        qid = q["id"]
        spec = kb[qid]
        if spec[0] == "func":
            src = FUNC_SNIPPETS[(n, qid)]
            snippets.append(src)
            entries.append(f'    "{qid}": _ans,\n')
            # rename per-question to avoid clashes (only one func per gate,
            # but be safe)
        else:
            entries.append(f'    "{qid}": {spec[1]!r},\n')
    body = "".join(entries)
    return "ANSWERS = {\n" + body + "}\n", "\n".join(snippets)


def write_answers(n, mutate=None):
    body, snippets = correct_answers_source(n)
    if mutate:
        body = mutate(body)
    (REPO / "answers" / f"phase-{n}.py").write_text(snippets + body)


def run(*args, expect_rc=None):
    p = subprocess.run([sys.executable, "unlock.py", *map(str, args)],
                       cwd=REPO, capture_output=True, text=True)
    out = p.stdout + p.stderr
    if expect_rc is not None:
        ok(p.returncode == expect_rc,
           f"unlock.py {' '.join(map(str, args))} -> rc={p.returncode}"
           f" (want {expect_rc})")
    return p, out


def doc_path(stem):
    return REPO / "curriculum" / f"{stem}.md"


def reset():
    run("reset", "--yes", expect_rc=0)


def pass_gate(n):
    write_answers(n)
    p, out = run("grade", n, expect_rc=0)
    return p, out


def main():
    print(f"selftest repo: {REPO}")
    shutil.copytree(ROOT, REPO, ignore=shutil.ignore_patterns(
        ".git", "data", "__pycache__", ".unlock_state", "CERTIFICATE.txt",
        ".venv"))

    print("\n[suite] structure & manifest")
    import base64, hashlib, json
    sys.path.insert(0, str(REPO))
    from unlock import xor
    man = json.loads((REPO / "vault" / "manifest.json").read_text())
    ok(len(man) == 7, f"manifest has 7 vaulted modules (got {len(man)})")
    bad = [s for s, e in man.items()
           if hashlib.sha256(xor((REPO / "vault" / e["file"]).read_bytes(),
                                 base64.b64decode(e["key"]))).hexdigest()
           != e["sha256"]]
    ok(not bad, f"vault sha256 integrity ({bad})")
    ok(not any(doc_path(s).exists() for s in man),
       "no vaulted module ships as plaintext")
    ok((REPO / "curriculum" / "phase-0-proof-literacy.md").exists(),
       "phase-0 ships unlocked")

    print("\n[suite] fresh student view")
    _, out = run("status", expect_rc=0)
    ok("gate 0" in out and "open" in out, "status shows gate 0 open")
    ok("locked" in out, "status shows gates 1+ locked")
    run("grade", 0, expect_rc=1)  # shipped stub = all missing
    ok(not doc_path("phase-1-elementary-number-theory").exists(),
       "stub answers unlock nothing")
    _, out = run("grade", 3, expect_rc=2)
    ok("LOCKED" in out, "order-lock: gate 3 refuses before gate 2")

    print("\n[suite] full pass chain 0 -> 7")
    for n in range(8):
        gate = gate_mod(n)
        stem = getattr(gate, "NEXT_DOC", None)
        args = ["grade", n] + (["--name", "Selftest Student"] if n == 7
                               else [])
        write_answers(n)
        p, out = run(*args, expect_rc=0)
        ok("100%" in out or "GATE PASSED" in out or "COURSE COMPLETE" in out,
           f"gate {n} perfect pass message")
        if stem:
            ok(doc_path(stem).exists(), f"gate {n} unlocked {stem}.md")
    ok((REPO / "CERTIFICATE.txt").exists(), "certificate minted")
    ok("Selftest Student" in (REPO / "CERTIFICATE.txt").read_text(),
       "certificate carries the name")
    _, out = run("status", expect_rc=0)
    ok("COURSE COMPLETE" in out, "status reports completion")

    print("\n[suite] tamper tests")
    reset()
    body, snips = correct_answers_source(0)
    body_t = body.replace('"q01": 5050', '"q01": 5051', 1)
    (REPO / "answers" / "phase-0.py").write_text(snips + body_t)
    p, out = run("grade", 0, expect_rc=1)
    ok("q01" in out and "incorrect" in out, "tampered int reported & failed")
    ok(not doc_path("phase-1-elementary-number-theory").exists(),
       "99%-gate unlocks nothing")

    # regression: same-size edit in the same second must NOT serve stale
    # bytecode (importlib pyc trap hit during development)
    write_answers(0)                                  # correct, size S
    body, snips = correct_answers_source(0)
    (REPO / "answers" / "phase-0.py").write_text(
        snips + body.replace('"q01": 5050', '"q01": 5051', 1))  # size S
    (REPO / "answers" / "phase-0.py").write_text(snips + body)  # size S again
    p, out = run("grade", 0, expect_rc=0)
    ok(p.returncode == 0, "same-second same-size edit not served stale")
    reset()

    reset()
    pass_gate(0)
    pass_gate(1)
    body, snips = correct_answers_source(2)
    import re
    m = re.search(r'"q01": ([0-9.]+)', body)
    bumped = float(m.group(1)) + 2e-4
    body_t = body[:m.start(1)] + repr(bumped) + body[m.end(1):]
    (REPO / "answers" / "phase-2.py").write_text(snips + body_t)
    p, out = run("grade", 2, expect_rc=1)
    ok(not doc_path("phase-3-prime-distribution").exists(),
       "float outside tolerance rejected")

    reset()
    for n in (0, 1, 2):
        pass_gate(n)
    (REPO / "answers" / "phase-3.py").write_text(
        "def _ans(x):\n    return 0.0\n\nANSWERS = {"
        + "".join(f'"{q["id"]}": None,' for q in gate_mod(3).questions() if
                  q["id"] != "q12")
        + '"q12": _ans}\n')
    # all non-func answers removed -> they will count wrong; func wrong too
    p, out = run("grade", 3, expect_rc=1)
    ok(not doc_path("phase-4-complex-analysis").exists(),
       "broken function + empty answers rejected")

    print("\n[suite] resync, leak warning, reset")
    reset()
    pass_gate(0)
    p1 = doc_path("phase-1-elementary-number-theory")
    p1.unlink()
    run("resync", expect_rc=0)
    ok(p1.exists(), "resync restores deleted-but-earned module")
    reset()
    doc_path("phase-5-rh-explicit-formula").write_text("# contraband\n")
    _, out = run("status", expect_rc=0)
    ok("WARNING" in out, "status flags unearned plaintext (leak warning)")
    reset()
    ok(not any(doc_path(s).exists() for s in man), "reset re-locks all")

    print()
    if FAILURES:
        print(f"SELFTEST FAILED ({len(FAILURES)}):")
        for f in FAILURES:
            print("  -", f)
        sys.exit(1)
    print("SELFTEST OK")
    shutil.rmtree(TMP, ignore_errors=True)


if __name__ == "__main__":
    main()
