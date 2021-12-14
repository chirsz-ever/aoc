#!/usr/bin/env python3

import sys
import re
from collections import Counter

def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default

inputFile = getArg(1, 'input')
N = int(getArg(2, 10))

tmpl = ""
rules = dict()
reLine = re.compile(r'([A-Z]{2}) -> ([A-Z])')
with open(inputFile) as fin:
    tmpl = list(fin.readline().strip())
    for line in fin:
        if m := reLine.match(line):
            rules[m[1][0], m[1][1]] = m[2]

def step(s):
    r = [s[0]]
    lc = s[0]
    for c in s[1:]:
        r.append(rules[lc, c])
        r.append(c)
        lc = c
    return r

s = tmpl
for _ in range(N):
    s = step(s)

cnt = Counter(s)
print(f'{max(cnt.values()) - min(cnt.values())}')
