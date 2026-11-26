# Phase 1 — Elementary Number Theory

**Budget: 3–5 months. Requires Phase 0. This is the toolkit phase: every
object you'll meet in later phases is built here with complete proofs.**

## Reading

- **Silverman, *A Friendly Introduction to Number Theory*** — first book;
  exercise-driven, friendly, rigorous enough.
- **MIT OCW 18.781 Number Theory (Sutherland)** — free notes + problem sets;
  switch to this as your spine when Silverman feels slow.
- **Crandall & Pomerance, *Prime Numbers: A Computational Perspective*** —
  keep open beside you all phase (and all course); chapters 1–3 match here.

## The lecture (definitions and theorems you must own)

**1. Divisibility.** a | b. Euclidean algorithm: gcd(a,b) via division
chain; **extended** version returns x, y with ax + by = gcd(a,b) — see
`src/phase1/congruences.py` for the algorithm you will prove correct.

**2. The Fundamental Theorem of Arithmetic.** Every n > 1 is a *unique*
product of primes. Existence was Phase-0 exercise 8. Uniqueness is the
famous Euclid's-lemma argument: if p | ab then p | a or p | b — prove it
from Bézout (ax + by = 1 case); the rest is an induction chase. *Write this
proof out in full. It is the first real theorem of the course.*

**3. Congruences.** a ≡ b (mod m) as m | (a−b); arithmetic of classes;
inverses exist iff gcd = 1 (again Bézout). (Z/m)* is a group of order φ(m) —
you now know enough group theory to say that; learn "group, order,
subgroup, coset" at definition level here.

**4. Fermat's little theorem.** p prime, p ∤ a ⇒ a^{p−1} ≡ 1 (mod p).
Proof via counting (Z/p)* or via the binomial trick (a+1)^p ≡ a^p + 1.
Then Euler's generalization with φ.

**5. Chinese Remainder Theorem.** Coprime moduli ⇒ classes combine
bijectively. The proof IS an algorithm; `congruences.py::crt` is that
algorithm. Solve Sun Tzu's 2/3/2 problem by hand first.

**6. Order, primitive roots.** ord_p(a) divides p−1 (Lagrange's theorem for
finite groups — a two-line proof you should do: multiply the subgroup by an
element, count). Primitive root = element of order p−1; existence for prime
p is a genuine theorem (count by orders) — and once one generator g exists,
the generators are exactly g^k with gcd(k, p−1) = 1, so there are **φ(p−1)**
of them (e.g. φ(28) = 12 primitive roots mod 29; the lab prints the count). The lab prints orders of every
element for p = 7, 11, 13, 29, 97 — check the divisors.

**7. Quadratic residues & reciprocity.** Which a are squares mod p? Exactly
(p−1)/2 of them (pair x, −x). Legendre symbol (a/p); Euler's criterion
(a/p) ≡ a^{(p−1)/2}; quadratic reciprocity: (p/q)(q/p) = (−1)^{((p−1)/2)((q−1)/2)}.
Gauss gave 8 proofs; you need one (Eisenstein's lattice-count proof is the
shortest; Silverman's is fine). The lab exhaustively verifies it for all
odd prime pairs < 50.

**8. Arithmetic functions (first taste).** φ, μ (Möbius), τ, σ. Dirichlet
convolution (f*g)(n) = Σ_{d|n} f(d)g(n/d); μ * 1 = ε is Möbius inversion
in one line — the trick you'll use daily in Phase 3.

## Exercises

★1. Prove Euclid's lemma and FTA (full prose).
★2. Compute 17^{-1} mod 3819 by hand (extended Euclid), verify vs the lab.
★3. Solve x ≡ 2 (3), x ≡ 3 (5), x ≡ 2 (7) by hand; then x ≡ a (m), b, n
   pattern-generalize.
★★4. Prove: n is prime ⇒ n | (a^n − a) for all a. Then find (by computer)
   the smallest composite with the same property (that's a Carmichael
   number; the lab prints them: verify 561 by hand with Korselt's
   criterion: squarefree and p−1 | n−1 for all p | n).
★★5. Prove: ord_p(a) | p−1. Find ord_101(10) by hand (the "1/101 has period
   4" surprise — check with long division).
★★6. Miller–Rabin: prove that for odd prime n, the squaring chain
   a^d, a^{2d}, …, a^{2^r d} must start at 1 or hit −1. (Factor
   x² − 1 = (x−1)(x+1) in a field — one line, whole theorem.)
★★7. (2026/2029) by reciprocity, fully reduced. Then find the first prime q
   with (2026/q) = −1 by computer, and verify x² ≡ 2026 (mod q) has no
   solution by brute force.
★★8. Write your own Miller–Rabin and beat the lab: factor 1000000007·1000000009
   with Pollard rho (implement rho yourself; ~10 lines).
★★★9. Convince yourself 1729 = 12³+1³ = 10³+9³ is also a Carmichael number
   (the lab says it is): verify Korselt for p ∈ {7, 13, 19}.

## Labs

- `src/phase1/sieve_evolution.py` — trial division → classic → segmented
  sieve; π(1e6) = 78,498 exact.
- `src/phase1/primality_lab.py` — Fermat fails (Carmichaels), Miller–Rabin
  saves the day; the 3,215,031,751 example shows why base sets matter
  (factored live: 151 · 751 · 28351).
- `src/phase1/congruences.py` — egcd/CRT/orders/primitive roots/QR, all
  exhaustively checked on small cases.

## When you're done

You can prove the theorems you use. When a later phase says "by CRT" or
"by reciprocity", you could reconstruct the argument. This is the difference
between knowing number theory and having read about it.
