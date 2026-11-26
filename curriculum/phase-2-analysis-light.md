# Phase 2 — Analysis Light

**Budget: 2–4 months. Requires Phases 0–1. Everything you need is in this
file, this repo's code, and nothing else — books at the end are optional.**

This phase is an armory, not a survey: asymptotics, series, the harmonic
constant, the **Euler product** (the bridge between primes and analysis),
Abel summation (the master move), and the logarithmic integral *computed
correctly* (a trap this repo stepped in so you don't have to). Every
Gate-2 question is a skill taught in a numbered section below.

```bash
python3 src/phase2/euler_product_lab.py     # run it while reading §2.4
```

---

## 2.1 Asymptotic notation is quantifier grammar

All four sentences are statements with the same shape as Phase 0's ε–N
drill. Read them as English, not as decoration:

- **f ~ g** means f/g → 1: *for every ε > 0 there is N such that x > N ⇒
  |f/g − 1| < ε.* "Eventually indistinguishable."
- **f = O(g)** means ∃C > 0, ∃N, ∀x > N: |f(x)| ≤ C·g(x). "Bounded to
  within a constant." (This is the Gate-2 MCQ answer — memorize the
  quantifiers, not the vibe.)
- **f = o(g)** means f/g → 0: for every ε > 0, …, |f| ≤ ε·g. "Smaller
  than any constant multiple."
- f = Ω(g), f = Θ(g): g = O(f); both ways.

Note "f = O(g)" is a set-membership statement (O(g) is a *class* of
functions); "O(g) = O(h)" is legal abuse but "O(x) − O(x) = 0" is how
sloppy people lose terms. Keep C's invisible but *existent*.

**Worked O-proof.** 3x² + 2x − 7 = O(x²). Take C = 4, N = 3: for x > 3,
3x² + 2x − 7 ≤ 3x² + 2x ≤ 3x² + (2/3)x² < 4x². ∎ (Any C, any N — the game
is finding *one* pair.)

**Growth hierarchy to internalize** (each strictly o of the next):

```
ln ln x  ≪  ln x  ≪  x^ε (any ε>0)  ≪  x  ≪  x ln x  ≪  x^{1+ε}  ≪  e^x  ≪  x!
```

Prime number theory speaks this natively: "π(x) ~ x/ln x" is one ∀∃
sentence claiming a staircase and a smooth curve are eventually
indistinguishable. Practice translating: say each notation sentence out
loud in quantifier English until it's boring.

## 2.2 Series: the five tools you'll actually use

For positive terms: **comparison** (termwise ≤ a known series), **integral
test** (f decreasing ⇒ Σf(n) and ∫f agree up to f(a): squeeze with upper /
lower Riemann sums — prove it once, it's 4 lines), **ratio** and **root**
tests (Σ 1/n²: ratio test gives → 1 — *inconclusive*! The integral test
wins: ∫₁^∞ dx/x² = 1 < ∞. Knowing when a test fails is part of knowing
it), **p-series**: Σ 1/nᵖ converges ⇔ p > 1 (integral test in one line —
the boundary p = 1 is where ln enters the story).

**Σ 1/n diverges, twice.** (i) Integral/Riemann: H_N ≥ ∫₁^{N+1} dt/t =
ln(N+1) → ∞. (ii) Oresme's grouping: 1 + ½ + (¼+⅛) + (1/16+…+1/32) + ⋯ —
each bracket ≥ ½. Both proofs encode one truth: *the harmonic series
diverges like ln* — the rate is the content, and it will run this whole
course.

**Alternating series (Leibniz).** aₖ ↓ 0 ⇒ Σ(−1)ᵏaₖ converges, and the
error after n terms is ≤ aₙ₊₁. *Proof sketch:* even/odd partial sums are
squeezed (evens ↑, odds ↓, gap = next term). Applied to Σ(−1)ᵏ⁺¹/k = ln 2.

**Absolute vs conditional.** Σ|aₖ| < ∞ ⇒ Σaₖ converges (comparison:
0 ≤ a + |a| ≤ 2|a|). Converse false: alternating harmonic converges,
Σ1/k doesn't — *conditionally*. Rearrangement (Riemann's theorem):
conditionally convergent series can be shuffled to any sum — absolutely
convergent ones cannot be moved. Why you care: the Euler product's proof
*rearranges terms* and gets away with it only because everything is
positive or absolutely convergent. That's the whole lesson of this
paragraph — keep it loaded.

