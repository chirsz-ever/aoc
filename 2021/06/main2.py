#!/usr/bin/env python3

import sys, re
from itertools import combinations
from typing import Optional

# a(n) = a(n - 7) + a(n - 9)

inputFile = 'input'
N = 80
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]
if len(sys.argv) >= 3:
    N = int(sys.argv[2])

fs: list[int] = []
with open(inputFile) as fin:
    for f in fin.read().split(','):
        f = f.strip()
        if len(f) != 0:
            fs.append(int(f))

# print(f'{fs = }')

def step(fs: list[int]) -> list[int]:
    nextfs = []
    newfs = []
    for f in fs:
        if f == 0:
            nextfs.append(6)
            newfs.append(8)
        else:
            nextfs.append(f - 1)
    nextfs += newfs
    return nextfs

ns = fs.copy()
stats = []
for d in range(9):
    ns = step(ns)
    print(f'After {d + 1:3} day: {len(ns) = }')
    stats.append(len(ns))

assert len(stats) == 9

for d in range(9, N):
    stats[d % 9] = stats[(d - 7) % 9] + stats[(d - 9) % 9]

print(f'{stats[(N - 1) % 9] = }')
