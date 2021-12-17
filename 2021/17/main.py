#!/usr/bin/env python3

import sys
import re
from math import ceil, floor
from typing import Optional

def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default

inputFile = getArg(1, 'input')

def getY(vy: int, t: int) -> int:
    return - (t - 1) * t // 2 + vy * t

def getX(vx: int, t: int) -> int:
    if t < vx:
        return - (t - 1) * t // 2 + vx * t
    else:
        return vx * (vx + 1) // 2

def canResolveX(x0: int, x1: int, t: int) -> Optional[int]:
    vxmin = ceil((2 * x0 + 0.25)**0.5 - 0.5)
    vxmax = x1
    for vx in range(vxmin, vxmax + 1):
        if x0 <= getX(vx, t) <= x1:
            return vx
    return None

def canResolve(vy: int, x0: int, x1: int, y0: int, y1:int) -> Optional[tuple[int, int]]:
    d0 = -2 * y0 + (vy + 0.5)**2
    d1 = -2 * y1 + (vy + 0.5)**2
    print(f"{(d0, d1) = }")
    if d0 < 0:
        return None
    if d1 < 0:
        d1 = 0
    t0 = d0 ** 0.5 + vy + 0.5
    t1 = d1 ** 0.5 + vy + 0.5
    print(f"{(t1, t0) = }")
    for t in range(ceil(t1), floor(t0) + 1):
        if vx := canResolveX(x0, x1, t):
            return vx, t
    return None

reLine = re.compile(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)")
with open(inputFile) as fin:
    for line in fin:
        if m := reLine.match(line):
            x0, x1, y0, y1 = int(m[1]), int(m[2]), int(m[3]), int(m[4])
            print(f"{(x0, x1, y0, y1) = }")
            for vy in range(-y0 + 1, -1, -1):
                print(f"test {vy = }")
                if (res := canResolve(vy, x0, x1, y0, y1)):
                    vx, t = res
                    print(f"highest y = {getY(vy, vy)}")
                    break

