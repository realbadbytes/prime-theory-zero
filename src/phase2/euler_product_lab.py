"""Phase 2 lab: the Euler product -- where primes meet analysis.

Three demonstrations of the bridge identity

    sum_n 1/n^s   =   prod_p (1 - p^-s)^-1        (s > 1)

  1. Harmonic growth:  sum_{n<=N} 1/n  =  ln N + gamma + O(1/N)
  2. Euler's surprise: sum_{p<=x} 1/p ~ ln ln x  (the primes are "almost"
     sparse enough for the reciprocal sum to diverge -- it diverges, but
     at a laughably slow rate)
  3. The product side: prod_p (1-p^-s)^-1 converges to zeta(s); at s=2
     that number is pi^2/6 (Basel problem, Euler 1734).

Run:  python src/phase2/euler_product_lab.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common.primes import primes_upto, ensure_outdir

GAMMA = 0.5772156649015329   # Euler-Mascheroni constant
MERTEN = 0.2614972128476428  # Meissel-Mertens constant


def main() -> None:
    out = ensure_outdir()

    print("=" * 62)
    print("1. Harmonic sum vs ln N + gamma")
    print("=" * 62)
    N = 2_000_000
    h = np.cumsum(1.0 / np.arange(1, N + 1, dtype=np.float64))
    for n in (10_000, 100_000, 1_000_000, N):
        err = h[n - 1] - (np.log(n) + GAMMA)
        print(f"N={n:>9,}: H_N - (ln N + gamma) = {err:+.3e}   (should be ~ -1/2N)")

    print()
    print("=" * 62)
    print("2. sum 1/p over primes vs ln ln x + M")
    print("=" * 62)
    xs = np.logspace(1, 7, 7).astype(np.int64)
    primes = primes_upto(int(xs[-1]))
    inv_cum = np.cumsum(1.0 / primes.astype(np.float64))
    rows = []
    for x in xs:
        cnt = np.searchsorted(primes, x, side="right")
        s = inv_cum[cnt - 1]
        pred = np.log(np.log(x)) + MERTEN
        rows.append((x, s, pred, s - pred))
        print(f"x={x:>9,}: sum 1/p = {s:.5f}   ln ln x + M = {pred:.5f}   diff {s-pred:+.5f}")
    print("(diverges! but reaches only ~3 by x = 10^7 -- Euler's theorem")
    print(" in slow motion: ln ln x -> infinity means 'there are infinitely")
    print(" many primes', via analysis. Prove: if primes were finite, the")
    print(" product would be finite. That is THE bridge.)")

    print()
    print("=" * 62)
    print("3. Euler product -> zeta(2) = pi^2/6, zeta(3) = 1.2020569...")
    print("=" * 62)
    p = primes.astype(np.float64)
    z2_target, z3_target = np.pi ** 2 / 6, 1.202056903159594
    for s, target, name in ((2.0, z2_target, "pi^2/6"), (3.0, z3_target, "Apery")):
        prod = np.prod(1.0 / (1.0 - p ** (-s)))
        print(f"prod over p<=1e7 (1-p^-{s})^-1 = {prod:.9f}   target ({name}) "
              f"= {target:.9f}   rel err {abs(prod/target-1):.2e}")

    # ---- figure ----------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    X = np.logspace(1, 7, 300)
    c = np.searchsorted(primes, X, side="right")
    s = np.where(c > 0, inv_cum[np.clip(c - 1, 0, None)], 0.0)
    ax1.plot(X, s, label="sum_{p<=x} 1/p")
    ax1.plot(X, np.log(np.log(X)) + MERTEN, "--", label="ln ln x + M")
    ax1.set_xscale("log")
    ax1.set_xlabel("x"); ax1.set_ylabel("sum of reciprocal primes")
    ax1.set_title("Euler: the primes are not summable... barely")
    ax1.legend(); ax1.grid(alpha=0.3)

    ax2.semilogy(np.arange(100, N + 1, 100),
                 np.abs(h[np.arange(100, N + 1, 100) - 1]
                        - (np.log(np.arange(100, N + 1, 100)) + GAMMA)),
                 label="|H_N - ln N - gamma|")
    ax2.semilogy(np.arange(100, N + 1, 100), 1 / (2 * np.arange(100, N + 1, 100)),
                 "--", label="1/(2N)")
    ax2.set_xlabel("N"); ax2.set_xscale("log")
    ax2.set_title("Harmonic sum locks onto ln N + gamma")
    ax2.legend(); ax2.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "phase2_euler_product.png"), dpi=150)
    plt.close(fig)
    print(f"\nfigure -> {out}/phase2_euler_product.png")


if __name__ == "__main__":
    main()
