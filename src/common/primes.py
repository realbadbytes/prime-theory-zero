"""Shared prime-generation utilities for the course labs.

A single, tested implementation of the segmented Sieve of Eratosthenes,
used by every later phase so that labs never disagree about what the
primes are.

Approach: odd-only segmented sieve.
  * Segment i holds the odd numbers in [low, low + 2*segment_odds), one
    byte per candidate (numpy bool).
  * Only base primes p >= 3 mark candidates (2 is handled by sieving
    odds only).
  * Memory is bounded by ~segment_odds bytes regardless of how far we
    sieve; nothing proportional to n^2 is ever allocated.
"""

from __future__ import annotations

import math
import os

import numpy as np


def small_sieve(limit: int) -> np.ndarray:
    """All primes <= limit (small, non-segmented; used for base primes)."""
    s = np.ones(limit + 1, dtype=bool)
    if limit >= 0:
        s[0] = False
    if limit >= 1:
        s[1] = False
    for i in range(2, math.isqrt(limit) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.flatnonzero(s).astype(np.uint32)


def segmented_primes(limit: int, segment_odds: int = 1 << 21):
    """Yield uint32 arrays of primes, in increasing order, up to `limit`.

    The first array may start with 2 and 3; every array contains only
    primes, and concatenating them gives every prime <= limit.
    """
    if limit < 2:
        return
    if limit == 2:
        yield np.array([2], dtype=np.uint32)
        return
    base = small_sieve(math.isqrt(limit) + 1)
    base_py = [int(p) for p in base if int(p) >= 3]

    low = 3
    while low <= limit:
        high = low + 2 * segment_odds          # exclusive, odd
        seg = np.ones(segment_odds, dtype=bool)
        for p in base_py:
            if p * p >= high:
                break
            k = max((low + p - 1) // p, p)     # first odd multiple >= low
            if k % 2 == 0:
                k += 1
            start = (k * p - low) // 2
            seg[start::p] = False
        hi = min(high, limit + 1)
        count = (hi - low + 1) // 2            # odds in [low, min(high, limit+1))
        idx = np.flatnonzero(seg[:count])
        out = (low + 2 * idx).astype(np.uint32)
        if out.size:
            if low == 3:
                out = np.concatenate((np.array([2], dtype=np.uint32), out))
            yield out
        low = high


def primes_upto(limit: int, segment_odds: int = 1 << 21) -> np.ndarray:
    """All primes <= limit as one uint32 array."""
    return np.concatenate(list(segmented_primes(limit, segment_odds)))


def pi_at(x: np.ndarray, primes: np.ndarray) -> np.ndarray:
    """Prime-counting function pi(x) evaluated at sorted checkpoints x."""
    return np.searchsorted(primes, x, side="right")


def ensure_outdir(path: str = "data") -> str:
    """Labs write figures/CSVs into ./data relative to repo root."""
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "data")
    os.makedirs(root, exist_ok=True)
    return root
