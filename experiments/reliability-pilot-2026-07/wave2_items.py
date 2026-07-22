#!/usr/bin/env python3
"""Wave 2 (exploratory): substantially harder verifiable items, ground truth by code."""
import json
from itertools import product
from pathlib import Path

items = []


def add(qid, text, answer):
    items.append({"id": qid, "question": text, "answer": str(answer)})


# W1 exact long multiplication
add("W1", "Compute exactly: 847361 x 592483. Give the exact integer.", 847361 * 592483)

# W2 Collatz steps
def collatz_steps(n):
    s = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        s += 1
    return s

add("W2", "Start from 97. Repeatedly apply: if the number is even divide it by 2, if odd multiply "
          "by 3 and add 1. How many steps does it take to reach 1 for the first time?",
    collatz_steps(97))

# W3 digit sum of 3^50
add("W3", "What is the sum of the decimal digits of 3^50?", sum(int(c) for c in str(3 ** 50)))

# W4 substring count
cnt = sum(1 for n in range(1, 2001) if "13" in str(n))
add("W4", 'How many integers from 1 to 2000 inclusive contain the digit string "13" in their '
          "decimal representation (like 13, 138, 213, 1305)?", cnt)

# W5 circular adjacency
def w5():
    from itertools import permutations
    people = "ABCDEF"
    total = 0
    for perm in permutations(people):
        ok = True
        for i in range(6):
            a, b = perm[i], perm[(i + 1) % 6]
            if {a, b} == {"A", "B"} or {a, b} == {"C", "D"}:
                ok = False
                break
        if ok:
            total += 1
    return total

add("W5", "Six people A, B, C, D, E, F sit at a round table with 6 labeled seats (seatings that "
          "differ by rotation count as different). A refuses to sit next to B, and C refuses to "
          "sit next to D. How many seatings are possible?", w5())

# W6 constrained strings
def w6():
    total = 0
    for s in product("abc", repeat=5):
        if all(s[i] != s[i + 1] for i in range(4)) and s.count("a") == 2:
            total += 1
    return total

add("W6", 'How many strings of length 5 over the alphabet {a, b, c} have no two equal adjacent '
          'letters AND contain exactly two letters "a"?', w6())

# W7 CRT
def w7():
    n = 1
    while True:
        if n % 7 == 3 and n % 11 == 4 and n % 13 == 5:
            return n
        n += 1

add("W7", "What is the smallest positive integer that leaves remainder 3 when divided by 7, "
          "remainder 4 when divided by 11, and remainder 5 when divided by 13?", w7())

# W8 sum of all-odd-digit 3-digit numbers
s = sum(100 * a + 10 * b + c for a in [1, 3, 5, 7, 9] for b in [1, 3, 5, 7, 9] for c in [1, 3, 5, 7, 9])
add("W8", "Consider all three-digit numbers whose digits are ALL odd (digits from 1,3,5,7,9). "
          "What is the sum of all these numbers?", s)

# W9 100th number without digit 9
def w9():
    c = 0
    n = 0
    while c < 100:
        n += 1
        if "9" not in str(n):
            c += 1
    return n

add("W9", "List the positive integers that do NOT contain the digit 9, in increasing order: "
          "1, 2, ..., 8, 10, 11, ... What is the 100th number in this list?", w9())

# W10 squares on grid
# NOTE: first version had an off-by-one bug ((m-k)*(n-k), k<min) giving 85;
# caught because all four models unanimously answered 133 - see DEVIATIONS.md D3.
def w10(m, n):
    return sum((m - k + 1) * (n - k + 1) for k in range(1, min(m, n) + 1))

add("W10", "An 8 x 6 grid of unit cells is drawn (8 columns, 6 rows of cells). How many "
           "axis-aligned squares of ANY size can be traced along the grid lines?", w10(8, 6))

Path("wave2_items.json").write_text(json.dumps(items, indent=2), encoding="utf-8")
Path("wave2_answers.json").write_text(
    json.dumps({i["id"]: i["answer"] for i in items}, indent=2), encoding="utf-8")
lines = [f"{k}. {it['question']}" for k, it in enumerate(items, 1)]
Path("wave2_block.txt").write_text("\n\n".join(lines), encoding="utf-8")
for i in items:
    print(i["id"], "->", i["answer"])
