#!/usr/bin/env python3

import sys, re
from itertools import combinations
from typing import Optional

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'Point({self.x}, {self.y})'

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

Line = tuple[Point, Point]

lines : list[Line] = []

reLine = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
with open(inputFile) as fin:
    for l in fin:
        m = reLine.match(l)
        lines.append((Point(int(m[1]), int(m[2])), Point(int(m[3]), int(m[4]))))

def isH(*ps) -> bool:
    if len(ps) == 1:
        l = ps[0]
        assert type(l) == tuple
        return l[0].y == l[1].y
    else:
        return len({p.y for p in ps}) == 1

def isV(*ps) -> bool:
    if len(ps) == 1:
        l = ps[0]
        assert type(l) == tuple
        return l[0].x == l[1].x
    else:
        return len({p.x for p in ps}) == 1

def isHV(*ps) -> bool:
    return isH(*ps) or isV(*ps)

def isBetween(x: float, a: float, b: float):
    return a <= x <= b or b <= x <= a

def setBetween(a: int, b: int):
    if a <= b:
        return set(range(a, b + 1))
    else:
        return set(range(b, a + 1))

def crossPoint(l1: Line, l2: Line) -> list[Point]:
    assert isHV(l1) and isHV(l2)
    if isH(l1) and isH(l2) and isH(l1[0], l2[0]):
        xs = setBetween(l1[0].x, l1[1].x) & setBetween(l2[0].x, l2[1].x)
        return [Point(x, l1[0].y) for x in xs]
    elif isV(l1) and isV(l2) and isV(l1[0], l2[0]):
        ys = setBetween(l1[0].y, l1[1].y) & setBetween(l2[0].y, l2[1].y)
        return [Point(l1[0].x, y) for y in ys]
    elif isH(l1) and isV(l2) and isBetween(l2[0].x, l1[0].x, l1[1].x) and isBetween(l1[0].y, l2[0].y, l2[1].y):
        return [Point(l2[0].x, l1[0].y)]
    elif isV(l1) and isH(l2) and isBetween(l1[0].x, l2[0].x, l2[1].x) and isBetween(l2[0].y, l1[0].y, l1[1].y):
        return [Point(l1[0].x, l2[0].y)]



xps : dict[tuple[int, int], int] = {}
for (l1, l2) in combinations((l for l in lines if isHV(l)), 2):
    if ps := crossPoint(l1, l2):
        for p in ps:
            xps.setdefault((p.x, p.y), 0)
            xps[p.x, p.y] += 1

print(f'{len(xps) = }')
