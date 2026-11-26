# Prime Theory Zero

**A self-contained path from "I don't really know math" to doing real prime
number theory — with code you run against the mathematics at every step.**

This repository is a complete curriculum: eight phases of material, each with
a compact lecture, an exercise set, and executable Python labs that make you
*fight the theorems with data* instead of just reading them. The destination
is concrete: by the end you will understand, reproduce, and extend the things
that usually stay magazine articles — the Prime Number Theorem, why pₙ ≈
n·ln n, Riemann's explicit formula (the primes as a superposition of waves at
the zeros of ζ), why the Riemann Hypothesis is "just" the tightest possible
error term, Cramér's model of prime gaps and the 2018 proof that it fails,
Zhang–Maynard–Tao bounded gaps, prime races, and the 2016 consecutive-prime
bias theorem.

## Who this is for

Someone who can write a few lines of Python, owns a calculator-grade intuition,
and has **not** written a formal proof. Everything else is built here, from
the definition of implication upward.

## Layout

```
unlock.py            the gate engine: status / grade / reset / music
curriculum/          ALL EIGHT guided lessons, public from day one
  phase-0-proof-literacy.md … phase-7-specialties.md
gates/               gate0.py … gate7.py — 12 auto-graded questions each
answers/             your answer sheets: fill phase-N.py, submit gate N
tools/               selftest.py (CI for the gate machinery itself)
ROADMAP.md           the whole path on one page, with time budget
src/                 runnable labs (developed on Python 3.14, any modern
                     3.x should do; never gated — they are your tools)
  common/primes.py   one tested segmented sieve shared by every lab
  phase1/            sieve evolution, primality testing, congruences lab
  phase2/            Euler product lab (Basel, Mertens, Σ 1/p)
  phase3/            PNT lab, prime-gap/Cramér lab
  phase5/            explicit formula: ψ(x) vs zeta-zero waves (mpmath)
  phase6/            prime races (mod 4 flip found exactly: 26,861) &
                     the Lemke Oliver–Soundararajan consecutive-prime bias
data/                figures and CSVs the labs write (git-ignored)
```

## Progress gates — the only way forward is through

Every lesson is public from day one — the model is
[ISLP_labs](https://github.com/intro-stat-learning/ISLP_labs): complete
guided theory, runnable examples, and exercises with solutions live in
this repo; no external textbook is required to pass any gate. What is
*gated* is your progress:

```bash
python3 unlock.py status          # the lockboard
python3 unlock.py grade 0         # prints the quiz & grades answers/phase-0.py
```

- Each gate = 12 auto-graded questions on that phase's theorems and data,
  including "write me a function" items tested against the shared sieve.
- **Gate N+1 refuses to run until gate N is passed at exactly 100%.**
  91.7% = not passed; fix `answers/phase-N.py` and resubmit freely.
- The report tells you *which* questions failed, never the right answers —
  the labs print those.
- **Ground truth is computed at grading time** from the same verified sieve
  the labs use (first race flip, record gaps, zeta zeros, …). There is no
  answer-key file anywhere in this repo.
- Passing all eight gates mints `CERTIFICATE.txt`.

Honest caveat: ground truth is computed on your machine and MCQ correct
values exist where the grader can see them, so a determined cheater can
extract every answer in ten lines of Python. The lock is social, not
cryptographic — what you would be cheating is the only part that was ever
for sale.

## Quickstart

```bash
python3 -m venv .venv && . .venv/bin/activate     # or any env you like
pip install -r requirements.txt
python3 unlock.py status                           # see the lockboard
less curriculum/phase-0-proof-literacy.md         # read Phase 0
python3 src/phase1/sieve_evolution.py              # labs are free to run
```

Every phase doc tells you which lab belongs to which week. Labs default to
small inputs and accept bigger ones (`python3 src/phase3/gap_lab.py 1e8`).

## Soundtrack

`unlock.py grade N` starts an ethereal 8-bit soundtrack for the gate trial
and plays a victory fanfare when you pass. There are no audio files in this
repo — the themes are **synthesized from the mathematics itself** (each
gate's key, tempo and melody come from the N-th prime and the digits of π),
pure stdlib, and playback talks to your sound card directly via
`ctypes`+libasound when no player like `mpv`/`paplay` is installed, so it
works even on a bare tty Linux box. Controls:

```bash
python3 unlock.py music status    # what's playing / available
python3 unlock.py music stop      # silence this trial
python3 unlock.py music off       # off for good (or: PTZ_MUSIC=0 one-off)
```

Prefer real music? Buy some (e.g. the *Wayward Souls* OST by Joey Grady,
joeygrady.bandcamp.com — that spooky-mathy chiptune is exactly this vibe)
and drop the files in `music/` (git-ignored): they replace the synth and
rotate per gate at prime indexes. Ship zero audio you don't license —
see `music/README.md`.

## The philosophy

1. **Every claim ships with a computation.** When a doc says "the Li(x)
   error wobbles", `phase3/pnt_lab.py` makes it wobble on your screen.
2. **Books are the spine, labs are the sense-check.** The reading list in
   each phase marks what is free and what is worth buying.
3. **You are not ready for a phase until its lab's `Think about it:` block
   answers itself in your sleep.**
4. **Compute, don't quote.** Labs print computed facts, never folklore —
   and when folklore disagreed with the computation (it happened; see the
   mod-3 race in phase 6), the computation won and the doc was corrected.
5. **You cannot skip ahead and pretend.** The gates grade against freshly
   computed ground truth; 100% or the next gate stays locked.

## Licenses

Code: MIT (`LICENSE`). Prose/curriculum: CC BY 4.0 (`CONTENT-LICENSE.md`).
