# Phase 5 — Analytic Number Theory & the Riemann Hypothesis

**Budget: 4–8 months. Requires Phase 4. This is the destination the whole
course was built toward: the explicit formula, and RH understood not as a
million-dollar cryptic conjecture but as a sharp, physical statement about
the size of the error in the prime number theorem.**

## Reading

- **Davenport, *Multiplicative Number Theory*** — chapters 1–8. The classic.
- **Granville's notes / surveys** (free) — his PNT-with-error expositions
  are the clearest prose in the subject.
- **Montgomery & Vaughan, *The Distribution of Prime Numbers*** — once
  Davenport spins you up, this is the clearest path through the explicit
  formula material.
- **Reread Axler tonight.** After this phase the book is a victory lap.
- Optional and famous: *An Illustrated Proof of the Prime Number Theorem*
  (Aalto & Rempe-Gillen, free on arXiv) and Zagier's one-page proof —
  both become *readable* now; both are the whole theorem in miniature.

## The lecture

**1. ζ, continued.** Euler product for Re s > 1; analytic continuation to
ℂ∖{1} (Euler–Maclaurin or the theta trick — do one); functional equation
relating s ↔ 1−s; trivial zeros at −2, −4, …; the critical strip 0 < Re s < 1; the counting
function N(T) = #{0 < Im ρ ≤ T} obeys Riemann–von Mangoldt,
N(T) = (T/2π)·ln(T/2π) − T/2π + 7/8 + S(T) with S(T) = O(ln T) — memorize
the main terms; gates will ask you to evaluate them;
nontrivial zeros ρ = ½ + iγ. RH: all ρ have Re = 1/2. Known: infinitely
many on the line (Hardy 1914), >40% (Conrey), and verified numerically for
the first 10¹⁰+ zeros — all *theorems* you can now parse.

**2. The explicit formula — the summit.** For ψ(x) = Σ_{n≤x} Λ(n):

  ψ₀(x) = x − Σ_ρ x^ρ/ρ − ln(2π) − ½ ln(1 − x⁻²)

(the sum over zeros is a limit over |Im ρ| < T; each zero contributes a
wave x^{Re ρ} with frequency Im ρ). Read it aloud: *the prime-counting
staircase is the smooth line x plus an interference pattern of pure tones
at the imaginary parts of the zeros.* This is Riemann 1859. It is the
Fourier duality of number theory. `src/phase5/explicit_formula.py` draws
20 tones and shows them carving the staircase.

**3. Error terms, ordered.** PNT with de la Vallée Poussin's saving
(exp(−c√ln x)); zero-free regions are *where you can prove no zeros are*,
and every such region buys an error term; conversely an error term implies
a zero-free region. Table of the logic to memorize the direction of arrows:

  zero-free region  ⟺  explicit error term
  RH (Re ρ = ½ all ρ)  ⟹  ψ(x) = x + O(√x ln²x)
  ψ(x) = x + O(x^{1/2+ε}) ∀ε  ⟹  RH

(von Koch 1901: these are *equivalences*, not just one-way hopes.)

**4. Where Li wins and where it hurts.** π(x) = Li(x) − Σ_ρ Li(x^ρ) + …;
Littlewood (1914): π(x) − Li(x) changes sign infinitely often (RH-ish
oscillations forced by the zeros) — the first sign change is near 1.4×10³¹⁶
(Skewes made the famous number as the first explicit upper bound for it). Your phase-3 lab's
wobble is the visible tip of this.

**5. L-functions and races (preview of Phase 6).** Replace χ·Λ for a
Dirichlet character χ mod q; zeros of L(s,χ) control races π(x;q,a) vs
π(x;q,b); "primes in AP" = zeros off the real axis; RH generalized (GRH)
buys square-root error in every race. This one paragraph is a whole
second course — but you now speak enough of the language to know what the
billboard says.

## Exercises

★1. Show ζ(s) → ∞ as s → 1⁺ and ζ has a simple pole at 1 (integral test
   + Euler product comparison).
★2. From ψ ~ x + O(x^θ) for some θ < 1, derive π(x) = Li(x) + O(x^θ ln x)
   (Abel summation twice; this is the "error term travels" drill).
★★3. Read the explicit formula's proof in Montgomery–Vaughan (or
   Davenport) line by line; write the one-paragraph summary of which
   contour you close and why the poles you pick up are exactly: s=1 (the
   main term), the ρ (the waves), s = 0, −2, −4… (the small terms).
★★4. RH ⟹ ψ = x + O(√x ln²x): assuming all Re ρ = ½, justify bounding
   Σ_{|γ|<T} x^{1/2}/|ρ| by √x ln²x (count zeros with the Riemann–von Mangoldt formula
   N(T) = (T/2π)·ln(T/2π) − T/2π + 7/8 + S(T), S(T) = O(ln T);
   you may quote it).
★★5. Lab forensics: `explicit_formula.py` uses 20 zeros and x ≤ 400.
   Raise zeros to 100, x to 2000. Describe *where* the truncated formula
   still fails and why (Gibbs-like tails of the omitted waves; the trivial
   terms; the x^{1/2}-wall).
★★★6. Compute ζ(−1) with mpmath (−0.08333… = −1/12); explain in 3
   sentences exactly why this does not contradict Σ n = ∞ (analytic
   continuation ≠ summation of the divergent series).

## Lab

`src/phase5/explicit_formula.py [n_zeros] [xmax]` — prints zeros, compares
exact ψ(x) against (a) the main-term-only formula and (b) the 20-wave
version, and plots the residuals. Punchline printed by the lab: each wave's
amplitude is x^{Re ρ}; pin every Re ρ at ½ and the error is √x-sized —
which is RH, wearing its working clothes.

## When you're done

Someone says "RH is about the error term of the PNT" and you can complete
the sentence with "...because the explicit formula expresses the error as
a sum over zeros, each wave having amplitude x^{Re ρ}; bounding all
Re ρ ≤ ½ gives √x-scale waves — and von Koch shows the converse" —
and you would *mean* every word of it.
