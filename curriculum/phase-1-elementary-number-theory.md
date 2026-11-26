# Phase 1 — Elementary Number Theory

**Budget: 3–5 months. Requires Phase 0. Everything is taught in this file +
the three labs in `src/phase1/` — external books appear once, at the end,
as optional dessert.**

This is the toolkit phase. Every object later phases manipulate — inverses,
orders, characters, convolutions — is built here, with proofs you can
reproduce. After this lesson you should be able to answer every Gate-1
question *without looking*, which is the same skill the gate will test with
different numbers than the ones worked here.

Run every code block. The labs (`python3 src/phase1/sieve_evolution.py`,
`primality_lab.py`, `congruences.py`) are the phase's laboratory — do them
while reading, not after.

---

## 1.1 Divisibility, Euclid's algorithm, and living in mod-m worlds

`a | b` means b = ac for some integer c. **gcd(a, b)** is the greatest
common divisor. Two facts from Phase 0 we use constantly: any d dividing
both a, b divides every combination ax + by; and composites have a prime
factor ≤ √n.

**The Euclidean algorithm.** gcd(a, b) = gcd(b, a mod b); descend to
b = 0. Example, the Fibonacci pattern the gate loves:

```python
import math
math.gcd(233, 144)      # 1  — consecutive Fibonacci numbers
math.gcd(610, 233)      # 1
```

Why is gcd(Fₙ₊₁, Fₙ) = 1 *always* (prove it: the algorithm's quotients are
all 1, and the last nonzero remainder descends to gcd(F₂, F₁) = gcd(1,1) =
1)? Consecutive Fibonaccis are the *worst case* of Euclid's algorithm —
maximum steps, and always coprime. Every "gcd of consecutive Fibonaccis"
question you will ever meet answers **1**.

**Bézout's identity.** The *extended* algorithm returns x, y with
ax + by = gcd(a, b). Run it by hand on the numbers the way the code does
(each line: divide, keep the remainder, back-substitute at the end):

```
2600 = 113·23 + 1        ← one step: 23 divides 2599 = 2600 − 1
so   1 = 2600 − 113·23
so   x = −113 is a coefficient:  23·(−113) ≡ 1  (mod 2600)
and  the positive inverse is  −113 + 2600 = 2487.
check: 23·2487 % 2600 == 1  ✓
```

```python
def egcd(a, b):
    """return (g, x, y) with a*x + b*y = g = gcd(a,b)"""
    old_r, r = a, b
    old_s, s = 1, 0
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_r, old_s, (old_r - old_s * a) // b if b else 0

def invmod(a, m):
    g, x, _ = egcd(a, m)
    assert g == 1, "inverse exists iff gcd(a, m) = 1"
    return x % m

invmod(23, 2600)         # 2487
```

**The modular inverse, in one sentence:** `a⁻¹ mod m` is the unique x in
[0, m) with ax ≡ 1 (mod m); it **exists exactly when gcd(a, m) = 1**; you
get it from Bézout (ax + my = 1 read mod m says ax ≡ 1). Python gives you
the fast path: `pow(a, -1, m)` does exactly this (3.8+). Gate questions
about inverses are this function with different numbers.

**Congruences.** a ≡ b (mod m) means m | (a − b). You may add, subtract,
multiply both sides freely; you may **divide only by invertibles** — i.e.
by c with gcd(c, m) = 1 (multiply both sides by c⁻¹ instead).
`Z/mZ` has m classes; the **units** (invertible classes) form a group
`(Z/mZ)*` under multiplication — group = set + associative operation +
identity + inverses; the *order* of the group is φ(m) (next section).

## 1.2 Euclid's lemma and the Fundamental Theorem of Arithmetic

**Euclid's lemma.** If p is prime and p | ab, then p | a or p | b.
*Proof.* Suppose p ∤ a. Then gcd(p, a) = 1, so Bézout gives px + ay = 1.
Multiply by b: pbx + aby = b. Now p divides both terms on the left
(obviously pbx; and aby since p | ab) ⇒ p | b. ∎ — one line, and it is the
hinge of all arithmetic.

