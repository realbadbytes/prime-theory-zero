# Phase 5 — RH and the explicit formula: the primes' frequency spectrum

Phase 4 built the counting machine (argument principle, residues). This
phase points it at ζ and gets the most famous formula in number theory:
an *exact equation* that writes the primes as a sum over the zeros of
ζ. After this phase, "ψ(x) = x + error" is not a slogan — you'll have
computed the error as a superposition of waves, one per zero, and you
will see exactly why RH is the statement "all waves have equal, minimal
amplitude."

Self-contained: theory, derivations, verified numbers, exercises with
solutions. Nothing outside this repo is required for Gate 5.

After this lesson you can:

- continue ζ from σ > 1 to (almost) the whole plane via the eta trick;
- state the functional equation and verify it numerically at a point;
- name the trivial zeros and locate the critical strip;
- count zeros below height T with Riemann–von Mangoldt and explain the
  formula via the argument principle;
- write the explicit formula and reproduce ψ(x) from the first dozen
  zeros by hand;
- state RH, von Koch's theorem, and Littlewood's sign-change theorem,
  and know precisely what each one buys.

---

## 5.1 Getting off the starting line: eta continuation

Σ 1/nˢ dies at s = 1 and converges nowhere else on the real line.
The alternating cousin is stronger:

```
η(s) = 1 − 1/2ˢ + 1/3ˢ − 1/4ˢ + …        (converges for all σ > 0,
                                          by the alternating test)
```

and on σ > 1 the algebra is one line (split even/odd terms):

```
η(s) = (1 − 2^{1−s}) · ζ(s).
```

**Gate-5's first tool:** wherever 1 − 2^{1−s} ≠ 0, define ζ = η /
(1−2^{1−s}). That *defines* ζ on σ > 0 except s = 1 — an explicit
continuation, zero machinery. Live check at s = ½ (partial sums with the
standard alternating tail-correction +f(N)/2, N = 2·10⁶):

```
η(0.5) partial sum: 0.6045451  → corrected: 0.6048986435
(1 − 2^{1−0.5})·ζ(0.5)        : 0.6048986434        ✓ agreement 1e-10
```

