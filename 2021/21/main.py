#!/usr/bin/env python3

from typing import Union

import sys
import re
from itertools import repeat, cycle


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

positions = startPositons.copy()
scores = list(repeat(0, len(positions)))


def dice(turn: int) -> int:
    return turn % 100 + 1


turn = 0
winner = 0
for p in cycle(range(len(positions))):
    d1 = dice(turn)
    turn += 1
    d2 = dice(turn)
    turn += 1
    d3 = dice(turn)
    turn += 1
    positions[p] = (positions[p] + d1 + d2 + d3 - 1) % 10 + 1
    scores[p] += positions[p]
    # print(
    #     f"Player {p+1} rolls {d1}+{d2}+{d3} and moves to space {positions[p]} for a total score of {scores[p]}"
    # )
    if scores[p] >= 1000:
        winner = p
        break

print(f"{scores[(p+1)%2] * turn = }")
