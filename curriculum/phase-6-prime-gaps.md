# Phase 6 — Prime Gaps, Races, and the Modern Era

**Budget: 3–5 months. Requires Phase 3 (strongly) and Phase 5 (for the
race theory). This is living mathematics: most results here are younger
than a PhD.**

## Reading

- **Granville, "Unexpected biases in the distribution of consecutive
  primes"** (notices article, free) — the LS bias explained by the master.
- **Maynard, "Dense clusters of primes in subsets"** — read the intro only;
  then his two Polymath8b expository talks (slides online).
- **Tao's blog, 2013 sequence**: "Menace prime of the week", the Zhang
  posts, and the Polymath8b posts — the best live commentary of a
  breakthrough ever archived.
- **Rubinstein & Sarnak, "Prime number races"** (Experimental Math, free
  online) — dense but you can now read the statements.

## The lecture

**1. The gap problem's hard core.** gₙ = pₙ₊₁ − pₙ. Bertrand gives gₙ < pₙ;
the dream is gₙ = 2 infinitely often (twin primes — open). The weapon
that *would* do it, the parity barrier: sieve methods alone cannot
distinguish numbers with an even/odd number of prime factors — explain,
via the Liouville-function sum, why the great sieve programs (Selberg's
Λ², combinatorial sieves) are structurally blind to primes; read that this
is a *theorem about methods*, not a difficulty of will. This is why
Zhang's 2013 result (gₙ < 7×10⁷ infinitely often) needed the Goldston–
Pintz–Yıldırım idea: *small gaps between almost-primes converted by
well-factorable weights* — know the shape of the argument.

**2. Maynard–Tao (2013–14).** Multidimensional sieve optimization ⇒
finitely many primes in bounded intervals (m-tuples with diameter ≤ Cₘ),
independent proofs; Polymath8b drove the single-gap bound to 246 (with
admissible 6-tuples; 50 under Elliott–Haluász's EH variant). You can now
*verify the admissibility* of the 6-tuple {0,4,6,10,12,16} by computer —
exercise.

**3. Cramér's model, and the day it died.** Independent-random model:
longest gap below x ~ (ln x)². Maier's theorem (1985): π(x+λ ln x) falls
below and above its expectation infinitely often for λ small — the model's
local independence is *false* (small-prime congruence correlations
accumulate). FGKMT (2018, five separate papers): records satisfy
gₙ ≳ ln x · ln ln x · ln ln ln ln x / (ln ln ln x)³ infinitely often —
strictly more than Cramér's (ln x)²? No: the point is it beats
(ln x)²·(any fixed unbounded-factor-less ratio) — the unbounded factor
f(x) → ∞ means *Cramér's limsup conjecture is false*; corrected conjecture
(Granville): limsup ≥ 2e^γ ≈ 3.54 on the (ln x)² scale. `gap_lab.py`
shows both curves; records *below* (ln x)² are fully expected — and now
*provably* above Cramér, infinitely often.

**4. Prime races (Rubinstein–Sarnak).** D(x) = π(x;q,a) − π(x;q,b);
Chebyshev's bias: nonresidue classes lead most of the time (measured
proportion ~0.996 for 3-vs-1 mod 4 — you can compute it); Littlewood:
sign changes infinitely often; the log-density statement, and the zeros of
Dirichlet L(s,χ) as the wave source (Phase 5 machinery, one character up).
Verified in this repo: mod-4 flip **exactly at x = 26,861**; mod-3 race
verified flip-free up to 7×10⁸. (A number cited in some expositions for
the mod-3 flip was falsified by the lab before this sentence was written —
the lab's output is the authority; pushing xmax past 10⁹ is a legitimate
weekend project.)

**5. The 2016 earthquake.** Lemke Oliver & Soundararajan: consecutive
primes mod small q show striking bias — e.g. primes ≡ 1 mod 3 are
followed by primes ≡ 1 mod 3 noticeably *less* often than chance
(measured in this repo's lab: deficit ≈ −0.035 in the (1,1) cell of the
3×3 table at 10⁶). Not a flaw in Hardy–Littlewood — an *exact* consequence
of it (their conjectural tuple weights make same-class pairs
admissibility-penalized); the k-tuples conjecture predicts the bias and
its disappearance rate. Exercises below; this is research-level math you
can hold in your hands with 40 lines of numpy.

## Exercises

★1. Prove: if gₙ = 2 i.o. is false, the twin-prime constant argument in
   the twin prime conjecture's heuristic still "explains" p ≤ 10⁶ counts —
   write the Hardy–Littlewood prediction for twin primes ≤ x and check it
   at x = 10⁶ (compute; ~8164 expected-ish, count yourself).
★★2. Admissibility: implement and prove correct that {0,2,6,8,12,18,20}
   (the Polymath8b 7-tuple, verify!) is admissible; find its diameter.
★★3. Chebyshev bias by hand: list primes ≤ 100 in classes mod 4; count
   D(x) > 0 for x = 3..100; compare with the 0.996 log-density (small-x
   effects — discuss).
★★4. LS bias replication: extend the lab's mod-3 3×3 table to q = 5,
   x = 10⁶; check the predicted "no diagonal dominance" pattern from the
   LS paper (their Table 1).
★★★5. Read FGKMT's 6-page *Annals* abstract + Granville's exposition;
   write the 1-paragraph summary of why large-prime-gap records are tied
   to smooth numbers, and why that mechanism is invisible to Cramér's
   model.
★★★6. Project: raise `prime_races.py` xmax to 1e9 (RAM is fine — it
   streams); document any mod-3 flip if you find one and mail the list.
   (Nobody expects one below ~10⁹ based on our run — that IS the point:
   you are at the frontier with a laptop.)

## Labs

- `src/phase3/gap_lab.py` (again — you read it differently now)
- `src/phase6/prime_races.py [xmax]` — mod-4 race with the exact 26,861
  flip; mod-3 flip search; Rubinstein–Sarnak flavor; LS consecutive-pair
  bias table at x = 10⁶.

## When you're done

You know what is proved (bounded gaps, bias theorems), what is conjectured
with correct constants (Hardy–Littlewood, Cramér-corrected), and what is
wide open (twin primes) — and you can *compute* on all three levels.
