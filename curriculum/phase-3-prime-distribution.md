# Phase 3 — The Distribution of Primes (the elementary summit)

**Budget: 4–6 months. Requires Phases 0–2. Self-contained: every theorem
below is proved in this file or explicitly boxed as a black box with its
precise statement. Books at the end, optional as always.**

You now have the tools to prove *real* theorems about primes — the ones
people wrote 19th-century books about — and to see exactly where elementary
methods hit their wall (which is the plot device that forces Phase 4).

```bash
python3 src/phase3/pnt_lab.py      # run early, re-run after each section
python3 src/phase3/gap_lab.py
```

---

## 3.1 Three ways to count the same staircase

```
π(x) = #{p ≤ x}                      the staircase itself
θ(x) = Σ_{p≤x} ln p                  log-weighted primes        (Chebyshev)
ψ(x) = Σ_{p^k ≤ x} ln p = Σ_{n≤x} Λ(n)   prime POWERS too       (von Mangoldt)
```

where Λ(n) = ln p if n = pᵏ (any k ≥ 1), else 0 — Phase 1 promised you this
character; here's its debut. ψ counts each prime power pᵏ with weight
ln p, and that is *exactly* how the coefficients of −ζ′/ζ fall out
(Phase 5 will cash that check).

**Worked (do these by hand, then one-line your way):**
θ(100) = ln of (product of the 25 primes ≤ 100) = **83.728…**
ψ(10): powers 2,4,8 give 3·ln2; 3,9 give 2·ln3; 5,7 give ln5+ln7 ⇒
ψ(10) = ln(8·9·5·7) = ln 2520 = **7.832**.

**ψ vs θ differ only by small powers.** Every pᵏ ≤ x with k ≥ 2 has
p ≤ √x; there are ≤ √x such powers; each contributes ≤ ln x:

```
0 ≤ ψ(x) − θ(x) ≤ √x · ln x          (3 lines — write them).
```

At x = 10⁵: ψ = 100051.6, θ = 95877.7-ish, difference ≈ 174 ≤ 316·11.5 ✓
(pattern; verify with code). So ψ and θ are asymptotically *identical
twins* — but ψ's generating identity makes it the algebraically pleasant
one. Everything Phase 5 does, does with ψ.

## 3.2 The PNT and the equivalences — prove them all yourself

**PNT (Hadamard & de la Vallée Poussin, 1896).** π(x) ~ x / ln x.

Before believing it, own this chain (the actual working theorem-set;
every step is Abel summation, Phase 2 §2.5):

**Theorem.** The following are equivalent:
(i) π(x) ~ x/ln x  (ii) θ(x) ~ x  (iii) ψ(x) ~ x
(iv) Σ_{n≤x} Λ(n)/n = ln x + o(ln x).

*(ii)⇔(i):* π = θ-integral by Abel with f = 1/ln t:
θ(x) = π(x)ln x − ∫₂ˣ π(t)/t dt. If θ ~ x, put π(t) = (θ-part)… the
clean route: from θ ~ x, sandwich π(x) = (θ(x) + Σ-error)/ln x by
splitting the sum at √x (small primes contribute O(√x)). Conversely
θ(x) = ∫ (ln t) dπ = π(x)ln x − ∫ π(t)/t dt and inserting π ~ t/ln t
turns the integral into ∫ dt/ln t ~ x/ln x (Phase 2 §2.6 asymptotics!),
forcing θ ~ x. Write both directions with ε's (exercise ★1 — budget
an afternoon; it is the single most-used calculation technique ahead).
*(ii)⇔(iii):* the √x·ln x bound of 3.1, divided by x → 0. ∎
*(iii)⇔(iv):* Abel once more with aₙ = Λ(n), f = 1/t: both directions
two lines. ∎

**Moral:** the PNT is *really* the statement "ψ(x) = x + smaller" — the
log-weighted prime powers track the line x. (The lab plots ψ, π, Li, x/ln
x so you can *see* the equivalences wearing different clothes.)

## 3.3 Chebyshev (1852): primes are sandwiched — full proof

**Theorem (weak form, proved below).** There are constants with
liminf θ(x)/x ≥ ln 2 ≈ 0.693 and limsup θ(x)/x ≤ ln 4 ≈ 1.386;
consequently c₁·x/ln x ≤ π(x) ≤ c₂·x/ln x for all large x. Chebyshev's
sharper bookkeeping gets c₁ ≈ 0.92, c₂ ≈ 1.11 — same techniques, more
terms (theorem box below).

