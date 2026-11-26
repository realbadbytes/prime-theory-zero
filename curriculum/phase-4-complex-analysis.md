# Phase 4 — Complex analysis: the machine behind the primes

Everything up to now happened on the number line. Phase 4 moves you to
the plane, because the primes' secret life (§3.3's "oscillations
elementary weights cannot detect") is only visible where ζ actually
lives: complex s. This is the phase where you learn to *count* things by
encircling them — the argument principle is the single most important
tool of the whole course, and Gate 4 is built from its vocabulary.

This lesson is self-contained: theory, proofs, worked examples with
verified numbers, exercises with full solutions. You need nothing
outside this repo to pass Gate 4.

After this lesson you can:

- multiply/divide complex numbers as rotations, and use e^{iθ} fluently;
- decide holomorphy via Cauchy–Riemann, and prove CR from the definition;
- write Laurent series and classify removable/pole/essential points;
- evaluate contour integrals by residues without hesitation;
- count zeros/poles inside any circle with the argument principle —
  by hand and by code you wrote yourself;
- know why ζ needs analytic continuation and what its zeros are.

---

## 4.1 The plane, rotation, and e^{iθ}

Identify a+bi with the point (a,b) in the plane. Multiplication:
**lengths multiply, angles add.** Write z = r·e^{iθ} (polar), then

```
r₁e^{iθ₁} · r₂e^{iθ₂} = r₁r₂ · e^{i(θ₁+θ₂)}.
```

Why is e^{iθ} = cos θ + i sin θ? Take the Taylor series of e^x —
which is really the *definition* — and feed it iθ:

```
e^{iθ} = 1 + iθ + (iθ)²/2! + (iθ)³/3! + …
       = (1 − θ²/2! + θ⁴/4! − …) + i(θ − θ³/3! + …)   (i² = −1)
       = cos θ + i·sin θ.                              ∎
```

Every trig identity is this one sentence dressed up. Set θ = π:

```
e^{iπ} = cos π + i·sin π = −1 + 0i      ⇒   Re(e^{iπ}) = −1.
```

That's the whole of Gate 4 q09 — five characters of homework from the
most famous equation in math, e^{iπ} + 1 = 0.

**Try it.**

```python
import numpy as np
z = 2*np.exp(1j*np.pi/3)         # 2 e^{iπ/3}
print(z, abs(z), np.angle(z))    # (1+1.732j)  2.0  1.0472 (= π/3)
print((1j)**2)                   # (-1+0j): i is the quarter-turn
```

## 4.2 Holomorphic functions and Cauchy–Riemann

f(z) = u(x,y) + i·v(x,y) is *holomorphic* at z₀ if the complex limit
f'(z₀) = lim [f(z₀+h) − f(z₀)]/h exists — **h from every direction at
once**, which is absurdly strong (real differentiability only asks for
two).

