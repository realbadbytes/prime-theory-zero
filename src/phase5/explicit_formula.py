"""Phase 5 lab: the explicit formula -- primes as a superposition of waves.

Riemann-von Mangoldt explicit formula (smoothed Chebyshev function):

  psi(x) = x  -  sum_rho  x^rho / rho  -  ln(2*pi)  -  1/2 ln(1 - x^-2)

where psi(x) = sum over prime powers p^k <= x of ln p, and rho runs over
the nontrivial zeros of zeta. This single identity is the summit of the
course: the primes' fine structure equals a sum of waves, one per zero,
each with amplitude x^Re(rho).

  * If RH is true (all Re(rho) = 1/2): every wave has amplitude sqrt(x)
    -> the error psi(x) - x is O(sqrt(x) ln^2 x).  THAT is what "RH is
    about the error term of the PNT" means, concretely.
  * A zero with Re(rho) = 1/2 + eps would make its wave dominate forever.

This lab computes the first zeros with mpmath and plots how the truncated
wave sum already begins to reproduce psi(x)'s staircase -- see
data/phase5_explicit_formula.png.

Run:  python src/phase5/explicit_formula.py [num_zeros] [xmax]
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath
from common.primes import primes_upto, ensure_outdir

mpmath.mp.dps = 25


def psi_exact(x_max: int) -> tuple:
    """Return step-function samples of psi(x) on a fine grid up to x_max."""
    primes = primes_upto(x_max).astype(np.int64)
    X = np.linspace(3.0, x_max, 4000)
    psi = np.zeros_like(X)
    # psi(x) = theta(x) + theta(x^(1/2)) + theta(x^(1/3)) + ...
    power = 1
    while True:
        root = x_max ** (1.0 / power)
        cnt = np.searchsorted(primes, np.power(X, 1.0 / power), side="right")
        theta = np.log(primes[: int(max(cnt.max(), 1)) + 1].astype(np.float64))
        cum = np.concatenate(([0.0], np.cumsum(theta)))
        psi += cum[cnt]
        if root < 2:
            break
        power += 1
    return X, psi


def psi_explicit(X, zeros) -> np.ndarray:
    """Riemann-von Mangoldt explicit formula, zeros truncated to `zeros`.

    Waves evaluated in numpy complex128 (fast); zeros themselves come from
    mpmath at high precision, so their positions are not the bottleneck.
    """
    Z = np.array([complex(z) for z in zeros], dtype=np.complex128)
    out = X - float(mpmath.log(2 * mpmath.pi)) - 0.5 * np.log(1 - X ** -2)
    logX = np.log(X)[:, None]
    waves = np.exp(Z * logX) / Z          # x^rho / rho for all (x, rho)
    out -= 2.0 * np.real(waves).sum(axis=1)   # pair rho with conj(rho)
    return out


def main() -> None:
    n_zeros = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    x_max = int(float(sys.argv[2])) if len(sys.argv) > 2 else 400
    out = ensure_outdir()

    print("=" * 62)
    print(f"First {n_zeros} nontrivial zeros of zeta (mpmath, dps=25)")
    print("=" * 62)
    zeros = []
    for k in range(1, n_zeros + 1):
        z = mpmath.zetazero(k)
        zeros.append(mpmath.mpc(z))
        if k <= 5 or k == n_zeros:
            print(f"  rho_{k:<3} = {z}")
    real_parts = [mpmath.re(z) for z in zeros]
    max_dev = float(max(abs(r - mpmath.mpf("0.5")) for r in real_parts))
    print(f"all computed zeros sit on Re(s)=1/2 (RH holds here); "
          f"max deviation {max_dev:.2e}")
    print("(this is NOT a proof of RH -- we only looked at 20 of the "
          "infinitely many.)")

    X, psi = psi_exact(x_max)
    psi_formula = psi_explicit(X, zeros)
    main_term = X - float(mpmath.log(2 * mpmath.pi)) - \
        0.5 * np.log(1 - X ** -2)

    err_nz = np.max(np.abs(psi - main_term))
    err_w = np.max(np.abs(psi - psi_formula))
    print(f"\npsi(x) - main term:          max |error| over [3,{x_max}] = {err_nz:8.3f}")
    print(f"psi(x) - main - {n_zeros} waves:  max |error| over [3,{x_max}] = {err_w:8.3f}")
    print("The waves ARE the error term: what they don't cancel is the tail "
          "of the next thousands of zeros.")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    ax1.plot(X, psi, color="k", lw=1, label="psi(x) exact (staircase)")
    ax1.plot(X, main_term, ":", color="tab:red", label="main term (no zeros)")
    ax1.plot(X, psi_formula, color="tab:blue", lw=1,
             label=f"explicit formula, {n_zeros} zeros")
    ax1.set_ylabel("psi(x)")
    ax1.set_title(f"The primes of [3,{x_max}] as a sum of {n_zeros} zeta-zero waves")
    ax1.legend(); ax1.grid(alpha=0.3)

    ax2.plot(X, psi - main_term, color="tab:red", alpha=0.5,
             label="error WITHOUT zero-waves")
    ax2.plot(X, psi - psi_formula, color="tab:blue",
             label="error WITH 20 waves")
    ax2.axhline(0, color="k", lw=0.5)
    ax2.set_xlabel("x"); ax2.set_ylabel("residual")
    ax2.set_title("What the waves cancel (the rest is the next thousand zeros)")
    ax2.legend(); ax2.grid(alpha=0.3)
    fig.tight_layout()
    png = os.path.join(out, "phase5_explicit_formula.png")
    fig.savefig(png, dpi=150)
    plt.close(fig)
    print(f"\nfigure -> {png}")
    print("\nNow the punchline, in one line: each wave x^rho/rho has size "
          f"x^{{Re(rho)}}.\nRH (all Re=1/2) <=> error ~ sqrt(x) => psi(x) = x + "
          "O(sqrt(x) ln^2 x).\nThe green curve in phase3/pnt_lab.py is "
          "pi(x)-Li(x): THIS is what makes it wiggle.")


if __name__ == "__main__":
    main()
