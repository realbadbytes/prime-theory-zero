#!/usr/bin/env python3
"""Self-test for the gate/unlock machinery.

Runs in a THROWAWAY COPY of the repo (never touches real progress).
Scenarios: fresh status, unpassed-stub, order-lock, full 0->7 pass chain,
certificate, reset, tamper (int/float/function), order-lock, progression.
Exit 0 + "SELFTEST OK" on success.
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
    env = {**__import__("os").environ, "PTZ_MUSIC": "0"}
    p = subprocess.run([sys.executable, "unlock.py", *map(str, args)],
                       cwd=REPO, capture_output=True, text=True, env=env)
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


def passed_ids():
    import json
    sp = REPO / ".unlock_state" / "state.json"
    return set(json.loads(sp.read_text())["passed"]) if sp.exists() else set()


def pass_gate(n):
    write_answers(n)
    p, out = run("grade", n, expect_rc=0)
    return p, out


def main():
    print(f"selftest repo: {REPO}")
    shutil.copytree(ROOT, REPO, ignore=shutil.ignore_patterns(
        ".git", "data", "__pycache__", ".unlock_state", "CERTIFICATE.txt",
        ".venv"))

    print("\n[suite] structure (fully public curriculum, ISLP model)")
    stems = [s for n in range(8)
             if (s := getattr(gate_mod(n), "NEXT_DOC", None))]
    ok(len(stems) == 7, f"7 gated lessons + phase-0 entry (got {len(stems)})")
    ok((REPO / "curriculum" / "phase-0-proof-literacy.md").exists()
       and all(doc_path(s).exists() for s in stems),
       "all eight lessons ship public and plaintext")
    ok(not (REPO / "vault").exists()
       and not (REPO / "tools" / "build_vault.py").exists(),
       "vault machinery fully removed")
    thin = [s for s in stems
            if len(doc_path(s).read_text().splitlines()) < 150]
    ok(not thin, f"every lesson is a substantive doc (>=150 lines) {thin}")

    print("\n[suite] fresh student view")
    _, out = run("status", expect_rc=0)
    ok("gate 0" in out and "open" in out, "status shows gate 0 open")
    ok("locked" in out, "status shows gates 1+ locked")
    run("grade", 0, expect_rc=1)  # shipped stub = all missing
    ok(passed_ids() == set(), "stub answers record no progress")
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
            ok(f"curriculum/{stem}.md" in out,
               f"gate {n} pass points the student at {stem}.md")
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
    ok("0" not in passed_ids(), "99%-gate records no progress")

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
    ok("2" not in passed_ids(), "float outside tolerance rejected")

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
    ok("3" not in passed_ids(), "broken function + empty answers rejected")

    print("\n[suite] progression & reset")
    reset()
    ok(all(doc_path(s).exists() for s in stems),
       "reset leaves the public curriculum on disk")
    pass_gate(0)
    ok("0" in passed_ids(), "state records the gate-0 pass")
    _, out = run("status", expect_rc=0)
    ok("PASS 100%" in out, "status shows the pass")
    _, out7 = run("grade", 7, expect_rc=2)
    ok("LOCKED" in out7, "order-lock holds mid-course (gate 7 refused)")
    reset()
    ok(passed_ids() == set(), "reset clears all progress")
    _, out = run("status", expect_rc=0)
    ok("locked" in out and "PASS" not in out,
       "after reset gates 1+ locked again")

    print("\n[suite] ground-truth numerical locks")
    from gate_common import li, ls_bias_cell
    ok(abs(li(1e6) - 78626.5039957) < 1e-3,
       "Li(1e6) matches mpmath exactly (regression: uniform-t Simpson "
       "silently lies by ~15)")
    ok(abs(li(1e7) - 664917.3604) < 1e-2, "Li(1e7) machine-accurate")
    ok(round(li(1e6)) == 78627, "gate value Li(1e6) -> 78627")
    ok(abs(ls_bias_cell(3, 10 ** 6, 1, 1) - 0.2089) < 2e-4,
       "LS(1,1)@1e6 = 0.2089 under primes>q convention")
    ok(abs(ls_bias_cell(3, 10 ** 7, 1, 1) - 0.2150) < 2e-4,
       "LS(1,1)@1e7 = 0.2150 (bias decays, doc says so)")

    print("\n[suite] soundtrack engine")
    sys.path.insert(0, str(ROOT / "tools"))
    import gate_music as gm
    import wave as _wv
    w = gm.render_gate_wav(2, force=True)
    with _wv.open(str(w)) as h:
        ok(h.getnchannels() == 2 and h.getframerate() == 44100
           and h.getnframes() > 44100 * 10,
           "gate theme renders: stereo 44.1k, >10 s")
        data = h.readframes(h.getnframes())
    peak = max(abs(int.from_bytes(data[i:i + 2], "little", signed=True))
               for i in range(0, min(len(data), 400000), 2))
    ok(peak > 3000, f"theme has real signal (peak {peak})")
    ok(gm.render_fanfare_wav(force=True).stat().st_size > 100_000,
       "fanfare renders")
    ok(gm.playlist_for(3) == [],
       "no phantom own-music tracks leak into a clean checkout")
    run("music", "status", expect_rc=0)
    _, out = run("music", "stop", expect_rc=0)
    ok("playing" in out or "stopped" in out, "music stop idempotent")
    _, out = run("music", "off", expect_rc=0)
    ok("disabled" in out, "music off switches config")

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
