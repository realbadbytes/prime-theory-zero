"""Shared grading primitives for the phase gates.

Answer specs are tuples:
  ("int", exact)                 exact integer
  ("float", value, tol)         |got - value| <= tol
  ("str", canonical_lower)      case/whitespace-insensitive string
  ("bool", value)               True/False
  ("func", checker)             callable student answer; checker(f) -> bool

Ground truth is COMPUTED here or in the gate modules at grade time --
there is no answer key sitting in the repo. MCQ correct values appear as
canonical strings inside the gate sources (a study aid; the lock is social,
not cryptographic -- see README).
"""
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from common.primes import primes_upto  # noqa: E402


def match(spec, got):
    kind = spec[0]
    if kind == "int":
        return isinstance(got, int) and not isinstance(got, bool) and got == spec[1]
    if kind == "float":
        if not isinstance(got, (int, float)) or isinstance(got, bool):
            return False
        return abs(float(got) - spec[1]) <= spec[2]
    if kind == "str":
        return isinstance(got, str) and got.strip().lower() == spec[1]
    if kind == "bool":
        return isinstance(got, bool) and got is spec[1]
    if kind == "func":
        try:
            return bool(spec[1](got))
        except Exception:
            return False
    raise ValueError(f"bad spec kind: {kind!r}")


# ---------------------------------------------------------------- sieving
_PI_CACHE = {}


def primes_le(x):
    x = int(x)
    if x not in _PI_CACHE:
        _PI_CACHE[x] = primes_upto(x)
    return _PI_CACHE[x]


def pi(x):
    p = primes_le(x)
    return int(np.searchsorted(p, int(x), side="right"))


def nth_prime(n):
    """1-indexed. Sieve with a safe upper bound, then count."""
    n = int(n)
    assert n >= 1
    if n < 6:
        return [2, 3, 5, 7, 11][n - 1]
    import math
    ln, lnln = math.log(n), math.log(math.log(n))
    lim = int(n * (ln + lnln)) + 100          # Rosser-Schoenfeld bound
    return int(primes_le(lim)[n - 1])


def li(x, steps=20000):
    """Li(x) = int_2^x dt/ln t, the definition every gate in this repo uses.

    Quadrature note (learned the hard way): uniform Simpson panels in t
    are WRONG here -- near t=2 the integrand varies on a scale far finer
    than (x-2)/steps, giving errors ~15 at x=1e6. The substitution
    t = e^u turns the integral into int_{ln 2}^{ln x} e^u/u du, which is
    smooth on a uniform u-grid: machine precision with these step counts.
    """
    x = float(x)
    if x <= 2:
        return 0.0
    a, b = math.log(2.0), math.log(x)
    m = steps if steps % 2 == 0 else steps + 1
    h = (b - a) / m
    u = np.linspace(a, b, m + 1)
    y = np.exp(u) / u
    s = y[0] + y[-1] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-2:2].sum()
    return float(s * h / 3.0)


def theta(x):
    p = primes_le(x)
    p = p[p <= x]
    return float(np.log(p).sum()) if len(p) else 0.0


def psi(x):
    """psi(x) = sum_{p^k <= x} ln p."""
    import math
    p = primes_le(x)
    total = 0.0
    x = float(x)
    for q in p:
        q = int(q)
        if q > x:
            break
        pk = float(q)
        while pk <= x:
            total += math.log(q)
            pk *= q
    return total


def race_stream(q, lead_cls, lag_cls, xmax):
    """D(x) = pi(x;q,lead_cls) - pi(x;q,lag_cls) evaluated right after every
    prime <= xmax. Returns (flips, primes_list, D_after_each_prime)."""
    p = primes_le(xmax)
    v = p % q
    step = np.where(v == lead_cls, 1, np.where(v == lag_cls, -1, 0))
    D = np.cumsum(step)
    neg = np.flatnonzero(D < 0)
    flips = int(p[neg[0]]) if len(neg) else None
    return flips, p, D


def gap_records(xmax):
    p = primes_le(xmax)
    g = np.diff(p)
    best = 0
    idx = []
    for i in range(len(g)):
        if g[i] > best:
            best = int(g[i])
            idx.append(i)
    return [(int(p[i]), int(g[i])) for i in idx]  # (start prime, gap)


def ls_bias_cell(q, xmax, a, b):
    """Fraction of consecutive-prime pairs with classes (a, b) mod q,
    counting only primes p > q (the LS convention for q=3: primes >= 5;
    primes dividing q itself sit in class 0 and dilute the table)."""
    p = primes_le(xmax)
    p = p[p > q]
    c = p % q
    A = c[:-1] == a
    B = c[1:] == b
    return float((A & B).sum()) / float(len(c) - 1)
