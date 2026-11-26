"""GATE 3 — Prime Distribution (PNT) checkpoint.

12 questions. Ground truth computed at grading time via the shared sieve.
100% required to unlock Phase 4.
"""
import math

PHASE = 3
NEXT_DOC = "phase-4-complex-analysis"
TITLE = "Gate 3 — Prime Distribution"

FORMAT_NOTES = """
Sieve values: use src/common/primes.py, phase-3 labs, or your own code.
"rounded to nearest integer" -> int; "to k decimals" -> float.
"""


def questions():
    return [
        {"id": "q01", "prompt": "pi(10^6). (Integer.)"},
        {"id": "q02",
         "prompt": "theta(10^5) = sum of ln p over primes p <= 10^5, "
                   "ROUNDED TO NEAREST INTEGER. (Integer.)"},
        {"id": "q03",
         "prompt": "psi(100) = sum_{p^k <= 100} ln p (sum over prime POWERS "
                   "<= 100), rounded to 3 decimals. (Float.)"},
        {"id": "q04",
         "prompt": "The smallest prime strictly between 1000 and 2000 "
                   "(Bertrand's postulate exhibit). (Integer.)"},
        {"id": "q05",
         "prompt": "Mertens: product_{p<=10^4} (1 - 1/p) * ln(10^4), "
                   "rounded to 3 decimals (approximates e^-gamma). "
                   "(Float.)"},
        {"id": "q06",
         "prompt": "The LARGEST prime gap below 10^6 (largest p_{n+1}-p_n "
                   "with p_n < 10^6). (Integer -- gap_lab.py territory.)"},
        {"id": "q07",
         "prompt": "Li(10^6) (repo definition: u=ln t substitution + "
                   "Simpson, 20000 panels -- see gate 2 q09), "
                   "ROUNDED TO NEAREST INTEGER. (Integer.)"},
        {"id": "q08",
         "prompt": "Cramer's predicted longest gap below 10^10: round "
                   "(ln 1e10)^2 to nearest integer. (Integer.)"},
        {"id": "q09",
         "prompt": "(1e6/ln(1e6)) / pi(1e6), rounded to 4 decimals. "
                   "(Float.)"},
        {"id": "q10",
         "prompt": "MCQ. Which statement is EQUIVALENT to the PNT?\n"
                   "  A) theta(x) = O(x)\n"
                   "  B) psi(x) ~ x\n"
                   "  C) sum 1/p converges\n"
                   "  D) pi(x) < x for all large x\n"
                   "Answer (letter)."},
        {"id": "q11",
         "prompt": "Li(10^7) - pi(10^7), ROUNDED TO NEAREST INTEGER. "
                   "(Integer.)"},
        {"id": "q12",
         "prompt": "Define theta(x) = sum_{p<=x} ln p (float). (Function.)"},
    ]


def _check_theta(f):
    from gate_common import theta
    for x in (100, 1000, 5000):
        w = theta(x)
        if abs(float(f(x)) - w) > 1e-6 * max(1.0, w):
            return False
    return True


def keybook():
    from gate_common import gap_records, li, pi, primes_le, psi, theta
    import numpy as np
    p1e4 = primes_le(10 ** 4).astype(float)
    mertens = float(np.prod(1.0 - 1.0 / p1e4)) * math.log(1e4)
    gaps = gap_records(10 ** 6)
    return {
        "q01": ("int", pi(10 ** 6)),
        "q02": ("int", round(theta(10 ** 5))),
        "q03": ("float", round(psi(100), 3), 1e-3),
        "q04": ("int", int(primes_le(2000)[primes_le(2000) > 1000][0])),
        "q05": ("float", round(mertens, 3), 1e-3),
        "q06": ("int", max(g for _, g in gaps)),
        "q07": ("int", round(li(1e6))),
        "q08": ("int", round(math.log(1e10) ** 2)),
        "q09": ("float", round((1e6 / math.log(1e6)) / pi(10 ** 6), 4),
                1e-4),
        "q10": ("str", "b"),
        "q11": ("int", round(li(1e7)) - pi(10 ** 7)),
        "q12": ("func", _check_theta),
    }
