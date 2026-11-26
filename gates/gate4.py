"""GATE 4 — Complex Analysis checkpoint.

12 questions. 100% required to unlock Phase 5. Requires numpy (and mpmath
for q06). q10's function is graded by testing YOUR contour integral
against an independent zero-count (np.roots) on several polynomials --
a numerical-contour implementation is expected, not a root-finder in
disguise (though we cannot stop you; we can only decline to learn).
"""
import numpy as np

PHASE = 4
NEXT_DOC = "phase-5-rh-explicit-formula"
TITLE = "Gate 4 — Complex Analysis"

FORMAT_NOTES = """
Integrals around circles: parametrize z = R*exp(it), t in [0, 2pi), trapz
with plenty of panels. Integers exact; floats within stated tolerance.
"""


def questions():
    return [
        {"id": "q01",
         "prompt": "Residue of 1/(z^2 * sin z) at z = 0, rounded to 6 "
                   "decimals (it is 1/6 if your Laurent game is strong). "
                   "(Float.)"},
        {"id": "q02",
         "prompt": "The integral of e^(1/z) around |z|=1 counterclockwise "
                   "equals c * 2*pi*i. Give c. (Integer.)"},
        {"id": "q03",
         "prompt": "How many zeros of p(z) = z^5 + 3z + 12 lie inside "
                   "|z| = 2? (Integer; argument principle or np.roots — "
                   "both are legitimate here.)"},
        {"id": "q04",
         "prompt": "Classify the singularity of sin(z)/z at z = 0 as "
                   "'removable', 'pole', or 'essential'. (String.)"},
        {"id": "q05",
         "prompt": "True/false: if f is complex-differentiable at z0 then "
                   "the Cauchy-Riemann equations hold at z0. (Boolean.)"},
        {"id": "q06",
         "prompt": "How many nontrivial zeros of zeta have 0 < Im(rho) < "
                   "30? (Integer; mpmath.zetazero.)"},
        {"id": "q07",
         "prompt": "Sum of ALL residues of (3z+2)/(z(z+1)) (finite plane). "
                   "(Integer.)"},
        {"id": "q08",
         "prompt": "MCQ. The argument principle says (1/2 pi i) times the "
                   "closed contour integral of f'/f equals:\n"
                   "  A) #zeros - #poles inside\n"
                   "  B) #poles - #zeros inside\n"
                   "  C) #zeros + #poles inside\n"
                   "  D) the sum of residues of f\n"
                   "Answer (letter)."},
        {"id": "q09",
         "prompt": "Real part of e^(i*pi). (Integer.)"},
        {"id": "q10",
         "prompt": "Define arg_count(coeffs, R): number of zeros of the "
                   "polynomial with numpy-order coeffs strictly inside "
                   "|z|=R, computed by numerically integrating p'/p over "
                   "the circle (>= 4000 panels) and rounding the "
                   "winding number. Return int."},
        {"id": "q11",
         "prompt": "Value of the counterclockwise contour integral of "
                   "1/(z^2+1) around |z|=3 (both poles inside; think "
                   "before computing). Rounded to 4 decimals. (Float.)"},
        {"id": "q12",
         "prompt": "True/false: two functions holomorphic on a connected "
                   "domain that agree on a subset with an accumulation "
                   "point in the domain must agree everywhere. (Boolean.)"},
    ]


def _arg_truth(coeffs, R):
    r = np.roots(coeffs)
    return int((np.abs(r) < R).sum())


def _check_arg_count(f):
    tests = [
        ([1, 0, 0, 0, 3, 12], 2.0),          # straddles
        ([1, 0, 0, 0, 3, 1], 2.0),           # all inside
        ([1, 0, -3, 0, 2], 1.0),             # mixed
        ([1, 0, 0, -1], 2.0),                # all inside (roots of unity)
    ]
    for coeffs, R in tests:
        got = f(coeffs, R)
        if not isinstance(got, (int, np.integer)):
            return False
        if int(got) != _arg_truth(coeffs, R):
            return False
    return True


def keybook():
    import mpmath as mp
    mp.mp.dps = 15
    n30, k = 0, 1
    while mp.im(mp.zetazero(k)) < 30:
        n30 += 1
        k += 1
    return {
        "q01": ("float", round(1 / 6, 6), 1e-6),
        "q02": ("int", 1),
        "q03": ("int", _arg_truth([1, 0, 0, 0, 3, 12], 2.0)),
        "q04": ("str", "removable"),
        "q05": ("bool", True),
        "q06": ("int", n30),
        "q07": ("int", 3),
        "q08": ("str", "a"),
        "q09": ("int", -1),
        "q10": ("func", _check_arg_count),
        "q11": ("float", 0.0, 1e-4),
        "q12": ("bool", True),
    }
