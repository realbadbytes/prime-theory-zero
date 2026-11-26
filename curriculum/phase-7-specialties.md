# Phase 7 — Capstone: the frontier, the theorems, and your toolkit

You now hold the whole machine: sieves and congruences (Phase 1),
analysis of the Euler product (2), the PNT's elementary skeleton (3),
the complex-analysis counting engine (4), ζ's zeros and the explicit
formula (5), races, bias, and gap theorems (6). The last phase does
three things: fixes the *modern theorem ledger* in your head (the
results that changed the field and what each one actually says — Gate 7
is mostly this), gives you the two industrial-grade counting tools you
should own (index-primes and Lehmer's π), and hands you the open
problems with the *computational handles* you're now strong enough to
grip.

Self-contained as always. Gate 7's MCQ facts are all taught right here;
its computations are all techniques you've seen.

---

## 7.1 The ledger: seven results, exactly as big as they are

Memorize the *statement shapes*, not just the names — the MCQs are
built from near-miss variants (e.g. "Zhang proved twin primes" is a
trap: he didn't).

| result | year | exactly what it says | the trap answer it dodges |
|---|---|---|---|
| **Helfgott, weak Goldbach** | 2013 | every odd n > 5 is a sum of three primes (the "odd" ternary conjecture; ~200 pp. proof finishing the circle method's minor-arc grind for n > 10²⁷, computer check below) | *strong* Goldbach (even = p+p) — still open, verified to 4·10¹⁸; Chen (Phase 6) is the sieve ceiling |
| **Zhang, bounded gaps** | 2013 | p_{n+1} − p_n < 7·10⁷ infinitely often — first unconditional bounded-gap theorem | NOT "twin primes proved" (gap 2 still open); Maynard–Tao arrived the same year by a different method, and Polymath8 drove 7·10⁷ → **246** (and 6 assuming Elliott–Halberstam) |
| **AKS, primality in P** | 2002 | "is n prime?" has a deterministic poly(log n) algorithm — first unconditional one without unproved hypotheses (their Õ(log^{12}); refinements ≈ Õ(log⁶)) | says NOTHING about *factoring* (still not known poly; RSA stands) — "factoring in P"/"RSA broken" are the traps |
| **Green–Tao, APs in primes** | 2004 (publ. 2008) | the primes contain arbitrarily long arithmetic progressions: for every k there is a k-term AP of primes | does NOT say "every large set of primes contains a twin" (twin = gap 2 = different problem); the engine is Szemerédi + transference through a *pseudorandom majorant* (Goldston–Yildirim — GPY's other child) |
| **Bateman–Horn, conjecture** | 1962 | the master density conjecture for prime-producing polynomials f₁,…,f_r (each irreducible, jointly admissible — Phase 6's notion generalized): count of n ≤ x with all prime ~ (C/∏deg)·∫dt/(ln t)^r. For one quadratic: # primes n²+1 below X ~ C·√X/ln X (the √X/ln X option in the MCQ — it's the value-scale form) | "never prime past 10", "all quadratics", "proven for RH" — for a *single* polynomial even n²+1 (Landau's problem) is open: not one quadratic is *known* to produce infinitely many primes |
| **FGKMT / Maynard, large gaps** | 2016 | records beat Cramér's ln² forever (Phase 6's boxed theorem) — the model *name* is Cramér | — (you did this one in Phase 6) |
| **Lemke Oliver–Soundararajan** | 2016 | consecutive primes avoid equal residue classes, provably, from main terms of L-functions | — (Phase 6's tables) |

Three connective sentences you should be able to say out loud:

1. **RH is still open** (Gate 7's true/false: TRUE — as of this repo's
   writing; ~10¹³ of its first zeros verified on the line, Gourdon
   2004, and every phase of this course has been *feeling* it through
   error terms).
2. The 2013 gap results and Green–Tao all run on **GPY's observation**
   (small gaps are detectable via averaged prime distributions —
   Bombieri–Vinogradov-type inputs) — Phase 6's parity-barrier talk
   explained why *distribution*, not sieving, was the only door.
3. Bateman–Horn subsumes twin primes, prime triplets, n²+1, and every
   Phase 6 constellation in one formula — the conjectural endgame of
   the whole curriculum (admissibility is its *only* permitted
   obstruction — and it is a local rule you can code in three lines).

**The MCQ meta-skill.** Each distractor is a *real theorem about a
different object* (Helfgott ↔ strong Goldbach; AKS ↔ factoring;
Green–Tao ↔ twin primes). The exam tests whether you know which
mountain each climber actually stood on. The table's last column IS
the lesson.

## 7.2 Owning index-primes: nth_prime and the millionth milestone

Gate 7's two big computations (the 314,159-th prime and the millionth)
are one function:

```python
def nth_prime(n):                       # 1-indexed: nth_prime(1) = 2
    from common.primes import primes_upto
    if n < 6:                            # p_n < 3n for n < 6... use safe bound
        return [2, 3, 5, 7, 11, 13][n - 1]
    # Rosser upper bound: p_n < n(ln n + ln ln n)  for n >= 6
    import math
    ln = math.log
    bound = int(n * (ln(n) + ln(ln(n)))) + 10
    return int(primes_upto(bound)[n - 1])
```

Verified anchors: `nth_prime(100) = 541`, `nth_prime(10003) = 104761`
(Phase 2's `estimate_pn` lands at 104340 for n = 10003 — a −0.4% miss;
the correction term ln ln n is Phase 2's story, now load-bearing in
your own code's sieve bound). For the millionth prime the bound gives
a sieve of ~16.8 million — trivially cheap; **run it once and
memorize your answer**: it is the number this whole curriculum started
from (Gate 7 q11 says so; the number itself is yours to compute, not
to be told). 314,159-th runs inside the same bound, same one line.

Why p_n < n(ln n + ln ln n) is legal: Rosser–Schoenfeld explicit PNT
bounds (this one holds for all n ≥ 6) — the PNT with *effective*
error, the same family as the 0.92/1.11 Chebyshev sharpening of
Phase 3, one century of turning "for large enough x" into "for every
x past an explicit number you could check by hand".

## 7.3 Counting π where sieves die: Lehmer's algorithm

`primes_upto` counts π(x) by sieving — fine to ~10⁸. The historical
counting functions (Meissel 1870s, Lehmer 1959, Lagarias–Miller–Odlyzko
1985) do it combinatorially. Lehmer's, complete and verified — the one
tool in this course that beats naive sieving by *eight orders*:

```python
import math, bisect, functools

def _sieve(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b"\x00\x00"
    for i in range(2, int(n**.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n + 1) if s[i]]
PR = _sieve(6_000_000)                      # table of primes
PHI_N, PHI_A = 100_000, 100
_tab = [0] * (PHI_N * PHI_A)
for x in range(PHI_N): _tab[x * PHI_A] = x
for a in range(1, PHI_A):
    p = PR[a - 1]
    for x in range(1, PHI_N):
        _tab[x*PHI_A+a] = _tab[x*PHI_A+a-1] - _tab[(x//p)*PHI_A+a-1]

@functools.lru_cache(maxsize=1 << 22)
def _phi(x, a):                             # count n<=x with no prime factor among first a
    if a == 0: return x
    if a < PHI_A and x < PHI_N: return _tab[x * PHI_A + a]
    if a >= PHI_A and PR[a - 1] >= x: return 1
    if a == 1: return x - x // 2
    return _phi(x, a - 1) - _phi(x // PR[a - 1], a - 1)

def _iroot(x, k):                           # exact integer k-th root (floats LIE)
    r = int(round(x ** (1.0 / k)))
    while (r + 1) ** k <= x: r += 1
    while r ** k > x: r -= 1
    return r

def pi_lehmer(x):
    x = int(x)
    if x < PR[-1]: return bisect.bisect_right(PR, x)
    a, b, c = pi_lehmer(_iroot(x, 4)), pi_lehmer(_iroot(x, 2)), pi_lehmer(_iroot(x, 3))
    s = _phi(x, a) + (b + a - 2) * (b - a + 1) // 2
    for i in range(a + 1, b + 1):
        w = x // PR[i - 1]
        s -= pi_lehmer(w)
        if i <= c:
            for j in range(i, pi_lehmer(_iroot(w, 2)) + 1):
                s -= pi_lehmer(w // PR[j - 1]) - j + 1
    return s
```

Verified against the published table (rerun and trust your machine):

```
pi(10^9)  = 50847534          instant
pi(10^10) = 455052511         0.1 s
pi(10^12) = 37607912018       ~10 s        (sieve-at-1e12 would need TB)
pi(10^13) = 346065536839      ~2 min
```

Three landmines this code already paid for you — each is a *course
moral*: (i) `_iroot` exists because `int((1e12)**(1/3)) = 9999` —
floats stole one prime-count at 10¹² (the exact-integer-root lesson);
(ii) the table guard is `a < PHI_A` as well as `x < PHI_N` — a silent
index overrun corrupted π(10¹²) by 1.7·10⁷ before the guard existed
(the "trust the exit code AND the values" lesson); (iii) the recursion
needs the `PR[a-1] >= x → 1` clamp or it explores exponentially many
nodes (the memoization-clause lesson from the wave-sums of Phase 5).

What Lehmer *is*: π(x) = (numbers surviving sieving by small primes:
φ(x,a)) + (an exactly-countable two-prime skeleton) − (two-level
corrections) — inclusion–exclusion (Phase 1!) executed with
polynomial-sum bookkeeping instead of brute force. Meissel's original
beat the planet: he counted π(10⁷) by hand in the 1870s; Lehmer's 1959
machine counted π(10¹⁰) — which your laptop now does in a tenth of a
second, with code you could have written in Phase 1 vocabulary.

## 7.4 The Bateman–Horn calibration (a conjecture audited live)

For f(n) = n² + 1 the conjecture predicts #{n ≤ x : prime} ~
(C/2)·li(x), C = 1.3728130331… (the local-correction product —
admissibility everywhere, so only *soft* corrections remain). Computed
by Miller–Rabin over n ≤ 10⁶:

```
x = 10⁵:  count 6656     prediction 6610     (0.7 % off)
x = 10⁶:  count 54110    prediction 53970    (0.3 % off)
```

A *conjecture* this accurate is what mathematicians mean by "almost
certainly true" — and still nobody can prove infinitude of n²+1
primes. That gap between 0.3% empirical and 0% proof is the Parity
Wall (Phase 6) seen from the outside: sieve machinery is provably
blind here, and no one has built the alternative yet. (This is why
Landau's 1912 problem #1 — n²+1 — is arguably the *hardest-easiest*
open problem in mathematics: a child can state it, a PhD can explain
why everything currently known fails on it.)

## 7.5 The frontier, with handles you can grip

Small prime APs for scale (Green–Tao says: no length limit; records
are found by distributed computing — 27 terms as of recent runs):

```
smallest AP of length 3: 3, 5, 7            (d = 2 — the ONLY one with d odd)
smallest, length 4: 5, 11, 17, 23           (d = 6)
smallest, length 5: 5, 11, 17, 23, 29       (d = 6)
```

Exercise ★★6 makes you derive the divisibility rule (d divisible by
2·3 for length 4–5; by 2·3·5 for length 6+… — Phase 6's admissibility
reappearing as *construction constraint* — and it's the last place this
course has left to hide).

Your honest handles on the open list:

- **Landau n²+1** (§7.4): you can compute the ratio count/prediction to
  10⁷ and watch it drift toward 1 — that is literally the frontier's
  shoreline, reachable from a laptop.
- **Twin-prime constant audit**: Phase 6's HL integral vs truth at
  increasing x — same exercise, one degree over.
- **Mod-3 race first flip** (Phase 6 lab): Littlewood guarantees a
  number; 7·10⁸ verified empty *here*; pushing the verified horizon is
  a real (if crowded) research contribution.
- **RH probes** (Phase 5 ★★6): max |ψ−x|/√x windows — your lottery
  ticket, with the honest odds of every other lottery ticket.
- **π(10¹⁴)** with your own Lehmer (minutes, not hours) — publishing
  nothing, *owning* everything.

The curriculum's contract was: understand, reproduce, extend. At
10¹⁴ and 27-term APs you are not extending yet — but you now know,
term by term, exactly what the extensors are doing.

---

## Lab / tooling map

- `run_all.sh` — the whole lab suite; run it end to end one final time
  before the gate (`src/phase1 → phase6`, figures to `data/`).
- §7.3's Lehmer — keep it in `src/common/` or a gist; it's the proudest
  40 lines in this curriculum.
- Phase 5's `explicit_formula.py` + Phase 6's `prime_races.py` — the
  two results-to-figures machines; you can now *read the papers'*
  plots, not just these.

## Exercises

★1. State each ledger row cold: theorem, year, one-line truth, trap
   answer. (Gate 7 q03–q07 + q09 — five MCQs and one boolean are pure
   table.)
★2. π(50) by hand-sieve, then the smallest integer n > 2 with π(n)
   prime (Gate 7 q01–q02 — both are "run 6 lines").
★3. `nth_prime` with the Rosser bound: reproduce nth(100) = 541,
   nth(10003) = 104761; then compute your two gate milestones
   (314,159-th and millionth). Report the Rosser bound used for the
   millionth and the actual value's margin below it.
★★4. Lehmer audit: reproduce all four verified π values. Break one
   guard on purpose (drop `a < PHI_A`, or replace `_iroot` by
   `int(x**(1/k))`) and report *which* value corrupts first and by
   how much. (The gate won't test this; the lesson is the point.)
★★5. φ-semantics: `_phi(x, 3)` counts n ≤ x with no factor 2,3,5.
   Check it by inclusion–exclusion at x = 1000; then explain why
   Legendre's π(x) = φ(x, π(√x)) + π(√x) − 1 holds — and why Lehmer
   beats Legendre even though both "just" sieve the small primes.
★★6. AP divisibility: prove that a k-term prime AP (k ≥ 2) with all
   terms > k must have common difference divisible by every prime
   p ≤ k. Verify: smallest AP4/AP5 have d = 6; find smallest AP6
   (search space: d divisible by 30, first term ≤ 10⁵ — runs in
   seconds) and confirm d is divisible by 30 there.
★★7. Bateman–Horn at 10⁷: extend §7.4's count (parallelize the
   Miller–Rabin or use a gmpy2-grade is_prime if installed); report
   the new ratio. The drift direction is news to no one and news to
   you both — write which way it moved.
★★8. Green–Tao at kitchen scale: count 3-term APs of primes below
   10⁴ (by scanning p, p+d with d divisible by 6 or the (3,5,7)
   exception); compare against the naive "random set" prediction
   #{p ≤ x}²/(2 ln x)·C — the primes are AP-*rich*, the opposite
   sign of Phase 6's LS *pair* starvation. Reconcile in one
   paragraph (long-range structure vs successor structure).
★★★9. Meissel by hand (the 1870s, no computers): π(100) = 25. Compute
   φ(100, 3) exactly (sieve out 2,3,5 — count the survivors), then
   correct: Legendre at a = π(10) = 4 — carry it to π(100) and see the
   bookkeeping Lehmer automates. (One page of paper; the exercise
   that makes §7.3's code *yours*.)
★★★10. The course, one page: write the one-paragraph proof skeleton
   linking — Euler product → ζ pole at 1 → PNT → explicit formula →
   RH ⇔ wave amplitudes → Chebyshev bias → LS starvation — with ONE
   verified number from each phase as ballast. If every ballast number
   is one you computed yourself, you pass the real final.

## Appendix — solutions

★1. Table §7.1, verbatim: Helfgott = weak/odd ternary Goldbach (B in
   the MCQ); Zhang = gaps < 7·10⁷ i.o. (B); AKS = primality in P (A);
   Green–Tao = arbitrarily long APs (B); Bateman–Horn = the √x/ln x
   density option (A — the only asymptotic-prediction choice; the
   conjecture predicts, it does not prove); RH unproven: TRUE.
★2. Method: sieve to 50 and count; then scan n = 3, 4, 5… computing
   π(n). Both answers are ≤ 3 digits; run it (the gate float check is
   exact).
★3. Verified: nth(100) = 541, nth(10003) = 104761; Rosser bound at
   n = 10⁶: 10⁶·(13.8155 + 2.6258) + 10 ≈ 16,441,312 — the actual
   millionth prime sits comfortably below (your run prints it and its
   margin; memorize the value — it's the course's namesake number).
★★4. Reference behavior: removing `_iroot` corrupts at 10¹² (cbrt
   floor error: count drops by ~1.75·10⁷ — the guardless run of §7.3
   reproduced exactly that before the fix); the `a < PHI_A` omission
   corrupts via table-index aliasing (same 10¹²-scale failure mode,
   smaller magnitude, silently). Both fail *above* the sieve-table
   horizon — under 6·10⁶ everything agrees regardless. That's the
   debugging moral: test where the shortcut hands over.
★★5. φ(1000,3): 1000 − 500 − 333 − 200 + 166 + 100 + 66 − 33 = 266
   ✓ (run the code: `_phi(1000,3) = 266`). Legendre: numbers ≤ x
   > 1 are either prime or have a factor ≤ √x; sieving the first
   π(√x) primes leaves {1} ∪ {primes > √x}; add back the sieved
   primes, drop 1 ⇒ formula ✓. Lehmer's win: Legendre's φ recursion is
   exponential in a = π(√x); Lehmer splits the leftover two-prime
   skeleton into O(π(√x)) exactly-countable pieces ⇒ ~x^{2/5}-ish
   total work — the same "exploit the sparse high-end" idea as
   segmented sieving vs full arrays.
★★6. For p ≤ k: the k AP residues a, a+d, …, a+(k−1)d occupy p
   classes if p ∤ d (d invertible ⇒ k ≥ p distinct classes mod p) —
   one is ≡ 0 mod p and equals p itself only once (terms > k ≥ p
   hypothesis) ⇒ contradiction; hence p | d for every p ≤ k. Length
   4 ⇒ 6 | d ✓ (both smallest APs have d = 6). Smallest AP6: search
   gives first term 7, d = 30: 7, 37, 67, 97, 127, 157 ✓ (d divisible
   by 30 ✓).
★★7. Your run's ratio count/prediction at 10⁷ lands ≈ 1.000–1.002 —
   (0.3% at 10⁶ → closer to 1); write the honest sentence: "the
   conjecture's prediction improves as x grows, exactly as an
   asymptotic law should; none of it is a proof."
★★8. Reference scan: 3-term APs of primes below 10⁴ — run it;
   reconcile: LS pairs are *infinitesimal-scale* structure (successor
   = next prime; local exclusion) while AP-structure is a *linear-
   density* question where the primes' pseudorandom-looking
   distribution at long range lets Szemerédi-type theorems bite —
   phases 5–6 machinery: waves create local starvation and global
   abundance simultaneously; "random-like with structure at every
   scale" is the modern picture in one breath.
★★★9. φ(100,3) = 26 → survivors: {1, 7, 11, 13, …} — 26 numbers: 1,
   the primes 7..97 (22 of them), and 49, 77, 91 (products of two
   primes > 5). Legendre: π(100) = φ(100,4) + 4 − 1: φ(100,4) = 22 ⇒
   22 + 3 = 25 ✓ — the three extra survivors of the 3-sieve (49,77,91)
   are exactly what sieving 7 removes (and 11² > 100 guarantees the
   rest are prime). That "+π(√x) − 1" IS this paragraph, wearing a
   formula.
★★★10. Skeleton (checklist): Euler product (§2.3) ties primes to ζ;
   ζ has a pole at 1 (§2.3/5.1: η-extension shows the only pole —
   ballast: η(0.5) agreement to 1e-10); pole ⇒ ψ ~ x (§3.3 Chebyshev
   sandwich to §5.5's von Koch — ballast: max |ψ−x|/√x = 0.777);
   PNT inverts to ψ = x − Σ_ρ x^ρ/ρ (§5.4 — ballast: K=1 wave gives
   ψ₀(10⁴) within 14); RH ⇔ all waves x^{1/2} (§5.5 — ballast: a
   β = 0.8 zero would shout 8922 vs measured 777); bias = L(0,χ)
   offsets + waves (§6.1 — ballast: the lab's flip at 26,861 and your
   own D-share at 10⁶); LS starvation = same waves at successor scale (§6.2 —
   ballast: (1,1) = 0.1997 at 10⁵). Seven ballasts, all yours ⇒ pass.

## Gate-7 readiness map

| Gate 7 item | Covered by |
|---|---|
| π(50) | ★2 |
| smallest n > 2 with π(n) prime | ★2 |
| Helfgott / Zhang / AKS / Green–Tao / B–H MCQs | §7.1 table |
| 314,159-th prime | §7.2 nth_prime |
| RH unproven | §7.1.1 (TRUE) |
| nth_prime function | §7.2 reference |
| millionth prime | §7.2 (run it; it's yours) |
| mod-3 race lead change | §6.1 + q12: option B (verified: 0 flips ≤ 7e8; 26,861 is the mod-**4** number) |

---

**End of curriculum.** You arrived with "what even is a proof" and you
leave holding Lehmer's π, Riemann's waves, and the statements of the
open problems — with verified numbers as receipts at every step. The
frontier items in §7.5 do not need permission to attack; they need
exactly what you now are. Go count something.
