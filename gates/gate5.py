"""GATE 5 — RH & explicit formula checkpoint.

12 questions. 100% required to unlock Phase 6.
"""
import math

PHASE = 5
NEXT_DOC = "phase-6-prime-gaps"
TITLE = "Gate 5 — RH & the Explicit Formula"

FORMAT_NOTES = """
zeta computations: mpmath (mp.zeta / mp.zetazero), dps >= 15.
"""


def questions():
    return [
        {"id": "q01",
         "prompt": "Im(rho_1), the imaginary part of the first nontrivial "
                   "zero of zeta, rounded to 4 decimals. (Float.)"},
        {"id": "q02",
         "prompt": "Sum of the trivial zeros of zeta with |s| <= 10. "
                   "(Integer.)"},
        {"id": "q03",
         "prompt": "zeta(0), rounded to 6 decimals. (Float.)"},
        {"id": "q04",
         "prompt": "von Koch: RH is equivalent to psi(x) = x + O(x^a * "
                   "(ln x)^2). Give a. (Float.)"},
        {"id": "q05",
         "prompt": "Number of nontrivial zeros with 0 < Im(rho) < 100 "
                   "(mpmath count). (Integer.)"},
        {"id": "q06",
         "prompt": "Li(1e6) - pi(1e6) rounded to nearest integer (repo "
                   "Li: int_2^x dt/ln t via u=ln t substitution, gate 2 q09). "
                   "(Integer.)"},
        {"id": "q07",
         "prompt": "Who proved that pi(x) - Li(x) changes sign infinitely "
                   "often? Surname, lowercase. (String.)"},
        {"id": "q08",
         "prompt": "Riemann-von Mangoldt main terms at T = 14: "
                   "(T/2pi)*ln(T/2pi) - T/2pi + 7/8, rounded to 3 "
                   "decimals. (Float.)"},
        {"id": "q09",
         "prompt": "The zeta functional equation relates zeta(s) to "
                   "zeta(?). Answer like '1-s'. (String.)"},
        {"id": "q10",
         "prompt": "Define psi(x) = sum_{n<=x} vonMangoldt(n) as a float. "
                   "(Function.)"},
        {"id": "q11",
         "prompt": "Li(1e4) - pi(1e4) rounded to nearest integer. "
                   "(Integer.)"},
        {"id": "q12",
         "prompt": "MCQ. Under RH, each zero rho contributes a wave to "
                   "psi(x) of size:\n"
                   "  A) x^Im(rho)\n"
                   "  B) x^(1/2)\n"
                   "  C) x / ln x\n"
                   "  D) ln x / |rho|\n"
                   "Answer (letter)."},
    ]


def _check_psi(f):
    from gate_common import psi
    for x in (100, 1000, 1234):
        w = psi(x)
        if abs(float(f(x)) - w) > 1e-6 * max(1.0, w):
            return False
    return True


def keybook():
    import mpmath as mp
    from gate_common import li, pi
    mp.mp.dps = 15
    n100, k = 0, 1
    while mp.im(mp.zetazero(k)) < 100:
        n100 += 1
        k += 1
    T = 14.0
    r = T / (2 * math.pi)
    return {
        "q01": ("float", round(float(mp.im(mp.zetazero(1))), 4), 1e-4),
        "q02": ("int", -(2 + 4 + 6 + 8 + 10)),
        "q03": ("float", round(float(mp.zeta(0)), 6), 1e-6),
        "q04": ("float", 0.5, 1e-9),
        "q05": ("int", n100),
        "q06": ("int", round(li(1e6)) - pi(10 ** 6)),
        "q07": ("str", "littlewood"),
        "q08": ("float", round(r * math.log(r) - r + 7 / 8, 3), 1e-3),
        "q09": ("str", "1-s"),
        "q10": ("func", _check_psi),
        "q11": ("int", round(li(1e4)) - pi(10 ** 4)),
        "q12": ("str", "b"),
    }
