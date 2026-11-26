# Phase 3 — The Distribution of Primes (elementary route)

**Budget: 4–6 months. Requires Phase 0–2. The summit of the elementary
world: you will prove things that are genuinely hard, see exactly where
elementary methods hit their wall, and understand the PNT at the level of
*what is true, what is proved, and what is left over*.**

## Reading

- **Apostol, *Introduction to Analytic Number Theory*** — chapters 1–4
  (convolution, μ, φ, Dirichlet series), then 13 (Chebyshev, PNT history).
  Dense; that's the price of the standard gateway.
- **Granville's notes** (free) in parallel — clearer prose on the same ground.
- **Axler, *Prime Obsession*** — read it now, in bed, once. It explains RH
  at your current level; you'll re-read it after Phase 5 and it will be a
  different book.

## The lecture

**1. Chebyshev functions.** θ(x) = Σ_{p≤x} ln p, ψ(x) = Σ_{p^k≤x} ln p =
Σ_{n≤x} Λ(n) (von Mangoldt Λ). π ↔ θ ↔ ψ are Abel-summation-equivalent —
do the two reductions once (θ(x) ~ x ⟺ π(x) ~ x/ln x; ψ vs θ differ by
√x-scale terms).

**2. Chebyshev's theorem (1852).** c₁ x/ln x ≤ π(x) ≤ c₂ x/ln x with
explicit c₁ < 1 < c₂ (around 0.92/1.11 for large x; the *proofs* give
weaker constants — that honesty matters). Route: bounds for binomial
coefficients / central binomials, ψ(x) ≲ x ≲ ψ(2x). Do it twice; it is the
model of every sandwich proof ahead.

**3. Bertrand's postulate (1850).** A prime in (x, 2x]. Erdős's 1932 proof
(ages 19) is 6 pages of binomial bookkeeping and is the friendliest
"real theorem" in number theory — prove it first thing this phase.

**4. Mertens theorems (1874).** Σ_{p≤x} ln p/p = ln x + O(1); Π_{p≤x} (1−1/p)
~ e^{−γ}/ln x; Σ_{p≤x} 1/p = ln ln x + M + o(1). These are the *elementary*
shadow of the PNT: same logarithmic texture, provable without complex
analysis.

**5. ζ(s), s real.** ζ(s) = Π (1−p^{-s})^{-1} for s > 1 (Phase 2); as
s → 1⁺, ζ(s) ~ 1/(s−1). The pole at s = 1 is "the reason there are
primes at all" — every later proof is an exploitation of this sentence.

**6. The Prime Number Theorem (1896).** π(x) ~ x/ln x, Hadamard & de la
Vallée Poussin independently; de la Vallée Poussin also:
π(x) = li(x) + O(x e^{−c√ln x}). Elementary proofs came in 1949 (Selberg,
Erdős — the "elementary method"; Selberg's proof needs the key identity
Λ*Λ ≈ …; read the history: Hardy judged elementary proofs *uninteresting*,
which is one of the funniest wrong predictions in mathematics).
You must be able to state: π ~ x/lnx ⟺ ψ ~ x ⟺ Σ Λ(n)/n ~ ln x, and prove
the implications you can with Abel summation.

**7. Why elementary methods hit a wall.** Chebyshev's c₁, c₂ can be tuned
but never *closed* to 1; the obstruction is exactly that the error term
requires understanding ζ beyond the real line (the pole at 1 controls the
main term; *zeros* nearby control the error). Read this as the season
finale: Phase 4–5 is the sequel.

**8. The gap problem opens.** Bertrand ⇒ gaps < pₙ. n!+2..n!+n ⇒ gaps as
long as you like. Cramér model (1936): treat "n prime" as independent event
of probability 1/ln n ⇒ longest gap below x ~ (ln x)². State Cramér's
conjecture (lim sup gₙ/ln²pₙ = 1). Maier's theorem (1985) and the 2018
Ford–Green–Konyagin–Maynard–Tao theorem (records beat (ln x)² times an
unbounded factor) will be *understood* in Phase 6 — now just know the lab
shows records sitting below the prediction, and that this is a theorem-level
truth about models, not a numerical fluke.

## Exercises

★1. Prove π ~ x/lnx ⟹ θ ~ x and converse (Abel both ways).
★2. Full Erdős proof of Bertrand's postulate. (Do it; budget 2 weeks.)
★★3. Chebyshev: prove ψ(x) = O(x) and ψ(x) ≳ x via central binomials.
★★4. From ψ(x) ~ x prove Π_{p≤x}(1−1/p) ~ e^{−γ}/ln x (Mertens 3) or cite
   carefully and derive Σ 1/p = ln ln x + M + o(1) from it.
★★5. Show li(x) ~ x/ln x + x/ln²x + 2x/ln³x by repeated integration by
   parts; then explain in one paragraph why `pnt_lab.py` shows Li beating
   x/ln x by orders of magnitude at x = 10⁶ (hint: ln 10⁶ ≈ 13.8).
★★6. Cramér-model derivation: P(gap > λ ln² x) ≈ e^{−λ}; expected longest
   gap ~ (ln x)²; then answer: what independence assumption fails, and
   which lab/theorem from Phase 6 punishes it?
★★★7. Rosser–Schoenfeld: π(x) > x/ln x for x ≥ 17 is a *proved* inequality;
   `gap_lab.py`/`pnt_lab.py` data agrees up to 2e7. Where does the ratio
   x/ln x / π(x) bottom out at 10⁸ (compute it)? Why must it return toward
   1 forever?

## Labs

- `src/phase3/pnt_lab.py [xmax]` — π(x) counted vs x/ln x vs Li(x);
  relative-error figure; CSV for your own plots.
- `src/phase3/gap_lab.py [xmax]` — every gap even; record-gap table;
  Cramér and Maier–Pomerance reference curves. At 2e7 the true record is
  180 (at p = 17,051,707) — verify the table against PrimePages if you
  don't trust us (you shouldn't, blindly).

## When you're done

You can prove Bertrand and Chebyshev's bounds; you can explain the PNT, its
history, and the *precise* sense in which "the error term is the whole game
now". Next phase is the tool that makes the error term visible: complex
analysis.