(Note mpmath's raw `nsum` on this slowly-convergent alternating series
misconverges — 0.867, 0.570 depending on method. Trust partial sums +
tail correction, or trust the identity above; both agree, and the
lesson generalizes: *accelerators can lie, definitions can't*.)

**ζ(0) = −1/2, the honest route.** Grandi's series 1 − 1 + 1 − … is
Abel-summed to 1/2, and Abel summation agrees with analytic continuation
here (Abel's theorem) ⇒ η(0) = 1/2. Then 1 − 2^{1−0} = −1:

```
ζ(0) = η(0) / (1 − 2) = −1/2.        (mpmath: mp.zeta(0) → -0.5)
```

And one floor down, where η's series has left the building entirely, the
*continuation* (via the functional equation in §5.2, not the eta trick)
gives ζ(−1) = −1/12 — mpmath prints −0.0833333, Phase 4 already saw it.
These two values are the standard calibration points of the whole
theory: the "sum of all naturals" folklore is a misquoted ζ(−1), and
ζ(0) = −1/2 is why the functional equation's symmetry line sits at ½.

## 5.2 The functional equation

Riemann's completion of ζ: put all the correction factors in one box,

```
ξ(s) = ½ s(s−1) π^{−s/2} Γ(s/2) ζ(s),

FUNCTIONAL EQUATION:   ξ(s) = ξ(1 − s).
```

Equivalently, ζ(s) is expressed in terms of **ζ(1 − s)** (Gate 5:
"zeta(s) relates to zeta(?)": `1-s`) via

```
ζ(s) = 2ˢ π^{s−1} sin(πs/2) Γ(1−s) ζ(1−s).
```

**Try it** (a point where nothing hits a pole, s = 2.5):

```python
import mpmath as mp
mp.mp.dps = 15
s = mp.mpf('2.5')
lhs = mp.zeta(s)
rhs = 2**s * mp.pi**(s-1) * mp.sin(mp.pi*s/2) * mp.gamma(1-s) * mp.zeta(1-s)
print(lhs)    # 1.34148725725092
print(rhs)    # 1.34148725725092   ✓ identical
```

Don't test at integers — Γ(1−s) has its poles exactly there, hiding
behind sin(πs/2)'s zeros. And that collision IS the next fact:

**Trivial zeros.** At s = −2, −4, −6, …: sin(πs/2) = 0 while ζ(1−s) is
an ordinary convergent value (e.g. ζ(3)) and Γ(1−s) is finite — ζ
vanishes, cleanly, no mystery. These are the trivial zeros. (At s = −1,
−3, … the sin factor is ±1 and there's no zero — ζ(−1) = −1/12 was just
a value, not a zero.) The full zero census:

- trivial: the negative even integers;
- nontrivial: inside the critical strip 0 < σ < 1 (see 5.3).

Gate 5 asks for the sum of trivial zeros with |s| ≤ 10 — it's an
arithmetic progression exercise once you know the list; do it in your
head, not by reading anyone's table.

## 5.3 The critical strip, and the hypothesis about it

The functional equation + §5.1 pin ζ on all of ℂ (pole at s = 1 only).
Where can nontrivial zeros live? Euler product (Phase 2) ⇒ no zeros for
σ > 1; FE reflects that to no zeros for σ < 0 — after removing the
trivial ones. What's left: the **critical strip** 0 ≤ σ ≤ 1.

> **RH.** Every nontrivial zero has Re(ρ) = 1/2.

Facts of life inside the strip: zeros are symmetric about both the real
axis (ζ(real reals) → conjugate symmetry) and the line σ = ½ (the FE) —
two mirror walls, four-way kaleidoscope. ζ(½ + it) is real on the line
in the right normalization (Hardy's Z-function), so counting its sign
changes counts zeros on the line: Hardy proved (1914) infinitely many
zeros sit ON the line; ~40% (Conrey) is the proven floor for the
proportion. The first zero lives a little above t = 14 — compute it
yourself with `mp.im(mp.zetazero(1))`, it's the single most famous
coordinate in mathematics and you should own it, not be told it.

**Counting zeros: Riemann–von Mangoldt.** Apply the argument principle
(Phase 4!) to ξ along the rectangle with corners −ε, 1+ε, 1+ε+iT,
−ε+iT. #zeros = the winding of ξ(γ) about 0 = total Δarg along four
sides. Three sides contribute elementary terms (the ξ = ½s(s−1)…, the
π^{−s/2}, and Γ factors rotate by computable amounts along the real
axis; the right side contributes (T/2π)ln(T/2πe) from ζ ~ …) and the
top side contributes T·θ'(T)-ish. Grinding the four sides gives:

```
N(T) = (T/2π) ln(T/2π) − T/2π + 7/8 + S(T),    S(T) = (1/π)·arg ζ(1/2+iT)
```

— the "+7/8" is bookkeeping dust; S(T) is the wiggle the argument of ζ
pays for the top edge (|S| ≤ O(ln T), and it's genuinely
unpin-downable). Verified against mpmath (counts you can rerun):

```
T = 20:  main 1.3775,  N = 1     (S = −0.3775)
T = 50:  main 9.4228,  N = 10    (S = +0.5772)
T = 60:  main 12.8734, N = 13    (S = +0.1266)
```

Gate 5 will ask you for a count at a height we have NOT printed here —
the loop is four lines and you've seen it twice now.

## 5.4 The explicit formula: primes = Σ over zeros

Riemann (1859), with the ψ₀ smoothing (ψ₀(x) = ψ(x) away from prime
powers, half-value at jumps — same convention as the repo lab):

> **EXPLICIT FORMULA.**
> ```
> ψ₀(x) = x − Σ_ρ x^ρ/ρ − ln(2π) − ½ ln(1 − x^{−2})
> ```
> Σ over nontrivial zeros, paired symmetrically (ρ and ρ̄ together, so
> each pair is a real cosine wave: x^{1/2}cos(γ ln x)/|ρ|·2-ish).

Read it like a sound engineer: ψ₀(x) = the pure tone **x**, minus a
superposition of **one wave per zero** — wave ρ has frequency γ = Im ρ
(in ln x scale) and amplitude x^{Re ρ}/|ρ| — plus two tiny DC offsets
(ln 2π and the trivial-zeros tail, the last term; check: it's ~ −1/(2x²),
dead weight beyond x = 10).

**Try it** — rebuild ψ(1000) = 996.6809 from raw zeros (each pair ρ, ρ̄
summed; the −ln2π −½ln(1−x⁻²) offsets included):

```python
import mpmath as mp, math
def psi_ef(x, K):
    tot = mp.re(sum(mp.e**(mp.zetazero(k)*mp.log(x))/mp.zetazero(k)
                  + mp.e**((1-mp.zetazero(k))*mp.log(x))/(1-mp.zetazero(k))
                  for k in range(1, K+1)))
    return x - tot - math.log(2*math.pi) - 0.5*math.log(1 - x**-2)
for K in (1, 3, 10, 30):
    print(K, float(psi_ef(1000.0, K)))
# 1  → 999.4203    3  → 997.4276
# 10 → 997.2061    30 → 993.6821      truth: 996.6809
```

Three zeros already know ψ(1000) to 0.3%; then it *oscillates* as more
waves are added — the partial sums ring (Gibbs-style) around the truth.
This is not a bug; truncated spectral sums always ring, and the ringing
IS the prime error term for moderate x. `src/phase5/explicit_formula.py`
does the same at x ≤ 1e5 with plots; its own closing lines:

> "The waves ARE the error term: what they don't cancel is the tail of
> the next thousands of zeros. … RH (all Re=1/2) <=> error ~ sqrt(x)".

Sanity anchor: ψ(10⁴) = 10013.3967 (direct sieve) vs 10021.3 (K=10
waves) — relative error 0.08% from ten complex numbers.

## 5.5 What RH actually buys: von Koch

Each wave has size x^{Re ρ}/|ρ|. Sum over zeros near height T ~
(T ln T)/2π of them (5.3's count) — a hypothetical zero at Re ρ = β
makes waves of size x^β, and bookkeeping turns the worst β into the
error term:

> **THEOREM (von Koch 1901).** RH ⇔ ψ(x) = x + O(x^{1/2}(ln x)²).
> (Gate 5 wants the exponent a in O(x^a(ln x)²): **1/2** — the (ln x)²
> absorbs the 1/|ρ| decay across heights.)

Unconditionally (zeros known to hide at Re ≤ 1 − c/ln, the zero-free
region) you get ψ(x) = x + O(x·e^{−c√ln x}) — Phase 3's error, now
*explained*: that strange shape is what a zero-free region that narrows
like 1/ln T costs you in wave amplitudes.

Empirical feel, direct computation over x ∈ [10², 10⁵]:

```
max |ψ(x) − x| / √x        = 0.777   (at x = 1422)
max |ψ(x) − x| / (√x ln²x) = 0.0281
ψ(10⁵) − 10⁵ = 51.56       vs   √(10⁵)·(ln 10⁵)² ≈ 42 000 (von Koch budget)
```

The truth is three orders inside the RH budget even at these sizes —
RH is not tight empirically at small x; it's a claim about the *last*
wave, forever.

**Same content, π flavor:** via Abel + the Li integral (Phase 2), RH ⇔
π(x) = Li(x) + O(√x · ln x). The wiggly green curve in
`src/phase3/pnt_lab.py` is this error, plotted.

## 5.6 Li overtakes π — eventually, and infinitely often

At every x you can actually *run*, Li(x) > π(x) (Phase 2: 9629 vs 9592
at 10⁵; 78626.5 vs 78498 at 10⁶). Tempting to conjecture "Li leads
forever". **Littlewood (1914) proved the opposite:** π(x) − Li(x)
changes sign infinitely often — proved by feeding the explicit formula
's wave race: the zeros conspire to build a coherent chorus near some
astronomical x (his method gave a bound around 10^{10^{10^{…}}};
Skewes made it famous). Modern computation (Bays–Hudson 2000) located
the first reversal near **1.397 × 10³¹⁶**. Beyond that x, and again and
again forever, the primes briefly outrun their own density. Gate 5
wants the surname: `littlewood`.

The lesson inside the lesson: a formula can be *right about the
average* and *eventually wrong in the lead* — asymptotics and records
are different mathematics. Phase 6 is where this moral gets a whole
season.

## 5.7 The two functions Gate 5 will ask you to *write*

psi, as a float over reals (no numpy needed at gate scale):

```python
import math
def psi(x):
    """sum_{n <= x} Λ(n) = Σ_{p^k <= x} ln p."""
    from src.common.primes import primes_upto   # or your own sieve
    out = 0.0
    for p in primes_upto(int(x)):
        pk = p
        while pk <= x:
            out += math.log(p)
            pk *= p
    return out
# anchors: psi(1000) = 996.6809,  psi(10⁴) = 10013.3967,
#          psi(10⁵) = 100051.5640
```

(Remember ψ's staircase: value constant between prime powers; if the
gate passes a non-integer, `pk <= x` handles it — that's exactly why
the loop bound uses x, not int(x).)

And the wave-sum `psi_ef` from §5.4 — know both directions: zeros→ψ
and ψ→"which wave is missing".

---

## Lab / tooling map

- `src/phase5/explicit_formula.py` — J(x), ψ₀(x), zero-wave overlays,
  figures to `data/`. Run it once before the gate; it's the season
  montage.
- `src/phase3/pnt_lab.py` — π(x)−Li(x) is the same wave story; the
  green curve is §5.6's protagonist as a teenager.
- `gates/gate_common.py::Li` — the repo's Li = ∫₂ˣ dt/ln t (u = ln t
  substitution); Gate 5's two Li−π questions use THIS definition —
  it differs from the classical li by the constant −li(2) ≈ −1.045.

## Exercises

★1. From η(s) = (1 − 2^{1−s})ζ(s) on σ > 1, prove η's series converges
   for every σ > 0 (alternating test, uniformly on [δ, ∞)) and deduce
   ζ extends to σ > 0 minus {1}. Where exactly did "1 − 2^{1−s} ≠ 0"
   fail to hold besides s = 1? (Answer includes a line of complex
   exponentials — they're the trivial zeros' twin siblings.)
★2. Use the FE to compute ζ(−1) from ζ(2): track sin(πs/2), Γ(1−s), and
   the powers at s = −1. Cross-check with mpmath.
★3. List all trivial zeros with |s| ≤ 12 and give their sum (gate
   twin). Then: ζ(−8) = 0 or ≠ 0? ζ(−9)? (No mpmath — decide.)
★★4. Count zeros with 0 < Im < 45 by mpmath; give RvM's main term at
   45 and S(45). (You have the table at 20/50/60 to calibrate your
   suspicion about the sign of S.)
★★5. Reproduce §5.4's table at x = 10⁴ for K = 1, 5, 15. Which single
   wave carries most of ψ₀(10⁴) − 10⁴? (Print per-zero contributions;
   the amplitude ranking of x^ρ/ρ vs Im ρ is the answer.)
★★6. von Koch budget: compute |ψ(x) − x|/√x at every jump point
   p^k ≤ 10⁵ (reuse psi's sieve); report the max and its location.
   Then the same for [10⁵, 10⁶]. Which window leans closer to violating
   0.777? (This is a probe for RH — it never succeeds; run one window
   and feel the odds.)
★★7. The ringing: at x = 10⁴, print psi_ef for K = 1..40 and find
   where |psi_ef − 10013.3967| attains its MINIMUM and the k right
   after its largest overshoot. Explain both in one sentence each using
   wave amplitudes.
★★8. Littlewood arithmetic: first sign change x₀ ≈ 1.397·10³¹⁶. How
   many zeros of ζ (RvM main term) have height below x₀? (ln x₀ ≈ 729.6
   ⇒ plug into 5.3's formula.) Sanity: is "the first reversal needs
   ~10⁸² waves conspiring" consistent with a lead that looked stable up
   to 10⁶?
★★★9. Derive the wave-amplitude claim: for a zero ρ = β+iγ, show the
   pair-contribution to ψ₀ is 2x^β·cos(γ ln x − arg ρ)/|ρ|. Then: if a
   single zero existed at β = 0.8, estimate its wave size at x = 10⁶
   against √x·ln²x. Would you notice?
★★★10. Read `src/phase5/explicit_formula.py` end to end; change K (zero
   count) and xmax, regenerate the figure, and write two sentences on
   where the overlay starts to lie and why (hint: 5.4's ringing).

## Appendix — solutions

★1. Alternating test: 1/n^σ ↓ 0 for σ > 0. Uniform on σ ≥ δ ⇒ η
   holomorphic there. ζ = η/(1−2^{1−s}): the factor vanishes where
   2^{1−s} = 1 ⇔ (1−s)ln2 ∈ 2πiℤ ⇔ s = 1 − 2πik/ln2 — a vertical
   arithmetic progression; at those points η also vanishes (they're the
   removable ones of this chart) — this is why eta-chart continuation
   needs a stitch at each, and why the FE is the cleaner global object.
★2. s = −1: sin(−π/2) = −1; Γ(2) = 1; 2^{−1} = ½; π^{−2}:
   ζ(−1) = 2^{−1}π^{−2}·(−1)·1·ζ(2) = −(π²/6)/(2π²) = −1/12 ✓ mpmath
   −0.0833333. (This derivation is the "−1/12 folklore" made honest.)
★3. −2, −4, −6, −8, −10, −12; sum −42 (progression: −2·(1+…+6)); ζ(−8)
   = 0 (trivial list), ζ(−9) ≠ 0 (odd negatives are values: ζ(−9) =
   −B₁₀/10 = −1/132 ≈ −0.00758 — value, not zero; mpmath agrees).
★4. Reference: N(45) = **8**, main term 7.8134, S(45) = +0.1866.
   Cross-check your own run against the calibrated table — S values at
   20/45/50/60 are −0.3775/+0.1866/+0.5772/+0.1266: no sign pattern,
   no monotonicity; S is pure wiggle.
★5. Verified: K=1 → 10012.1331, K=5 → 10025.6166, K=15 → 10024.0827
   (truth 10013.3967). The needed wiggle is ψ₀−x+ln 2π = +15.23, and
   the first wave alone supplies −w₁ = +13.97 — peak amplitude
   2√x/|ρ₁| ≈ 14.2 (divide 200 by the |ρ₁| you computed in §5.3) — so
   ρ₁ *carries* the signal; the later
   waves are a chorus of competitors of comparable size (each
   200/|ρ_k|), which is exactly why partial sums ring instead of
   settling.
★6. Reference runs: max over [100, 10⁵] = 0.777 at x = 1422; the
   [10⁵, 10⁶] window dips lower (deviation grows ~√x while √x is
   divided out — ratio slowly shrinks). One window ≈ lottery ticket.
★7. Verified over K = 1..60 at x = 10⁴: the *closest* partial sum is
   K = 1 (error 1.26 — luck: the lone wave lands near the truth before
   the chorus starts shoving), and the *worst* is K = 4 (error 18.2 —
   the ρ₄ wave enters with the wrong phase at this x). Partial sums
   ring; there is no monotone approach, and "more zeros = better" fails
   locally for every x. Same physics as §5.6's stable-looking lead that
   hides a coming reversal.
★8. ln x₀ = ln(1.397·10³¹⁶) = 727.95. Wave γ oscillates with period
   2π/γ in the ln x variable — a wave is "slow" (able to hold a fixed
   sign near x₀) only for γ ≲ ln x₀ ≈ 728: RvM main term at 728 gives
   ≈ **436** such zeros (mpmath's N(728) sits within the wiggle). At
   x = 10⁶ the same test leaves ln x = 13.8 and the count is **zero** —
   no slow wave exists below the first zero's height, so the +bias
   looks permanent. The reversal is a *phase-locking* event among a few
   hundred slow waves of size √x₀/|ρ|, whose coherent sum can swallow
   the ordinary error once ln x is big enough. 10⁶ vs 10³¹⁶ is a phase
   problem, not a count problem.
★9. Pair: x^ρ/ρ + x^{ρ̄}/ρ̄ = 2 Re(x^ρ/ρ) = 2x^β cos(γ ln x − arg ρ)/|ρ|
   ✓. At β = 0.8, x = 10⁶, the ρ₁-wave peaks at 2·10^{4.8}/|ρ₁| ≈
   8922. Observed deviation in range obeys |ψ(x)−x| ≤ 0.777√x ≤ 777
   (§5.5's scan) — a rogue β = 0.8 zero would shout 10× louder than the
   entire measured error. Nothing like it is audible ⇒ β > ~0.6 is
   empirically dead in the checked range; RH is that sentence, forever.
★10. Subjective; key line to notice: overlay degrades first at *large*
   x (more zeros needed as waves get denser in ln x) and the trivial-
   zero correction −½ln(1−x⁻²) becomes negligible past x ≈ 10 (size
   ~ 1/(2x²)) while −ln 2π ≈ −1.8379 is a permanent DC offset.

## Gate-5 readiness map

| Gate 5 item | Covered by |
|---|---|
| Im(ρ₁) | §5.3 (mpmath one-liner) |
| sum of trivial zeros \|s\|≤10 | §5.2 list + ★3 twin |
| ζ(0) | §5.1 derivation |
| von Koch exponent a | §5.5 |
| #zeros with Im < 100 | §5.3 loop + verify vs RvM |
| Li(10⁶) − π(10⁶) | §5.6 (subtract the two printed values) |
| sign-change theorem | §5.6 (`littlewood`) |
| RvM main term at T = 14 | §5.3 formula (plug in) |
| FE partner of s | §5.2 box (`1-s`) |
| psi(x) as float | §5.7 reference code |
| Li(10⁴) − π(10⁴) | §5.6 method (gate_common.Li!) |
| wave size under RH | §5.5 (x^{1/2}: option B) |

When this feels boring, take the gate. The zeros will follow you into
Phase 6: same waves, but now asked who wins the *races* — and who is
allowed to be alone.