## 2.3 The harmonic sum and Euler's constant γ

**Theorem.** H_N := Σ_{k≤N} 1/k = ln N + γ + 1/(2N) + O(1/N²), where
γ = 0.5772156649… exists.
*Proof sketch you should fully execute (exercise ★1).* Each
dₖ = 1/k − ∫ₖ^{k+1} dt/t is > 0 (1/t < 1/k on (k, k+1)) and
Σdₖ = H_N − ln(N+1) converges because dₖ ≤ 1/k − 1/(k+1)… (no — that's
too crude; the sharp bound: dₖ < 1/(2k(k+1)) by the midpoint/tangent
estimate of 1/t; telescoping Σ 1/(2k(k+1)) converges). Then
H_N − ln N = γ + (ln(N+1) − ln N) + tail → γ, and expanding the correction
by Taylor gives the +1/(2N) term. ∎-ish — make it rigorous once.

**Numbers that make it real:**

```python
import math
H = lambda N: sum(1.0/k for k in range(1, N+1))
H(100)  - math.log(100)                 # 0.582207…  = γ + 1/200 + O(10⁻⁵) ✓
H(1000) - math.log(1000)                # 0.577716…  — still above γ!
H(1000) - math.log(1000) - 1/2000       # 0.5772156… — γ to 7 decimals
```

**The +1/2N correction is the difference between a right answer and a
wrong one.** At N = 1000 the naive H−ln sits *above* γ by 1/2N = 5·10⁻⁴ —
enough to corrupt the 4th decimal. This is exactly the trap Gate-2's
first question sets: when a prompt tells you "approaches from ABOVE at
~ +1/2N", believe your computation, apply Phase 0's habit — *compute the
quantity the prompt defines, to the precision it defines, and know which
side of the limit you're on.*

## 2.4 The Euler product — THE bridge

**Theorem (Euler, 1737).** For real s > 1:

```
ζ(s) := Σ_{n≥1} n^{−s}  =  ∏_p (1 − p^{−s})^{−1}.
```

*Full proof.* Both sides have positive terms, so rearrangement is legal
(§2.2 warning discharged). Finite version: expand each geometric series
(1 − p^{−s})^{−1} = 1 + p^{−s} + p^{−2s} + ⋯ over primes p ≤ y, multiply
out — by **FTA (Phase 1!)** every product of these primes is a unique
n whose prime factors are all ≤ y ("y-smooth"), each appearing once:

```
∏_{p≤y} (1 − p^{−s})^{−1}  =  Σ_{n y-smooth} n^{−s}.
```

Now let y → ∞: the partial sum over y-smooth n ≥ x⁻ˢ… more carefully:
for every fixed x, all n ≤ x are y-smooth once y ≥ x, so the smooth-sum
squeezes Σ_{n≤x} n^{−s} ≤ LHS_y ≤ ζ(s), and both limits give ζ(s)
(the tails Σ_{n>x}n^{−s} ≤ ∫ₓ^∞ t^{−s}dt → 0 since s > 1). ∎

Feel the vertigo: the LEFT speaks of all integers, the RIGHT only of
primes, and they're *equal* — the bridge between the two worlds this whole
course crosses back and forth.

