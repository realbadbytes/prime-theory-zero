# Phase 6 — Races, biases, and the anatomy of prime gaps

The PNT says the classes tie asymptotically. This phase is about the
*manner of losing*: who leads while the tie approaches (prime races),
which successors primes refuse (consecutive-prime bias), which residue
patterns are even *allowed* to be prime infinitely often (admissible
tuples), and how far apart consecutive primes can force themselves to
be (gaps). Nearly every headline result Gate 7 will quiz you on lives
here or in its shadow.

Self-contained: definitions, theorems, verified numerics, exercises with
solutions. The lab does the heavy lifting; you do the thinking.

After this lesson you can:

- run and interpret a prime race, state Chebyshev's bias and
  Littlewood's flip theorems, and locate the mod-4 flip exactly;
- read a Lemke Oliver–Soundararajan bias table and know what's provable
  about it unconditionally;
- decide admissibility of any tuple in three lines of code;
- state the Zhang–Maynard–Tao bounded-gaps theorem and the
  Ford–Green–Konyagin–Maynard–Tao large-gap theorem, and know which
  heuristic each one overruns;
- explain the parity barrier to a friend using semiprimes.

---

## 6.1 The race: π(x; q, a)

π(x; q, a) = #{p ≤ x : p ≡ a (mod q)}, gcd(a, q) = 1. Dirichlet (the
theorem you'd expect — arithmetic progressions with gcd 1 contain
infinitely many primes) has a quantitative face: π(x; q, a) ~
π(x)/φ(q). The classes *end* in a dead tie. But the approach is a
race with a notorious favorite:

**Chebyshev's bias (1853, observed):** π(x; 4, 3) > π(x; 4, 1) "always"
— 3 mod 4 primes lead essentially the entire way. Live, from
`src/phase6/prime_races.py` (default xmax = 1e7):

```
mod 4:  3 vs 1: leader = 3 mod 4, margin |D| = 218, flips = 1
        (first flip EXACTLY at x = 26,861)
mod 3:  2 vs 1: leader = 2 mod 3, margin |D| = 190, flips = 0
```

Read those two lines hard, because Gate 6 is built from them:

- **mod 4:** the first x where the 1-side takes the lead is **26,861** —
  a prime ≡ 1 mod 4, where π(x;4,1) first catches and passes. The lab
  *computes* it; rerun and believe it once with your own eyes.
