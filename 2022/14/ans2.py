#!/usr/bin/env python3

import sys
from functools import cmp_to_key

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

def myrange(a, b):
    if a > b:
        a, b = b, a
    return range(a, b + 1)

def unpdate_map(map: dict[tuple[int, int], str], c1: tuple[int, int], c2: tuple[int, int]):
    x1, y1 = c1
    x2, y2 = c2
    if x1 == x2:
        for y in myrange(y1, y2):
            map[x1, y] = '#'
    elif y1 == y2:
        for x in myrange(x1, x2):
            map[x, y1] = '#'


def read_input(fname) -> dict[tuple[int, int], str]:
    map: dict[tuple[int, int], str] = dict()
    with open(fname) as fin:
        for l in fin:
            coords = []
            for c in l.strip().split(' -> '):
                x, y = c.split(',')
                coords.append((int(x), int(y)))
            for i in range(len(coords) - 1):
                unpdate_map(map, coords[i], coords[i + 1])
    return map

def perform_step(map: dict[tuple[int, int], str], ground: int) -> bool:
    x, y = 500, 0
    while True:
        assert y < ground
        if y == ground - 1:
            map[x, y] = 'o'
            return True
        if (x, y + 1) not in map:
            y = y + 1
        elif (x - 1, y + 1) not in map:
            x, y = x - 1, y + 1
        elif (x + 1, y + 1) not in map:
            x, y = x + 1, y + 1
        else:
            map[x, y] = 'o'
            return True

map = read_input(inputFile)
ground = max(y for _, y in map) + 2

cnt = 0
while True:
    if not perform_step(map, ground):
        break
    cnt += 1
    if (500, 0) in map:
        break

print(cnt)
