#!/usr/bin/env python3

import sys

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
for i in range(height):
    for j in range(width):
        if isLowPoint(i, j):
            lowpoints.append((i, j))

# for i, j in lowpoints:
#     print(f'{(i, j)} : {heightmap[i][j]}')

print(f'{sum(heightmap[i][j] + 1 for i, j in lowpoints) = }')