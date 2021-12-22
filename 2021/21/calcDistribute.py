#!/usr/bin/env python3

from itertools import product

times: list[int] = [0 for _ in range(9 + 1)]

for x1, x2, x3 in product((1, 2, 3), repeat=3):
    times[x1 + x2 + x3] += 1

for i in range(3, 9 + 1):
    print(f"distrib[{i}] = {times[i]}")
