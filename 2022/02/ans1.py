#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

entries : list[tuple[str, str]] = []
with open(inputFile) as fin:
    for l in fin:
        x, y = l.strip().split()
        entries.append((x, y))

mapX = { 'A': 0, 'B': 1, 'C': 2 }
mapY = { 'X': 0, 'Y': 1, 'Z': 2 }

scoreMapResult = [ 3, 6, 0 ]

def score1(xy):
    x, y = xy
    mx = mapX[x]
    my = mapY[y]
    return my + 1 + scoreMapResult[(my - mx) % 3]

def score2(xy):
    x, y = xy
    mx = mapX[x]
    ms = mapY[y]
    my = (mx + ms - 1) % 3
    return my + 1 + scoreMapResult[(ms - 1) % 3]

print(sum(map(score1, entries)))
print(sum(map(score2, entries)))
