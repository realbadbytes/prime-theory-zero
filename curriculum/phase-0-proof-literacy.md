# Phase 0 — Proof Literacy

**Budget: 4–6 weeks. Prerequisites: high-school algebra. Everything you need
is in this file and this repo — no external textbook is required (books are
listed at the end, strictly optional).**

Everything later in this course is written in one language: proof. This
phase teaches that language completely. It is not "math lite" — it is the
highest-leverage skill here. By the end you will have *written* proofs using
every technique Gate 0 can ask about, and the gate will feel like a formality.

**How to work this lesson.** Read one section. Run the code block (copy it
into a file or the REPL — don't just nod along). Do the exercises at the end
*before* looking at the solutions. When a claim is marked **Try it**, prove
it yourself on paper first, then check against the solution.

---

## 0.1 Statements, implication, and the three siblings

A theorem is usually an **implication**: `P ⇒ Q` ("if P then Q"). Four
statements orbit any pair P, Q:

| name | form | example (P = "n is odd", Q = "n² is odd") |
|---|---|---|
| implication | P ⇒ Q | odd n ⇒ odd n² — TRUE |
| converse | Q ⇒ P | odd n² ⇒ odd n — TRUE (lucky) |
| contrapositive | ¬Q ⇒ ¬P | even n² ⇒ even n — always same truth as implication |
| inverse | ¬P ⇒ ¬Q | even n ⇒ even n² — TRUE here (one-line direct proof), though inverse/converse truth is *never* guaranteed by the original's truth |

**The load-bearing fact:** a statement and its **contrapositive are
logically identical** — always the same truth value. The converse and the
inverse are identical to *each other*, and independent of the implication.

**Try it (this is a Gate-0 question type):** the contrapositive of
"if n² is even then n is even" is: swap and negate both — "if n is **not**
even then n² is **not** even". Say it in English: "if n is odd then n² is
odd". Notice that's the true implication from the table — so the original
is true too, and *one* proof covers both.

> **Common trap:** "converse of contrapositive of P ⇒ Q" — chase the
> letters, don't wing it. contrapositive(¬Q ⇒ ¬P) swaps back to P ⇒ Q.

## 0.2 Quantifiers: ∀, ∃, and how to destroy them

Two symbols and one rule run all of analysis.

- `∀x P(x)` — "for all x, P(x)". A **universal** claim.
- `∃x P(x)` — "there exists x with P(x)". An **existential** claim.

To **disprove** ∀x P(x): produce one x with ¬P(x) (a *counterexample*).
To **disprove** ∃x P(x): show ¬P(x) for every x (a *uniform argument*).

To **negate**, push the symbol through and flip it, right to left:

```
¬ [∀x ∃y P(x,y)]   ≡   ∃x ∀y ¬P(x,y)
```

Every ∀ becomes ∃, every ∃ becomes ∀, and the predicate flips. That's the
whole rule. **Order matters:** `∀x∃y` ("everyone loves someone") is NOT
`∃y∀x` ("someone is loved by everyone").

**Worked negation, slowly** (Gate-0's hardest question type):

> Negate: "for every ε > 0 there exists N such that for all n > N,
> |aₙ − L| < ε."

Flip each symbol as you pass it:

1. ¬∀ε>0 → **∃ε > 0 such that ¬…**
2. ¬∃N → **∀N, ¬…**
3. ¬∀n>N → **∃n > N with ¬…**
4. ¬(|aₙ − L| < ε) → **|aₙ − L| ≥ ε**  (note: `<` becomes `≥`, not `>`)

Result: *"there exists ε > 0 such that for every N there exists n > N with
|aₙ − L| ≥ ε."* That sentence means exactly "**the sequence does not
converge to L**" — which is what a negation must mean. Always sanity-check
the English like this.

**Try it:** negate "there exists a prime p such that p is even."
Push: "for every prime p, p is not even" i.e. "every prime is odd."
**Truth value:** the original is TRUE (p = 2), so the negation is
**FALSE**. When a gate asks for the truth value of a negation, decide the
truth of the original and flip — proving the negation directly is just
extra work you didn't need.

## 0.3 Direct proof — unfold, algebra, refold

The default technique. Template: *unfold the definition of the hypothesis,
do honest algebra, refold into the definition of the conclusion.*

**Theorem.** If n is odd, then n² is odd.
**Proof.** n odd means n = 2k + 1 for some integer k (unfold). Then
n² = 4k² + 4k + 1 = 2(2k² + 2k) + 1. Since 2k² + 2k is an integer, n² has
the form 2·(integer) + 1, i.e. odd (refold). ∎

Notice what made it a proof: the words "for some integer" and "is an
integer" did real work. Boring and correct is the goal.

**Theorem.** If n is even, then n² is even. **Proof.** n = 2k ⇒ n² =
4k² = 2(2k²), even. ∎ — and its converse, "n² even ⇒ n even", is *not*
directly provable this way (unfolding "n² even" gives you nothing to use).
That one wants the next tool.

## 0.4 Contrapositive — prove the twin instead

When the hypothesis gives you nothing but the negation would give you a
concrete object, prove the contrapositive.

**Theorem.** If 3n + 2 is odd, then n is odd.
**Proof (contrapositive).** We prove: if n is even, then 3n + 2 is even.
Let n = 2k. Then 3n + 2 = 6k + 2 = 2(3k + 1), even. Since the
contrapositive is true, the original is true. ∎

**Theorem** (the one from 0.3 that resisted). If n² is even, then n is even.
**Proof (contrapositive).** If n is odd, n = 2k+1, and n² = 2(2k²+2k) + 1
is odd (that exact computation was 0.3). ∎

## 0.5 Contradiction — assume the opposite and break reality

To prove P: assume ¬P and derive something impossible (0 = 1, or a specific
statement and its negation).

**Theorem (Euclid).** There are infinitely many primes.
**Proof.** Suppose not: finitely many, say p₁, …, pᵣ, and that's all of
them. Build **N = p₁p₂⋯pᵣ + 1** — the product of *all* primes, plus one.
N > 1, so N has some prime divisor p (every integer > 1 has one — see 0.7).
This p must be on our complete list. But p | N and p | p₁⋯pᵣ together force
p | (N − p₁⋯pᵣ) = 1. No prime divides 1. Reality broken; the primes are
infinite. ∎

Gate-0 asks *how N is constructed*: **product of all the primes, plus one**
— never "largest prime plus one" (that number can be composite and
divisible by smaller primes; the product is what makes *every* listed prime
leave remainder 1).

**Theorem.** √2 is irrational.
**Proof (contradiction).** Suppose √2 = a/b with integers a, b ≠ 0. **Choose
the fraction in lowest terms** (this choice is load-bearing — it's what
actually gets broken). Then a² = 2b².

1. a² = 2b² is even ⇒ a is even (by 0.4's theorem applied with n = a).
   Write a = 2c.
2. Substitute: 4c² = 2b² ⇒ b² = 2c² ⇒ b is even, same argument.
3. Both a and b even ⇒ a/b wasn't in lowest terms. Contradiction. ∎

Gate-0 asks you to *name the technique*: **contradiction**. When you can
rewrite the proof as contrapositive (like 0.4), contradiction is cosmetic;
here it's load-bearing — there's no direct route to "isn't a fraction."

## 0.6 Induction — the ladder, and the one rung that always bites

**Principle.** To prove ∀n ≥ 1: P(n), prove (a) **base case** P(1),
and (b) **inductive step**: for every k ≥ 1, P(k) ⇒ P(k+1). Then P(n) holds
for all n ≥ 1. (Gate-0 asks if that's true: **yes** — that is the principle
of induction, an axiom of the natural numbers, not a theorem.)

**Theorem (Gauss).** 1 + 2 + ⋯ + n = n(n+1)/2 for all n ≥ 1.
**Proof.** Base: 1 = 1·2/2. ✓
Step: assume 1 + ⋯ + k = k(k+1)/2 (the **inductive hypothesis**). Then
1 + 2 + ⋯ + k + (k+1) = k(k+1)/2 + (k+1)
= (k+1)(k/2 + 1) = (k+1)(k+2)/2. ✓
By induction, done. ∎

You never "prove the formula for a general n directly" — you prove the
*implication* using the hypothesis. That's the whole trick of the trade.
(The same sum, computed instantly: n terms each pairing to n+1 —
(1,n), (2,n−1), … — so total n(n+1)/2. Use the pairing to *guess*,
induction to *prove*.)

**Theorem.** 1 + 3 + 5 + ⋯ + (2n−1) = n².
**Proof.** Base: 1 = 1². Step: k² + (2k+1) = (k+1)². ∎ — one line each;
that's the size of the algebra you're aiming at.

**Strong induction.** Assume P(1), …, P(k) all at once to prove P(k+1).
Valid, and sometimes *necessary*:

**Theorem.** Every integer n ≥ 2 is a product of primes.
**Proof (strong induction on n).** Base: 2 is prime. Step: let n > 2 and
assume every 2 ≤ m < n is a product of primes. If n is prime, done.
Else n = ab with 2 ≤ a, b < n; by the strong hypothesis a and b are
products of primes, so concatenate their factorizations. ∎

Gate-0's question: the *existence* half of the Fundamental Theorem of
Arithmetic needs **strong induction** (ordinary induction at step k→k+1
gives you no handle on the factors a, b — you need *all* smaller cases).

**The doomed ladder (know this cold).** The "all horses are the same color"
fake proof: base P(1) trivially true; "step": take k+1 horses, drop one
(first k same color by hypothesis), drop a *different* one (last k same
color), and **chain the colors through the overlap** of the two sub-herds.
Where does it fail? The overlap needs both sub-herds to *share a horse*,
which requires k ≥ 2. At the transition **k = 1 → k = 2** the two herds are
{horse 1} and {horse 2} — disjoint, no chain. **The inductive step is false
for k = 1**, so the ladder never gets off the ground even though the base
case is true. Moral: the step must hold for *every* k ≥ 1, starting at the
first one. (This fake proof is folklore; you never needed to hunt it down —
now you own it.)

## 0.7 The divisibility toolbox (three lemmas carry the whole course)

Write `a | b` for "a divides b": b = ac for some integer c.

**Lemma 1 (linear combinations).** If d | a and d | b then d | (ax + by)
for all integers x, y.
*Proof.* a = dc₁, b = dc₂ ⇒ ax + by = d(c₁x + c₂y). ∎ — that's it; one
line that Euclid, CRT, and half of Phase 1 are built on. (You used it in
0.5: p | N and p | product ⇒ p | 1.)

**Lemma 2 (coprime version).** If gcd(a, b) = 1 and a | bc then a | c.
This is *Euclid's lemma*; it needs Bézout (there exist x, y with
ax + by = 1 — Phase 1 proves that from the extended Euclidean algorithm),
and it fails without coprimality: 6 | 2·3 but 6 ∤ 2 and 6 ∤ 3.

**Lemma 3 (the "both" trap).** "n divisible by a AND by b" ⇒ n divisible
by **lcm(a, b)** — not by a·b unless gcd(a, b) = 1. Examples: divisible by
both 4 and 6 ⇒ divisible by 12 (not 24: 12 itself is a counterexample to
the naive claim). Counting question pattern: *how many 1 ≤ n ≤ N are
divisible by both a and b?* — it's ⌊N / lcm(a,b)⌋.

**Worked example.** How many 1 ≤ n ≤ 60 are divisible by both 4 and 6?
lcm(4, 6) = 12; answer ⌊60/12⌋ = 5, namely 12, 24, 36, 48, 60. Counting
multiples of a single d: ⌊N/d⌋ — the *floor* is where off-by-one errors
live; always test the endpoints (is 60 counted? is 0?).

**Try it:** how many 1 ≤ n ≤ 100 are divisible by 3 or 5? (Inclusion–
exclusion: ⌊100/3⌋ + ⌊100/5⌋ − ⌊100/15⌋ = 33 + 20 − 6 = 47. The minus
sign is the "or" tax; "and" is the lcm.)

## 0.8 The hand sieve — meeting your first data set

**Definition.** A **prime** is an integer p ≥ 2 whose only positive
divisors are 1 and p. (1 is not prime — it would break unique
factorization; and "not prime" is exactly right for the one-divisor case.)

**Lemma.** If n is composite, it has a divisor d with 2 ≤ d ≤ √n.
*Proof.* n = ab with 2 ≤ a ≤ b ⇒ a² ≤ ab = n ⇒ a ≤ √n. ∎
So to test primality you only trial-divide by 2, 3, …, ⌊√n⌋. You'll
implement exactly this in Phase 1.

Sieve by hand (the real algorithm of Phase 1's first lab): write 2..30,
cross out multiples of 2 (from 4), of 3 (from 9), of 5 (from 25 — since
√30 < 6):

```
2  3  4  5  6  7  8  9  10 11
12 13 14 15 16 17 18 19 20 21
22 23 24 25 26 27 28 29 30

survivors: 2 3 5 7 11 13 17 19 23 29   — ten primes ≤ 30.
```

Verify with one line (never trust a hand sieve once code is closer):

```python
primes30 = [n for n in range(2, 31)
            if all(n % d for d in range(2, int(n**0.5) + 1))]
print(primes30, len(primes30))   # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] 10
```

Notice the pattern you'll use all course long: *hand-compute small, check
with code, trust neither when they disagree until you find who was wrong.*

## 0.9 Proving ∃, disproving ∀, and the counterexample muscle

- To prove `∃x P(x)`: **exhibit** one x and verify (constructive), or prove
  ¬∃ is impossible (nonconstructive — you've seen one: Euclid shows a prime
  off any finite list *without naming the next prime*).
- To disprove `∀x P(x)`: one explicit **counterexample**. "Every odd number
  ≥ 3 is prime" dies at 9.
- Negations of "∃" statements (0.2 again): "some prime is even" ⇄ its
  negation "every prime is odd" — exactly one of the pair can be true.

**Try it.** Two claims to work on. (a) Prove: every prime p > 3 is
≡ 1 or 5 (mod 6). (Every integer is 0–5 mod 6; classes 0, 2, 4 are even and
3 is divisible by 3 — four classes die, two remain.) (b) Disprove: "every
prime ≡ 1 (mod 6) is a sum of two squares." Candidates: 7 ≡ 1 (mod 6);
the sums of two squares ≤ 7 are 1, 2, 4, 5 — **7 is your counterexample**.
(The true statement is Fermat's: an odd prime is a sum of two squares iff
p ≡ 1 mod **4** — you'll earn it in Phase 1.) The muscle to practice here
is the loop itself: conjecture → test → die at a small number → refine.
That loop is the actual course; the theorems are its fossils.

## 0.10 Habits that pay for the whole course

- **Proof journal.** One file, `notes.md` (or `.py`). Every claim you read
  gets: your prose proof + an `assert`-checked example. If you can't write
  it boringly, you don't own it.
- **Compute next to prove.** Python 3 gives you `pow(a, b, m)` (modular
  exponentiation, exact, fast), `math.gcd`, integers that never overflow.
  Every experiment in this course starts there.
- **Say the English.** "For every ε there is an N…" out loud, until the
  quantifier sentences land as single thoughts. This is vocabulary, not
  difficulty — and it's 80% of why analysis later "feels hard."
- **Endpoints.** Off-by-one is the native enemy: floor/ceil, "for all
  n ≥ 1" vs n ≥ 0, strict vs non-strict inequality. Test n = 1. Test the
  boundary every single time.

---

## Exercises

Write full prose proofs first (in your journal), then check the solutions.
Do 1–6 flawlessly before the gate; 7–8 are the bridge to Phase 1.

★1. Prove: the sum of two odd integers is even.
★2. Prove by contrapositive: if 5n − 3 is even, then n is odd.
★3. Induction: 1 + 2 + ⋯ + n = n(n+1)/2 (the full ladder: base, hypothesis,
   step).
★4. Induction: 1 + 3 + 5 + ⋯ + (2n−1) = n², and use the identity to get the
   sum of the first 40 odd numbers without adding anything.
★5. Negate (symbolically *and* in English): "there exists N such that for
   all n > N, |aₙ| > 1000." Then negate: "every prime is odd."
★6. How many integers 1 ≤ n ≤ 120 are (a) divisible by both 6 and 8;
   (b) divisible by 6 or 8?
★★7. Prove √3 is irrational (the √2 proof adapts — but you need Lemma 2 or
   an "a² divisible by 3 ⇒ a divisible by 3" argument; do the parity-free
   version carefully).
★★8. Sieve by hand up to 50; count. Then verify with a one-liner. Next,
   disprove "for every n, n² + n + 41 is prime" with the smallest
   counterexample you can find (hint: the n that makes the quadratic
   obviously composite is hiding at the end of the run).
★★★9. The horses, part 2: fix the fake proof by strengthening the claim to
   "any k horses with k ≥ 2 are the same color"? Show exactly why the base
   case you'd now need (P(2)) is itself unprovable — locate the false
   sentence in the "step" for k = 2 → 3 as practice.
★★★10. Prove: every integer n ≥ 2 has a prime divisor (use 0.7's lemma or
   well-ordering), and prove the existence half of unique factorization by
   strong induction (uniqueness waits for Euclid's lemma in Phase 1).

## Solutions to the exercises

**★1.** Odd n = 2k+1, m = 2j+1 ⇒ n + m = 2(k + j + 1), and k + j + 1 is an
integer, so the sum is even. ∎ (unfold–algebra–refold, exactly 0.3's shape.)

**★2.** Contrapositive: "n even ⇒ 5n − 3 even"? No — careful: if n = 2k
then 5n − 3 = 10k − 3 = 2(5k − 2) + 1, which is **odd**. Recheck the
direction: the claim is "5n − 3 even ⇒ n odd"; its contrapositive is
"n even ⇒ 5n − 3 odd". Let n = 2k: 5n − 3 = 2(5k − 2) + 1, odd. ✓ Hence the
original holds. ∎ (If this felt backwards, reread 0.1: the contrapositive
of P⇒Q is ¬Q⇒¬P — negate *both* halves and swap.)

**★3.** Base: 1 = 1·2/2. Step: assume 1+⋯+k = k(k+1)/2. Then
1+⋯+k+(k+1) = k(k+1)/2 + (k+1) = (k²+k+2k+2)/2 = (k+1)(k+2)/2. ∎

**★4.** Base: 1 = 1². Step: k² + (2k+1) = k² + 2k + 1 = (k+1)². ∎
First 40 odds: 40² = **1600**.

**★5.** (a) "For every N there exists n > N with |aₙ| ≤ 1000" (flip ∀, flip
∃, flip `<`→`≥`-complement: `>` becomes `≤`). English: the sequence returns
below 1000 infinitely often — exactly the denial of "eventually above
1000." (b) "There exists a prime that is even" — which is *true* (p = 2),
so the original "every prime is odd" is false.

**★6.** (a) lcm(6, 8) = 24 ⇒ ⌊120/24⌋ = **5**. (b) ⌊120/6⌋ + ⌊120/8⌋ −
⌊120/24⌋ = 20 + 15 − 5 = **30**.

**★★7.** Suppose √3 = a/b in lowest terms. a² = 3b². Claim: 3 | a² ⇒ 3 | a.
Proof of claim: write a = 3q + r, r ∈ {0,1,2}; then a² ≡ r² ≡ 0 or 1
(mod 3), so 3 | a² forces r = 0. So a = 3c; then 9c² = 3b² ⇒ b² = 3c² ⇒
3 | b by the claim. Both divisible by 3 — not lowest terms. ∎ (Note what
changed from √2: the parity step was "a² even ⇒ a even"; here you had to
*earn* the analogous fact for 3. For 2 the parity argument was one line;
that's a preview of how the shape of a modulus controls the proof —
Phase 1's whole theme.)

**★★8.** Primes ≤ 50: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
47 — **15 of them**. (Cross out multiples of 2, 3, 5, 7 up to √50 ≈ 7.07 —
that's enough.) One-liner check:
`[n for n in range(2,51) if all(n%d for d in range(2,int(n**0.5)+1))]`.
Euler's polynomial dies at **n = 40**: 40² + 40 + 41 = 1681 = 41². It
cannot survive n = 41 either (41 divides all three terms there), and the
honest lesson is that any fixed quadratic is composite somewhere — the
*question* is how often it's prime, which becomes Phase 7's Bateman–Horn.

**★★9.** With the claim "any k ≥ 2 horses are the same color," the new
base case P(2) is *itself the false statement*: two randomly picked horses
need not match — no proof exists because it's false. For the step k = 2 → 3
the two sub-herds {h₁,h₂}, {h₂,h₃} **do** overlap (at h₂), so the chaining
sentence is true for this k — the reasoning is sound *conditionally*; it's
hypothesis P(2) that's false. Moral refined: every ladder has exactly one
weakest rung; moving it from the step to the base doesn't build the
building. (For k ≥ 2 the step is genuinely valid; recall from 0.6 that the
k = 1→2 rung was the original spot where the *step itself* was the lie.)

**★★★10.** (i) Let n ≥ 2 and consider the nonempty set S of divisors of n
that exceed 1 (n ∈ S). By well-ordering, S has a least element d. If d were
composite, d = ef with 1 < e < d; then e | d | n so e ∈ S, contradicting
minimality. So d is prime. (ii) Existence of factorizations: strong
induction exactly as in 0.6 (n prime: done; n = ab with 2 ≤ a, b < n:
combine the factorizations of a and b, which exist by the strong
hypothesis). ∎

## Gate-0 readiness map

| gate question | skills from |
|---|---|
| q01 (sum 1..100) | 0.6 (pairing + ladder); compute `n*(n+1)//2` |
| q02 (sum first n odds) | 0.6 (identity n²) |
| q03 (contrapositive MCQ) | 0.1 (swap-and-negate) |
| q04 (negate ∀∃∀ nested) | 0.2 worked example — flip symbols L→R, `<`→`≥` |
| q05 (√2 technique name) | 0.5 — "contradiction", lowercase |
| q06 (primes ≤ 30) | 0.8 (sieve + one-liner) |
| q07 (Euclid's N) | 0.5 — product of all primes + 1 |
| q08 (induction principle T/F) | 0.6 — True |
| q09 (FTA existence technique) | 0.6 strong induction |
| q10 ("divisible by both" count) | 0.7 Lemma 3 — lcm + floor |
| q11 (horses: failing transition) | 0.6 — k = 1 → 2, no herd overlap |
| q12 (truth value of ¬∃ statement) | 0.2 / 0.9 — flip the original's truth |

## Checkpoint protocol

Fill `answers/phase-0.py` (`ANSWERS = {"q01": …, "q02": …}`), then
`python3 unlock.py grade 0`. A **perfect 100%** passes the gate and opens
gate 1; anything less tells you *which* questions failed (never the right
answers). Ground truth is computed fresh by the shared sieve — there is no
answer key in this repo. `python3 unlock.py status` shows the lockboard;
all lessons stay public regardless. (A soundtrack starts for the trial if
you like company — `unlock.py music off` if you don't.)

## Optional deeper reading (never required)

Hammack, *Book of Proof* (free PDF) ch. 1–6, 10–12, for extra exercise
volume; Velleman, *How to Prove It* if you want even more scaffolding. You
have passed nothing here by owning these books, and you pass the gate
without opening them.
