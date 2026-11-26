"""Phase 1 lab: primality testing, from Fermat to Miller-Rabin.

Arc of the lab:
  1. Fermat's little theorem as a *test* -- and why it fails.
  2. Carmichael numbers: the exact integers that fool the Fermat test.
  3. Miller-Rabin: the fix (strong pseudoprimes), with a famous number
     that fools the small base-set but not the full deterministic one.

Facts used below are classical and can be checked in any Phase-1 book:
  * Deterministic Miller-Rabin: testing bases 2,3,5,7,11,13,17 is enough
    for all n < 341,550,071,728,321.
  * 3,215,031,751 is a strong pseudoprime to bases 2,3,5 and 7 (so bases
    2..7 alone are NOT deterministic past 3.2e9), but base 11 catches it.
  * The smallest Carmichael numbers are 561, 1105, 1729 (the Hardy-Ramanujan
    taxicab number!), 2465, 2821.

Run:  python src/phase1/primality_lab.py
"""

import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def fermat_passes(n: int, a: int) -> bool:
    """Fermat test base a: passes iff a^n == a (mod n)."""
    return pow(a, n, n) == a % n


def is_prime_by_fermat_all_bases(n: int) -> bool:
    """'Prime' if it passes for EVERY base 1..n-1. (Definition-level test.)"""
    return all(fermat_passes(n, a) for a in range(2, n - 1))


def find_carmichael(limit: int):
    """Composite n passing the Fermat test for all bases -- brute force."""
    found = []
    for n in range(3, limit, 2):
        # quick compositeness via trial division
        d = 2
        composite = False
        while d * d <= n:
            if n % d == 0:
                composite = True
                break
            d += 1 if d == 2 else 2
        if not composite:
            continue                      # actually prime, not a pseudoprime
        if all(pow(a, n, n) == a % n for a in range(2, n - 1)):
            found.append(n)
    return found


def miller_rabin_probable(n: int, bases) -> bool:
    """Miller-Rabin with a fixed base set. True = 'probably prime'."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in bases:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def main() -> None:
    print("=" * 62)
    print("1. Fermat's little theorem, felt numerically")
    print("=" * 62)
    p = 7919                                  # a prime (p_1000)
    bad = [a for a in range(2, 200) if not fermat_passes(p, a)]
    print(f"prime p={p}: bases 2..199 that VIOLATE a^p == a (mod p): {bad}")
    print("(empty, as FLT promises; and its proof is Exercise in phase-1 doc)")

    print()
    print("=" * 62)
    print("2. Carmichael numbers: the Fermat test's Achilles heel")
    print("=" * 62)
    cars = find_carmichael(10_000)
    print(f"composites below 10,000 passing Fermat for ALL bases: {cars}")
    assert 561 in cars and 1105 in cars and 1729 in cars
    print("the classic trio 561, 1105, 1729 is present (1729 = taxicab number)")

    print()
    print("=" * 62)
    print("3. Miller-Rabin and the price of a too-small base set")
    print("=" * 62)
    tricky = 3_215_031_751
    small = miller_rabin_probable(tricky, (2, 3, 5, 7))
    full = miller_rabin_probable(tricky, (2, 3, 5, 7, 11, 13, 17))
    # factor it by trial division so the claim printed below is computed, not quoted
    m, fs = tricky, []
    d = 2
    while d * d <= m:
        while m % d == 0:
            fs.append(d); m //= d
        d += 1
    if m > 1:
        fs.append(m)
    print(f"n = {tricky:,} (composite: {' * '.join(map(str, fs))})")
    print(f"  Miller-Rabin bases 2,3,5,7   -> says prime?  {small}   <- fooled")
    print(f"  Miller-Rabin bases 2..17     -> says prime?  {full}   <- correct")

    big = 2**61 - 1                           # Mersenne prime M61 (1952!)
    print(f"M61 = 2^61-1 = {big:,}: MR(2..17) probable prime? "
          f"{miller_rabin_probable(big, (2,3,5,7,11,13,17))}")

    rng = random.Random(1)
    def rand_prime(bits):
        while True:
            c = rng.randrange(1 << (bits - 1), 1 << bits) | 1
            if miller_rabin_probable(c, (2, 3, 5, 7, 11, 13, 17)):
                return c
    composites = []
    while len(composites) < 500:
        a, b = rand_prime(25), rand_prime(25)
        if a != b:
            composites.append(a * b)               # definitely composite
    liars = sum(miller_rabin_probable(n, (2, 3, 5, 7, 11, 13, 17))
                for n in composites)
    print(f"500 semiprimes (~1e15, two random 25-bit primes): "
          f"{liars}/500 slipped through 7 bases (must be 0 here)")

    print()
    print("Think about it:")
    print(" - the Fermat test fails because a^{n-1}=1 can hold for ALL a when")
    print("   the group (Z/n)* has exponent dividing n-1 (Carmichael, Korselt).")
    print(" - Miller-Rabin asks the STRONGER question: is -1 the first hit of")
    print("   x^2=1 along the squaring chain? Prove: prime n => chain ends at")
    print("   -1 or starts at 1. That one line is the whole theorem.")


if __name__ == "__main__":
    main()