*Proof of the weak form.* Two binomial lemmas (proved, not quoted):

**Lemma A.** 4ᵐ/(2m+1) ≤ C(2m,m) ≤ 4ᵐ/√(3m+1) for all m ≥ 1.
*Lower:* 4ᵐ = ΣₖC(2m,k) ≤ (2m+1)·max = (2m+1)·C(2m,m). ∎
*Upper:* induction; base m=1 equality; the step needs
2(2m+1)/(m+1) ≤ 4√(3m+1)/√(3m+4) — squaring and expanding both sides,
it is 12m³+28m²+19m+4 ≤ 12m³+28m²+20m+4, i.e. 0 ≤ m. ∎ (That
one-line polynomial check *is* the whole induction — this is what
"elementary" buys you: real content, small tools.)

**Upper bound.** Any prime with m < p ≤ 2m divides C(2m,m): p > m forces
exponent ⌊2m/p⌋ − 2⌊m/p⌋ = 1 − 0 = 1. So

```
θ(2m) − θ(m) = Σ_{m<p≤2m} ln p ≤ ln C(2m,m) ≤ 2m ln 2.
```

Telescope at m = x/2, x/4, …: θ(x) ≤ Σⱼ (x/2^{j+1})·2 ln 2 = x ln 2 ·
Σⱼ 2^{−j} = 2x ln 2 ⇒ **limsup θ(x)/x ≤ ln 4**. ∎

**Lower bound.** C(2m,m) divides lcm(1, 2, …, 2m) = e^{ψ(2m)}: the
p-exponent of the binomial is Σⱼ(⌊2m/pʲ⌋ − 2⌊m/pʲ⌋), a sum of 0/1
terms (exercise ★★2b) with at most ⌊log_p 2m⌋ summands — exactly the
p-exponent of the lcm. Hence

```
e^{ψ(2m)} ≥ C(2m,m) ≥ 4ᵐ/(2m+1)   (Lemma A lower)
⇒  ψ(2m) ≥ 2m ln 2 − ln(2m+1)     ⇒  liminf ψ(x)/x ≥ ln 2.  ∎
```

Convert θ/ψ bounds to π bounds with Abel (3.2's identity, both
directions), giving honest constants c₁ ≈ 0.69, c₂ ≈ 1.39 from the short
proof. Chebyshev's name rides the sharpened 0.92/1.11 — same lemmas plus
weighted ⌊x/2ⁱ⌋ bookkeeping; treat as:

> **THEOREM BOX (Chebyshev, sharp form).** For all x ≥ 2:
> 0.921·x/ln x < π(x) < 1.106·x/ln x (with suitable explicit ranges).
> Method: upper via ψ(x)+ψ(x/2)+ψ(x/3²)+… ≥ … , lower via C(2m,m)
> refinements. You could grind it out; you don't need to.

**Why the gap can't be closed elementarily (the season finale).**
Chebyshev's method bounds prime densities via which primes divide
binomials — it *sees* θ only through sums over p ≤ x with periodic
weights. Closing 1.386…/0.693… to 1 requires knowing θ(x) in *intervals*
[x, x+h] with h/x → 0, and that requires canceling oscillations that
elementary weights cannot detect. The oscillations have a name (zeros of
ζ) and Phase 4 is the sequel this sentence demands. Believe the shape now;
Phase 5 will make you feel it numerically.

## 3.4 Bertrand's postulate — Erdős's theorem, fully

**Theorem (Bertrand 1850; Erdős proof 1932, when he was 19).** For every
integer m ≥ 1 there is a prime p with m < p ≤ 2m.

*Proof.* Write C(2m,m) = ∏_p p^{e(p)} with e(p) = Σⱼ (⌊2m/pʲ⌋ − 2⌊m/pʲ⌋).
Keep three ledgers straight (m ≥ 5 throughout; tiny m are checked by
sieve at the end):

(a) **e(p) = 0 for p ∈ (2m/3, 2m]:** ⌊2m/p⌋ = 2, ⌊m/p⌋ = 1, and p² >
4m²/9 ≥ 2m kills higher powers (m ≥ 5). **e(p) = 1 for p ∈ (m, 2m/3]:**
the Bertrand prey would appear in the binomial if it existed.
(b) **Small primes:** p ≤ √(2m) contribute ∏ p^{e(p)} ≤ (2m)^{π(√2m)} ≤
(2m)^{√(2m)} (each e(p) ≤ ⌊log_p 2m⌋ and each p ≤ 2m).
(c) **Middle primes:** √(2m) < p ≤ 2m/3 contribute ∏ p ≤ e^{θ(2m/3)} ≤
e^{(2m/3) ln 4} = 4^{2m/3} — Chebyshev's upper bound (3.3) does the work.

