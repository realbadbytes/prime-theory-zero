"""GATE 1 — Elementary Number Theory checkpoint.

12 questions; all ground truth is computed at grading time (you may use the
labs / your own code to find each value). 100% required to unlock Phase 2.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_common import pi, primes_le  # noqa: E402

PHASE = 1
NEXT_DOC = "phase-2-analysis-light"
TITLE = "Gate 1 — Elementary Number Theory"

FORMAT_NOTES = """
Compute the requested quantities (your own code, pow()/math.gcd, the Phase-1
labs, or by hand — we cannot tell, and only you care). Integers exact.
For q12 define a real function, not a value.
"""


def questions():
    return [
        {"id": "q01",
         "prompt": "The inverse of 17 modulo 3819: the unique 0 <= x < 3819 "
                   "with 17x = 1 (mod 3819). (Extended Euclid, like "
                   "congruences.py.) (Integer.)"},
        {"id": "q02",
         "prompt": "Smallest x >= 0 with x = 2 (mod 3), x = 3 (mod 5), "
                   "x = 2 (mod 7). (Integer.)"},
        {"id": "q03",
         "prompt": "phi(360) = #{1 <= k <= 360 : gcd(k,360)=1}. (Integer.)"},
        {"id": "q04",
         "prompt": "ord_101(10): the smallest d >= 1 with 10^d = 1 (mod 101)."
                   " (Integer.)"},
        {"id": "q05",
         "prompt": "How many primitive roots does p = 29 have? (= phi(28).)"
                   " (Integer.)"},
        {"id": "q06",
         "prompt": "How many quadratic residues lie among 1,2,...,p-1 for "
                   "p = 41? (Integer.)"},
        {"id": "q07",
         "prompt": "Euler's criterion value pow(3, 6, 13). (Integer; it is "
                   "1 if 3 is a QR mod 13.)"},
        {"id": "q08",
         "prompt": "The smallest Carmichael number (the lab prints them)."
                   " (Integer.)"},
        {"id": "q09",
         "prompt": "pow(2, 100, 101). (Integer — FLT at work.)"},
        {"id": "q10",
         "prompt": "math.gcd(4181, 4087). (Integer — consecutive Fibonacci "
                   "numbers; what SHOULD it be?)"},
        {"id": "q11",
         "prompt": "The Miller-Rabin villain from primality_lab.py, "
                   "3215031751 = 151 * 751 * 28351. Give its LARGEST prime "
                   "factor. (Integer.)"},
        {"id": "q12",
         "prompt": "Define a function is_prime(n) (trial division is fine; "
                   "must be correct for n = 1, 2, squares, Carmichael "
                   "numbers). It will be tested against a sieve."},
    ]


def _check_is_prime(f):
    for n in (1, 2, 3, 4, 561, 1729, 7919, 1000000007, 1000000009,
              2026, 999983):
        if bool(f(n)) != (n in {2, 3, 5, 7, 11, 13, 7919, 999983,
                                1000000007, 1000000009}):
            return False
    p = primes_le(20000)
    s = set(int(v) for v in p)
    for n in range(1, 20001):
        if bool(f(n)) != (n in s):
            return False
    return True


def _carmichael_first():
    def spf_squarefree(n):
        fac, m = [], n
        d = 2
        while d * d <= m:
            if m % d == 0:
                m //= d
                if m % d == 0:
                    return None
                fac.append(d)
            d += 1
        if m > 1:
            fac.append(m)
        return fac
    n = 3
    while True:
        fac = spf_squarefree(n)
        if (fac and len(fac) > 1 and all((n - 1) % (p - 1) == 0
                                         for p in fac)):
            return n
        n += 2


def keybook():
    import math
    inv = pow(17, -1, 3819)
    crt = next(x for x in range(105)
               if x % 3 == 2 and x % 5 == 3 and x % 7 == 2)
    phi360 = sum(1 for k in range(1, 361) if math.gcd(k, 360) == 1)
    d = 1
    while pow(10, d, 101) != 1:
        d += 1
    phi28 = sum(1 for k in range(1, 29) if math.gcd(k, 28) == 1)
    qr41 = len({x * x % 41 for x in range(1, 41)})
    n = 3215031751
    largest = 0
    for p in (151, 751, 28351):
        while n % p == 0:
            n //= p
        largest = max(largest, p)
    assert n == 1
    return {
        "q01": ("int", inv),
        "q02": ("int", crt),
        "q03": ("int", phi360),
        "q04": ("int", d),
        "q05": ("int", phi28),
        "q06": ("int", qr41),
        "q07": ("int", pow(3, 6, 13)),
        "q08": ("int", _carmichael_first()),
        "q09": ("int", pow(2, 100, 101)),
        "q10": ("int", math.gcd(4181, 4087)),
        "q11": ("int", largest),
        "q12": ("func", _check_is_prime),
    }