**Consequence 1 (Euler's infinitude proof, fully).** As s → 1⁺, ζ(s) ≥
H_{⌊x⌋}·x^{−s}-ish… simplest honest route: Σn^{−s} ≥ ∫₁^∞ t^{−s}dt-ish —
just: ζ(s) → ∞ as s → 1⁺ (integral test lower bound, §2.2). If primes
were finite, the product ∏(1−p^{−s})^{−1} would be a finite product of
finite numbers at s = 1 — each factor Σp^{−k} converges (geometric, ratio
1/p < 1) — bounded, contradiction. ∎

**Consequence 2 (the stronger one).** Σ_p 1/p **diverges**, and
Σ_{p≤x} 1/p = ln ln x + M + o(1) with **M = 0.261497…**
(Meissel–Mertens constant; the rate-theorem is Phase 3's, the divergence
is now). *Proof of divergence:* take logs of the product at s > 1:

```
ln ζ(s) = Σ_p Σ_{k≥1} 1/(k p^{ks}) = Σ_p p^{−s} + R(s),   0 < R(s) ≤ Σ_p Σ_{k≥2} p^{−ks}·(1/(k))
```

and R(s) stays bounded as s→1⁺ (compare Σ_p p^{−2s}/(1−p^{−s}) — converges
for s > 1/2). Since ζ(s) → ∞ as s→1⁺, ln ζ(s) → ∞ forces Σ_p p^{−s} → ∞;
positive terms ⇒ the plain series Σ 1/p diverges (a monotone-sup argument:
every finite partial sum ≤ limsup of Σp^{−s} = ∞). ∎ — this is Gate-2's
MCQ: it's **Σ 1/p** whose divergence proves infinitude through the
product, not Σ1/n² and not Σ1/2ᵖ.

**Numbers** (lab prints these and more):

```
x        Σ_{p≤x} 1/p     ln ln x      estimate of M = difference
10⁴      2.48306         2.22034      0.26273
10⁵      2.70527         2.44347      0.26180
10⁶      2.88733         2.62579      0.26154      → M = 0.261497…
```

**Exercise ★★6 in the wild:** ln ln x alone gets within 5% of Σ1/p only
around **x ≈ 10⁸¹**. The constant M is *the whole story* at human scales:
ln ln grows so slowly that its "error" outlives civilizations. This is
your inoculation against "the graphs look close" arguments for the rest
of the course.

**Basel.** ζ(2) = π²/6 = 1.6449340668… (Euler 1734; you won't reprove it —
any course that asks you to is a different course). Watch two utterly
different roads hit the same number:

```
Σ_{n≤1500} 1/n²                    = 1.644268…   (tail ≈ 1/1500)
∏_{p≤500} (1 − 1/p²)^{−1}          = 1.644485…
both → 1.644934…  = π²/6
```

The lab pushes both to 9+ digits over 664,579 primes. Partial sums
converge at rate ~1/N (integrate the tail!) — so when a gate asks for a
partial sum to 6 decimals, *sum what's asked, don't substitute the limit.*

## 2.5 Abel summation — integration by parts for sums

**Discrete identity.** For any aₙ and any C¹ function f:

```
Σ_{n≤x} aₙ f(n) = A(x)f(x) − ∫₁ˣ A(t) f′(t) dt,   A(t) := Σ_{n≤t} aₙ.
```

*Proof.* Write aₙ = A(n) − A(n−1), swap sums ("summation by parts"
Σ(A(n)−A(n−1))f(n) = Σ A(n)(f(n) − f(n+1)) + boundary), read the last as
−∫A f′. Do the discrete version in full once (exercise ★3). Keep only the
moral: **A counts something → the identity converts counting statements
into integral statements and back.** Every hard conversion in Phases 3–6
is this.

**Warm-up double count (a Gate-2 question type).** Σ_{n=1}^{N} ⌊N/n⌋ =
Σ_{m≤N} τ(m), where τ(m) = # divisors. *Proof:* n | m contributes 1 to
the left's term for n exactly when m ≤ N; count the lattice points
{(n, m) : n·k = m ≤ N} two ways. Check at N = 100: left = 482 (compute —
one line of Python), right = Σ_{m≤100}τ(m). Both roads, same 482 — and
the asymptotic reading (left ≈ N Σ1/n ≈ N ln N) proves *average τ ≈ ln N*
in one line. Dirichlet's divisor trick is in your pocket now.

**The inversion drill (the phase's summit).**
**π(x) ~ x/ln x ⟺ pₙ ~ n ln n.**
*⇒ direction with Abel.* ψ-ish-free route: assume π ~ x/ln x. Then
x = y with π(y) = n ⇒ n ~ y/ln y; solve for y = y(n): put y = n·L; then
n ~ nL/(ln n + ln L) ⇒ ln n + ln L ~ L. Try L = ln n + b: get
ln ln n + b + ln(1 + b/ln n)… ~ ln n + b + … ⇒ b = ln ln n − 1 absorbs the
log-log drift ⇒ **y ~ n(ln n + ln ln n − 1)**. The o(n/ln n) bookkeeping is
exercise ★★★5 — do it with every O named.

**Numbers** (formula e(n) := n(ln n + ln ln n − 1)):

```
n=1000:   e = 7840.4   p₁₀₀₀ = 7919     error −78.6  (−1.0%)
n=10⁴:    e = 104306.7 p₁₀₀₀₀ = 104729  error −422.3 (−0.40%)
```

Errors *shrinking* toward zero in relative terms — the estimate is the
first two terms of an infinite asymptotic expansion, not a guess.
Gate-2 asks e(10⁵) rounded to nearest integer — the formula, plainly
evaluated:

```python
def estimate_pn(n): return n*(math.log(n) + math.log(math.log(n)) - 1)
```

(Remember `math.log` = ln; round only at the end.)

## 2.6 The logarithmic integral Li — and how to compute it truthfully

**ln x = ∫₁ˣ dt/t** — Phase 0's quantifiers made you careful with words;
here be careful with *numerical quadrature*.

**Definition used by this repo (and every gate):**

```
Li(x) := ∫₂ˣ dt/ln t        (lower limit 2; NOT the principal-value li(x)
                             from 0 that many books use — never confuse them)
```

**Asymptotics (integrate by parts twice, see the pattern):**

```
Li(x) ~ x/ln x · (1 + 1/ln x + 2/ln²x + 6/ln³x + ⋯)   (never converges;
          truncating near k ≈ ln x is the best you can do)
```

At x = 10⁶, ln x ≈ 13.8: the correction series contributes factors
(1 + 0.072 + 0.0052 + …) ≈ 1.078 — which is *why Li beats x/ln x
decisively* in Phase 3's lab (x/ln x undershoots π(x) at every x up to
10⁸+; Li doesn't undershoot until ~10³¹⁶ — Phase 5's Littlewood
payoff).

**The numerical trap (this repo stepped in it; the gates use the fixed
definition — learn both halves).** The integrand 1/ln t has huge
derivative near t = 2 (ln t ≈ t − 2 there, so 1/ln t ≈ 1/(t−2) — steep).
Simpson on **uniform panels in t** from 2 to 10⁶ puts 20000 panels across a
10⁶-wide interval: panel width 50; the first panels see a singularity-like
cliff and lie:

```python
# WRONG (uniform panels in t):  Li(1e6) → 78632.8   (off by ~6)
# RIGHT (substitute u = ln t):  Li(1e6) → 78626.5   (machine-trustworthy)
```

**Substitution u = ln t** (t = eᵘ, dt = eᵘ du):

```
Li(x) = ∫_{ln 2}^{ln x} eᵘ/u du     — smooth, gentle, any fixed-panel
                                       Simpson is accurate.
```

`gates/gate_common.py::li` implements exactly the substitution + Simpson
with 20000 panels — and gates will ask you for Li values computed *with
that definition* (they say so; use `from gate_common import li` or
reproduce it). Reference: Li(1000) = 176.56, Li(10⁵) ≈ 9629 vs
π(10⁵) = 9592 (Li runs *ahead* of π by +37 — the "Li leads forever"
illusion Phase 5 shatters).

**Float-answer habits for gates:** return a Python float, not a string;
round only the final answer to the exact number of decimals the prompt
names; never round intermediates; when a prompt says "rounded to nearest
integer", hand back `round(value)` as an int-or-float exactly as the
prompt's own recipe computes it.

---

## Lab

`src/phase2/euler_product_lab.py` — Basel partial sums vs prime products,
Σ1/p vs ln ln x + M, and the γ-correction demo, figure in
`data/phase2_euler_product.png`. Read its `Think about it:` blocks before
and after running.

## Exercises

★1. Prove H_N − ln N converges (§2.3 sketch → rigorous: dₖ < 1/(2k(k+1))
   comes from concavity of 1/t — draw it). Identify the limit as γ.
★2. Prove Σ 1/(2k−1) diverges TWO ways (comparison with H; grouping).
★3. Prove the discrete Abel identity in full (all boundary terms named),
   then deduce Σ_{n≤x} 1/n = ln x + γ + O(1/x) from A(t) ≈ t (H itself!).
   Circular? Write why it isn't (you're converting a *bound*, not proving
   convergence).
