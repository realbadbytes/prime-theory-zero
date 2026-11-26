"""GATE 0 — Proof Literacy checkpoint.

12 questions. 100% required to unlock Phase 1.
Strings are matched case-insensitively; match the format hints exactly.
Everything here is checkable by hand — this gate tests understanding,
not computation.
"""
PHASE = 0
NEXT_DOC = "phase-1-elementary-number-theory"
TITLE = "Gate 0 — Proof Literacy"

FORMAT_NOTES = """
Format rules for answers/phase-0.py ANSWERS dict:
  - exact integers as ints, strings exactly as cased in the prompt
    (comparison ignores surrounding case/whitespace, nothing else)
  - MCQ answers: the letter, e.g. "B"
"""


def questions():
    return [
        {"id": "q01",
         "prompt": "Sum 1+2+3+...+100. (Integer.)"},
        {"id": "q02",
         "prompt": "1+3+5+...+(2n-1) for n=37. (Integer — the odd-sum "
                   "identity from the phase doc.)"},
        {"id": "q03",
         "prompt": "MCQ. The CONTRAPOSITIVE of 'if n^2 is even then n is "
                   "even' is:\n"
                   "  A) if n is even then n^2 is even\n"
                   "  B) if n is not even then n^2 is not even\n"
                   "  C) if n^2 is not even then n is not even\n"
                   "  D) n^2 is even and n is odd\n"
                   "Answer (letter)."},
        {"id": "q04",
         "prompt": "MCQ. Negation of 'for every eps > 0 there exists N such "
                   "that for all n > N, |a_n - L| < eps':\n"
                   "  A) for every eps > 0 and every N, |a_n - L| >= eps\n"
                   "  B) there exists eps > 0 such that for every N there "
                   "exists n > N with |a_n - L| >= eps\n"
                   "  C) there exists eps > 0 such that for all n, "
                   "|a_n - L| >= eps\n"
                   "  D) for every eps > 0 there exists N such that for all "
                   "n > N, |a_n - L| > eps\n"
                   "Answer (letter)."},
        {"id": "q05",
         "prompt": "The proof that sqrt(2) is irrational assumes sqrt(2)=a/b "
                   "in lowest terms and derives that both are even. Name the "
                   "proof technique used. (One word, lowercase.)"},
        {"id": "q06",
         "prompt": "How many primes are <= 30? (Integer.)"},
        {"id": "q07",
         "prompt": "MCQ. In Euclid's infinitude-of-primes proof, N is "
                   "constructed as:\n"
                   "  A) the largest prime plus one\n"
                   "  B) the product of all primes plus one\n"
                   "  C) the sum of all primes plus one\n"
                   "  D) two to the power of the number of primes\n"
                   "Answer (letter)."},
        {"id": "q08",
         "prompt": "True/false: proving P(1), and proving P(k)=>P(k+1) for "
                   "all k>=1, suffices to prove P(n) for every integer "
                   "n >= 1. (Boolean True/False.)"},
        {"id": "q09",
         "prompt": "MCQ. Which proof technique is needed for the "
                   "existence half of the Fundamental Theorem of "
                   "Arithmetic (every n>=2 is a product of primes)?\n"
                   "  A) direct proof\n"
                   "  B) proof by contrapositive\n"
                   "  C) strong induction\n"
                   "  D) proof by contradiction\n"
                   "Answer (letter)."},
        {"id": "q10",
         "prompt": "How many integers n with 1 <= n <= 50 are divisible by "
                   "both 3 and 5? (Integer.)"},
        {"id": "q11",
         "prompt": "In the 'all horses are the same color' fake induction, "
                   "the two sub-herds must INTERSECT for the color-chain to "
                   "work. In which transition does that overlap vanish? "
                   "Answer exactly in the form 'k=1 to k=2' (or whichever "
                   "transition fails). HINT: P(1) itself is trivially true; "
                   "the argument looks fine for general k >= 2."},
        {"id": "q12",
         "prompt": "Consider the statement S: 'there exists a prime p such "
                   "that p is even'. Give the truth value of the NEGATION "
                   "of S. (Boolean True/False.)"},
    ]


def keybook():
    return {
        "q01": ("int", 5050),
        "q02": ("int", 37 * 37),
        "q03": ("str", "c"),
        "q04": ("str", "b"),
        "q05": ("str", "contradiction"),
        "q06": ("int", 10),
        "q07": ("str", "b"),
        "q08": ("bool", True),
        "q09": ("str", "c"),
        "q10": ("int", 50 // 15),          # 3
        "q11": ("str", "k=1 to k=2"),
        "q12": ("bool", False),            # negation of a true statement is false
    }