- **mod 3:** the underdog never leads through **7·10⁸** — the lab's
  verified claim (rerun: `python3 src/phase6/prime_races.py 7e8`; it's
  the repo's verified fact). Gate 6 asks how many mod-3 lead changes
  exist there: **zero**. Littlewood says changes exist — *somewhere*.
  Finding the first is genuine open-ended exploration; the honest
  statement of Littlewood's promise is "infinitely often", with
  astronomically bad bounds on "when".

**Why the bias exists (the honest mechanism).** Same machinery as
Phase 5, per character: π(x; q, a) unfolds via the explicit formula
for L(s, χ) into x/φ(q)·1/ln x + waves − a **constant-ish correction**
−χ(a)·ln L(0, χ)/φ(q)·… Each class with χ(a) = −1 gets a standing boost
from the L(0,χ) offset; the leader in the 4-race (and 3-race) is exactly
the class where the nontrivial character is −1. Rubinstein–Sarnak (1994)
built the full probability theory: the lead sets have well-defined
densities, all > 1/2 for the boosted class (the 4-race 3-side density is
0.9958-ish — literature value; verify the *trend* with your own runs,
the value with your own citations).

**Try it — the gate-style "share" computation** (fraction of primes with
the leader actually in the lead at that moment). D(p) = π(p;4,3) −
π(p;4,1) evaluated right after p; over primes 5 ≤ p ≤ 10⁵ the fraction
of p with D(p) > 0 is **0.9989** — one flip at 26,861 barely dents a
cumulative leader. Gate 6 q02 runs the identical loop to 10⁶:

```python
import numpy as np
from common.primes import primes_upto
P = primes_upto(10**6); P = P[P >= 3]
D = np.cumsum(np.where(P % 4 == 3, 1, -1))
print((D[P >= 5] > 0).mean())        # your 1e6 share, 3 decimals
```

## 6.2 Consecutive primes refuse their own class (LS 2016)

Ask: of consecutive primes p, p' ≥ 5, what fraction lands (1,1) mod 3?
Fair-coin answer: 1/4. Real answer, two runs of the lab:

```
xmax = 1e5:   [[0.1997 0.2991]      xmax = 1e7:  [[0.2150 0.2848]
               [0.2992 0.2020]]                   [0.2848 0.2153]]
              rows/cols: 1 mod 3, 2 mod 3
```

The diagonal — same class twice — is **starved** by ~4–5 points, the
off-diagonal gorged. This is Lemke Oliver–Soundararajan (Annals 2016),
whose main term from the explicit formula *predicts* the deficit
proportionally to li(x)/x·(constant) — provably, unconditionally,
with the waves of Dirichlet L-functions doing the work (same cast as
§6.1, next scene: pairs instead of counts). The lab's own warning is
part of the theorem's texture: the deficit **wobbles** across x
(−0.041 at 1e6, −0.035 at 1e7 — the lab prints both). Gate 6 q03 asks
the (1,1) cell at 10⁶: run the lab at 1e6, read the table, round the
printed fraction — no one hands you that digit.

## 6.3 Admissible tuples: the rule that decides who may hope

A k-tuple H = (h₁,…,hₖ) of distinct integers is **admissible** iff for
every prime p it misses at least one residue class mod p — equivalently
(it hits ≤ p−1 classes mod p for every p ≤ k; beyond p > k there aren't
even k elements to cover p classes… precisely: p > k ⇒ at most k < p
classes hit automatically, so testing p ≤ len(H) is enough).

Why the definition exists: if H covers every class mod p, then *every*
translate n+H contains a multiple of p — infinitely-many-primes is
trivially dead. Admissibility is the *only* known local obstruction:

> **Hardy–Littlewood prime k-tuples conjecture.** Every admissible
> tuple has asymptotically  C(H)·x/lnᵏ x  translates n ≤ x with all
> n+hᵢ prime (C(H) a product-of-local-corrections constant).

Twin primes = the conjecture for (0,2). Green–Tao is the one theorem in
this neighborhood that's *proven* (Phase 7) — everything else is
conjecture or partial.

**Try it — three lines, gate-authority version:**

```python
def is_admissible(t):
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        p = int(p)
        if p > len(t): break
        if len({x % p for x in t}) == p:
            return False
    return True
```

Verified runs:

```
is_admissible((0,2,4))                    → False   # {0,2,1} mod 3: full
is_admissible((0,2,6))                    → True
is_admissible((0,4,10,12,18,20))          → False   # mod 3 classes {0,1,2}
```

The middle one says {n, n+2, n+6} (a prime triplet) is *allowed* by
every local obstruction; the last says that pretty-looking sextuplet is
doomed mod 3 forever. Counting classes mod p is also its own gate
question species ("how many DISTINCT residue classes mod 7 does tuple X
occupy" — one `len({x % 7 for x in t})`, but *understand* why p = 7 is
the last prime worth checking for a 6-tuple — it isn't: for a k-tuple,
p > k can't block; the interesting checks are the small p).

**Where admissibility becomes theorems (the 2013 revolution).**

- **GPY (2005):** admissible tuples + Bombieri–Vinogradov ⇒ infinitely
  often some n+H contains *many* primes (positive lower density of the
  "at least two" events for twin-type tuples).
- **Zhang (2013):** the first unconditional bounded gap: p_{n+1}−p_n <
  7·10⁷ infinitely often (tuples with two primes inside; Phase 7 quiz).
- **Maynard–Tao (2013) + Polymath8:** multidimensional sieve weights:
  for admissible H of size k ≫ m², some translate has ≥ m primes
  infinitely often. Consequences: gaps < 246 i.o. unconditionally, < 6
  assuming Elliott–Halberstam; m = 2 with clever admissible tuples *is*
  the twin-prime-shaped theorem, one admissibility check away… forever.

## 6.4 Gap records: what the Cramér model said, and what's true

Phase 3 established the record table below 10³ — rerun the scan, same
eight records ending (887, 20). Extending the scan is `gap_lab`'s one
liner; the *model* to fight with (Cramér, Phase 3): independent prime
"coin" at density 1/ln x ⇒ longest gap below x ≈ **ln² x**.
Verified anchor (Phase 3): record 180 at 1.7·10⁷ vs ln² = 286 —
records sit below the model. The model is *wrong*, provably:

> **Theorem (Ford–Green–Konyagin–Maynard–Tao, 2016, independently
> Maynard).** With g_n = p_{n+1}−p_n:
> ```
> limsup  g_n / ( ln p_n · ln₂ p_n · ln₄ p_n / (ln₃ p_n)² )  > 0.
> ```
> The factor ln₂·ln₄/(ln₃)² → ∞, so these gaps eventually exceed
> C·ln² p_n for every C — **the Cramér model's prediction for record
> gaps is beaten, infinitely often.** (Gate 6 q08: the model's name,
> lowercase: `cramer`.)

History of that inequality: Westzynthius (1931) proved limsup g_n/ln
p_n = ∞; Erdős–Rankin sharpened the multiplier for 85 years until the
2016 near-optimal form. The *upper* bound remains ln-territory:
known results pin g_n ≪ p_n^{0.525} (Baker–Harman–Pintz; RH would give
gaps ≪ √p·ln p — Phase 5's error term speaking through
π(x+h)−π(x)). Between the lower 2016 monster and the upper 0.525 sits
Cramér's conjecture g_n ≪ (ln p_n)² — a chasm this large is why "the
model" has a name and a status.

The elementary floor you can *construct* (exercise ★★2): for every m
there are m−1 consecutive composites (m!+2, …, m!+m), giving gaps
≫ ln x somewhere — Westzynthius's whole career started from the seed
of this observation.

**Record scanning, verified below 10³** (from Phase 3, re-embed):
records = (2,1), (3,2), (7,4), (23,6), (89,8), (113,14), (523,18),
(887,20) — the two largest sum to 38. Gate 6 q06 asks the same scan
below 10⁴: `gap_lab` extends the table; *you* report its sum. (Hint
that you're right: exactly three new records appear between 10³ and
10⁴ — the middle and last of them are the ones that matter.)

## 6.5 Twins: data, the Hardy–Littlewood constant, and Chen

Count twin pairs (p, p+2) with p+2 ≤ x, computed:

```
x = 10⁴:  205        x = 10⁵: 1224        x = 10⁶: 8169
```

Hardy–Littlewood prediction: 2C₂·∫₂ˣ dt/ln²t, C₂ =
∏_{p≥3} (1−1/(p−1)²) = **0.6601618…** (the twin prime constant — the
product over odd primes to 10⁶ reproduces 0.6601619; careful: p = 2 is
excluded and its "factor" would be 0, a trap the naive product falls
into). At 10⁶ the integral form
gives **8248** against truth **8169** — within 1%; the cruder
2C₂·x/ln²x shortcut gives 6917 (the integral-vs-shortcut gap is the
same lesson Phase 2 taught with Li vs x/ln x — *always* integrate).
(Gate 6's twin count at 10³ is the same loop, smaller: run it.)

**Chen's theorem (1966):** infinitely many p with p+2 prime *or a
product of two primes* (a "P₂"). The strongest sieve achievement in
this direction — and the reason it stops at P₂ is structural:

**The parity barrier.** A sieve counts by inclusion-exclusion with
weights over squarefree divisors — operations insensitive to whether
the *number* of prime factors is even or odd. Selberg's exhibit: there
exist sieve problems where a set of primes and a set of semiprimes
produce *identical sifted counts* at every stage. So no pure sieve can
ever certify "this sifted survivor is prime" — twins are out of reach
of sieve theory *alone*, provably. Chen's P₂ is the parity-respecting
ceilings made visible. Zhang (2013) *broke* parity not by smarter
sifting but by importing distribution results (Bombieri–Vinogradov,
pushed past its level for smooth moduli) — information *about* primes
that sieve weights can't see. Gate 6 q07: pick the option saying
"sieve methods alone cannot distinguish even vs odd numbers of prime
factors".

## 6.6 The zeta connection (why all of this is Phase 5 again)

Every claim above has the same engine: counts unfold into main term +
Σ_ρ waves over zeros of the relevant L-function (ζ for counts and
gaps-in-average, L(s,χ) for races and LS bias):

- races: race outcome = L(0,χ) offsets + Σ_ρ x^{ρ}/ρ·χ(ρ)-ish waves ⇒
  Littlewood flips = waves don't die (Phase 5 §5.6, verbatim);
- LS bias: pair-count correction = the same waves, one octave up;
- gaps: Cramér's model implicitly assumes *no structure* — FGKMT's
  long gaps are pure local sieve construction (covering congruences),
  and the *upper* bounds are where zero-free regions enter.

You already own the machinery; Phase 6 is its sociology.

---

## Lab / tooling map

- `src/phase6/prime_races.py [xmax]` — races + LS tables + figures.
  Run defaults (1e7) once, then 1e6 for the gate's LS cell, then 7e8
  once to watch mod-3 refuse to flip (it earns its runtime).
- `src/phase3/gap_lab.py` — record gap scan; pass larger xmax for q06.
- `common/primes.py::segmented_primes` — the streamer that makes 7e8
  cheap-ish; study how `race()` folds it into cumulative D.

## Exercises

★1. Rerun the lab to 1e7 and to 1e6. Report: first mod-4 flip; margin
   |D| at 1e6; the LS table at 1e6. (Gate rehearsal — three of its
   questions are these numbers.)
★2. Construct 6 consecutive composites below 100 without sieving —
   use the factorial trick. Generalize: prove gap ≫ ln x infinitely
   often (as x→∞ through n!).
★★3. The (0,2,6,8,12,18,26) constellation: diameter, admissibility
   verdict by hand (list classes mod 2, 3, 5, 7), and the code's
   verdict. (The literature's poster constellation differs from this
   one by a single entry — the check you're doing is the check the
   papers run.)
★★4. Compute distinct classes mod 7 for (0,4,10,12,18,20) and for
   (0,2,6,8,12,18,20); find which prime is the *last* one capable of
   killing each tuple and why primes beyond it are decoration.
★★5. D-share convergence: compute the fraction of primes p ≤ x (p ≥ 5)
   with D(p) > 0 for x = 10⁵, 10⁶, 10⁷ using the §6.1 loop. Describe
   the trend and reconcile it with "flips happen infinitely often" —
   a density can be 0.99…-adjacent while flips continue forever.
★★6. LS wobble: run the bias table at 1e5, 1e5·3, 1e6, 3e6 (lab args)
   and plot the (1,1) fraction vs xmax on log-x. Locate two local
   extrema and connect them to the lab's "deficit shakes" line.
★★7. Record scan to 10⁴ and to 10⁵: new record list (beyond Phase 3's
   table) and the p-values where they occur. Check Bertrand's bound
   (each record p_{next} < 2p) and Cramér's ln² yardstick: which
   records sit ABOVE ln² p — and why that's not a contradiction of
   §6.4's direction of failure.
★★8. Zhang-lite arithmetic: an admissible 50-tuple exists inside
   [0, 10⁶] with dense structure; *you* don't build it — instead:
   (a) write the predicate "translate n has ≥ 2 primes among n+H" and
   scan the first 10⁴ translates of (0,2,6,8,12) reporting every n
   that fires twice; (b) explain in one paragraph why the multidim
   Maynard weights beat a scan.
★★★9. Prove that admissibility is preserved by: (a) passing to a
   subset; (b) translation H + c; (c) dilation d·H for any nonzero
   integer d — including d divisible by primes. (If (c) surprises you,
   test it on (0,2)·2 and (0,2,6,8,12,18,20)·7 before the proof.)
★★★10. Parity barrier, hands: sift {n ≤ 30 : n ≡ 1 mod 2… free} by
   the primes {2,3}: compute the sifted sets and exhibit one number
   the sieve "wants prime" that is a semiprime — then explain, on this
   toy, why inclusion-exclusion weights (μ(d)) cannot tell p from p·q.

## Appendix — solutions

★1. Lab values (verified at writing): first mod-4 flip **26,861**;
   mod-4 margin at 1e7: |D| = 218, one flip only; mod-3: 0 flips,
   |D| = 190 at 1e7; LS table at 1e5: (1,1) 0.1997, (1,2) 0.2991,
   (2,1) 0.2992, (2,2) 0.2020; at 1e7: 0.2150/0.2848/0.2848/0.2153.
   (1e6 LS numbers: the lab's own printout is the authority — that's
   Gate 6 q03.)
★2. 7!+2,…,7!+6 = 5042,…,5046: five evens/multiples… (7!+2 even?
   7!+2 = 2(2521): composite; +3 divisible by 3; +4 by 2; +5 by 5; +6
   by 2·3 — six consecutive composites, though 5040+ > 100: use 4!:
   26, 27, 28 — 4!+2=26 (2·13), +3=27 (3³), +4=28 — three in a row.
   General: n!+2 … n!+n are n−1 composites; take x = n! ⇒ gap ≫ n ~
   ln x/ln ln x at x = n! — slightly below ln x raw; the classical
   cleanup uses lcm(1..n) ~ eⁿ (Phase 3's ψ!) to get ≫ ln x exactly.
★★3. Diameter 26; mod 2: all even — 1 class ≤ 1 ✓; mod 3:
   {0,2,0,2,0,0,2} → {0,2}: 2 ≤ 2 ✓; mod 5: {0,2,1,3,2,3,1} → 4
   classes ≤ 4 ✓; mod 7: {0,2,6,1,5,4,5} → 6 classes ≤ 6 ✓ ⇒
   admissible (code agrees: True). Conjecturally infinitely many
   all-prime translates. (And yes — the code's `break` at p > len(t)
   means p = 7 was the last real check for this 7-tuple.)
★★4. (0,4,10,12,18,20): mod 7 → {0,4,3,5,4,6} = **5** classes; the
   killer is p = 3 (all of {0,1,2}), which is ≤ len = 6, so the
   verdict is already in. (0,2,6,8,12,18,20): mod 7 → **6** classes,
   survives (6 ≤ 7−1? 6 classes means misses one ✓). Last relevant
   prime = largest p ≤ len(H); beyond it, k < p elements cannot cover
   p classes — the rest is decoration by pigeonhole.
★★5. Verified endpoints: share(10⁵) = 0.9989, share(10⁷) = 0.9995 —
   and the midpoint is NOT between them (run 10⁶ yourself; the gate
   lives there): share(10⁶) dips *below both*. Non-monotone: the
   26,861 flip drags the
   running mean down for millions of primes, then a long leader run
   pushes it back up. Reconciliation: flips occur infinitely often
   (the waves never die — §6.6/Phase 5), but the *time-share* of the
   underdog can stay tiny — Littlewood's flips are allowed to be
   thin. Density-one-adjacent lead and infinite flips are compatible;
   Rubinstein–Sarnak's positive-but-<1 densities are the refined
   statement, and your three data points are it in embryonic form.
★★6. Subjective plot; extrema land where an L-wave peaks (ln-periodic
   ~ every factor exp(2π/Im ρ_{χ}) for the relevant L-function's first
   zero — locate your two extrema's ratio and compare with that
   period; expect ±-ish agreement, the wobble is the same physics as
   Phase 5's Li-vs-π ringing).
★★7. Verified scan to 10⁵: new records beyond 10³ are 22 at p = 1129,
   34 at p = 1327, 36 at p = 9551 (that's the 10⁴ horizon — the two
   largest below 10⁴ are two lines of `sum(sorted(...)[-2:])` away,
   Gate 6 q06), then 44 at p = 15683, 52 at p = 19609, 72 at p =
   31397. Every record obeys p_next < 2p ✓ (Bertrand, Phase 3).
   Above-ln² check: ln²(1327) ≈ 52.8 > 34 — none of these early
   records exceed ln²; they cross the Cramér yardstick only
   sporadically much later, and §6.4's theorem says the crossing
   becomes *systematic* at scales beyond any computer. Direction
   matters: model overpredicts early, underpredicts in the far tail.
★★8. (a) Verified first fires of (0,2,6,8,12), n ≤ 20: n = 1 → 3
   primes {3,7,13}; n = 3 → 3; n = 5 → **all five** {5,7,11,13,17};
   n = 7 → 3 {7,13,19}; n = 11 → **all five again** {11,13,17,19,23}.
   n = 5 and 11 are the celebrated prime quintuplets — your scan just
   walked past the rarest small constellations. (b) Maynard's weights
   prove a *lower bound on a weighted count* — positive main term for
   every large x, hence some translate carries ≥ m primes forever;
   a scan certifies individual n below its horizon and says nothing
   about existence beyond it, and the proof's input (primes in APs
   with well-distributed moduli) is a theorem, not a table.
★★9. (a) #classes of a subset ≤ #classes of the set: |H' mod p| ≤
   |H mod p| ≤ p−1 ✓. (b) x ↦ x + c is a bijection mod p: class count
   exactly preserved ✓. (c) x ↦ dx is *any* map: the image of a set
   with m residue classes has ≤ m classes (collisions only shrink);
   ≤ p−1 survives even when p | d (then d·H ≡ {0} — one class). So all
   three operations preserve admissibility — (0,2)·2 = (0,4) and the
   constellation ·7 check out. (The converses all fail: dilation can
   create admissibility from inadmissible, e.g. (0,2,4)·3.)
★★★10. Sift {1,…,30} by 2,3: survivors = {1,5,7,11,13,17,19,23,25,29}
   — 25 = 5² and 1, plus primes: the sieve's μ-weights assign every
   survivor the same "primeness certificate" structure; 25 ≡ 1 mod
   {2,3}-sift is indistinguishable from 5 at that stage (same residue
   behavior against 2 and 3). Extending the argument forever requires
   knowing divisibility by 5 itself — which is exactly the parity
   theorem's toy: the weights count {p} and {p·q} with equal
   enthusiasm because μ only sees parity of factor-count, and it can't
   break the tie without an input that isn't sieve data.

## Gate-6 readiness map

| Gate 6 item | Covered by |
|---|---|
| first sign change of 4-race | §6.1 + lab (26,861) |
| mod-4 D-share at 1e6 | §6.1 code (verified 0.9989 @1e5 twin) |
| LS (1,1) cell at 1e6 | §6.2 + lab at 1e6 |
| (0,2,6,8,12,18,20) admissible? | §6.3 + ★★3 (True) |
| distinct classes mod 7 | §6.3 + ★★4 method |
| records <10⁴, sum of two largest | §6.4 + gap_lab |
| parity barrier MCQ | §6.5 |
| FGKMT beats which model | §6.4 (`cramer`) |
| tuple diameter | trivial arithmetic (`max−min`) |
| is_admissible code | §6.3 reference |
| twin pairs p+2 ≤ 1000 | §6.5 loop |
| mod-3 flips ≤ 7e8 | §6.1 lab fact (**0**) |

Next: the capstone — Phase 7 collects the theorems whose *proofs* you
still can't do, but whose *statements, scale, and machinery* you can
now evaluate like a referee.