**FTA.** Every n ≥ 2 is a product of primes, uniquely up to order.
*Existence:* Phase 0 exercise ★★★10 (strong induction).
*Uniqueness:* suppose n = p₁⋯pᵣ = q₁⋯qₛ. Then p₁ | q₁⋯qₛ, so by Euclid's
lemma p₁ = qⱼ for some j; cancel it and recurse on the shorter products.
∎ (The recursion is an induction on r + s — write it out fully once; it is
Phase 0's ladder with fresh rails.)

Where uniqueness fails you can *see* the failure mode: in
{1, 4, 6, 9, 10, …} ("numbers ≡ 1 mod 3"), "primes" are 4, 10, 22, 34, …
and 100 = 4·25 = 10·10 has two factorizations — Euclid's lemma breaks there
because the domain lacks the Bézout property. Unique factorization is not a
feature of "multiplication"; it's a feature of the *algorithm*. (Later
rings — like the integers of ℚ(√−5) where 6 = 2·3 = (1+√−5)(1−√−5) —
recycle this exact lesson. Keep it as a scar.)

## 1.3 The Chinese Remainder Theorem — a proof that is an algorithm

**Theorem.** If m₁, …, mᵣ are pairwise coprime, then as x runs over
Z/(m₁⋯mᵣ)Z, the tuple (x mod m₁, …, x mod mᵣ) runs over all tuples, each
once.

**Proof by construction.** Let M = m₁⋯mᵣ and Mᵢ = M/mᵢ. Since mᵢ is coprime
to Mᵢ, eᵢ = Mᵢ·(Mᵢ)⁻¹ (mod mᵢ) is ≡ 1 (mod mᵢ) and ≡ 0 (mod all other mⱼ)
(one line: mⱼ | Mᵢ). Then

```
x = a₁e₁ + a₂e₂ + ⋯ + aᵣeᵣ   satisfies  x ≡ aᵢ (mod mᵢ)  for every i.
```

