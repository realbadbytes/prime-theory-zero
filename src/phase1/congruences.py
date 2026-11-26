"""Phase 1 lab: congruences, CRT, orders, and quadratic reciprocity.

The workbench for the algebraic half of elementary number theory:

  * extended Euclid + modular inverses
  * Chinese Remainder Theorem, built constructively (proof = algorithm)
  * multiplicative order and primitive roots (baby steps toward (Z/p)* structure)
  * Legendre symbol + an experimental verification of quadratic reciprocity

Run:  python src/phase1/congruences.py
"""

import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.primes import small_sieve


def egcd(a: int, b: int):
    """Extended Euclid: returns (g, x, y) with a*x + b*y = g = gcd(a,b)."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a % m, m)
    assert g == 1, f"{a} not invertible mod {m}"
    return x % m


def crt(residues, moduli):
    """Constructive CRT. Returns x in [0, prod(moduli)) with x = r_i mod m_i."""
    N = 1
    for m in moduli:
        N *= m
    x = 0
    for r, m in zip(residues, moduli):
        Mi = N // m
        x += r * Mi * modinv(Mi, m)
    return x % N


def order(a: int, p: int) -> int:
    """Multiplicative order of a mod p (brute force; p small)."""
    assert pow(a, 1, p) != 0
    d = 1
    x = a % p
    while x != 1:
        x = x * a % p
        d += 1
    return d


def primitive_root(p: int) -> int:
    """Smallest g with ord_p(g) = p-1 (brute force; p small)."""
    for g in range(2, p):
        if order(g, p) == p - 1:
            return g


def legendre(a: int, p: int) -> int:
    """Legendre symbol (a/p) via Euler's criterion."""
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def main() -> None:
    print("=" * 62)
    print("1. Extended Euclid + inverses")
    print("=" * 62)
    inv = modinv(17, 3819)
    print(f"17^-1 mod 3819 = {inv}   check: 17*{inv} mod 3819 = {17 * inv % 3819}")

    print()
    print("=" * 62)
    print("2. Chinese Remainder Theorem (the sun-tzu problem)")
    print("=" * 62)
    x = crt([2, 3, 2], [3, 5, 7])
    print(f"x = 2 mod 3, 3 mod 5, 2 mod 7  ->  x = {x}  (classic answer: 23)")
    assert x == 23

    print()
    print("=" * 62)
    print("3. The group (Z/p)*: orders and primitive roots")
    print("=" * 62)
    for p in (7, 11, 13, 29, 97):
        g = primitive_root(p)
        ords = sorted(order(a, p) for a in range(1, p))
        assert all((p - 1) % d == 0 for d in ords)      # Lagrange, felt
        print(f"p={p:>3}: primitive root g={g:>3}; orders of all elements: {sorted(set(ords))}"
              f"  (all divide p-1={p-1})")

    print()
    print("=" * 62)
    print("4. Quadratic reciprocity, verified exhaustively for p,q < 50")
    print("=" * 62)
    primes = small_sieve(50)[1:].tolist()            # odd primes < 50
    checked = 0
    for p, q in itertools.combinations(primes, 2):
        lhs = legendre(p, q) * legendre(q, p)
        rhs = -1 if (p % 4 == 3 and q % 4 == 3) else 1
        assert lhs == rhs, f"QR failed for {p},{q}"
        checked += 1
    print(f"(p/q)(q/p) = (-1)^((p-1)/2 * (q-1)/2) held for all {checked} pairs < 50")

    # sanity: Legendre symbol vs brute-force squares
    p = 101
    squares = {i * i % p for i in range(1, p)}
    for a in range(1, p):
        assert (a in squares) == (legendre(a, p) == 1)
    print(f"Euler's criterion matches brute-force squares mod {p}: all {p-1} cases")

    print()
    print("Think about it:")
    print(" - CRT's proof IS the function crt() above: build idempotents.")
    print(" - primitive roots mean (Z/p)* is cyclic -- why is that remarkable?")
    print("   (finite subgroup of a field's multiplicative group is cyclic)")
    print(" - QR lets you flip (p/q) <-> (q/p); use it to compute (2026/2029).")


if __name__ == "__main__":
    main()
