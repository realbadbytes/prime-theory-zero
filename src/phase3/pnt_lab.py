"""Phase 3 lab: the Prime Number Theorem, measured.

pi(x)  vs  x/ln x  vs  Li(x)

  * pi(x): counted exactly, via the segmented sieve in src/common.
  * x/ln x: the PNT's canonical main term (Gauss guessed density ~1/ln x
    around 1792; the equivalence pi(x) ~ x/ln x is the Prime Number Theorem).
  * Li(x) = integral_2^x dt/ln t: Gauss's sharper guess (computed via mpmath).

The PNT says pi(x) ~ x/ln x. Gauss knew something sharper: Li(x) matches
far better. You will watch the RELATIVE error of each approximation decay,
and see Li(x) win by orders of magnitude -- and you'll see the error
curve's shape, which is the thing Phase 5 explains with zeros of zeta.

Run:  python src/phase3/pnt_lab.py [xmax]        (default 2e7)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath
from common.primes import primes_upto, ensure_outdir


def main() -> None:
    xmax = int(float(sys.argv[1])) if len(sys.argv) > 1 else 20_000_000
    out = ensure_outdir()

    primes = primes_upto(xmax)
    pi = primes.size
    print(f"pi({xmax:,}) = {pi:,}")

    X = np.logspace(1, np.log10(xmax), 40).astype(np.int64)
    cnt = np.searchsorted(primes, X, side="right").astype(np.float64)
    xf = X.astype(np.float64)
    li = np.array([float(mpmath.li(float(x))) for x in X])
    naive = xf / np.log(xf)

    print(f"{'x':>12}  {'pi(x)':>10}  {'x/ln x':>10}  {'relerr%':>8}  "
          f"{'Li(x)':>10}  {'relerr%':>8}")
    for i in range(len(X)):
        if X[i] < 1000:
            continue
        e1 = 100 * (naive[i] / cnt[i] - 1)
        e2 = 100 * (li[i] / cnt[i] - 1)
        print(f"{X[i]:>12,}  {cnt[i]:>10,.0f}  {naive[i]:>10,.0f}  {e1:>8.3f}  "
              f"{li[i]:>10,.0f}  {e2:>8.3f}")

    ratio = cnt / (xf / np.log(xf))
    mask = X >= 541
    print(f"\nratio pi(x)/(x/ln x) at checkpoints >= 541: "
          f"max {ratio[mask].max():.4f} -> min {ratio[mask].min():.4f}")
    print("The ratio never touches 1 on this scale but keeps sliding down")
    print("toward it. 'Squeezed to 1, ever slower' is exactly what")
    print("pi(x) ~ x/ln x means. (Rosser-Schoenfeld: pi(x) > x/ln x for all")
    print("x >= 17 -- and that inequality is still strict at 10^7 up here.)")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    ax1.plot(xf, cnt, label="pi(x) counted")
    ax1.plot(xf, naive, "--", label="x/ln x")
    ax1.plot(xf, li, ":", label="Li(x)")
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_title("pi(x) and its two guesses (log-log)")
    ax1.legend(); ax1.grid(alpha=0.3, which="both")

    m = X >= 1000
    ax2.semilogy(xf[m], np.abs(naive[m] / cnt[m] - 1), label="|x/ln x error|")
    ax2.semilogy(xf[m], np.abs(li[m] / cnt[m] - 1), label="|Li(x) error|")
    ax2.set_xscale("log")
    ax2.set_title("Relative errors: Li(x) dominates by orders of magnitude")
    ax2.legend(); ax2.grid(alpha=0.3, which="both")
    fig.tight_layout()
    png = os.path.join(out, "phase3_pnt.png")
    fig.savefig(png, dpi=150)
    plt.close(fig)

    csv = os.path.join(out, "phase3_pnt.csv")
    np.savetxt(csv, np.column_stack([X, cnt, naive, li]), delimiter=",",
               header="x,pi,x_over_lnx,Li", comments="")
    print(f"\nfigures -> {png}\ncsv     -> {csv}")
    print("\nThink about it: the Li relative error does NOT decay smoothly --")
    print("it wobbles on log-log. That wobble is a superposition of waves at")
    print("the heights of the zeta zeros. Phase 5 will reconstruct them.")


if __name__ == "__main__":
    main()
