#!/usr/bin/env python3

import sys
import re

def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default

inputFile = getArg(1, 'input')

Pos = tuple[int, int, int]

scanners :list[tuple[int, list[Pos]]] = []

reScanner = re.compile(r"--- scanner (\d+) ---")
rePos = re.compile(r"(-?\d+),(-?\d+),(-?\d+)")
with open(inputFile) as fin:
    for line in fin:
        if m := reScanner.match(line):
            n = int(m[1])
            scanners.append((n, []))
        elif m := rePos.match(line):
            x, y, z = int(m[1]), int(m[2]), int(m[3])
            scanners[-1][1].append((x, y, z))

