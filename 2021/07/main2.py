#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

hs : list[int] = []
with open(inputFile) as fin:
    hs = [int(x.strip()) for x in fin.read().split(',') if len(x.strip()) != 0]

def calcStep(p: int):
    return sum(abs(p - h) * (abs(p - h) + 1) // 2 for h in hs)

mid = round(sum(hs) / len(hs))
minStep = min(calcStep(p) for p in range(mid - 100, mid + 100))

print(f'{minStep = }')
