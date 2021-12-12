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

paths = 0

def dfs(c: Cave, path: list[Cave], allowTwice: bool):
    global paths
    npath = path + [c]
    for a in caveMap[c]:
        if isBig(a):
            dfs(a, npath, allowTwice)
        elif a == 'end':
            paths += 1
        elif a != 'start':
            n = npath.count(a)
            if n == 0:
                dfs(a, npath, allowTwice)
            elif n == 1 and allowTwice:
                dfs(a, npath, allowTwice=False)


dfs('start', [], True)

print(f'{paths = }')
