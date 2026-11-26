#!/usr/bin/env bash
# Run every lab in order. Outputs land in data/. ~2 minutes total.
set -euo pipefail
cd "$(dirname "$0")"

run() {
  printf '\n\033[1m==> %s\033[0m\n' "$*"
  "$@"
}

run python3 src/phase1/sieve_evolution.py
run python3 src/phase1/primality_lab.py
run python3 src/phase1/congruences.py
run python3 src/phase2/euler_product_lab.py
run python3 src/phase3/pnt_lab.py
run python3 src/phase3/gap_lab.py
run python3 src/phase5/explicit_formula.py
run python3 src/phase6/prime_races.py

printf '\n\033[1mall labs passed\033[0m\n'
