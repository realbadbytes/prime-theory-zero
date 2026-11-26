#!/usr/bin/env bash
# Run every lab in order. Outputs land in data/. ~2 minutes total.
set -euo pipefail
cd "$(dirname "$0")"

# Prefer the repo virtualenv if it exists, even when the shell didn't
# activate it -- students routinely forget, and macOS system Python
# (PEP 668) refuses to pip-install into it anyway.
PY="${PYTHON:-python3}"
if [ -x ".venv/bin/python3" ]; then
  case "$(command -v "$PY" || true)" in
    "$PWD"/.venv/*) : ;;                       # already venv-active
    *) PY=".venv/bin/python3" ;;
  esac
fi

# Dependency preflight: a readable one-liner beats a numpy traceback.
if ! "$PY" -c "import numpy, matplotlib, mpmath" 2>/dev/null; then
  echo "missing Python packages (numpy / matplotlib / mpmath) for: $("$PY" -c 'import sys;print(sys.executable)')" >&2
  echo >&2
  echo "Fix it with:" >&2
  echo "  python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt" >&2
  echo >&2
  echo "(macOS note: system Homebrew Python blocks 'pip install' outside a" >&2
  echo " virtualenv by design -- use the .venv lines above, then re-run ./run_all.sh)" >&2
  exit 1
fi

run() {
  printf '\n\033[1m==> %s\033[0m\n' "$*"
  "$@"
}

run "$PY" src/phase1/sieve_evolution.py
run "$PY" src/phase1/primality_lab.py
run "$PY" src/phase1/congruences.py
run "$PY" src/phase2/euler_product_lab.py
run "$PY" src/phase3/pnt_lab.py
run "$PY" src/phase3/gap_lab.py
run "$PY" src/phase5/explicit_formula.py
run "$PY" src/phase6/prime_races.py

printf '\n\033[1mall labs passed\033[0m\n'
