# Phase 2 — Analysis Light

**Budget: 2–4 months. Requires Phase 0–1. Purpose: sharpen exactly the
analysis tools the prime theorems need — nothing more. This is not a full
analysis course; it is an armory.**

## Reading

- **Abbott, *Understanding Analysis*** — sequences and series chapters only
  (plus uniform convergence *read, don't grind*). Skip metric-space detours.
- **Granville, *Introduction to Analytic Number Theory* lecture notes**
  (free, University of Waterloo) — read chapters 1–3 now as motivation;
  the rest after Phase 4. Granville is arguably the best mathematical
  expositor alive; let his prose set your standard.

## The lecture

**1. Asymptotic notation, seriously.** f ~ g means f/g → 1; O(g) is a
bound, o(g) is a smaller-than. These are *quantifier statements* — rewrite
them with ∀ε∃N until mechanical. Prime number theory speaks this natively:
"π(x) ~ x/ln x" is one ∀∃ statement about a staircase and a smooth curve.

**2. Series.** Comparison/ratio/root tests; alternating series; absolute vs
conditional. Key gut-level fact: Σ 1/n diverges (integral/telescope proof),
Σ 1/n² converges — and the boundary between them, ln, will run the show.

**3. The harmonic sum.** H_N = ln N + γ + O(1/N), γ = 0.5772…
Derive it by comparing H_N with ∫dt/t (upper/lower Riemann sums — you did
this in Abbott; make it an exercise). *This asymptotic will reappear,
disguised, three more times in this course.*

**4. Euler products — THE bridge.**
Σ_n 1/nˢ = ∏_p (1 − p^{−s})^{−1} for s > 1.
Proof = unique factorization (Phase 1!) + geometric series + a limiting
argument. Two lines each. Feel the vertigo: a statement about *all integers*
on the left, a statement about *primes* on the right, analytically equal.
Consequences you must be able to state and prove:
  - ζ(1⁺) = ∞ ⇒ primes infinite (Euler's proof).
  - Σ_p 1/p diverges (logarithm-of-the-logarithm rate: Σ_{p≤x} 1/p =
    ln ln x + M + o(1), M = 0.26149…). Prove or cite Mertens (Phase 3
    course), but *feel* it via the lab: at x = 10⁷ the sum is only ≈ 3.
  - ζ(2) = π²/6 (Basel; Euler 1734). You won't reprove it, but the lab
    multiplies over all 664,579 primes up to 1e7 and hits π²/6 to 9 digits —
    *that* is what "the bridge" means numerically.

**5. Abel summation (summation by parts).** For a_n with A(x) = Σ_{n≤x} a_n:
Σ_{n≤x} a_n f(n) = A(x)f(x) − ∫₁ˣ A(t) f′(t) dt (smooth version; discrete
version first). This is integration-by-parts for sums, and it is THE master
move: it converts *any* counting statement (A(t) counts something) into an
integral statement, and vice versa.
  - Show (exercise, do it twice): π(x) ~ x/ln x  ⟺  pₙ ~ n ln n.
    The inversion trick: put y = x/ln x, solve asymptotically via
    x = y(ln y + ln ln y − 1 + …). This is the *rigorous* version of the
    "k(n) drift" curiosity from the project that started this course.

**6. ln as ∫ dt/t and the logarithmic integral.** Li(x) = ∫₂ˣ dt/ln t is
the *other* antiderivative of 1/ln t you will meet constantly. (Notation
warning: many books write li for the principal-value integral from 0 —
this repo always means the offset version from 2, and always writes Li.)
Integration by parts gives the asymptotic series Li(x) ~ x/ln x · Σ k!/ln^k x
— learn the first three terms; they explain Phase 3's Li-vs-x/lnx winner.
  Numerical warning, learned the hard way: never integrate 1/ln t on
*uniform panels in t* — near t = 2 it varies far below any panel width
that reaches out to 10⁶, and a textbook Simpson silently lies by ~15.
Substitute u = ln t: Li(x) = ∫_{ln 2}^{ln x} eᵘ/u du is smooth and any
fixed-panel Simpson is machine-accurate. (A ground truth that a
*correctly computing* student fails is a broken ground truth.)

## Exercises

★1. Prove H_N − ln N converges (monotone + bounded). The limit is γ.
★2. Full proof of the Euler product identity for s > 1.
★★3. Prove: if Σ_p 1/p converged then Σ_n 1/n would converge. Contradiction
   = Euler's infinitude proof, upgraded.
★★4. Abel: derive Σ_{p≤x} (ln p)/p = ln x + O(1) from Σ_{p≤x} ln p = O(x)
   (Chebyshev's bound, which you prove in Phase 3 — accept it now).
★★★5. The inversion: π(x) ~ x/ln x ⇒ pₙ ~ n ln n, with every O/ε tracked.
   Then the sharper version pₙ = n(ln n + ln ln n − 1) + o(n/ln n).
   (This is the exact formula `phase5` and the polycheck page used — now
   you *own* it.)
★★★6. Numerical experiment: fit Σ_{p≤x} 1/p against ln ln x + M and against
   ln ln x only, on [10², 10⁷]; the constant M = 0.26149… is Meissel–Mertens.
   How much x do you need before ln ln x alone gets within 5%? (Answer is a
   sobering lesson in convergence rates.)

## Lab

`src/phase2/euler_product_lab.py` — all three demonstrations, figure in
`data/phase2_euler_product.png`.

## When you're done

You can state and prove the Euler product and its two infinitude
consequences, use Abel summation reflexively, and you know that pₙ ~ n ln n
is a *theorem equivalent* to the PNT — not a plot guess.
