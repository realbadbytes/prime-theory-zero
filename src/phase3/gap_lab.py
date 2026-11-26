"""Phase 3 lab: prime gaps and the Cramer model.

gap g_n = p_(n+1) - p_n. Facts you will measure:

  * every gap is even (except 2-3 = 1)
  * gaps grow slowly: the LONGEST gap below x, G(x), grows roughly like
    (ln x)^2  -- this is Cramer's 1936 probabilistic prediction
  * the true records run BELOW (ln x)^2 at reachable x and keep creeping
    up toward it: models are asymptotic statements, and "asymptotic" can
    be slow

Run: python3 src/phase3/gap_lab.py [xmax]      (default 2e7)
"""

import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common.primes import primes_upto, ensure_outdir

EULER_GAMMA = 0.5772156649015329


def main() -> None:
    xmax = int(float(sys.argv[1])) if len(sys.argv) > 1 else 20_000_000
    out = ensure_outdir()

    p = primes_upto(xmax)
    g = np.diff(p)

    print(f"primes up to {xmax:,}: {p.size:,}; gaps: {g.size:,}")
    print(f"min gap {g.min()}, max gap {g.max()}, mean {g.mean():.4f}")
    odd = g[1:][g[1:] % 2 == 1]
    assert odd.size == 0, "unexpected odd gap beyond 2->3"
    print("every gap except 2->3 is even: parity forces it (odd-odd).")

    gm = g.astype(np.int64)
    # record gaps: strict rises of the running maximum
    cum = np.maximum.accumulate(gm)
    rec_mask = np.concatenate(([True], cum[1:] > cum[:-1]))
    rec_idx = np.flatnonzero(rec_mask)
    rec_g = gm[rec_idx]
    rec_p = p[rec_idx]                       # gap sits between rec_p and rec_p+rec_g

    print(f"\n{len(rec_g)} record gaps below {xmax:,}. Last 8:")
    print(f"{'gap':>5}  {'first prime of gap':>18}  {'ln(x)^2':>8}  {'2 e^-g ln(x)^2':>14}")
    for gg, pp in list(zip(rec_g, rec_p))[-8:]:
        l2 = math.log(float(pp)) ** 2
        print(f"{gg:>5}  {int(pp):>18,}  {l2:>8.0f}  {2*math.exp(-EULER_GAMMA)*l2:>14.0f}")

    print("""
Read the last two columns: actual records still sit BELOW Cramer's (ln x)^2
and below the Maier-Pomerance refinement 2*e^(-gamma)*(ln x)^2 at this x.
Cramer's model says record/ln(x)^2 -> 1; convergence is glacial, and in
2018 it was PROVEN (Ford-Green-Konyagin-Maynard-Tao) that records
eventually exceed (ln x)^2 times an unbounded factor. The model is wrong
in the long run -- an ocean away. That tension IS the subject.""")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    ax1.hist(np.asarray(g), bins=range(1, int(g.max()) + 2), color="tab:green")
    ax1.set_yscale("log")
    ax1.set_xlabel("gap"); ax1.set_ylabel("count (log)")
    ax1.set_title(f"Gap distribution to {xmax:,}")
    ax1.grid(alpha=0.3)

    X = np.logspace(1, math.log10(xmax), 400)
    ax2.semilogy(X, np.log(X) ** 2, "--", label="(ln x)^2  Cramer")
    ax2.semilogy(X, 2 * math.exp(-EULER_GAMMA) * np.log(X) ** 2, ":",
                 label="2 e^-gamma (ln x)^2  refinement")
    ax2.semilogy(rec_p.astype(np.float64), rec_g, "o-", ms=3,
                 color="tab:red", label="record gaps (actual)")
    ax2.set_xscale("log")
    ax2.set_xlabel("x"); ax2.set_ylabel("longest gap below x")
    ax2.set_title("Record gaps vs Cramer predictions")
    ax2.legend(); ax2.grid(alpha=0.3, which="both")
    fig.tight_layout()
    png = os.path.join(out, "phase3_gaps.png")
    fig.savefig(png, dpi=150)
    plt.close(fig)
    print(f"\nfigure -> {png}")

    print()
    print("Think about it:")
    print(" - Mean gap is ln x, record gap must beat the mean - why does the")
    print("   Cramer model turn 'beat the mean' into (ln x)^2 exactly?")
    print(" - The Maier-Pomerance constant 2e^-gamma ~ 1.122: which probabilistic")
    print("   mistake in Cramer's naive model does it correct?")
    print(" - Your data shows records still BELOW 2e^-gamma (ln x)^2 at this x.")
    print("   The theorem says they EXCEED (2e^-gamma - eps)(ln x)^2 infinitely")
    print("   often. How far out would you have to run to feel the crossing?")


if __name__ == "__main__":
    main()
