#!/usr/bin/env python3
"""Prime Theory Zero — progress gate engine.

Protocol
--------
  1. Read the current unlocked module in curriculum/.
  2. Work its labs and exercises.
  3. Fill answers/phase-N.py  (ANSWERS = {"q01": ..., "q02": ..., ...}).
  4. python unlock.py grade N
  5. A perfect 100% decrypts the next module into curriculum/.
     Anything less and it stays sealed in the vault. Gate N+1 also
     refuses to run until gate N is passed.

Commands
--------
  status                 where you stand
  grade <N>              grade answers/phase-N.py (may unlock N+1)
  grade 7 --name "..."   finish the course (certificate)
  resync                 re-decrypt any module you passed but lost
  reset                  wipe ALL progress and re-lock everything
  name <you>             store your display name (for the certificate)

Honesty notice: this is an EDUCATIONAL lock. The vault keys sit on your
disk and the vault format is ~15 lines of stdlib crypto; a curious student
can open the modules early. Nothing stops them except the fact that the
labs' ground truth, the certificate, and the point of the course all live
on the far side of the quiz. Read the README's "Progress gates" section.
"""
import argparse
import base64
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / ".unlock_state"
STATE = STATE_DIR / "state.json"
VAULT = ROOT / "vault"
MANIFEST = VAULT / "manifest.json"
GATES = ROOT / "gates"
ANSWERS_DIR = ROOT / "answers"
CURRICULUM = ROOT / "curriculum"
CERT = ROOT / "CERTIFICATE.txt"
N_GATES = 8  # gates 0..7

sys.path.insert(0, str(GATES))
from gate_common import match  # noqa: E402


# ------------------------------------------------------------- vault crypto
def _keystream(key: bytes, n: int) -> bytes:
    out = bytearray()
    ctr = 0
    while len(out) < n:
        out += hashlib.sha256(key + ctr.to_bytes(8, "big")).digest()
        ctr += 1
    return bytes(out[:n])


def xor(data: bytes, key: bytes) -> bytes:
    ks = _keystream(key, len(data))
    return bytes(a ^ b for a, b in zip(data, ks))


def load_manifest():
    return json.loads(MANIFEST.read_text())


# ------------------------------------------------------------- state
def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"passed": {}, "name": None, "log": []}


def save_state(st):
    STATE_DIR.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(st, indent=2))


