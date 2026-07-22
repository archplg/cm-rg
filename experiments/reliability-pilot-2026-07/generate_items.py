#!/usr/bin/env python3
"""Generate 20 verifiable items with code-computed ground truth.

Freshly generated (not copied from benchmarks) -> no training-data leakage.
Answers: plain integer, reduced fraction a/b, or an English weekday name.
"""
import json
from datetime import date, timedelta
from fractions import Fraction
from itertools import product
from math import comb, factorial
from pathlib import Path


def v_p(n, p):
    """Exponent of prime p in n!."""
    e = 0
    q = p
    while q <= n:
        e += n // q
        q *= p
    return e


def trailing_zeros_base(n, base_factors):
    return min(v_p(n, p) // k for p, k in base_factors.items())


def derangements(n):
    d = [1, 0]
    for i in range(2, n + 1):
        d.append((i - 1) * (d[i - 1] + d[i - 2]))
    return d[n]


items = []


def add(qid, text, answer, fmt):
    items.append({"id": qid, "question": text, "answer": str(answer), "format": fmt})


# 1-2 factorial trailing zeros in odd bases
add("Q1", "How many trailing zeros does 87! have when written in base 12?",
    trailing_zeros_base(87, {2: 2, 3: 1}), "integer")
add("Q2", "How many trailing zeros does 60! have when written in base 15?",
    trailing_zeros_base(60, {3: 1, 5: 1}), "integer")

# 3-4 modular powers
add("Q3", "What are the last two digits of 3^123? Give the two-digit number.",
    f"{pow(3, 123, 100):02d}", "integer")
add("Q4", "What are the last two digits of 7^222? Give the two-digit number.",
    f"{pow(7, 222, 100):02d}", "integer")

# 5-6 calendar
d1 = date(2021, 3, 15) + timedelta(days=1000)
add("Q5", "March 15, 2021 was a Monday. What day of the week is exactly 1000 days after March 15, 2021?",
    d1.strftime("%A"), "weekday")
d2 = date(2026, 1, 1) - timedelta(days=777)
add("Q6", "January 1, 2026 is a Thursday. What day of the week was exactly 777 days before January 1, 2026?",
    d2.strftime("%A"), "weekday")

# 7 lattice paths avoiding a point
paths = comb(11, 5) - comb(5, 2) * comb(6, 3)
add("Q7", "On a grid, you walk from (0,0) to (6,5) moving only right or up, one unit per step. "
          "How many such paths do NOT pass through the point (3,2)?", paths, "integer")

# 8 partial derangement
add("Q8", "Seven letters are placed randomly into seven addressed envelopes, one letter per envelope. "
          "In how many arrangements does EXACTLY two letters end up in their correct envelopes?",
    comb(7, 2) * derangements(5), "integer")

# 9 inclusion-exclusion with exclusion
cnt = sum(1 for n in range(1, 1001) if (n % 3 == 0 or n % 5 == 0) and n % 7 != 0)
add("Q9", "How many integers from 1 to 1000 inclusive are divisible by 3 or 5, but NOT divisible by 7?",
    cnt, "integer")

# 10-11 dice probabilities (reduced fractions)
outcomes = list(product(range(1, 7), repeat=3))
p10 = Fraction(sum(1 for o in outcomes if sum(o) == 10), len(outcomes))
add("Q10", "Three fair six-sided dice are rolled. What is the probability that the sum is exactly 10? "
           "Answer as a reduced fraction.", f"{p10.numerator}/{p10.denominator}", "fraction")
two = list(product(range(1, 7), repeat=2))
primes = {2, 3, 5, 7, 11}
pp = Fraction(sum(1 for o in two if sum(o) in primes), len(two))
add("Q11", "Two fair six-sided dice are rolled. What is the probability that the sum is a prime number? "
           "Answer as a reduced fraction.", f"{pp.numerator}/{pp.denominator}", "fraction")

# 12 digit sum of a power
add("Q12", "What is the sum of the decimal digits of 2^40?",
    sum(int(c) for c in str(2 ** 40)), "integer")

# 13-14 clock angles (chosen to be integer degrees)
def clock_angle(h, m):
    a = abs((h % 12) * 30 + m * 0.5 - m * 6)
    a = min(a, 360 - a)
    assert a == int(a)
    return int(a)

add("Q13", "What is the angle in degrees between the hour and minute hands of a clock at 7:38? "
           "Give the smaller angle as a whole number.", clock_angle(7, 38), "integer")
add("Q14", "What is the angle in degrees between the hour and minute hands of a clock at 4:52? "
           "Give the smaller angle as a whole number.", clock_angle(4, 52), "integer")

# 15 base-9 palindromes divisible by 4
c = 0
for a in range(1, 9):
    for b in range(0, 9):
        n = a * 81 + b * 9 + a
        if n % 4 == 0:
            c += 1
add("Q15", "Consider all numbers that have exactly three digits when written in base 9 and are "
           "palindromes in base 9. How many of them are divisible by 4 (in ordinary decimal terms)?",
    c, "integer")

# 16 Fibonacci mod
fib = [0, 1]
for _ in range(30):
    fib.append(fib[-1] + fib[-2])
add("Q16", "Let F(1)=1, F(2)=1, F(n)=F(n-1)+F(n-2). What is the remainder when F(30) is divided by 9?",
    fib[30] % 9, "integer")

# 17 strictly increasing digits
add("Q17", "How many integers between 100 and 999 inclusive have strictly increasing digits "
           "(each digit larger than the one before)?", comb(9, 3), "integer")

# 18 full derangement
add("Q18", "Six people check their hats. In how many ways can the hats be returned so that "
           "NO person receives their own hat?", derangements(6), "integer")

# 19 smallest n with >= 30 trailing zeros
n = 1
while v_p(n, 5) < 30:
    n += 1
add("Q19", "What is the smallest positive integer n such that n! ends in at least 30 zeros "
           "(in ordinary base 10)?", n, "integer")

# 20 exactly two aces avoided -> use a cleaner one: committee with constraint
total = comb(10, 4) - comb(8, 2)  # committees of 4 from 10 where two specific people are not both in
add("Q20", "From 10 people, a committee of 4 is chosen. Two particular people, A and B, refuse to "
           "serve together. How many committees are possible?", total, "integer")

Path("items.json").write_text(json.dumps(items, indent=2), encoding="utf-8")
answers = {i["id"]: i["answer"] for i in items}
Path("answers.json").write_text(json.dumps(answers, indent=2), encoding="utf-8")
for i in items:
    print(i["id"], "->", i["answer"])
print(f"\n{len(items)} items written to items.json (answers in answers.json)")
