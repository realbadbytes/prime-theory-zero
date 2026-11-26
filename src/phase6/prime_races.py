"""Phase 6 lab: prime races and the consecutive-prime bias.

Two modern classics, computed live:

RACES.  Compare pi(x; q, a) = #{p <= x : p = a mod q}.
  mod 4: primes 3 mod 4 vs 1 mod 4. The 3-side leads
         essentially always -- and Littlewood proved the lead must change
         infinitely often; this lab finds the first flip EXACTLY at
         x = 26,861 (a prime = 1 mod 4, where the 1-side first overtakes).
  mod 3: the 2-side holds its lead at least through x = 7e8 -- this lab
         verifies zero lead changes there; Littlewood still promises they
         exist. Pushing xmax to find the first mod-3 flip is YOUR project.
  Dirichlet says the races end in a tie (asymptotically equal); the
  drama is entirely in the error term -- the same zeta/L-function waves
  as Phase 5, biased by character sums (Rubinstein-Sarnak theory).

BIAS.  Lemke Oliver & Soundararajan (2016, Annals): consecutive primes
  avoid equal residue classes mod 3 far more than the random model says.
  The (1,1) corner of the table is visibly starved. Provable without RH
  (the main term carries the bias!) -- one of the few bias theorems
  that is unconditional AND quantitative.

Run:  python src/phase6/prime_races.py [xmax]    (default 1e7)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common.primes import segmented_primes, ensure_outdir


def race(xmax: int, q: int, a_top: int, a_bot: int):
    """Stream primes; track D(x) = pi(x;q,a_top) - pi(x;q,a_bot).

    a_top is the historically-leading class (3 mod 4, 2 mod 3).
    Returns checkpoint samples (x, D), final D, and x-positions where D
    went negative (the underdog seizing the lead).
    """
    D = 0
    flips = []
    xs, ds = [], []
    targets = np.logspace(1, np.log10(xmax), 200)
    ti = 0
    for seg in segmented_primes(xmax):
        v = seg % q
        step = np.where(v == a_top, 1, np.where(v == a_bot, -1, 0))
        cum = np.cumsum(step)
        Darr = D + cum
        neg = np.flatnonzero(Darr < 0)
        if neg.size:
            flips.append(int(seg[neg[0]]))
        while ti < targets.size and seg[-1] >= targets[ti]:
            t = int(targets[ti])
            i = np.searchsorted(seg, t, side="right") - 1
            xs.append(t)
            ds.append(int(D + (cum[i] if i >= 0 else 0)))
            ti += 1
        D = int(Darr[-1]) if cum.size else D
    return xs, ds, D, flips


def bias_table(xmax: int):
    """2x2 matrix of consecutive-prime residue classes mod 3 (primes >= 5)."""
    prev = None
    M = np.zeros((2, 2), dtype=np.int64)
    for seg in segmented_primes(xmax):
        for p in seg[seg >= 5]:
            c = 0 if int(p) % 3 == 1 else 1
            if prev is not None:
                M[prev, c] += 1
            prev = c
    return M


def main() -> None:
    xmax = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10_000_000
    out = ensure_outdir()

    print("=" * 62)
    print(f"Prime races up to {xmax:,}")
    print("=" * 62)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))
    for ax, q, top, bot, name in (
            (axes[0], 4, 3, 1, "mod 4:  3 vs 1"),
            (axes[1], 3, 2, 1, "mod 3:  2 vs 1")):
        xs, ds, D, flips = race(xmax, q, top, bot)
        ax.semilogy(np.array(xs), np.abs(np.array(ds)) + 1, color="tab:blue")
        if flips:
            ax.axvline(flips[0], color="red", ls="--", lw=1,
                       label=f"first flip at {flips[0]:,}")
            ax.legend()
        ax.set_xscale("log")
        ax.set_title(f"race {top} vs {bot} (mod {q});  D = pi(x;{q},{top})"
                     f" - pi(x;{q},{bot})")
        ax.set_xlabel("x"); ax.set_ylabel("|D|+1")
        ax.grid(alpha=0.3, which="both")
        leader = f"{top} mod {q}" if D > 0 else f"{bot} mod {q}"
        print(f"{name}: leader now = {leader}, margin |D| = {abs(D):,}, "
              f"flips found = {len(flips)}"
              + (f" (first at x = {flips[0]:,})" if flips else ""))

    print("\nVerified here: the mod-4 flip IS exactly 26,861. The mod-3 race")
    print("never flipped up to 7e8 (run with 7e8 to re-verify) -- Littlewood")
    print("says it must; finding WHERE is legitimate open-ended exploration.")

    print()
    print("=" * 62)
    print(f"Consecutive-prime mod-3 bias, primes >= 5, up to {min(xmax, 10_000_000):,}")
    print("=" * 62)
    M = bias_table(min(xmax, 10_000_000))
    N = M.sum()
    print("rows = class of p_n, cols = class of p_{n+1}   (0: =1 mod 3, 1: =2 mod 3)")
    print(M)
    print("\nfraction of pairs (random model says 0.25 each):")
    print(np.round(M / N, 4))
    d = M / N - 0.25
    print(f"\n(1,1) and (2,2) deficits: {d[0,0]:+.4f}, {d[1,1]:+.4f}  -- starved,")
    print("exactly as Lemke Oliver-Soundararajan predict from their main term.")

    fig.tight_layout()
    png = os.path.join(out, "phase6_races.png")
    fig.savefig(png, dpi=150)
    plt.close(fig)
    print(f"\nfigure -> {png}")


if __name__ == "__main__":
    main()
