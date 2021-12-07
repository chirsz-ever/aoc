#!/usr/bin/env python3

import sys, re
from itertools import combinations
from typing import Optional

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

print(f'{fs = }')

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
for d in range(N):
    ns = step(ns)
    print(f'After {d + 1:3} day: {len(ns) = }')

print(f'{len(ns) = }')
