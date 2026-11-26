# Phase 7 — Specialties and Open Problems

**Budget: ongoing. You are no longer a student of the subject; you are a
junior member of it. Pick ONE track, go deep for a year, and produce
something: a computation, a proof of a known theorem rewritten cleanly, a
paper-replication report, or a genuine experiment with a writeup.**

## Track A — Computational prime theory (lowest barrier, most fun)

- Replicate a paper's tables: the LS bias paper's Tables 1–3 (q ≤ 7, all
  congruence classes, x = 10⁷) — the machinery is `prime_races.py` scaled
  up with `numba` or plain C.
- Maximal prime gaps: reproduce the known record table up to your RAM
  allows; verify against the PrimePages / Oliveira e Silva records; write
  the segmented-sieve record hunt as a clean library.
- Zeros of ζ: implement the Riemann–Siegel Z-function; locate the first
  10⁶ zeros and check GUE pair-correlation statistics (Montgomery's law —
  compare against random-matrix eigenvalues; this experiment is a
  publishable-quality undergraduate project; the Odlyzko dataset gives you
  ground truth).
- Verify GRH-style claims in small ranges: zero-free region checks for
  L(s,χ), χ mod q ≤ 20, up to height 10⁴.

## Track B — Ulam spirals, primes-generating polynomials (the gateway drug)

- The 2026 arXiv preprint "Prime numbers on spiral trajectories" (search:
  *prime spiral trajectories* — the claim in that paper is testable by you;
  the lecture-notes route: any prime-generating quadratic's discriminant
  class-number story = Heegner/Stark; read Granville & Odlyzko-style
  expositions of why y²+x²+41 hits prime for x=0..39 (Euler) — class
  number one explains everything and Phase-5-you can *follow that argument*).
- Bateman–Horn conjecture: implement the heuristic prediction for primes
  of form n²+1 and compare at x = 10⁸ (the divergence of Σ 1/f(n) = "why
  we believe it" — prove that divergence for f = n²+1).

## Track C — Primes in P (complexity)

- AKS primality: read the original (it's readable after Phase 1!), implement
  the naive O(log^{12} n) version, then the Bernstein variant. Write a
  comparison vs ECPP intuition; this pairs perfectly with Phase 1's
  Miller–Rabin lab.
- Primes ∈ P was easy; the frontier is *deterministic* factoring and the
  number-field sieve records — replicate the linear-algebra stage of NFS
  on a 60-digit semiprime.

## Track D — Additive prime theory (hardest, most rewarding)

- Green–Tao road map: Szemerédi (read Tao–Vu ch. on it) ⇒ Green's theorem
  for APs in primes via transference. Realistic 12-month version: prove
  van der Waerden's theorem, then Roth's theorem (Fourier-analytic proof
  — your Phase 4 contours return in disguise), then read Green's "primes
  contain arbitrarily long APs" with a seminar of yourself.
- Goldbach: Hardy–Littlewood circle method (read Vaughan's monograph
  ch. 1–3); weak Goldbach is *theorem* — Helfgott 2013, a long
  computer-assisted proof that is a masterclass in honest explicit
  bounds; read its short arXiv announcement first.

## The open problems board (keep this list; update it yearly)

| Problem | Status | Your angle |
|---|---|---|
| Twin primes | open (gaps ≤ 246 i.o.) | parity barrier — Track A experiments on sieve limits |
| RH | open; 40%+ zeros on line | Track A zero computations |
| Cramér corrected constant | conjecture (Granville) | gap record hunts |
| Legendre (prime between squares) | open; Baker–Harman–Pintz gaps x^{0.525} | explicit-bound territory |
| Goldbach strong | open (weak ✓ Helfgott) | circle-method study |
| ∃∞ primes n²+1 | Bateman–Horn predicts | Track B replication |
| First mod-3 race flip | verified absent ≤ 7×10⁸ here | Track A weekend |

## How to keep growing

- Read one paper a month from the *prime* arXiv categories (math.NT,
  search "primes"); keep a replication log in this repo under
  `experiments/` — it becomes your portfolio.
- Monthly: rerun the whole `src/` suite against a fresh dataset; when a
  printed fact disagrees with the docs, **the computation wins and the doc
  gets corrected** — that discipline (used three times during the writing
  of this repo) is the only method that has ever worked.

Welcome to the field. The primes are still doing things nobody has proved;
you now have every tool required to be surprised usefully.