★4. Full proof of the Euler product as written in §2.4 — the squeeze
   Σ_{n≤x} ≤ lim_y smooth-sum ≤ ζ(s) with all ε's.
★★5. From Σ_p 1/p diverging, deduce infinitude of primes in ONE line;
   then explain why the converse route (Σ1/p diverges ⇒ more primes than
   squares) has content: compare Σ 1/p vs Σ 1/p² over any candidate
   sparse prime set — quantify "the primes are thin but not too thin"
   (write the inequality you'd need; there is no proof needed — the
   exercise is the *shape* of thinking).
★★6. §2.4's "within 5%" claim: solve ln ln x = M/0.05 → x = e^{e^{5.23}}.
   Write the number of digits. Then compute Σ_{p≤1e6}1/p/(ln ln 1e6) —
   how far from 5% at a million? (≈9.1% — the plateau is *slow*.)
★★7. Abel inversion worked example, numbers: π(10⁵) = 9592. Estimate
   p₉₅₉₂ with n ln n and with the 3-term estimate; the true p₉₅₉₂ = 99991.
   Errors? Which formula wins and by what factor?
★★8. Compute Li(1000) three ways: repo `li`, mpmath's Li (note: mpmath's
   li has the 0-limit convention — check `mpmath.li(100) = 30.126…` vs
   repo `li(100) = 29`!). Explain the discrepancy exactly (which chunk of
   ∫₀²… region does the principal value add?). THIS is the convention
   trap; the gate names its definition — always yours wins.
