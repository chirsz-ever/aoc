#!/usr/bin/env python3

import sys
from itertools import repeat, product
from operator import mul
from functools import reduce

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

heightmap : list[list[int]] = []
with open(inputFile) as fin:
    for line in fin:
        heightmap.append([int(c) for c in line.strip()])

width = len(heightmap[0])
height = len(heightmap)

def isLowPoint(i, j):
    h = heightmap[i][j]
    if i != 0 and heightmap[i - 1][j] <= h:
        return False
    if i != height - 1 and heightmap[i + 1][j] <= h:
        return False
    if j != 0 and heightmap[i][j - 1] <= h:
        return False
    if j != width - 1 and heightmap[i][j + 1] <= h:
        return False
    return True

lowpoints : list[tuple[int, int]] = []
for i, j in product(range(height), range(width)):
    if isLowPoint(i, j):
        lowpoints.append((i, j))

basinlog = [[0 for _ in range(width)] for _ in range(height)]

for i, j in product(range(height), range(width)):
    if heightmap[i][j] == 9:
        basinlog[i][j] = -1

def findbasin(i, j, t) -> int:
    if basinlog[i][j] != 0:
        return 0
    basinlog[i][j] = t
    size = 1
    if i != 0 and heightmap[i - 1][j] != 9:
        size += findbasin(i - 1, j, t)
    if i != height - 1 and heightmap[i + 1][j] != 9:
        size += findbasin(i + 1, j, t)
    if j != 0 and heightmap[i][j - 1] != 9:
        size += findbasin(i, j - 1, t)
    if j != width - 1 and heightmap[i][j + 1] != 9:
        size += findbasin(i, j + 1, t)
    return size


basinsizes : list[int, int] = []
basintoken = 1
for i, j in lowpoints:
    if (size := findbasin(i, j, basintoken)) != 0:
        basinsizes.append(size)
    basintoken += 1

print(f'{reduce(mul, sorted(basinsizes, reverse=True)[:3]) = }')