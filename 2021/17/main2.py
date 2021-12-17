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

def canResolveX(x0: int, x1: int, t: int) -> set[int]:
    vxmin = ceil((2 * x0 + 0.25)**0.5 - 0.5)
    vxmax = x1
    vxs = set()
    for vx in range(vxmin, vxmax + 1):
        xt = getX(vx, t)
        # print(f"  {vx = } {t = } {xt = }")
        if x0 <= xt <= x1:
            vxs.add(vx)
    return vxs

def canResolve(vy: int, x0: int, x1: int, y0: int, y1:int) -> set[int]:
    d0 = -2 * y0 + (vy + 0.5)**2
    d1 = -2 * y1 + (vy + 0.5)**2
    # print(f"{  (d0, d1) = }")
    vxs: set[int] = set()
    if d0 < 0:
        return vxs
    if d1 < 0:
        d1 = 0
    t0 = d0 ** 0.5 + vy + 0.5
    t1 = d1 ** 0.5 + vy + 0.5
    # print(f"{  (t1, t0) = }")
    for t in range(ceil(t1), floor(t0) + 1):
        if vx := canResolveX(x0, x1, t):
            vxs |= vx
    return vxs

reLine = re.compile(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)")
with open(inputFile) as fin:
    for line in fin:
        if m := reLine.match(line):
            x0, x1, y0, y1 = int(m[1]), int(m[2]), int(m[3]), int(m[4])
            # print(f"{(x0, x1, y0, y1) = }")
            cnt = 0
            for vy in range(-y0 + 1, y0 - 1, -1):
                # print(f"test {vy = }")
                if len(vxs := canResolve(vy, x0, x1, y0, y1)) != 0:
                    # print(f"{(vxs, vy)}")
                    cnt += len(vxs)
            print(f"{cnt = }")

