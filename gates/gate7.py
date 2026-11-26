"""GATE 7 — Capstone checkpoint (course final).

12 questions spanning everything; passing unlocks the certificate and
declares the course complete. Ground truth computed at grading time.
"""
PHASE = 7
NEXT_DOC = None
TITLE = "Gate 7 — Capstone"

FORMAT_NOTES = """
Some questions re-test Phase 1-6 skills under new names. Functions are
graded against the shared sieve.
"""


def questions():
    return [
        {"id": "q01", "prompt": "pi(50). (Integer.)"},
        {"id": "q02",
         "prompt": "Smallest integer n > 2 such that pi(n) is prime. "
                   "(Integer.)"},
        {"id": "q03",
         "prompt": "MCQ. Helfgott (2013) proved:\n"
                   "  A) the strong Goldbach conjecture\n"
                   "  B) the weak Goldbach conjecture (odd n > 5 is a sum "
                   "of three primes)\n"
                   "  C) bounded prime gaps\n"
                   "  D) RH for most zeros\n"
                   "Answer (letter)."},
        {"id": "q04",
         "prompt": "MCQ. Zhang (2013) proved:\n"
                   "  A) twin primes are infinite\n"
                   "  B) gaps p_{n+1}-p_n < 7*10^7 infinitely often\n"
                   "  C) primes contain 3-term APs\n"
                   "  D) Cramer's model is right\n"
                   "Answer (letter)."},
        {"id": "q05",
         "prompt": "MCQ. AKS (2002) proved:\n"
                   "  A) primality testing is in P\n"
                   "  B) factoring is in P\n"
                   "  C) RSA is breakable\n"
                   "  D) RH implies P=NP\n"
                   "Answer (letter)."},
        {"id": "q06",
         "prompt": "MCQ. Green and Tao (2004) proved:\n"
                   "  A) every large set of primes contains a twin\n"
                   "  B) the primes contain arbitrarily long arithmetic "
                   "progressions\n"
                   "  C) Dirichlet's theorem\n"
                   "  D) Bertrand's postulate for large x\n"
                   "Answer (letter)."},
        {"id": "q07",
         "prompt": "MCQ. Bateman-Horn predicts:\n"
                   "  A) #{n <= x : n^2+1 prime} ~ C * sqrt(x)/ln x\n"
                   "  B) n^2+1 is never prime for n > 10\n"
                   "  C) all quadratics produce infinitely many primes\n"
                   "  D) primes are equidistributed on Archimedean "
                   "spirals\n"
                   "Answer (letter)."},
        {"id": "q08",
         "prompt": "The 314,159-th prime number. (Integer.)"},
        {"id": "q09",
         "prompt": "True/false: the Riemann Hypothesis is (as of this "
                   "repo's writing) still UNPROVEN. (Boolean.)"},
        {"id": "q10",
         "prompt": "Define nth_prime(n): the n-th prime, n 1-indexed "
                   "(nth_prime(1)=2). (Function.)"},
        {"id": "q11",
         "prompt": "The 1,000,000-th prime -- the number this whole "
                   "curriculum started from. (Integer.)"},
        {"id": "q12",
         "prompt": "MCQ. In the mod-3 prime race, the first lead change "
                   "verified in THIS repo's runs:\n"
                   "  A) happens at 26,861\n"
                   "  B) was never found below 7*10^8\n"
                   "  C) happens at 561\n"
                   "  D) is impossible by Dirichlet\n"
                   "Answer (letter)."},
    ]


def _check_nth_prime(f):
    for n, want in [(1, 2), (2, 3), (10, 29), (100, 541), (500, 3571),
                    (1000, 7919)]:
        if int(f(n)) != want:
            return False
    return True


def keybook():
    from gate_common import nth_prime, pi
    return {
        "q01": ("int", pi(50)),
        "q02": ("int", next(n for n in range(3, 100)
                            if pi(n) in (2, 3, 5, 7, 11, 13, 17, 19))),
        "q03": ("str", "b"),
        "q04": ("str", "b"),
        "q05": ("str", "a"),
        "q06": ("str", "b"),
        "q07": ("str", "a"),
        "q08": ("int", nth_prime(314159)),
        "q09": ("bool", True),
        "q10": ("func", _check_nth_prime),
        "q11": ("int", nth_prime(10 ** 6)),
        "q12": ("str", "b"),
    }