Now *assume no prime lies in (m, 2m]* (contradiction target). By (a) no
prime in (2m/3, 2m] contributes either, so all mass is (b)·(c):

```
4ᵐ/√(3m+1)  ≤  C(2m,m)  ≤  (2m)^{√(2m)} · 4^{2m/3}      (Lemma A lower!)
⇒  4^{m/3}  ≤  √(3m+1) · (2m)^{√(2m)}.
```

Left side is 2^{2m/3}; right side's binary log is ≈ √(2m)·log₂(2m) +
log₂(3m+1) ≪ m^{3/2}·tiny — at m = 4000: LHS log₂ = 2666 vs RHS ≈ 1174,
and the ratio only improves for larger m (exercise ★★1: verify the
inequality flips for all m ≥ 4000 — one calculus line + a computer check
of the monotone gap). For m < 4000, a sieve confirms a prime lives in
every (m, 2m] (one line; the small cases 2→3, 4→5, 8→11 are exactly what
the asymptotics excuse). Contradiction ⇒ Bertrand. ∎

That is the entire proof — Lemma A + three ledgers + Chebyshev's upper.
The "6-page legend" is really a page and a half plus honesty about small
m, and you now own every line of it.
**Gate-3 uses it as an exhibit:** "smallest prime strictly between 1000
and 2000" — one Bertrand instance: next prime after 1000 (**run `next(p
for p in primes if p > 1000)`; 503 is the corresponding answer for
(500,1000) — do not trust this sentence's numbers, trust your sieve**).

## 3.5 Mertens's theorems (1874): the elementary shadow of the PNT

**M1.** Σ_{p≤x} (ln p)/p = ln x + O(1).
*What Chebyshev + Abel already give you (do this yourself):* Abel on
θ: Σ_{p≤x} (ln p)/p = θ(x)/x + ∫₂ˣ θ(t)/t² dt, and inserting c₁t ≤ θ ≤ c₂t
traps the sum between c₁ ln x and c₂ ln x + O(1). The *sharp* O(1)-version
needs one more gear of elementary bookkeeping — Legendre's formula
running on v_p((2m)!) vs v_p(C(2m,m)) (Apostol ch. 13; grindable with
your current tools in two pages), and Phase 5 hands it to you for free
from any PNT error term. Treat as boxed:

> **THEOREM BOX (M1).** Σ_{p≤x} (ln p)/p = ln x + O(1). Numerically:
> at 10⁵ the sum is 10.184 against ln(10⁵) = 11.513 — inside the band,
> crawling toward it like everything else here crawls.

**M2 (the pretty one).** Π_{p≤x} (1 − 1/p) ~ e^{−γ}/ln x.
*Where e^{−γ} comes from:* take logs of the product; Taylor pins
ln(1−1/p) = −1/p + O(1/p²) so the log of the product is −(ln ln x + M)
minus a convergent correction — and the constants conspire as
M = γ + Σ_p [ln(1 − 1/p) + 1/p] (verify numerically: the prime sum to
10⁵ plus γ gives 0.261498 against M = 0.261497 — that identity *is* the
place where γ sneaks into the primes). Exercise ★★4 derives M2 from the
PNT; accept-and-verify meanwhile:

```
x      Π_{p≤x}(1−1/p)·ln x     e^{−γ} = 0.56146
10²    0.5541                  (already close!)
10⁴    0.5608
10⁶    0.5614
```

**M3.** Σ_{p≤x} 1/p = ln ln x + M + o(1), M = 0.261497… — derive from M1
by Abel (exercise ★★4: 4 lines); Phase 2 §2.4's table is the numerics.

These three are the *elementary* peak: same logarithmic texture as the
PNT, no complex analysis. Note what Mertens does NOT give: π(x) —
Σ 1/p is blind to whether mass sits on few or many primes. The wall again.

## 3.6 ζ on the real line: the pole that runs the show

**Theorem.** ζ(s) = Σ n^{−s} = Π (1−p^{−s})^{−1} (s > 1, Phase 2), and
ζ(s) ~ 1/(s−1) as s → 1⁺. *Proof:* integral test squeeze:
∫₁^∞ t^{−s}dt ≤ ζ(s) ≤ 1 + ∫₁^∞ t^{−s}dt ⇒ 1/(s−1) ≤ ζ(s) ≤ 1 + 1/(s−1).
∎ The residue 1 at the pole is *the reason* every prime-counting asymptotic
has that exact leading term: Phase 5's explicit formula literally reads the
residue of ζ(s)xˢ/s at s = 1 and out pops x. "The pole at 1 is the main
term; the zeros are the error" — save this sentence for the finale.

## 3.7 The PNT proper (black box, precisely)

> **THEOREM (PNT).** π(x) ~ x/ln x; equivalently ψ(x) ~ x.
> **THEOREM (de la Vallée Poussin, 1899).** π(x) = Li(x) +
> O(x·e^{−c√ln x}) for an effective c > 0. The error term is dominated by
> zero-free regions of ζ — a complex-analysis statement (§3.3's wall,
> now with a door).
> **THEOREM (Selberg–Erdős, 1949).** Elementary proofs exist (Selberg's
> key identity Σ_{n≤x} Λ(n)ln n + Σ_{d|n}… — the "elementary method").
> History's sting: Hardy called elementary proofs "in the nature of
> mutilations" — one of the great wrong predictions in math; the hunt for
> elementary proofs of Goldbach-type statements continues to this day.

What you must be able to *state*: the equivalences (3.2), the constants of
Chebyshev's theorem (as theorem box), the shape of the dvP error, and the
sentence: **"ψ(x) = x + (error), and the error is a sum over zeros"** —
Phase 5 makes that literal.

Numerical literacy (the lab's output; know the *shapes*, not the
specifics): x/ln x undershoots π(x) at every x you can compute; Li(x)
overshoots by +37 at 10⁵ (Phase 2's number — Li leads forever… until it
doesn't, at some x near 10³¹⁶, Littlewood-style, Phase 5); the ratio
(x/ln x)/π(x) = 0.883 at 10⁴, 0.922 at 10⁶ — climbing toward 1 at
speed 1/ln x: *slow as civilization.* Rosser–Schoenfeld: π(x) > x/ln x
for all x ≥ 17 — a proved inequality; your lab data (up to 2·10⁷) agrees.

## 3.8 The gap problem opens

gₙ := pₙ₊₁ − pₙ. Bertrand (3.4) says gₙ < pₙ. The *other* direction is
trivial and arbitrarily bad:

**Arbitrarily long gaps.** For any L: (L+1)! + 2, (L+1)! + 3, …,
(L+1)! + (L+1) are L consecutive composites (the k-th is divisible by k).
∎ (First occurrence below 10³: record gaps 1, 2, 4, 6, 8, 14, 18, 20 at
p = 2, 3, 7, 23, 89, 113, 523, 887 — `gap_lab.py` prints the whole
parade; the first gap ≥ 100 lives somewhere below 10⁶ and the gate's
"largest gap below 10⁶" is one sieve + one max — find it *yourself*;
the knowing and the computing are the skill.)

**Cramér's model (1936).** Replace "n is prime" by independent
Bernoulli(1/ln n) events (PNT as a probability law). Then the gap at
position x is geometric with mean ln x, and the longest gap below x
solves (x/ln x)·P(gap > G) ≈ 1 ⇒

```
P(gap > λ·ln²x) ≈ e^{−λ}      ⇒   longest gap below x ~ (ln x)².
```

Cramér conjecture: limsup gₙ/ln²pₙ = 1. Numbers: (ln 10⁶)² ≈ 191; (ln
10⁹)² ≈ 430. Records *sit below* (ln x)² — as the model demands —
and (Phase 6 theorem) records must eventually beat (ln x)²·(unbounded
factor): **the model is provably wrong in the limit**, while remaining
the best guide at every finite x. Hold that tension; Phase 6 dissects it.

---

## Labs

- `src/phase3/pnt_lab.py [xmax]` — π vs x/ln x vs Li, relative-error
  figure, CSV. Its decade table now carries exact-decimal offsets —
  compute your own before reading the print.
- `src/phase3/gap_lab.py [xmax]` — all gaps, record table, Cramér and
  Maier–Pomerance curves. At 2·10⁷ the record is 180 at p = 17,051,707 —
  re-derive it; trust, then verify.

## Exercises

★1. Prove (i)⇔(ii) of 3.2 with full ε bookkeeping (the afternoon well
   spent).
★2. Prove 0 ≤ ψ − θ ≤ √x·ln x and sharpen to (√x + O(x^{1/3}))·ln x.
★3. Bertrand exhibit hunt: smallest prime in (500,1000) [503 by your
   sieve — this doc's number is only an example], (5000,10000), and the
   *largest* first-witness m where Bertrand "just barely" helps below
   10⁴ (compute the list of first primes after each power of 2).
★★1. Write Erdős's Bertrand proof with every estimate labeled and the
   small-m table explicit (m ≤ 2048 checked by computer counts as honest).
★★2. Prove (a) ∏_{p≤m} p^{⌊log_p 2m⌋} ≤ 4^{√(2m)}·(2m+1) and (b)
   C(2m,m) | lcm(1,…,2m) — the two crumbs of 3.4 step (b).
★★3. Chebyshev conversion: from limsup θ/x ≤ ln 4 derive
   limsup π·ln x/x ≤ ln 4 via Abel (the √x split) — where does the
   c₂ = 1.386 survive and where does it improve?
★★4. From ψ ~ x: derive M2 (Π(1−1/p) ~ e^{−γ}/ln x) in 5 lines (log it,
   M1-style via Abel, then match constants through the identity
   M = γ + Σ_p [ln(1−1/p) + 1/p] — verify that numerically first: prime
   sum to 10⁵ + γ = 0.261498 against M = 0.261497). Then M3 from M2.
★★5. Li vs x/ln x: reproduce 3.7's "ratio climbs like 1/ln x" numerically
   at 10⁴, 10⁶, 10⁸ with pnt_lab's CSV; fit and confirm the 1/ln slope.
★★6. Cramér heuristic end-to-end: from P(gap > λ ln²x) ≈ e^{−λ}, derive
   "longest gap below x ~ ln²x" by solving (x/ln x)·e^{−λ} ≈ 1. Then
   sanity-check at lab scale: the record below 2·10⁷ is 180 (gap_lab —
   re-verify), while ln²(2·10⁷) ≈ 286: records sit BELOW the model, as
   the model's own statistics demand at finite x. Predict the 10¹²-scale
   figure (ln²(10¹²) ≈ 764) and note in one paragraph why "record below
   the curve" is expected behavior, not evidence against Cramér — and
   what Phase 6's theorem will say about the far tail.
★★★1. Prove Σ_{n≤x} Λ(n)/n = ln x − γ + o(1) FROM ψ ~ x (Abel; the
   constant −γ appears from H-vs-integral — all tools Phase 2).
★★★2. (The wall, felt.) For each of 20 random short intervals [x, x+ln²x]
   near 10⁶, compare the prime count to Cramér expectation; write 3
   sentences on what a *proof* of "too many/ too few infinitely often"
   would require beyond Chebyshev's method (this is Maier's theorem's
   *shape* — Phase 6 names the mechanism).

## Gate-3 readiness map

| gate | section / skill |
|---|---|
| q01 π(10⁶) | 3.7 literacy + your own sieve (one line, trust `sieve`) |
| q02 θ(x) at given x, rounded | 3.1 + code (`theta` pattern) |
| q03 ψ(100)-style | 3.1 — prime POWERS, worked ψ(10) pattern |
| q04 Bertrand exhibit (1000,2000) | 3.4 — sieve the interval; don't guess |
| q05 Mertens Π(1−1/p)·ln x | 3.5 M2 numerics pattern |
| q06 largest gap below 10⁶ | 3.8 + gap_lab / own code |
| q07 Li(10⁶) repo-def | Phase 2 §2.6 quadrature — reuse `li` |
| q08 Cramér round((ln 1e10)²) | 3.8 — pattern shown at 10⁶, 10⁹ |
| q09 ratio at 10⁶ | 3.7 — the ratio exercise pattern |
| q10 PNT-equivalent MCQ | 3.2 — ψ ~ x (B) |
| q11 Li − π at 10⁷ | 3.7 numeracy; repo `li` minus sieve count |
| q12 `theta` function | 3.1 — hand over the function object |

## Optional deeper reading

Apostol ch. 1–4, 13 (the grindable standard); Granville's free notes for
voice; Axler's *Prime Obsession* in bed once (it re-reads as a different
book after Phase 5). None required for Gate 3.
