#!/usr/bin/env python3

import sys
from itertools import product

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

N = 100
if len(sys.argv) >= 3:
    N = int(sys.argv[2])

def printMap(m: list[list[int]]):
    for row in m:
        print(''.join(str(lvl) for lvl in row))

elvlMap : list[list[int]] = []
with open(inputFile) as fin:
    for line in fin:
        elvlMap.append([int(c) for c in line.strip()])

width = len(elvlMap[0])
height = len(elvlMap)


def flashAdjacents(m, i, j):
    newps = []
    for ai, aj in product([i-1, i, i+1], [j-1, j, j+1]):
        if 0 <= ai < height and 0 <= aj < width and m[ai][aj] > 0:
            m[ai][aj] += 1
            newps.append((ai, aj))
    return newps


def step(m: list[list[int]]) -> tuple[list[list[int]], int]:
    m1 = [[lvl + 1 for lvl in row] for row in m]
    flashCount = 0
    newps = list(product(range(height), range(width)))
    while len(newps) > 0:
        i, j = newps.pop(0)
        if m1[i][j] > 9:
            m1[i][j] = 0
            flashCount += 1
            newps += flashAdjacents(m1, i, j)
    return m1, flashCount

m = elvlMap
tfc = 0
for _ in range(N):
    m, fc = step(m)
    tfc += fc

print(f'{tfc = }')
