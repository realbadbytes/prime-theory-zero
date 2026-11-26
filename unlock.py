#!/usr/bin/env python3
"""Prime Theory Zero — progress gate engine.

Protocol
--------
  1. Work the current phase in curriculum/ (every lesson is fully public --
     the model is ISLP_labs: all theory, guided code, and exercises in-repo).
  2. Run its labs, do its exercises.
  3. Fill answers/phase-N.py  (ANSWERS = {"q01": ..., "q02": ..., ...}).
  4. python unlock.py grade N
  5. A perfect 100% passes the gate: gate N+1 opens. Anything less and
     gate N+1 refuses to run until you pass.

Commands
--------
  status                 where you stand
  grade <N>              grade answers/phase-N.py (may open gate N+1)
  grade 7 --name "..."   finish the course (certificate)
  reset                  wipe ALL progress
  name <you>             store your display name (for the certificate)
  music [status|stop|on|off]   gate-trial soundtrack (8-bit synth or
                         your own tracks in music/; PTZ_MUSIC=0 disables)

Honesty notice: the lock is social, not cryptographic. Ground truth is
computed live on your machine, so a curious student could extract it.
Nothing stops them except that the certificate, the labs' intuition, and
the entire point of the course live on the far side of doing the work.
"""
import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / ".unlock_state"
STATE = STATE_DIR / "state.json"
GATES = ROOT / "gates"
ANSWERS_DIR = ROOT / "answers"
CURRICULUM = ROOT / "curriculum"
CERT = ROOT / "CERTIFICATE.txt"
N_GATES = 8  # gates 0..7

sys.path.insert(0, str(GATES))
sys.path.insert(0, str(ROOT / "tools"))
from gate_common import match  # noqa: E402

try:                                   # soundtrack is strictly optional:
    import gate_music as _gm           # the course works with it broken
except Exception:                      # or absent, silently
    _gm = None


def _music_begin(n):
    if _gm is None:
        return
    try:
        if _gm.ensure_playing(n):
            print("  \u266a gate-trial soundtrack started  "
                  "('unlock.py music stop' silences; 'music off' forever)")
    except Exception:
        pass


def _music_fanfare():
    if _gm is None:
        return
    try:
        _gm.fanfare()
    except Exception:
        pass


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

    _music_begin(n)

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
        print("\n  Gate not passed. Revisit the labs and phase doc, fix "
              "answers/\nphase-%d.py, and resubmit. The grader does not "
              "reveal correct\nanswers -- the labs do.\n" % n)
        sys.exit(1)

    # PERFECT
    st["passed"][str(n)] = {
        "score": 100.0,
        "when": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    st["log"].append({"event": f"gate{n}-pass", "when":
                      st["passed"][str(n)]["when"]})
    _music_fanfare()
    stem = getattr(gate, "NEXT_DOC", None)
    if stem:
        print("  *** 100% — GATE PASSED ***\n"
              f"  gate {n + 1} is now open — next lesson: "
              f"{doc_path(stem).relative_to(ROOT)}\n")
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


def cmd_reset(args):
    if _gm is not None:
        try:
            _gm.stop()
        except Exception:
            pass
    if not args.yes:
        resp = input("This wipes ALL progress (the lessons stay public). "
                     "Type 'lock' to confirm: ")
        if resp.strip().lower() != "lock":
            print("aborted")
            return
    if STATE.exists():
        STATE.unlink()
    if CERT.exists():
        CERT.unlink()
    print("progress wiped; gate 0 open again. All lessons remain readable "
          "in curriculum/.")


def cmd_music(args):
    if _gm is None:
        print("soundtrack module unavailable (tools/gate_music.py)")
        sys.exit(1)
    act = args.action
    if act == "stop":
        print("stopped." if _gm.stop() else "nothing was playing.")
        return
    if act == "on":
        _gm.set_enabled(True)
        print("music enabled (env PTZ_MUSIC overrides this)")
        return
    if act == "off":
        _gm.set_enabled(False)
        _gm.stop()
        print("music disabled")
        return
    d = _gm.status_dict()
    print(f"\n  soundtrack:      {'on' if d['enabled'] else 'OFF'} "
          f"(env PTZ_MUSIC wins over 'music on/off')")
    print(f"  audio route:     {d['player']}")
    if d["daemon_pid"]:
        print(f"  daemon:          playing gate {d['daemon_gate']} "
              f"(pid {d['daemon_pid']})")
    else:
        print("  daemon:          idle")
    if d["own_music_tracks"]:
        print(f"  own music:       {d['own_music_tracks']} track(s) in "
              f"music/ -- rotating by prime index; e.g. "
              f"{', '.join(d['own_music'])}")
        if d["user_fanfare"]:
            print("  own fanfare:     music/fanfare.* overrides the synth "
                  "jingle")
    else:
        print("  own music:       none -- procedural chiptune synthesized "
              "from primes (drop licensed tracks into music/ to replace it)")
    print(f"  cache:           {d['cache']}\n")


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
    r = sub.add_parser("reset")
    r.add_argument("--yes", action="store_true")
    nm = sub.add_parser("name")
    nm.add_argument("you")
    mu = sub.add_parser("music")
    mu.add_argument("action", nargs="?", default="status",
                    choices=["status", "stop", "on", "off"])
    args = ap.parse_args()
    {"status": cmd_status, "grade": cmd_grade,
     "reset": cmd_reset, "name": cmd_name,
     "music": cmd_music}[args.cmd](args)


if __name__ == "__main__":
    main()
