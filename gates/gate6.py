"""GATE 6 — Prime gaps & races checkpoint.

12 questions. Ground truth computed at grading time (the mod-3 race scan
to 7e8 takes a few seconds). 100% required to unlock Phase 7.
"""
import numpy as np

PHASE = 6
NEXT_DOC = "phase-7-specialties"
TITLE = "Gate 6 — Gaps, Races & Modern Era"

FORMAT_NOTES = """
Race convention: D(x) = pi(x;q,a) - pi(x;q,b) evaluated right after each
prime, counting ALL primes (including 2). Same convention as prime_races.py.
"""


def questions():
    return [
        {"id": "q01",
         "prompt": "First sign change of pi(x;4,3) - pi(x;4,1): the exact "
                   "x where the 1-mod-4 side first takes the lead. "
                   "(Integer.)"},
        {"id": "q02",
         "prompt": "Chebyshev-bias share: over all primes p with 5 <= p <= "
                   "1e6, what FRACTION have D(p) > 0 for the mod-4 3-vs-1 "
                   "race (D right after p, all primes counted)? Rounded to "
                   "3 decimals. (Float.)"},
        {"id": "q03",
         "prompt": "Lemke Oliver - Soundararajan cell: fraction of "
                   "consecutive-prime pairs below 1e6 (starting from the "
                   "first prime >= 5) that are (1 mod 3, 1 mod 3), rounded "
                   "to 3 decimals. (Float.)"},
        {"id": "q04",
         "prompt": "Is the 7-tuple (0,2,6,8,12,18,20) admissible? "
                   "(Boolean.)"},
        {"id": "q05",
         "prompt": "How many DISTINCT residue classes mod 7 does the "
                   "6-tuple (0,4,6,10,12,16) occupy? (Integer.)"},
        {"id": "q06",
         "prompt": "List the RECORD prime gaps (new maxima of p_{n+1}-p_n) "
                   "below 10^4. Give the sum of the two largest record "
                   "values. (Integer.)"},
        {"id": "q07",
         "prompt": "MCQ. The parity barrier says:\n"
                   "  A) primes are never odd-positioned\n"
                   "  B) sieve methods alone cannot distinguish numbers "
                   "with an even vs odd number of prime factors, so they "
                   "cannot find twin primes\n"
                   "  C) all gaps are even\n"
                   "  D) the zeta zeros have symmetric parity\n"
                   "Answer (letter)."},
        {"id": "q08",
         "prompt": "The 2018 Ford-Green-Konyagin-Maynard-Tao results prove "
                   "that large prime gaps beat the prediction of which "
                   "MODEL? (One name, lowercase.)"},
        {"id": "q09",
         "prompt": "Diameter (max - min) of the admissible 7-tuple "
                   "(0,2,6,8,12,18,20). (Integer.)"},
        {"id": "q10",
         "prompt": "Define is_admissible(t): True iff the integer tuple t "
                   "hits at most p-1 residue classes mod p for EVERY prime "
                   "p <= len(t). (Function.)"},
        {"id": "q11",
         "prompt": "Number of twin prime pairs (p, p+2) with p+2 <= 1000. "
                   "(Integer.)"},
        {"id": "q12",
         "prompt": "How many times does the mod-3 race pi(x;3,2)-pi(x;3,1) "
                   "change leader for 3 <= x <= 7e8? (Integer. This is the "
                   "verified fact of this repo.)"},
    ]


def _admissible_truth(t):
    t = list(t)
    k = len(t)
    primes_small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for p in primes_small:
        if p > k:
            break
        if len({x % p for x in t}) >= p:
            return False
    return True


def _check_is_admissible(f):
    tests = [
        (0, 2, 6, 8, 12, 18, 20),
        (0, 4, 6, 10, 12, 16),
        (0, 1),
        (0, 2, 4),
        (0, 2, 8, 14, 68, 152, 158),
        (0, 1, 2, 3, 4, 5, 6),
    ]
    for t in tests:
        if bool(f(t)) is not _admissible_truth(t):
            return False
    return True


def _race_flip_count(q, a, b, xmax):
    from gate_common import race_stream
    _, p, D = race_stream(q, a, b, xmax)
    s = np.sign(D)
    nz = np.flatnonzero(s != 0)          # skip exact ties
    snz = s[nz]
    return int((snz[1:] != snz[:-1]).sum())


def keybook():
    from gate_common import (gap_records, ls_bias_cell, primes_le,
                             race_stream)
    flip4, p4, D4 = race_stream(4, 3, 1, 10 ** 6)
    share = float((D4[(p4 >= 5)] > 0).mean())
    p1k = primes_le(1000)
    twin = int(((p1k[:-1] + 2 == p1k[1:]) & (p1k[1:] <= 1000)).sum())
    recs = sorted(g for _, g in gap_records(10 ** 4))
    return {
        "q01": ("int", flip4),
        "q02": ("float", round(share, 3), 1e-3),
        "q03": ("float", round(ls_bias_cell(3, 10 ** 6, 1, 1), 3), 1e-3),
        "q04": ("bool", _admissible_truth((0, 2, 6, 8, 12, 18, 20))),
        "q05": ("int", len({x % 7 for x in (0, 4, 6, 10, 12, 16)})),
        "q06": ("int", recs[-1] + recs[-2]),
        "q07": ("str", "b"),
        "q08": ("str", "cramer"),
        "q09": ("int", 20 - 0),
        "q10": ("func", _check_is_admissible),
        "q11": ("int", twin),
        "q12": ("int", _race_flip_count(3, 2, 1, 7 * 10 ** 7)),
    }
