#!/usr/bin/env python3

from collections import defaultdict
from itertools import product

import sys
import re
from typing import Iterable

def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default

inputFile = getArg(1, 'input')
# print(f'{inputFile = }')

Range = tuple[int, int]
Pos = tuple[int, int, int]

reLine = re.compile(r"(off|on) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")
insts: list[tuple[bool, Range, Range, Range]] = []
with open(inputFile) as fin:
    for line in fin:
        if m := reLine.match(line):
            onOff = m[1] == "on"
            rx = (int(m[2]), int(m[3]))
            ry = (int(m[4]), int(m[5]))
            rz = (int(m[6]), int(m[7]))
            insts.append((onOff, rx, ry, rz))

status: dict[Pos, bool] = {}

def genRange(r: Range) -> Iterable[int]:
    a, b = r
    return range(max(a, -50), min(b, 50) + 1)

for on, rx, ry, rz in insts:
    if on:
        for p in product(genRange(rx), genRange(ry), genRange(rz)):
            status[p] = True
    else:
        for p in product(genRange(rx), genRange(ry), genRange(rz)):
            if p in status:
                status[p] = False


print(f"{sum(1 for b in status.values() if b) = }")
