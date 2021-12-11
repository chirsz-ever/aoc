#!/usr/bin/env python3

import sys
import re
from itertools import combinations
from math import floor
from typing import Optional, Iterable

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y


class K:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, k):
        return self.x * k.y == k.x * self.y


Line = tuple[Point, Point]


def getK(l: Line) -> K:
    return K(l[1].x - l[0].x, l[1].y - l[0].y)


def isLegalK(k: K) -> bool:
    return k in [K(0, 1), K(1, 0), K(1, 1), K(1, -1)]


lines: list[Line] = []

reLine = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
with open(inputFile) as fin:
    for l in fin:
        if m := reLine.match(l):
            lines.append((Point(int(m[1]), int(m[2])),
                          Point(int(m[3]), int(m[4]))))


def rangeIntersection(a1: int, a2: int, b1: int, b2: int) -> Iterable[int]:
    if a1 > a2:
        return rangeIntersection(a2, a1, b1, b2)
    if b1 > b2:
        return rangeIntersection(a1, a2, b2, b1)
    if a1 > b1:
        return rangeIntersection(b1, b2, a1, a2)
    # print(f'rangeIntersection({a1}, {a2}, {b1}, {b2})')
    assert a1 < a2 and b1 < b2
    return range(b1, min(a2, b2) + 1)


def crossPoints(l1: Line, l2: Line) -> Optional[list[Point]]:
    k1 = getK(l1)
    k2 = getK(l2)
    p1 = l1[0]
    p2 = l2[0]
    assert isLegalK(k1) and isLegalK(k2)
    if k1 != k2:
        t2 = (k1.y*p1.x + k1.x*p2.y - k1.y*p2.x -
              k1.x * p1.y)/(k1.y * k2.x - k1.x * k2.y)
        x = p2.x + k2.x * t2
        y = p2.y + k2.y * t2
        t1 = (x - p1.x) / k1.x if k1.x != 0 else (y - p1.y) / k1.y
        if 0 <= t1 <= 1 and 0 <= t2 <= 1 and abs(x - round(x)) < 0.1:
            return [Point(round(x), round(y))]
    elif k1 == (getK((p1, p2)) if p1 != p2 else getK((p1, l2[1]))):
        if k1.x != 0:
            xps = []
            for x in rangeIntersection(p1.x, l1[1].x, p2.x, l2[1].x):
                y = p2.y + k2.y // k2.x * (x - p2.x)
                xps.append(Point(x, y))
            return xps
        else:
            assert k1.y != 0
            xps = []
            for y in rangeIntersection(p1.y, l1[1].y, p2.y, l2[1].y):
                xps.append(Point(p1.x, y))
            return xps
    return None


xps: dict[tuple[int, int], int] = {}
for (l1, l2) in combinations(lines, 2):
    if ps := crossPoints(l1, l2):
        for p in ps:
            xps.setdefault((p.x, p.y), 1)
            print(f'{l1[0]} -- {l1[1]} x {l2[0]} -- {l2[1]} at {p}')
            xps[p.x, p.y] += 1

# for k in sorted(xps.keys()):
#     print(f'{k}: {xps[k]}')
print(f'{len(xps) = }')
