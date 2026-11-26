# Phase 4 — Complex Analysis

**Budget: 4–6 months. Requires Phase 2's rigor instincts. This is the gate
of the whole course. It is also, done right, the most beautiful mathematics
you will ever learn; treat it as a reward, not a toll.**

## Reading

- **Needham, *Visual Complex Analysis*** — the intuition book. Chapters on
  complex dynamics, differentiation, Cauchy's theorem, winding numbers,
  residues. Read for the pictures; every theorem has a geometric soul and
  Needham shows it.
- **Stein & Shakarchi, *Complex Analysis*** — the rigor spine; chapters
  1–5 and 8. Do its exercises; Needham alone will not survive a problem set.
- Warm-up: 3Blue1Brown's Euler-formula and winding-number videos (free).

## The lecture (the route primes need)

**1. ℂ as geometry.** Multiplication = rotation × scaling; e^{iθ} =
rotation by θ; roots of unity as regular polygons. Euler's formula is a
definition to be felt, not a theorem to be feared.

**2. Holomorphic functions.** Complex derivative; Cauchy–Riemann equations;
"complex differentiable once ⇒ infinitely differentiable" — the first shock.
Holomorphic maps are conformal (angles preserved): needham's whole thesis.

**3. Contour integration; Cauchy's theorem.** ∮ f dz over closed curves = 0
when f is holomorphic inside — because it has a primitive, because of
Green's theorem + C-R. **Cauchy's integral formula**: values inside =
boundary integral. Read it as: a holomorphic function is a hologram.

**4. Power series & analytic continuation.** Holomorphic ⇒ locally a power
series; identity theorem: agreement on a tiny arc = agreement everywhere
connected. This is why "the" analytic continuation of ζ is unique — the
word "the" is earned.

**5. Residues.** Isolated singularities; Laurent; the residue theorem
∮ = 2πi Σ Res. Worked fluency target: real integrals ∫_{−∞}^{∞} R(x) dx via
closing contours; you must compute ∫₀^∞ dx/(1+x⁴) without notes — that
single integral contains the whole technique.

**6. Infinite products.** Weierstrass factorization: holomorphic functions
are determined by their zeros up to an exponential, the way polynomials are
up to a constant. This is the vocabulary in which ζ will speak: ζ is a
function, its zeros are data, and primes read that data.

**7. The argument principle.** (1/2πi) ∮ f′/f dz = #zeros − #poles inside.
Read it as a counting formula: *an integral counts zeros.* Everything in
Phase 5 is this sentence applied to ζ (and L-functions) with contours
pushed around the critical strip. Learn the winding-number picture.

## Exercises

★1. Prove Cauchy–Riemann; show f(z)=z̄ is nowhere complex-differentiable.
★2. Prove Cauchy's theorem for star-shaped domains (Green's theorem route).
★★3. Cauchy integral formula: derive all higher-derivative bounds; explain
    "differentiable once ⇒ smooth" in three sentences.
★★4. Classify singularities of: e^{1/z}, 1/sin z, ζ(s) (assume Phase-5
    facts about ζ for the last one — do it anyway as vocabulary practice).
★★5. ∫₀^∞ dx/(1+x⁴) = π/(2√2) via residues — full contour, full Jordan
    estimate. Then ∫₀^{2π} dθ/(2+cos θ) via |z|=1.
★★6. Argument principle: verify numerically (numpy complex128 suffices)
    that (1/2πi)∮ p′/p over |z|=2 counts the zeros of p(z) = z³ − z + 1
    inside. Write the 15-line script; keep it.
★★★7. Read: ζ's functional equation statement (any source; e.g. the first
    sections of Davenport ch. 2). Don't prove it — but write one paragraph
    predicting, from the argument principle, *how* one would convert "sum
    over zeros" into "sum over primes". Keep the paragraph; check it against
    Phase 5's explicit formula at the end of the course.

## Labs

No new lab this phase — you are arming. Do use `mpmath` to play:
`mp.zeta(0.5+14.134j)` is near zero; `mp.zetazero(1)` prints
14.13472514173469379045725… — these zeros are the instruments Phase 5's
lab will make play the primes.

## When you're done

You can compute residues; you can explain analytic continuation to a
physicist; and the phrase "the zeros of ζ encode the primes" has become a
suspect sentence you want to disprove — which is precisely the right state
for Phase 5.