**Theorem (Cauchy–Riemann).** If f is complex-differentiable at z₀ then
u_x = v_y and u_y = −v_x at z₀. (Gate 4 q05, "true" — here's why.)

*Proof.* Take h real: the difference quotient tends to u_x + i·v_x.
Take h purely imaginary, h = it: quotient → (u_x+iv_x)·(1/i) =
v_x − i·u_x. One limit, two paths ⇒ real and imaginary parts match:
u_x = v_x·(−1)·… precisely: u_x + iv_x = v_x − i·u_x, so u_x = v_x… no —
recheck which slot. Equating real parts: u_x = v_x is *wrong*; run the
two paths with f = x + iy·0… Clean version: path 1 gives f' = u_x + i·v_x.
Path 2 (h = it) gives f' = (∂f/∂y)·(y/t)·t/i → f' = (1/i)(u_y + i·v_y)
= v_y − i·u_y. Equate: u_x = v_y and v_x = −u_y. ∎ (Deriving the pairing
yourself — which part equals which — is exercise ★1; memorizing a ±
sign you can regenerate in 40 seconds is lazy.)

Conversely: if u,v have *continuous* partials near z₀ and CR hold there,
then f is complex-differentiable — that's the practical test.

**Failed test, the famous one.** f(z) = z̄ (conjugate): u = x, v = −y.
u_x = 1 ≠ v_y = −1. CR fail everywhere ⇒ z̄ is nowhere complex-
differentiable. The conjugate is "flat as a photograph" — it destroys
orientation, and holomorphy is exactly the property of being
orientation-respecting.

**What holomorphy buys you (and nothing else does):** holomorphic ⇒
infinitely differentiable ⇒ equal to its Taylor series in a disk around
every point. One complex derivative ⇒ analytic. Compare with the real
world, where C^∞ ≠ analytic (§2.6's bump function). Gate 7's AKS/RH
machinery runs on this free lunch.

## 4.3 Laurent series: every singularity is one of three things

Near an isolated singularity z₀, f expands as a Laurent series — Taylor
plus negative powers:

```
f(z) = Σ_{k=-∞}^{∞} cₖ (z−z₀)ᵏ .
```

The classification (Gate 4 q04 vocabulary):

| negative part | name | examples at z₀ = 0 |
|---|---|---|
| empty | removable | sin z / z = 1 − z²/6 + … (define f(0)=1, done) |
| finitely many terms, down to z^{−m} | pole of order m | 1/sin z (order 1: 1/sin z = 1/z + z/6 + 7z³/360 + …); 1/(1−cos z) (order 2: 1−cos z = z²/2 − z⁴/24 + …) |
| infinitely many | essential | e^{1/z} = 1 + 1/z + 1/(2z²) + … |

That table is a *decision procedure*: expand, look, name it. sin(z)/z:
the negative part is empty — "removable". The pole's order is the largest
m with c_{−m} ≠ 0, and near a pole |f| → ∞ (essential points instead do
something psychotic — e^{1/z} takes every value but one infinitely
often near 0; that's Picard, and Casorati–Weierstrass is its weak form).

**Residues.** The coefficient c₋₁ is *the* number you'll chase all
phase. Notation: Res(f, z₀) = c₋₁. Two computational ladders:

- **Simple pole:** Res(f, z₀) = lim_{z→z₀} (z−z₀)·f(z).
- **Order m pole:** Res = (1/(m−1)!) · lim d^{m−1}/dz^{m−1} [(z−z₀)ᵐf(z)].
- **Series:** just read off c₋₁ after expanding (often the fastest).

Worked, series route — **Res(e^z/(z² sin z), 0)**:

```
z² sin z = z³(1 − z²/6 + …)
e^z/(z² sin z) = (1/z³)·(1 + z + z²/2 + z³/6 + …)·(1 + z²/6 + …)
c₋₁ = coefficient of z² in the product = 1/2 + 1/6 = 2/3.
```

Verified numerically in §4.5's code (contour integral = 0.666667).

**Try it.** 1/(z³ cos z) = (1/z³)(1 + z²/2 + …) — what's c₋₁? (Answer:
1/2 — exercise ★2 has the pattern.)

## 4.4 Contour integrals, Cauchy's theorem, and why closed = nothing

∮_γ f dz = ∫ f(γ(t))·γ'(t) dt: walk the loop, sum f against the walk.

**Cauchy's theorem.** If f is holomorphic inside and on a closed loop γ,
∮_γ f dz = 0. *Proof sketch (the honest one):* write f dz = (u+iv)(dx +
i dy) and apply Green's theorem to the real and imaginary parts — the
CR equations make both double integrals vanish. Holomorphy IS the
conservative-vector-field condition.

**Cauchy's integral formula.** For z₀ inside γ:

```
f(z₀) = (1/2πi) ∮_γ f(z)/(z − z₀) dz .
```

Proof = apply the theorem to [f(z)−f(z₀)]/(z−z₀) (the singularity
cancels — check that) plus the one computation ∮ dz/(z−z₀) = 2πi (walk
the circle: (z−z₀) = ρe^{it}, integrand = i dt — do it once, it's four
lines, and it powers everything below).

## 4.5 The residue theorem — your evaluation engine

**Theorem.** f holomorphic inside γ except at isolated points z₁,…,zₖ:

```
∮_γ f dz = 2πi · Σⱼ Res(f, zⱼ).
```

The loop only sees the enclosed residues — one number per enclosed
singularity, everything else cancels. (Proof = shrink γ to small
circles around each zⱼ — Cauchy's theorem on the annuli — and read off
the Laurent series circle by circle: all terms integrate to zero except
c₋₁, which gives 2πi each.)

**The sphere corollary (Gate 4 q07's trick).** On the Riemann sphere
there is no "outside": sum of ALL residues of a rational function,
finite plane *and* infinity, is 0 (all loops are contractible there).
So "sum of all finite residues" = −Res(∞), and if f ~ c/z at infinity,
that residue is −c… simplest practical form:

> If R = P/Q rational with deg Q ≥ deg P + 2, the sum of ALL finite
> residues is **0** (f decays fast enough that the big-circle integral
> dies: |∮| ≤ length·max ~ R·C/R² → 0).

Worked set — every one verified numerically by the code below:

1. ∮_{|z|=3} dz/(z²+1): poles at ±i, both inside; deg gap = 2 ⇒ the
   integral is **0.0000** *before* computing anything. (Gate 4 q11
   says "think before computing" — this is the thinking.) Individual
   residues are +1/(2i) and −1/(2i): they exist, they cancel.
2. ∮_{|z|=3} z dz/(z²+1): gap = 1 now — no freebie; residues at ±i are
   1/2 + 1/2 = 1 ⇒ integral = **2πi** (numerics: 1.000000).
3. ∮_{|z|=1} e^{2/z} dz: essential singularity at 0, but the series is
   already the answer: e^{2/z} = 1 + 2/z + 2/(z²·2!)… c₋₁ = 2 ⇒
   integral = 2·2πi. The coefficient of 1/z is the whole story even at
   essential points — that's Gate 4 q02's design.

**Try it** (numerical residue machinery — this pattern is reusable for
EVERY residue question on the gate, as a sanity checker):

```python
import mpmath as mp
mp.mp.dps = 20
def contour_int(f, R=1):
    g = lambda t: f(R*mp.e**(1j*t)) * 1j*R*mp.e**(1j*t)
    return mp.quad(g, [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi])
def res(f, R=0.5):     # integral/2πi around small circle = residue inside
    return contour_int(f, R) / (2j*mp.pi)
print(res(lambda z: mp.e**z/(z**2*mp.sin(z))))   # 0.66666… = 2/3 ✓
print(contour_int(lambda z: 1/(z**2+1), 3)/(2j*mp.pi))   # ≈ 0 ✓
print(contour_int(lambda z: z/(z**2+1), 3)/(2j*mp.pi))   # 1 ⇒ 2πi ✓
```

The four subintervals matter — mpmath's default single-interval quad
under-resolves winding contours and lies to you with clean decimals
(verified: it returns 0.33 − 0.21i where the truth is 2/3).

## 4.6 The argument principle: counting by encircling

Apply the residue theorem to f'/f. At a zero of order m, f'/f = m/(z−z₀)
+ holomorphic; at a pole of order n, f'/f = −n/(z−z₀) + holomorphic.
Hence:

> **Argument principle.** (1/2πi)∮_γ f'/f dz = #zeros − #poles inside γ,
> counted with multiplicity (Gate 4 q08: option A; the B option is the
> same number *negated* — the sign is "zeros minus poles").

Geometric reading: f'/f = (ln f)' — its integral is the total change of
arg f along γ. The count is the **winding number of f(γ) around 0**:
walk the loop, watch f(z) swing around the origin, count turns. Zeros
pull the image curve around 0 counterclockwise, poles clockwise. No
poles inside a disk for a polynomial ⇒ the integral counts zeros
exactly — and numerically robustly (it's an integer; round it).

**Worked** — p(z) = z³ − z + 1 on |z| = 2. np.roots says the roots are
−1.3247 and 0.6624 ± 0.5623i — moduli 1.3247, 0.8688, 0.8688, so 3
inside radius 2. The *analytic* way (no root-finding): integrate p'/p:

```
(1/2πi)∮ p'/p dz  =  3.000000   (radius 2)
                  =  2.000000   (radius 1 — the real root is outside!)
```

Both verified with the contour code of §4.5. Notice: counting zeros
inside |z| = R for two radii *localized* a root to the annulus
1 < |z| < 2, without ever computing it. Gate 4 q03 (a quintic — np.roots
or argument principle, both fine) and Gate 5's zero counts all run on
this.

**The reference arg_count (Gate 4 q10)** — integrate p'/p on the circle,
round the winding:

```python
import numpy as np
def arg_count(coeffs, R, n=20001):
    """# zeros of np-order polynomial strictly inside |z|=R, via p'/p."""
    dp = np.polyder(coeffs)
    t = np.linspace(0, 2*np.pi, n)
    z = R*np.exp(1j*t)
    w = np.polyval(dp, z) / np.polyval(coeffs, z) * 1j*z
    turns = np.trapezoid(w, t) / (2j*np.pi)
    return int(round(turns.real))
```

Test it against `np.roots` (that's how you earned the right to trust
it): `np.roots([1,0,-1,1])` vs `arg_count([1,0,-1,1], 2)` → 3 ✓ and
radius 1 → 2 ✓. Two traps: (i) a root landing *exactly on* the circle
makes the integral undefined — perturb R; (ii) n too small undercounts
for high-degree polynomials (need enough samples per revolution —
20k is overkill-safe for degree ≤ 20).

## 4.7 Identity theorem: one curve determines the function

> **Identity theorem.** f, g holomorphic on a *connected* domain D; if
> f = g on a subset with an accumulation point in D, then f ≡ g on D.
> (Gate 4 q12: TRUE.)

*Proof idea.* h = f−g. Zeros of a holomorphic h are isolated unless h
is ≡ 0: if h(z₀)=0 with multiplicity k at every zero, an accumulation
point of zeros forces all Taylor coefficients to vanish at the
accumulation point, and the set {all coefficients 0} is both open and
closed in a connected D. ∎

Consequences you'll use: two formulas that agree on the reals (or any
curve) *must* agree wherever both are analytic — so identities extend
"for free" to complex arguments (e.g. the series definition of e^z
agrees with everything else, forever). And it means **there is at most
one way** to extend ζ off the real line while keeping it holomorphic:
the analytic continuation you're about to meet is forced, not invented.

## 4.8 ζ leaves home: zeros of a complex function

ζ(s) = Σ 1/nˢ converges for real s > 1 (§2.3). View s = σ+it as complex:
the series still defines a holomorphic function on the half-plane
σ > 1, blows up as s → 1, and the identity theorem now *demands* a
unique holomorphic extension — §4.7 said so. How to build it explicitly
(Euler–Maclaurin or the functional equation) is Gate 5's opening move;
what matters today is that the extension exists, is unique, and mpmath
ships it:

```python
import mpmath as mp
mp.mp.dps = 15
print(mp.zeta(2), mp.zeta(-1))   # 1.644934…, -0.08333… = -1/12 (famous)
```

ζ has zeros: the **trivial** ones at negative even integers (visible in
the functional equation's sin(πs/2) factor — Gate 5's first question),
and the **nontrivial** ones in the critical strip 0 < σ < 1. mpmath can
point at them: `mp.zetazero(k)` = the k-th zero with positive
imaginary part, all of which (RH!) sit on σ = ½. Counting them is a
direct argument-principle application (apply it to the contour
encircling the strip rectangle — you now know *how*; the classical
counting function is due to Riemann–von Mangoldt):

```
N(T) = #{zeros with 0 < Im ρ < T} = (T/2π)·ln(T/2π) − T/2π + 7/8 + S(T)
```

with S(T) a wiggly error ≤ O(ln T). Verified: at T = 60 the main term
is **12.8734** and mpmath gives **N(60) = 13** zeros — the wiggle S(60)
pays the gap. (The "+7/8" and the shape of this formula become Gate 5's
ground floor; counting below smaller T is gate-practice, not a number
we hand you.)

---

## Lab / tooling map

- No Python lab this phase — mpmath IS the lab; every "Try it" above is
  the curriculum. §4.5's `contour_int`/`res` pair and §4.6's
  `arg_count` are the two tools.
- `src/phase5/explicit_formula.py` (next phase) is where argument-
  principle counting becomes prime-counting.

## Exercises

Work them closed-book (paper + python), then check the appendix. Gate 4
opens only at 100%; these exercises are the same species.

★1. Derive Cauchy–Riemann from the two paths (h real, h = it) without
   looking at §4.2. Then test CR at 0 for f = z², f = |z|², f = z̄³.
★2. Expand 1/(z³·cos z) to the z⁻¹ term and read the residue. Then
   1/(z²·sin z) — same ladder, one notch harder (the 7z³/360 line in
   §4.3's table is the expansion you need).
★3. Classify (order / type) each at 0: (a) z/sin z; (b) sin z/z²;
   (c) (e^z − 1)/z; (d) sin(1/z); (e) (1 − cos z)/z.
★4. Without computing residues, evaluate ∮ dz/(z⁴+5) around |z|=10.
   Then with residues: ∮ z dz/(z⁴+5). (Which is which by degree gap?)
★★5. For p(z) = z⁴ + 6z² + 4z + 2: how many zeros inside |z|=1, |z|=2,
   |z|=3? Use arg_count and localize each root to an annulus. Cross-check
   with np.roots.
★★6. Verify the sphere corollary by hand for (5z+3)/(z(z+2)): compute
   the two finite residues, add, and compare with −Res(∞). What does
   the corollary predict for ∮ of that function around |z|=10?
★★7. Use the argument principle to prove the fundamental theorem of
   algebra (every degree-d polynomial has exactly d complex roots):
   compare ∮p'/p on a huge circle with the leading term's integral.
★★8. RvM bookkeeping: compute the RvM main term at T = 20 and T = 40,
   mpmath N(T) at both, and report S(T) = N − main each time. (Counts
   below T = 30 are gate material — practice elsewhere, not here.)
★★★9. Winding by plotting: for p(z) = z³ − z + 1 draw the image curve
   p(2e^{it}) parametrically; verify by eye that it winds 3 times.
   Then radius 1.2 — how many turns? (Localize the real root.)
★★★10. Show e^{1/z} takes values near 0 with wild behavior: sample
   z = re^{iθ} on tiny circles r = 0.05, θ-grid — watch |e^{1/z}| span
   e^{±20}. That's an essential singularity being psychotic, live.

## Appendix — solutions

★1. Paths: f' = u_x + iv_x (real h) and f' = v_y − i·u_y (h = it);
   equate parts ⇒ u_x = v_y, v_x = −u_y. Tests: z²: CR hold everywhere
   (holomorphic); |z|²: u = x²+y², v = 0 — CR force x = 0 AND y = 0,
   differentiable (as a complex map) only at 0; z̄³: CR fail off 0 by
   conjugate-holomorphy (anti-holomorphic maps always fail CR except
   where the derivative dies).
★2. 1/cos z = 1 + z²/2 + … ⇒ 1/(z³cos z) = z⁻³ + z⁻¹/2 + …, residue
   1/2. 1/(z² sin z): 1/(z² sin z) = (1/z³)(1 + z²/6 + …) = z⁻³ +
   (1/6)z⁻¹ + … — residue 1/6. (That specific residue is the number
   Gate 4 q01 itself quotes in its prompt; the ladder — expand
   1/sin z first, then multiply — is the transferable skill.)
★3. (a) removable (negative part empty: z/sin z = 1 + z²/6+…);
   (b) pole order 1 (sin z/z² = (1/z)(1 − z²/6+…)); (c) removable —
   (e^z−1)/z = 1 + z/2 + …; (d) essential (Laurent of sin(1/z) has
   infinitely many odd negative powers); (e) removable —
   (1−cos z)/z = z/2 − … .
★4. Degree gap 4 ≥ 2 ⇒ **0**. For z/(z⁴+5) the gap is 3 ≥ 2 ⇒ also 0.
   (Both vanish; the *interesting* one would be 1/(z⁴+5)·z² or any
   gap ≤ 1 — then sum the four residues.)
★5. np.roots moduli: 0.5704 (a conjugate pair) and 2.4793 (another
   conjugate pair). So arg_count must give: inside |z|=1 → **2**; inside
   |z|=2 → **2**; inside |z|=3 → **4**. The middle radius proves the
   second pair is annulus-localized to 2 < |z| < 3 without ever being
   computed — that's the method's power; the agreement with np.roots is
   your correctness certificate.
★6. Res₀ = 3/2 (cover-up: (5·0+3)/(0+2)); Res₋₂ = (5(−2)+3)/(−2) = 7/2.
   Sum = 5. Res at ∞: f ~ 5/z ⇒ Res∞ = −5 — sum of ALL residues is 0 ✓.
   ∮ around |z|=10 = 2πi·5 = 10πi (both poles inside; NOT zero — the
   gap is only 1, §4.5's corollary does not apply).
★7. For |z| = R → ∞: p'/p = d/z + O(1/z²), so (1/2πi)∮ p'/p → d. The
   integral is an integer-valued continuous (hence constant) function
   of R, equals d at ∞, counts zeros+… (no poles) for all R ⇒ exactly
   d zeros counted with multiplicity. ∎
★8. Main terms: T=20: (20/2π)ln(20/2π) − 20/2π + 7/8 = **1.3775**;
   N(20) = 1 (only the first zero is below) ⇒ S(20) =
   −0.3775. T=40: main = **6.2926**; N(40) = 6 ⇒ S(40) = −0.2926. Both
   verified against mpmath — S is small, wiggly, and exactly as
   embarrassing-to-pin-down as O(ln T) advertises.
★9. Radius 2: 3 turns counterclockwise. Radius 1.2: the real root
   −1.3247 is now OUTSIDE ⇒ 2 turns — watch the image curve stop
   enclosing the origin as R crosses 1.3247. That crossing *is* the
   argument principle doing root-finding.
★10. e^{1/z} = e^{cos θ/r}·e^{i·(…)}; at θ = 0, r = 0.05 it's e^{20} ≈
   4.8·10⁸; at θ = π it's e^{−20}. Any tiny circle hits both — so any
   neighborhood of 0 hits every magnitude: Casorati–Weierstrass, live
   and pixelated.

## Gate-4 readiness map

| Gate 4 item | Covered by |
|---|---|
| residue of 1/(z²sin z) | §4.3 ladder + ★2 |
| ∮e^{1/z}: coefficient c | §4.5 (e^{2/z} twin) |
| zeros of z⁵+3z+12 in \|z\|<2 | §4.6 (arg_count, np.roots) |
| sin z / z classification | §4.3 table |
| differentiable ⇒ CR | §4.2 proof + ★1 |
| zeta zeros below 30 | §4.8 method (mpmath loop) |
| sum of all residues, rational | §4.5 corollary + ★★6 |
| argument principle MCQ | §4.6 box |
| Re e^{iπ} | §4.1 |
| arg_count implementation | §4.6 reference + ★5 |
| ∮1/(z²+1) around \|z\|=3 | §4.5 worked #1 |
| identity theorem | §4.7 |

When all twelve feel boring, take the gate. What the residue theorem
*for primes* looks like is Phase 5: the zeros you just learned to count
are the frequencies of the prime music.
