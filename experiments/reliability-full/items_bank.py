#!/usr/bin/env python3
"""Parametric item bank with difficulty tiers for the full reliability
experiment. Every item is freshly generated from a seed and its ground truth
is computed by code - contamination-proof and regenerable.

Usage:
    python items_bank.py --seed 20260721 --tier-mix "1:5,2:10,3:15,4:15,5:5" --out items/

Tiers (calibrated after the pilot's double ceiling surprise - see
reliability-pilot-2026-07/DEVIATIONS.md):
  1  warm-up (pilot wave-1 level)            - expect near-ceiling for mid+
  2  pilot wave-2 level                      - cheap models start erring
  3  heavy arithmetic / multi-constraint     - target 30-70% for mid tier
  4  very heavy (8-digit products, long iterations, nested constraints)
  5  brutal (mainly to give flagships a non-ceiling region)

Escalation rule (pre-registered): if after the run the POOL-MEDIAN accuracy
exceeds 90%, regenerate tiers shifted up (2..6) with the same seed+1 and
re-run only the affected models. Never hand-tune single items after seeing
who failed them.
"""
import argparse
import json
import random
from fractions import Fraction
from itertools import product
from pathlib import Path


def collatz_steps(n):
    s = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        s += 1
    return s


def derangements(n):
    d = [1, 0]
    for i in range(2, n + 1):
        d.append((i - 1) * (d[i - 1] + d[i - 2]))
    return d[n]


def gen_mult(rng, digits_a, digits_b):
    a = rng.randint(10 ** (digits_a - 1), 10 ** digits_a - 1)
    b = rng.randint(10 ** (digits_b - 1), 10 ** digits_b - 1)
    return f"Compute exactly: {a} x {b}. Give the exact integer.", a * b


def gen_collatz(rng, lo, hi, min_steps):
    while True:
        n = rng.randint(lo, hi)
        s = collatz_steps(n)
        if s >= min_steps:
            return (f"Start from {n}. Repeatedly apply: if even divide by 2, if odd "
                    f"multiply by 3 and add 1. How many steps to reach 1?"), s


def gen_digitsum_power(rng, bases, lo, hi):
    b = rng.choice(bases)
    e = rng.randint(lo, hi)
    return f"What is the sum of the decimal digits of {b}^{e}?", sum(int(c) for c in str(b ** e))


def gen_substring(rng, limit):
    pat = str(rng.randint(11, 97))
    cnt = sum(1 for n in range(1, limit + 1) if pat in str(n))
    return (f'How many integers from 1 to {limit} inclusive contain the digit string '
            f'"{pat}" in their decimal representation?'), cnt


def gen_crt(rng):
    mods = rng.sample([7, 11, 13, 17, 19], 3)
    rems = [rng.randint(1, m - 1) for m in mods]
    n = 1
    while not all(n % m == r for m, r in zip(mods, rems)):
        n += 1
    return (f"What is the smallest positive integer leaving remainder {rems[0]} when divided "
            f"by {mods[0]}, remainder {rems[1]} when divided by {mods[1]}, and remainder "
            f"{rems[2]} when divided by {mods[2]}?"), n


def gen_strings(rng, length, letters, na):
    alph = "abc"
    cnt = sum(1 for s in product(alph, repeat=length)
              if all(s[i] != s[i + 1] for i in range(length - 1)) and s.count("a") == na)
    return (f'How many strings of length {length} over the alphabet {{a, b, c}} have no two '
            f'equal adjacent letters AND contain exactly {na} letters "a"?'), cnt


def gen_incl_excl(rng, limit):
    a, b, c = rng.sample([3, 5, 7, 11, 13], 3)
    cnt = sum(1 for n in range(1, limit + 1)
              if (n % a == 0 or n % b == 0) and n % c != 0)
    return (f"How many integers from 1 to {limit} inclusive are divisible by {a} or {b}, "
            f"but NOT divisible by {c}?"), cnt


