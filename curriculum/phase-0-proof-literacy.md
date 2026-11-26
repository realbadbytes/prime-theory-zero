# Phase 0 — Proof Literacy

**Budget: 4–6 weeks. No prerequisites beyond high-school algebra.**

Everything in this course is written in one language: proof. This phase is
not "math lite" — it is the single highest-leverage skill you will acquire.
Every later theorem you merely *read* now, you will *read* properly later,
and the difference is entirely this phase.

## Reading

- **Hammack, *Book of Proof*** — free PDF from the author's West Virginia
  University page. Chapters 1–6, 10–12. Exercises are non-optional.
- Alternative if you want more scaffolding: Velleman, *How to Prove It*.

## The five tools (with a taste of each)

**1. Direct proof.** "If n is odd, then n² is odd."
Proof: n odd means n = 2k+1 for some integer k. Then
n² = 4k² + 4k + 1 = 2(2k² + 2k) + 1, odd. ∎
Notice the shape: *unfold the definition, do algebra, refold into the target
definition.* Almost all early proofs look like this.

**2. Contrapositive.** "If n² is even, then n is even" is the same statement
as "if n is odd, then n² is odd" (tool 1). Proving P⇒Q by proving ¬Q⇒¬P is
often easier because the negation gives you a concrete object to use.

**3. Contradiction.** Assume the opposite and break reality. Euclid: suppose
primes were finite, list them all, consider N = (product of all) + 1 — any
prime dividing N divides the product too, so it divides 1. Reality broken;
primes are infinite. Learn when contradiction is load-bearing and when it is
cosmetic (here you can rewrite it directly: any prime factor of N is a prime
not on the list).

**4. Induction.** Prove P(1), prove P(k)⇒P(k+1), conclude ∀n. Example to do:
Σ_{i=1}^n i = n(n+1)/2. Strong induction: assume P(1..k) to prove P(k+1);
the Fundamental Theorem of Arithmetic (Phase 1) needs this version.

**5. Quantifiers.** ∀, ∃, their order, and their negations:
¬∀x∃y P(x,y) is ∃x∀y ¬P(x,y). Read statements out loud in English until
"for every ε > 0 there exists N such that for all n > N…" is a single
gestalt. This is 80% of why analysis feels like a foreign language; it is
vocabulary, not difficulty.

## Exercises (write full prose proofs; 1–4 must be flawless before leaving)

★1. Prove: the sum of two odd integers is even.
★2. Prove by contrapositive: if 3n + 2 is odd, then n is odd.
★3. Induction: 1 + 3 + 5 + … + (2n−1) = n².
★4. Negate, then prove: "for every integer n > 1 there is a prime p with
   p | n and p ≤ n."  (Hint: smallest divisor > 1; why must it be prime?)
★★5. Prove: √2 is irrational (contradiction + "choose the fraction in
   lowest terms" + parity chase).
★★6. A prime p > 2 is ≡ 1 or 3 mod 4. Prove p ≡ 1 or 3 (trivial) and find
   the first use of this fact ahead: which primes are sums of two squares?
   (Guess from data — compute — this is an experiment, not a proof.)
★★7. The doomed proof: find the error in "all horses are the same color."
   (Induction base/step subtlety; it's on Wikipedia, hunt it.)
★★★8. Prove: every integer n ≥ 2 is a product of primes (strong induction).
   Phase 1 will ask you to upgrade this to *uniqueness* — the real theorem.

## Coding habits to start now

- Keep a single notebook `notes.ipynb` (or `notes.py`). Every claim in every
  phase gets a check: `assert` statements on examples.
- Learn `pow(a, b, m)` now — modular exponentiation in one call, Python 3.

## The checkpoint protocol (how this course is gated)

Every phase ends at a **gate**: fill `answers/phase-N.py`, then

```bash
python unlock.py grade N
```

A **perfect 100%** decrypts the next phase's document into `curriculum/`;
anything less and it stays sealed in `vault/`, and gate N+1 refuses to run.
`python unlock.py status` shows where you stand. The gates are auto-graded
against ground truth computed fresh by the shared sieve — there are no
answer keys in this repo. (The vault is an educational lock, not real
security; see README.)

## When you're done

You can read a proof of √2-irrationality in a real book and tell *which*
line uses which tool, and you can write a direct proof that is boring,
formal, and correct. Boring and correct is the goal; cleverness comes after.

Then take the gate: read the prompts with `python unlock.py grade 0`,
fill `answers/phase-0.py`, and submit. Passing unlocks Phase 1.
Fun while you wait: `src/phase1/sieve_evolution.py` (labs are never gated).
