"""GATE 2 — Analysis Light checkpoint.

12 questions. Ground truth computed at grading time. 100% required to
unlock Phase 3.
"""
import math

PHASE = 2
NEXT_DOC = "phase-3-prime-distribution"
TITLE = "Gate 2 — Analysis Light"

FORMAT_NOTES = """
"to k decimals" means: give a float rounded to k decimals, e.g. 0.5772.
Tolerance is 10^-k, so rounding per the spec is exact and safe.
"""


def questions():
    return [
        {"id": "q01",
         "prompt": "H_1000 - ln(1000), rounded to 4 decimals (this is "
                   "gamma to 4 places). (Float.)"},
        {"id": "q02",
         "prompt": "Basel partial sum: sum 1/n^2 for n=1..2000, rounded to "
                   "6 decimals. (Float.)"},
        {"id": "q03",
         "prompt": "Euler-product side: product over primes p <= 1000 of "
                   "1/(1 - p^-2), rounded to 6 decimals. (Float.)"},
        {"id": "q04",
         "prompt": "sum of 1/p over primes p <= 10^6, rounded to 4 "
                   "decimals. (Float.)"},
        {"id": "q05",
         "prompt": "p_n 3-term estimate n*(ln n + ln ln n - 1) at n = "
                   "100000, ROUNDED TO NEAREST INTEGER. (Integer.)"},
        {"id": "q06",
         "prompt": "sum_{n=1}^{10000} floor(10000/n)  "
                   "(= sum of tau(m) for m<=10000). (Integer.)"},
        {"id": "q07",
         "prompt": "MCQ. Which divergence proves the infinitude of primes "
                   "via the Euler product?\n"
                   "  A) sum 1/n^2\n"
                   "  B) sum over primes of 1/p\n"
                   "  C) sum over primes of 1/2^p\n"
                   "  D) sum over primes of (ln p)/p^2\n"
                   "Answer (letter)."},
        {"id": "q08",
         "prompt": "MCQ. f = O(g) as x->infty means:\n"
                   "  A) f/g -> 0\n"
                   "  B) f/g -> 1\n"
                   "  C) |f| <= C*g for some C and all large x\n"
                   "  D) f <= g eventually\n"
                   "Answer (letter)."},
        {"id": "q09",
         "prompt": "Li(x) = integral of dt/ln t from 2 to x (Simpson, "
                   "20000 panels -- the repo definition). Ratio "
                   "Li(1e5) / (1e5/ln(1e5)), rounded to 4 decimals. "
                   "(Float.)"},
        {"id": "q10",
         "prompt": "sum_{p<=10^5} 1/p - ln(ln(10^5)), rounded to 4 "
                   "decimals (this is the Meissel-Mertens constant M to 4 "
                   "places). (Float.)"},
        {"id": "q11",
         "prompt": "Li(100) rounded to nearest integer (repo Simpson "
                   "definition). (Integer.)"},
        {"id": "q12",
         "prompt": "Define estimate_pn(n) returning n*(ln n + ln ln n - 1) "
                   "as a float. (Function.)"},
    ]


def _check_estimate_pn(f):
    for n in (1000, 12345, 77777):
        want = n * (math.log(n) + math.log(math.log(n)) - 1)
        if abs(float(f(n)) - want) > 1e-6 * max(1.0, abs(want)):
            return False
    return True


def keybook():
    from gate_common import li, primes_le
    import numpy as np
    H1000 = sum(1.0 / k for k in range(1, 1001))
    basel = sum(1.0 / (n * n) for n in range(1, 2001))
    p1000 = primes_le(1000)
    prod = float(np.prod(1.0 / (1.0 - p1000.astype(float) ** -2)))
    p1e6 = primes_le(10 ** 6).astype(float)
    s1e6 = float((1.0 / p1e6).sum())
    p1e5 = primes_le(10 ** 5).astype(float)
    s1e5 = float((1.0 / p1e5).sum())
    return {
        "q01": ("float", round(H1000 - math.log(1000), 4), 1e-4),
        "q02": ("float", round(basel, 6), 1e-6),
        "q03": ("float", round(prod, 6), 1e-6),
        "q04": ("float", round(s1e6, 4), 1e-4),
        "q05": ("int", round(100000 * (math.log(100000)
                                       + math.log(math.log(100000)) - 1))),
        "q06": ("int", sum(10000 // n for n in range(1, 10001))),
        "q07": ("str", "b"),
        "q08": ("str", "c"),
        "q09": ("float", round(li(1e5) / (1e5 / math.log(1e5)), 4), 1e-4),
        "q10": ("float", round(s1e5 - math.log(math.log(1e5)), 4), 1e-4),
        "q11": ("int", round(li(100))),
        "q12": ("func", _check_estimate_pn),
    }
