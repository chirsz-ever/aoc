#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

Cave = str


def isSmall(c: Cave) -> bool:
    return c.islower()


def isBig(c: Cave) -> bool:
    return c.isupper()


caveMap: dict[Cave, set[Cave]] = dict()
reLine = re.compile(r'([a-zA-Z]+)-([a-zA-Z]+)')
with open(inputFile) as fin:
    for line in fin:
        if m := reLine.match(line.strip()):
            a = m[1]
            b = m[2]
            assert (isSmall(a) or isBig(a)) and (isSmall(b) or isBig(b))
            caveMap.setdefault(a, set()).add(b)
            caveMap.setdefault(b, set()).add(a)


def dfs(c: Cave, path: list[Cave], paths: list[list[Cave]]):
    if isSmall(c) and c in path:
        return
    npath = path + [c]
    if c == 'end':
        paths.append(npath)
        return
    for a in caveMap[c]:
        dfs(a, npath, paths)


paths: list[list[Cave]] = []
dfs('start', [], paths)

# for p in paths:
#     print(p)

print(f'{len(paths) = }')