★★9. O-drills: prove (i) ln N = O(N^ε) for every ε > 0; (ii) Σ_{n≤N}
   1/√n = O(√N) (integral test!); (iii) 2^{ln N} = N^{ln 2} (rewrite
   2 = e^{ln 2}) — so 2^{ln N} = O(N) is TRUE and O(N^{0.69}) is FALSE.
   (iv) which of O, o, ~ is f = 3N + 7sin N vs g = N?
★★★10. Prove the +1/(2N) term: with eₖ = H_k − ln k − γ, show eₖ − eₖ₊₁
   = ln(1+1/k) − 1/(k+1)… Taylor ⇒ eₖ = 1/(2k) + O(1/k²). This is the
   exact correction the gate's q01 hint tells you about — own it.
★★★11. (Bridge to Phase 3.) Chebyshev's baby step: prove Σ_{p≤x} ln p ≤
   (2 ln 2)·x by induction on the central-binomial bound (sketch: 4ᵐ
   bounds Π_{m<p≤2m} p ≤ C(2m,m) ≤ 4ᵐ/√(2m+1)); this is your first
   ψ-bound and Phase 3 builds the house on it.

## Gate-2 readiness map

| gate question | section |
|---|---|
| q01 H_N − ln N at given N | 2.3 — compute as asked, know the +1/2N bias |
| q02 Basel partial sum | 2.4 — sum what's asked, `round(…, 6)` |
| q03 prime product ∏(1−p⁻²)^{−1} | 2.4 — primes via sieve, product via `math.prod` |
| q04 Σ_{p≤x} 1/p | 2.4 table pattern — sieve + sum |
| q05 pₙ estimate at given n | 2.5 — `estimate_pn`, round at the end |
| q06 Σ⌊N/n⌋ | 2.5 — double count / one-line sum, trust both |
| q07 which divergence | 2.4 — Σ 1/p |
| q08 O(g) definition | 2.1 — ∃C ∃N ∀x |
| q09 Li by repo quadrature | 2.6 — substitution + Simpson (or import `li`) |
| q10 Meissel–Mertens at given x | 2.4 — table pattern, 4 decimals |
| q11 Li(100) repo-definition | 2.6 — repo li, `round()` |
| q12 `estimate_pn` function | 2.5 — hand the function object over |

## Optional deeper reading (never required)

Abbott, *Understanding Analysis* (sequences/series chapters) for
extra proof drills; Granville's free ANTL notes for the analytic-number-
theory voice. Gate 2 needs neither.