def gen_partial_derangement(rng, n, k):
    from math import comb
    return (f"{n} letters are placed randomly into {n} addressed envelopes, one per envelope. "
            f"In how many arrangements do EXACTLY {k} letters end up in their correct "
            f"envelopes?"), comb(n, k) * derangements(n - k)


def gen_power_tail(rng):
    b = rng.choice([3, 7, 9, 13])
    e = rng.randint(200, 900)
    d = rng.choice([3, 4])
    return (f"What are the last {d} digits of {b}^{e}? Give them as a number "
            f"(may have leading zeros omitted)."), pow(b, e, 10 ** d)


def gen_iterated_digitmap(rng, start_digits, iters):
    n = rng.randint(10 ** (start_digits - 1), 10 ** start_digits - 1)
    x = n
    for _ in range(iters):
        x = x + sum(int(c) for c in str(x))
    return (f"Start with {n}. Repeat {iters} times: add the sum of the decimal digits of the "
            f"current number to itself. What number results?"), x


TIER_RECIPES = {
    1: [lambda r: gen_mult(r, 3, 3), lambda r: gen_strings(r, 5, "abc", 2),
        lambda r: gen_incl_excl(r, 1000), lambda r: gen_partial_derangement(r, 7, 2),
        lambda r: gen_crt(r)],
    2: [lambda r: gen_mult(r, 6, 6), lambda r: gen_collatz(r, 50, 150, 90),
        lambda r: gen_digitsum_power(r, [3, 7], 40, 60), lambda r: gen_substring(r, 2000),
        lambda r: gen_crt(r), lambda r: gen_strings(r, 7, "abc", 3)],
    3: [lambda r: gen_mult(r, 7, 7), lambda r: gen_collatz(r, 300, 900, 110),
        lambda r: gen_digitsum_power(r, [3, 7, 13], 60, 90), lambda r: gen_substring(r, 5000),
        lambda r: gen_incl_excl(r, 10000), lambda r: gen_iterated_digitmap(r, 3, 12),
        lambda r: gen_power_tail(r)],
    4: [lambda r: gen_mult(r, 8, 8), lambda r: gen_collatz(r, 1000, 6000, 130),
        lambda r: gen_digitsum_power(r, [7, 13], 90, 130), lambda r: gen_substring(r, 20000),
        lambda r: gen_iterated_digitmap(r, 4, 20), lambda r: gen_power_tail(r),
        lambda r: gen_strings(r, 9, "abc", 4)],
    5: [lambda r: gen_mult(r, 9, 9), lambda r: gen_collatz(r, 10000, 60000, 150),
        lambda r: gen_digitsum_power(r, [13, 17], 120, 160),
        lambda r: gen_iterated_digitmap(r, 5, 30), lambda r: gen_strings(r, 11, "abc", 5)],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--tier-mix", default="1:5,2:10,3:15,4:15,5:5")
    ap.add_argument("--out", default="items")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    mix = [(int(t), int(n)) for t, n in
           (part.split(":") for part in args.tier_mix.split(","))]
    items, k = [], 0
    for tier, n in mix:
        recipes = TIER_RECIPES[tier]
        for i in range(n):
            q, a = recipes[i % len(recipes)](rng)
            k += 1
            items.append({"id": f"I{k:03d}", "tier": tier, "question": q, "answer": str(a)})

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "items.json").write_text(json.dumps(
        [{k2: v for k2, v in it.items() if k2 != "answer"} for it in items], indent=2),
        encoding="utf-8")
    (out / "answers.json").write_text(json.dumps(
        {it["id"]: it["answer"] for it in items}, indent=2), encoding="utf-8")
    (out / "meta.json").write_text(json.dumps(
        {"seed": args.seed, "tier_mix": args.tier_mix, "n_items": len(items)}, indent=2),
        encoding="utf-8")
    print(f"{len(items)} items -> {out}/ (tiers: {args.tier_mix}, seed {args.seed})")


if __name__ == "__main__":
    main()
