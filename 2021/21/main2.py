#!/usr/bin/env python3

from typing import Union

import sys
import re
from itertools import repeat, cycle
import functools


def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default


inputFile = getArg(1, "input")
# print(f'{inputFile = }')

startPositons: list[int] = []
reLine = re.compile(r"Player (\d+) starting position: (\d+)")
with open(inputFile) as fin:
    p = 0
    for line in fin:
        if m := reLine.match(line):
            assert int(m[1]) == p + 1
            startPositons.append(int(m[2]))
            p += 1


def step(p: int, d: int) -> int:
    return (p + d - 1) % 10 + 1


distrib: list[int] = [0 for _ in range(10)]

distrib[3] = 1
distrib[4] = 3
distrib[5] = 6
distrib[6] = 7
distrib[7] = 6
distrib[8] = 3
distrib[9] = 1


@functools.cache
def calcResults(myLeftScore: int, yourLeftScore: int, myPos: int, yourPos: int) -> tuple[int, int]:
    if myLeftScore <= 0:
        return (1, 0)
    elif yourLeftScore <= 0:
        return (0, 1)
    r = [0, 0]
    for d in range(3, 9 + 1):
        myNewPos = step(myPos, d)
        r1 = calcResults(yourLeftScore, myLeftScore - myNewPos, yourPos, myNewPos)
        r = [r[0] + r1[1] * distrib[d], r[1] + r1[0] * distrib[d]]
    return (r[0], r[1])


r = calcResults(21, 21, startPositons[0], startPositons[1])

print(f"{r}")
print(f"most win universes: {max(r)}")
