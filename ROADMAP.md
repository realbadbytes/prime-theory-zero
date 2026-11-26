# Roadmap — the whole path on one page

Assumed effort: ~8 h/week. Total: 18–30 months. Phases 0–3 alone (≈ 1 year)
already make everything non-exotic about primes understandable.

**Every row is a locked door.** Finish a phase → fill `answers/phase-N.py`
→ `python unlock.py grade N` at **100%** decrypts the next module (see
README "Progress gates"). No passing, no proceeding.

| # | Phase | ~Time | Core texts | Lab |
|---|-------|-------|-----------|-----|
| 0 | Proof literacy | 4–6 wk | Hammack, *Book of Proof* (free) | — |
| 1 | Elementary number theory | 3–5 mo | Silverman; MIT 18.781 notes (free) | `src/phase1/*` |
| 2 | Analysis light | 2–4 mo | Abbott (partial); Granville notes (free) | `src/phase2/euler_product_lab.py` |
| 3 | Prime distribution | 4–6 mo | Apostol ch. 1–4; Axler, *Prime Obsession* | `src/phase3/pnt_lab.py`, `gap_lab.py` |
| 4 | Complex analysis | 4–6 mo | Needham; Stein–Shakarchi | (mpmath zeros, phase-5 warm-up) |
| 5 | RH & explicit formula | 4–8 mo | Davenport; Montgomery–Vaughan | `src/phase5/explicit_formula.py` |
| 6 | Prime gaps | 3–5 mo | Granville's survey; Tao's 2013 posts | `src/phase6/prime_races.py` |
| 7 | Specialties | ongoing | by taste (spiral / AKS / Green–Tao) | yours to write |

## Milestones — what each exit unlocks

| Finished | You now own |
|---|---|
| 1 | Sieves, Miller–Rabin with provable base sets, CRT, quadratic reciprocity |
| 2 | The Euler product; derivation of pₙ ~ n ln n from PNT; Σ 1/p diverges |
| 3 | The PNT (statement + Chebyshev-level proof machinery); Li(x); gap records vs Cramér |
| 4 | Contours, residues, analytic continuation — "zero of ζ" is now a concrete object |
| 5 | The explicit formula: ψ(x) = x − Σ x^ρ/ρ − …; RH ⇔ error O(√x ln²x) |
| 6 | Cramér's model + its 2018 disproof at the limsup; parity barrier; Zhang–Maynard; LS bias theorem |
| 7 | A specialty: Ulam/Bateman–Horn, AKS, or the Green–Tao route |

## Honest warnings

- Phase 4 is where people stall. Budget it generously; do Needham for
  intuition and Stein–Shakarchi exercises for truth.
- Books marked free are free as of this writing; if a link rots, search the
  title + author — this field's good expositors keep their notes online.
- The labs are part of the curriculum, not demos: reproduce every printed
  number yourself before believing it (this repo has already caught one
  wrong "literature fact" that way — see phase 6).
