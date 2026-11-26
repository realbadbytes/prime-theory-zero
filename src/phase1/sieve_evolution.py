"""Phase 1 lab: the evolution of prime sieving.

Three ways to list primes, run side by side:

  1. trial division      -- the "definition" method.  O(n sqrt n).
  2. classic sieve       -- Eratosthenes in one giant bool array.  O(n log log n)
                            but allocates n bytes at once.
  3. segmented sieve     -- same idea, constant memory (see src/common/primes.py).

Run: python3 src/phase1/sieve_evolution.py

Everything here is deliberately unoptimized: the point is to feel the
algorithmic differences, not to win benchmarks.
"""

import sys, os, time, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
from common.primes import primes_upto


def is_prime_trial(n: int) -> bool:
    """The definition: no divisor other than 1 and itself."""
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            return False
    return True


def trial_primes(limit: int):
    return np.array([n for n in range(2, limit + 1) if is_prime_trial(n)],
                    dtype=np.uint32)


def classic_sieve(limit: int) -> np.ndarray:
    """One full bool array of size limit+1. Fine at 1e6; at 1e12 it isn't."""
    s = np.ones(limit + 1, dtype=bool)
    s[0] = s[1] = False
    for i in range(2, math.isqrt(limit) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.flatnonzero(s).astype(np.uint32)


def main() -> None:
    print("=" * 62)
    print("1. Sanity: the first 25 primes, by definition")
    print("=" * 62)
    first25 = trial_primes(100)
    print(first25.tolist())
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    assert first25.tolist() == expected
    print("matches the classic first-25 list")

    print()
    print("=" * 62)
    print("2. Timing the three methods up to 1,000,000")
    print("=" * 62)
    n = 1_000_000

    t0 = time.perf_counter()
    a = trial_primes(100_000)                 # trial only to 1e5: already slow
    t_trial = time.perf_counter() - t0
    print(f"trial division   (1e5): {t_trial:6.2f}s -> {len(a):,} primes")

    t0 = time.perf_counter()
    b = classic_sieve(n)
    t_classic = time.perf_counter() - t0
    print(f"classic sieve    ({n:,}): {t_classic:6.2f}s -> {len(b):,} primes")

    t0 = time.perf_counter()
    c = primes_upto(n)
    t_seg = time.perf_counter() - t0
    print(f"segmented sieve  ({n:,}): {t_seg:6.2f}s -> {len(c):,} primes")

    assert np.array_equal(b, c)
    print("\nclassic and segmented agree exactly.")
    print(f"pi(1e6) = {len(b):,}   (textbook value: 78,498)")

    print()
    print("Think about it:")
    print(" - why did trial division need ~sqrt(n) work per candidate?")
    print(" - the classic sieve allocated 1 byte per NUMBER; the segmented")
    print("   sieve allocated 1 byte per number in ONE segment (a few MB")
    print("   fixed) no matter how high we go. Prove to yourself that the")
    print("   segment loop in src/common/primes.py never grows its buffer.")


if __name__ == "__main__":
    main()
