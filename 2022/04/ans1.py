#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

reLine = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')

entries: list[tuple[int, int, int, int]] = []

with open(inputFile) as fin:
    for l in fin:
        m = reLine.match(l)
        assert m
        entries.append(tuple(map(int, [m[1], m[2], m[3], m[4]])))

cnt = 0
for e in entries:
    s1 = set(range(e[0], e[1] + 1))
    s2 = set(range(e[2], e[3] + 1))
    if s1.issubset(s2) or s1.issuperset(s2):
        cnt += 1

print(cnt)

cnt = 0
for e in entries:
    s1 = set(range(e[0], e[1] + 1))
    s2 = set(range(e[2], e[3] + 1))
    if len(s1.intersection(s2)) != 0:
        cnt += 1

print(cnt)