Counting closes the bijection: the map is injective on equal-size finite
sets (two solutions differing by < M would vanish mod every mᵢ, hence mod
M by coprimality + Euclid's lemma applied repeatedly). ∎

**Worked example.** Solve x ≡ 2 (3), x ≡ 1 (5), x ≡ 6 (7).
M = 105. M₁ = 35, 35⁻¹ mod 3 = 2 (35 ≡ 2, 2·2 ≡ 1) ⇒ e₁ = 70.
M₂ = 21, 21⁻¹ mod 5 = 1 ⇒ e₂ = 21. M₃ = 15, 15⁻¹ mod 7 = 1 ⇒ e₃ = 15.
x = 2·70 + 1·21 + 6·15 = 140 + 21 + 90 = 251 ≡ **41** (mod 105).
Check: 41 % 3 = 2 ✓, 41 % 5 = 1 ✓, 41 % 7 = 6 ✓.

```python
def crt(rs, ms):
    M = math.prod(ms)
    return sum(r * invmod(M // m, m) * (M // m) for r, m in zip(rs, ms)) % M

crt([2, 1, 6], [3, 5, 7])     # 41
crt([1, 2, 3], [2, 3, 5])     # 23 — the "ancient Chinese" classic
```

Gate CRT questions are 3 small congruences; run the algorithm by hand once,
verify with the function, done.

## 1.4 Euler's φ — counting the units

**φ(n) = #{1 ≤ k ≤ n : gcd(k, n) = 1}.** Compute from the factorization
n = p₁^{a₁}⋯pᵣ^{aᵣ} by the **product formula**

```
φ(n) = n · ∏ᵢ (1 − 1/pᵢ).
```

*Why:* among 1..n the fraction divisible by pᵢ is 1/pᵢ, and the "avoid p₁
and avoid p₂ …" conditions are independent in the exact sense that
CRT makes them so (φ is *multiplicative*: φ(uv) = φ(u)φ(v) for gcd = 1 —
the bijection (Z/uv)* ≅ (Z/u)* × (Z/v)* is literally the CRT map).
For prime p: φ(p) = p − 1.

Worked: φ(240) = 240·(1−½)(1−⅓)(1−⅕) = 240·½·⅔·⅘ = **64**.
φ(91) = 91·(1−1/7)(1−1/13) = 91·6/7·12/13 = **72**.
Sanity pattern: φ is even for n ≥ 3 — think about why (k coprime ⇒ n−k
coprime, pairing k with n−k; the fun case is k = n/2).

```python
def phi(n):
    r, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            r -= r // p
            while m % p == 0: m //= p
        p += 1
    if m > 1: r -= r // m
    return r
```

Gate φ-questions are exactly this: factor (small primes first!), apply the
product, *check with the code*. A classic slip: forgetting a repeated
prime contributes once, not thrice — (1−1/p) appears once per *distinct*
prime.

## 1.5 Fermat, Euler, and reducing impossible exponents

**FLT.** p prime, p ∤ a ⇒ a^{p−1} ≡ 1 (mod p).
*Proof via the units.* (Z/p)* has p−1 elements. Multiply all of them by a
(mod p): you permute the set (a·x ≡ a·y ⇒ x ≡ y after multiplying by a⁻¹).
So ∏x ≡ ∏(ax) = a^{p−1}∏x; cancel ∏x (all invertible) ⇒ a^{p−1} ≡ 1. ∎
(Second proof worth doing as an exercise: binomial (a+1)^p ≡ a^p + 1,
because every middle binomial coefficient has p on top and nothing to
cancel it below; induct on a.)

**Euler's theorem.** gcd(a, m) = 1 ⇒ a^{φ(m)} ≡ 1 (mod m) — identical
proof inside (Z/m)*.

**The working skill — crushing huge exponents.** mod 13 (φ = 12):
7¹⁰⁰⁰ = 7^{12·83 + 4} = (7¹²)⁸³·7⁴ ≡ 1·2401 ≡ **9** (mod 13).
Always: reduce the *exponent* mod φ(m) first, then `pow(base, small, m)`.

```python
pow(3, 10, 11)    # 1   (FLT: exponent = 11−1)
pow(2, 12, 13)    # 1   (ditto)
pow(7, 1000, 13)  # 9   (reduced exponent 4)
pow(2, 1000, 15)  # 1?  Euler says a^φ(15)=a^8 ≡ 1 — check it, then ask
                  # why FLT alone does NOT apply (15 is not prime!)
```

Gate FLT questions test exactly this pattern: prime modulus + exponent
multiple of p−1 ⇒ answer **1** — and the *trap* versions where the modulus
is composite. Ask "is m prime?" before any theorem that starts "p prime".

## 1.6 Order, primitive roots — the *why* of repeating decimals

**ord_m(a)** = smallest d ≥ 1 with aᵈ ≡ 1 (mod m) (exists when gcd = 1;
by Euler it's ≤ φ(m)).

**Theorem.** ord_m(a) | φ(m); for prime p, ord_p(a) | p − 1.
*Proof (Lagrange, two lines).* The powers {1, a, a², …} form a subgroup of
(Z/m)* of size exactly d (first repeat closes the loop); a subgroup of a
finite group has size dividing the group's size — cosets partition, each
coset has d elements. ∎ (Writing *that* proof out is exercise ★★4; "list
the cosets, they partition, all have d elements" is the entire content.)

Order is *why* 1/7 = 0.142857 142857 … repeats every 6 digits: long
division has state (remainder), remainders live in (Z/7)*, period = the
order of 10 mod 7:

```
orders mod 7:  1:1  2:3  3:6  4:3  5:6  6:2   ← each divides 6 = 7−1
ord_7(10) = 6,  ord_11(10) = 2   (1/11 = 0.09 09 09…)
ord_97(10) = 96 = 97 − 1          ← 1/97 repeats for 96 digits!
```

A **primitive root** mod p is a g with ord_p(g) = p − 1 — a generator:
every nonzero class is a power of g. **Existence** (proof ★★5 in the
exercises — a genuine theorem, counting orders): the number of elements of
order exactly d in (Z/p)* is φ(d) (when d | p−1 — because *one* cyclic
subgroup of each size d exists, and a cyclic group of size d has φ(d)
generators). Total elements: Σ_{d | p−1} φ(d) = p−1, so at least one
element has order p−1. Then:

**Number of primitive roots mod p = φ(p − 1).**
*Reason:* with one generator g fixed, gᵏ has order (p−1)/gcd(k, p−1), so it
is itself a generator iff gcd(k, p−1) = 1 — exactly φ(p−1) choices of
k ∈ {1, …, p−1}. Worked: mod 31, φ(30) = **8** primitive roots; the lab
prints all orders for p = 7, 11, 13, 29, 97 — verify Σd | orders = p−1
there, and that 3 is a primitive root mod 31 (ord₃₁(3) = 30).

Gate primitive-root questions are always "how many?" = φ(p−1) with one
factorization step. Gate order questions: start at a, multiply mod p, stop
at 1 — or smarter: list divisors d of p−1, test a^d ≡ 1 for smallest
first. `pow(a, d, p)` makes both instant.

## 1.7 Quadratic residues, Legendre, reciprocity

Fix an odd prime p. a is a **quadratic residue (QR)** mod p if
x² ≡ a (mod p) is solvable (a ≢ 0). Among 1, …, p−1:

**Exactly (p−1)/2 classes are QR.** *Proof.* x² ≡ y² ⇔ (x−y)(x+y) ≡ 0 ⇔
y ≡ ±x (domain! — Euclid's lemma again). So each QR is hit by exactly two
of the p−1 nonzero inputs (x and −x; distinct since p odd). Count:
(p−1)/2 squares. Worked: mod 41 → **20**; mod 43 → 21. Squares mod 13:
{1², …, 6²} = {1, 4, 9, 3, 12, 10} = {1, 3, 4, 9, 10, 12}. ✓ 6 = (13−1)/2.

**Legendre symbol** (a/p) = +1 if QR, −1 if non-residue, 0 if p | a.

**Euler's criterion.** (a/p) ≡ a^{(p−1)/2} (mod p).
*Proof.* Let g be a primitive root, a ≡ gᵏ. Then a^{(p−1)/2} ≡
(g^{(p−1)/2})ᵏ ≡ (±1)ᵏ — and it is +1 exactly when k is even, which is
exactly when a = (g^{k/2})² is a square. ∎ (Check: the p−1/2 even-k powers
are precisely the squares.) Worked: 2 mod 13: 2⁶ = 64 ≡ 12 ≡ −1 → 2 is a
non-residue mod 13 ✓ (not in the square set above). 4⁶ ≡ 1 → QR ✓.

**Quadratic reciprocity.** For odd primes p ≠ q:

```
(p/q)(q/p) = (−1)^{ ((p−1)/2)·((q−1)/2) }
```

i.e. both symbols agree *unless* p ≡ q ≡ 3 (mod 4), where they oppose.
Supplementary law: **(2/p) = (−1)^{(p²−1)/8}** (+1 for p ≡ ±1 mod 8).

Worked, the full ritual:
- (83/101): both ≡ 3, 1 mod 4 → 83 ≡ 3 (mod 4), 101 ≡ 1 ⇒ agree. Direct:
  pow(83, 50, 101) = 100 ≡ −1, so (83/101) = −1, hence (101/83) = −1
  (sign exp ((82/2)(100/2)) = 41·50 even — consistent ✓).
- (29/53): 29 ≡ 1 (mod 4) ⇒ agree; pow(29, 26, 53) = 1 → both +1.
- (2/101) = −1 since 101 ≡ 5 (mod 8) — matches pow(2, 50, 101) = 100.

**Why you'll care.** Reciprocity turns "is a a square mod p" (hard-looking)
into "is p a square mod a" (small) + a sign — a *finite* Euclidean-style
descent. It's the first taste of the great theme: **a question mod p is
controlled by questions mod the other primes** — Phase 6's prime races and
Phase 5's L-functions are that sentence grown up. Gauss gave eight proofs;
Gauss's lemma proof (count lattice points under a line) is the most visual
— you'll meet its shadow in exercise ★★★7, and honestly the fastest way to
own reciprocity is Euler's-criterion computation + solving a few by hand.

Fermat's two-squares theorem (black box for now, you meet its proof in any
good book listed at the end, and its *flavor* in the lab): odd prime p =
x² + y² ⇔ p ≡ 1 (mod 4). That Phase-0 counterexample (7 fails) had its
reason waiting here: 7 ≡ 3 (mod 4).

## 1.8 Pseudoprimes, Carmichaels, Korselt — arithmetic's impostors

FLT's converse is **false**. 2047 = 23·89 and

```python
pow(2, 2046, 2047)      # 1  — 2047 passes the base-2 Fermat test, is composite
```

A composite passing a^{n−1} ≡ 1 for one base a is a **Fermat pseudoprime**
to base a. Passing for *every* base coprime to it is something worse:

**Carmichael number.** Composite n with a^{n−1} ≡ 1 (mod n) for all a with
gcd(a, n) = 1.

**Korselt's criterion (1912).** n is Carmichael ⇔ n is squarefree and
p − 1 | n − 1 for every prime p | n.
*Proof (⇒).* Fix p | n. (Z/p)* embeds (via CRT projection) — choose an
element b of order p−1 mod p, lift to a with a ≡ b (mod p), a ≡ 1 mod
other primes. Then p−1 = ord_p(b) | ord_n(a) | n−1 (last: Carmichael
property). Squarefreeness: if p² | n take a ≡ 1 + p mod p², ≡ 1 elsewhere;
a has order p mod p² — forcing p | n−1, contradicting p | n. (⇒ done;
⇐ is CRT + FLT in two lines.) ∎ (Full prose: exercise ★★★6.)

Worked verification on 1105 = 5·13·17 (squarefree; 4 | 1104, 12 | 1104,
16 | 1104 — all divide n − 1 ✓ ⇒ Carmichael; check:
`pow(2, 1104, 1105) == 1`). And 1729 = 7·13·19 — the Hardy–Ramanujan taxicab
*is also* a Carmichael number (6 | 1728, 12 | 1728, 18 | 1728).
The smallest Carmichael number: **don't take it from me** —
`primality_lab.py` finds it by exhaustive Fermat-search, and Korselt
verifies it; a search you run yourself is worth ten facts you copy.

## 1.9 Miller–Rabin — fixing Fermat, and why the fix works

**The theorem.** n odd prime, n − 1 = 2ʳd with d odd. For any a coprime to
n, the squaring chain a^d, a^{2d}, a^{4d}, …, a^{2ʳd} = a^{n−1} either
starts at 1 or **contains −1**.
*Proof.* In a field, x² = 1 has exactly two roots: (x−1)(x+1) = 0 ⇒
x = ±1. The chain ends at 1 (FLT). Walk back: the last non-1 entry squares
to 1, so it is −1. ∎ — "factor x² − 1 in a field" is the whole theorem.

A composite breaking the chain for base a is a **Miller–Rabin witness**:

```python
def mr_probable_prime(n, a):
    if n % 2 == 0: return n == 2
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    x = pow(a, d, n)
    if x in (1, n - 1): return True
    for _ in range(r - 1):
        x = x * x % n
        if x == n - 1: return True
    return False

mr_probable_prime(2047, 2)   # True  — base 2 fooled (chain: 1, 1)
mr_probable_prime(2047, 3)   # False — base 3 chain: 1565, 1013: breaks at −1? no.
```

Fermat liars are *square roots of 1 other than ±1* — which exist only in
non-fields (2047's chain base-2 is 1, 1: the impostor slipped through
because mod 23·89, "−1" exists in four flavors; the impostor used a mixed
one). Miller–Rabin tests the whole chain, so it catches them.

**Determinism facts you should own:** testing all bases a < 2·10¹² makes MR
unconditional for n < 3.3·10²⁴ (Classner et al. 2019: bases
{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37} for n < 2⁶⁴). For 32-bit n,
bases {2, 3, 5, 7} suffice. **The villain of the lab**, 3,215,031,751, is a
Carmichael number that fools base 2 (Fermat *and* MR-base-2!), and
primality_lab factors it live: **151 · 751 · 28351** — the lab's Pollard-rho
output is where Gate-1's "largest prime factor" lives.

**Pollard rho, ~12 lines** (birthday-paradox factoring; exercise ★★★8):
iterate x → x² + 1 mod n two walkers (tortoise/hare), gcd(|x − y|, n)
eventually leaks a factor:

```python
def pollard(n):
    x = y = 2; d = 1
    f = lambda v: (v * v + 1) % n
    while d == 1:
        x = f(x); y = f(f(y))
        d = math.gcd(abs(x - y), n)
    return d if d != n else pollard(n + 1)   # reroll c=1 sometimes fails

pollard(1000000007 * 1000000009)   # 1000000007 — instant
```

## 1.10 Arithmetic functions and one line of Möbius

φ (units), **τ(n)** (divisor count), **σ(n)** (divisor sum), and **μ(n)**:
μ(1) = 1; μ(n) = (−1)^k if n is a product of k distinct primes; 0 if a
square divides n. **Dirichlet convolution:**

```
(f * g)(n) = Σ_{d | n} f(d) · g(n/d).
```

Commutative, associative, identity ε (ε(1) = 1, ε(n>1) = 0). The one-line
engine of Phase 3:

**μ * 1 = ε.** Σ_{d|n} μ(d) = 1 if n = 1, else 0. *Proof:* n = p₁^{a₁}…;
only squarefree divisors survive; Σ_{k} (−1)^k C(r, k) = (1 − 1)^r = 0. ∎
Consequence (**Möbius inversion**): if g(n) = Σ_{d|n} f(d) then
f(n) = Σ_{d|n} μ(d) g(n/d). Memorize the pair; ψ(x) = Σ Λ(n) and every
"sum over divisors" trick in Phase 3 is this lever.

Also learn now: **Λ (von Mangoldt)** — Λ(n) = ln p if n = pᵏ, else 0 — it
looks arbitrary and becomes the protagonist in Phase 3.

## 1.11 Writing `is_prime` the way the gate checks it

Gate-1's function question tests *edge behavior*, not cleverness:

```python
def is_prime(n):
    if n < 2: return False          # 0, 1, negatives
    if n % 2 == 0: return n == 2    # the only even prime
    d = 3
    while d * d <= n:               # trial division to sqrt — Phase 0's lemma
        if n % d == 0: return False # squares die here: 9 → d=3
        d += 2
    return True

assert all(is_prime(p) for p in (2, 3, 5, 7, 7919))
assert not any(is_prime(x) for x in (1, 0, -7, 4, 9, 1681, 2047))
```

The checker runs your function against the shared sieve; the traps are
exactly: 1 (not prime), 2 (prime!), even numbers, squares, Carmichaels
(never trust Fermat tests alone inside your `is_prime` — or if you do, use
MR + a small-prime list). When the gate says "define a real function, not a
value," `answers/phase-1.py` must `def` it and put the *function object* in
`ANSWERS` (`"q12": is_prime`).

---

## Labs (do these while reading)

- `src/phase1/sieve_evolution.py` — trial division → classic → **segmented**
  sieve; you'll watch π(10⁶) = 78,498 come out of three increasingly clever
  machines. Read `Think about it:` blocks aloud.
- `src/phase1/primality_lab.py` — Fermat's failures (the Carmichael parade),
  Miller–Rabin rescue, the 3,215,031,751 case study (factored live).
- `src/phase1/congruences.py` — egcd / CRT / orders / primitive roots / QR
  tables, all exhaustively verified on small cases. Every worked example in
  this lesson has a bigger sibling here.

## Exercises

★1. Write Euclid's lemma + FTA uniqueness as full prose proofs (no gaps you
   can't fill by naming the theorem used on each line).
★2. Find 47⁻¹ mod 5280 by hand (extended Euclid — four quotient steps),
   then verify: `invmod(47, 5280)` = 4943.
★3. Solve x ≡ 3 (5), x ≡ 1 (7), x ≡ 6 (12) by hand with the eᵢ-construction.
   (Answer 78 mod 420 — then break it: what goes wrong if moduli are not
   pairwise coprime? Make your own failing example.)
★4. Prove Lagrange's theorem for (Z/p)* by the coset argument, then verify
   by computer that every order divides p−1 for p ≤ 97.
★5. Prove: if some g has order p−1 then the generators are the gᵏ with
   gcd(k, p−1) = 1; conclude #primitive roots = φ(p−1); compute for p = 31
   (8) and find all of them on the computer from g = 3.
★6. Prove Korselt's criterion in both directions (1.8's sketch has all the
   ideas; make them rigorous — the p²-division case is the sharp one).
   Then write a 6-line search over odd composites < 10⁴ checking Korselt;
   the *first* hit is a number Gate 1 will ask you for — but it will be
   asked with the same rule, not the same fact, so also prove why
   `pow(a, n-1, n) == 1` for all coprime a follows from your find.
★★7. Compute (101/83) *without* Euler: reduce by reciprocity + supplement
   to a question mod 83 → mod small → land on ±1; then check against
   `pow(101, 41, 83)`. Repeat for (2/101) and (−1/101); what does (−1/p)
   = +1 mean about √−1 mod p?
★★8. Implement Miller–Rabin with bases {2, 3, 5, 7} and factor
   1000000007·1000000009 with your own Pollard rho (from 1.9). Prove your
   factorization against `math.prod`.
★★9. Long division of 1/97 by hand for 20 digits; then `ord_97(10)` by
   code; then explain in one paragraph why the decimal period equals the
   order — where exactly do remainders "live" in (Z/97)*?
★★10. Count QRs mod 43 three ways: brute set-of-squares, (p−1)/2, and
   #\{a : pow(a, 21, 43) == 1\}. All 21? Now count mod 45 (composite!):
   why do all three answers *disagree*, and which definition survives?
★★★11. In (Z/7)*: list every element's order; verify Σ_{d|6} (#{order d}) =
   6 and that the multiset of orders {1, 2, 3, 3, 6, 6} matches
   {φ(1), φ(2), φ(3), φ(3), φ(6), φ(6)}. This "exactly φ(d) elements of
   order d" is the counting lemma of 1.6's existence proof — prove it.
★★★12. (Bridge to Phase 2) Prove Σ_{p≤x} 1/p diverges **knowing** Σ 1/n
   diverges and the Euler product (Phase 2 makes this airtight; here:
   guess the shape, check Σ_{p≤10⁶} 1/p ≈ 2.89 numerically, and write down
   why ln ln grows so slowly).

## Gate-1 readiness map

| gate question | skill (section) |
|---|---|
| q01 inverse mod m | 1.1 `invmod` — egcd by hand once, code verify |
| q02 3-congruence CRT | 1.3 eᵢ-construction + `crt` |
| q03 φ(n) | 1.4 factor → product formula → code-check |
| q04 ord_p(a) | 1.6 multiply-and-count or test divisors of p−1 |
| q05 #primitive roots of p | 1.6 = φ(p−1), one factorization |
| q06 #QRs in 1..p−1 | 1.7 (p−1)/2 — pairing proof |
| q07 Euler-criterion value | 1.7 `pow(a, (p-1)//2, p)` |
| q08 smallest Carmichael | 1.8 + lab search + Korselt-verify |
| q09 pow(2, p−1, p) pattern | 1.5 FLT = 1 (when p is prime!) |
| q10 gcd of consecutive Fibs | 1.1 always 1 (worst case of Euclid) |
| q11 largest prime factor of lab villain | 1.9 + `primality_lab.py` output |
| q12 `is_prime` function | 1.11 edge cases + hand the *function* to ANSWERS |

## Optional deeper reading (never required)

Silverman, *A Friendly Introduction to Number Theory* (exercise volume);
MIT OCW 18.781 (Sutherland) problem sets; Crandall & Pomerance ch. 1–3 for
the computational side. You pass Gate 1 without them; they make you faster
at everything after.
