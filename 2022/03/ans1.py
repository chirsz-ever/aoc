#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

entries : list[tuple[str, str]] = []
with open(inputFile) as fin:
    for l in fin:
        l = l.strip()
        if len(l)  == 0:
            continue
        assert len(l) % 2 == 0
        n = len(l) // 2
        l1 = l[:n]
        l2 = l[n:]
        entries.append((l1, l2))

def mapP(c):
    n = ord(c)
    if ord('a') <= n <= ord('z'):
        return n - ord('a') + 1
    if ord('A') <= n <= ord('Z'):
        return n - ord('A') + 27
    raise c

def score1():
    s = 0
    for ruck in entries:
        s += sum(mapP(c) for c in set(ruck[0]).intersection(ruck[1]))
    return s

def ruckAll(i):
    return entries[i][0] + entries[i][1]

def score2():
    assert len(entries) % 3 == 0
    s = 0
    for i in range(0, len(entries), 3):
        inters = set(ruckAll(i)).intersection(ruckAll(i + 1)).intersection(ruckAll(i + 2))
        assert len(inters) == 1
        s += mapP(inters.pop())
    return s

print(score1())
print(score2())