# ------------------------------------------------------------- gates
def load_gate(n):
    path = GATES / f"gate{n}.py"
    if not path.exists():
        sys.exit(f"no gate {n}: expected {path}")
    spec = importlib.util.spec_from_file_location(f"gate{n}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_answers(n):
    path = ANSWERS_DIR / f"phase-{n}.py"
    if not path.exists():
        return None, (f"answers file {path.relative_to(ROOT)} not found -- "
                      "copy the template and fill ANSWERS")
    import types
    # Compile the CURRENT text directly: importlib's pyc caching can serve
    # stale bytecode when edits keep file size and land in the same second.
    mod = types.ModuleType(f"answers{n}")
    mod.__file__ = str(path)
    try:
        exec(compile(path.read_text(), str(path), "exec"), mod.__dict__)
    except Exception as exc:
        return None, f"{path.relative_to(ROOT)} does not import: {exc!r}"
    if not isinstance(mod.__dict__.get("ANSWERS"), dict):
        return None, f"{path.relative_to(ROOT)} must define ANSWERS = {{...}}"
    return mod.ANSWERS, None


def doc_path(stem):
    return CURRICULUM / f"{stem}.md"


def unlock_doc(stem):
    man = load_manifest()
    if stem not in man:
        sys.exit(f"vault has no entry for {stem!r}")
    entry = man[stem]
    key = base64.b64decode(entry["key"])
    plain = xor((VAULT / entry["file"]).read_bytes(), key)
    if hashlib.sha256(plain).hexdigest() != entry["sha256"]:
        sys.exit("vault integrity check FAILED (manifest mismatch) -- "
                 "repo corrupted; re-clone or run tools/build_vault.py")
    out = doc_path(stem)
    out.write_bytes(plain)
    return out


def gate_passed(st, n):
    return str(n) in st["passed"]


# ------------------------------------------------------------- commands
def cmd_status(_args):
    st = load_state()
    print(f"\n{'=' * 64}\n  PRIME THEORY ZERO — progress"
          + (f"  (student: {st['name']})" if st.get("name") else "")
          + f"\n{'=' * 64}")
    for n in range(N_GATES):
        gate = load_gate(n)
        if gate_passed(st, n):
            info = st["passed"][str(n)]
            mark = f"PASS {info['score']:.0f}%  {info['when'][:10]}"
        else:
            mark = "locked" if not _available(st, n) else "open"
        stem = getattr(gate, "NEXT_DOC", None)
        nxt = f"-> {stem}" if stem else "-> certificate"
        print(f"  gate {n}  [{mark:>18}]  {gate.TITLE}  {nxt}")
    leaks = []
    for n in range(N_GATES):
        stem = getattr(load_gate(n), "NEXT_DOC", None)
        # a vaulted module is legitimate only if the gate that DECRYPTS it
        # (gate n itself) was passed
        if stem and doc_path(stem).exists() and not gate_passed(st, n):
            leaks.append(stem)
    if leaks:
        print("\n  WARNING: unlocked modules present WITHOUT passing their "
              "gate:")
        for s in leaks:
            print(f"    curriculum/{s}.md")
    done = all(gate_passed(st, n) for n in range(N_GATES))
    if done:
        print("\n  COURSE COMPLETE. Certificate:"
              f" {CERT.relative_to(ROOT) if CERT.exists() else '(run grade 7 again to mint)'}")
    print()


def _available(st, n):
    return n == 0 or gate_passed(st, n - 1)


def cmd_grade(args):
    n = args.n
    st = load_state()
    gate = load_gate(n)

    if not _available(st, n):
        print(f"\nLOCKED.  Gate {n} ({gate.TITLE}) requires a perfect "
              f"pass on gate {n-1} first.\n"
              "         python unlock.py status")
        sys.exit(2)

    answers, err = load_answers(n)
    if answers is None:
        print(f"\n{err}\n")
        sys.exit(1)

    print(f"\n{'=' * 64}\n  {gate.TITLE}  —  grading answers/phase-{n}.py"
          f"\n{'=' * 64}")
    if getattr(gate, "FORMAT_NOTES", "").strip():
        print(gate.FORMAT_NOTES.strip() + "\n")

    keybook = gate.keybook()
    questions = gate.questions()
    print("  QUESTIONS (also in the prompt printout of this command):\n")
    for q in questions:
        body = "\n".join("      " + ln for ln in q["prompt"].splitlines())
        print(f"  [{q['id']}]\n{body}\n")
    ids = [q["id"] for q in questions]
    if set(ids) != set(keybook):
        sys.exit(f"gate {n} is internally inconsistent (ids vs keybook) "
                 "-- report this; do not blame your answers")

    wrong, missing = [], []
    for q in questions:
        qid = q["id"]
        if qid not in answers:
            missing.append(qid)
            continue
        if not match(keybook[qid], answers[qid]):
            wrong.append(qid)

    total = len(ids)
    correct = total - len(wrong) - len(missing)
    score = 100.0 * correct / total

    print(f"\n  score: {correct}/{total}  =  {score:.1f}%   "
          f"(need 100.0%)\n")
    if wrong:
        print("  incorrect:", ", ".join(wrong))
    if missing:
        print("  missing:  ", ", ".join(missing))
    if wrong or missing:
        print("\n  The next module remains SEALED. Revisit the labs and "
              "phase\ndoc, fix answers/phase-%d.py, and resubmit. The "
              "grader does not\nreveal correct answers -- the labs do.\n"
              % n)
        sys.exit(1)

    # PERFECT
    st["passed"][str(n)] = {
        "score": 100.0,
        "when": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    st["log"].append({"event": f"gate{n}-pass", "when":
                      st["passed"][str(n)]["when"]})
    stem = getattr(gate, "NEXT_DOC", None)
    if stem:
        out = unlock_doc(stem)
        print("  *** 100% — GATE PASSED ***\n"
              f"  unlocked: {out.relative_to(ROOT)}\n")
    else:
        save_state(st)
        name = args.name or st.get("name") or "Anonymous Prime Hunter"
        st["name"] = name
        write_certificate(st)
        print("  *** 100% — CAPSTONE PASSED — COURSE COMPLETE ***\n"
              f"  certificate: {CERT.relative_to(ROOT)}\n")
    save_state(st)


def write_certificate(st):
    when = st["passed"].get("7", {}).get("when", "?")[:10]
    cert = f"""
+--------------------------------------------------------------+
|                                                              |
|            P R I M E   T H E O R Y   Z E R O                 |
|                                                              |
|      This certifies that                                         |
|                                                              |
|                    {st.get('name', ''):^44}  |
|                                                              |
|      passed all eight gates (0-7) at 100%, from proof        |
|      literacy through the explicit formula, prime races,     |
|      and the modern theory of gaps -- having computed,        |
|      not quoted, every claim that mattered.                   |
|                                                              |
|      issued {when}     psi(x) = x - sum_rho x^rho/rho - ...        |
|                                                              |
+--------------------------------------------------------------+
"""
    CERT.write_text(cert)


def cmd_resync(_args):
    st = load_state()
    count = 0
    for n in range(N_GATES):
        stem = getattr(load_gate(n), "NEXT_DOC", None)
        if stem and gate_passed(st, n) and not doc_path(stem).exists():
            unlock_doc(stem)
            print(f"  restored curriculum/{stem}.md")
            count += 1
    print(f"  {count} module(s) restored." if count else "  nothing missing.")


def cmd_reset(args):
    if not args.yes:
        resp = input("This wipes ALL progress and re-locks every module. "
                     "Type 'lock' to confirm: ")
        if resp.strip().lower() != "lock":
            print("aborted")
            return
    if STATE.exists():
        STATE.unlink()
    if CERT.exists():
        CERT.unlink()
    for n in range(N_GATES):
        stem = getattr(load_gate(n), "NEXT_DOC", None)
        if stem:
            p = doc_path(stem)
            if p.exists():
                p.unlink()
    print("progress wiped; only Phase 0 remains unlocked (phase-0 is the "
          "entry module and never vaulted)")


def cmd_name(args):
    st = load_state()
    st["name"] = args.you
    save_state(st)
    print(f"named: {args.you}")


def main():
    ap = argparse.ArgumentParser(prog="unlock.py",
                                 description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    g = sub.add_parser("grade")
    g.add_argument("n", type=int)
    g.add_argument("--name", default=None)
    sub.add_parser("resync")
    r = sub.add_parser("reset")
    r.add_argument("--yes", action="store_true")
    nm = sub.add_parser("name")
    nm.add_argument("you")
    args = ap.parse_args()
    {"status": cmd_status, "grade": cmd_grade, "resync": cmd_resync,
     "reset": cmd_reset, "name": cmd_name}[args.cmd](args)


if __name__ == "__main__":
    main()
