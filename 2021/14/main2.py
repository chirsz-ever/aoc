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
# print(f'{inputFile = }')
# print(f'{N = }')

tmpl = ""
rules : dict[tuple[str, str], str] = dict()
reLine = re.compile(r'([A-Z]{2}) -> ([A-Z])')
with open(inputFile) as fin:
    tmpl = fin.readline().strip()
    for line in fin:
        if m := reLine.match(line):
            rules[m[1][0], m[1][1]] = m[2]


cache : dict[tuple[str, str, int, str], int] = dict()
def f(a: str, b: str, n: int, c: str):
    k = (a, b, n, c)
    if k in cache:
        return cache[k]
    t = 0
    if n == 0:
        t = 0
    else:
        ab = rules[a, b]
        t = f(a, ab, n - 1, c) + f(ab, b, n - 1, c) + (1 if ab == c else 0)
    cache[k] = t
    return t

cnt = Counter(tmpl)

nodes :set[str] = set(rules.values()) | set(tmpl)

ltc = tmpl[0]
for tc in tmpl[1:]:
    for c in nodes:
        nc = f(ltc, tc, N, c)
        if nc > 0:
            cnt[c] = cnt.get(c, 0) + nc
    ltc = tc

# print(f'{cnt}')
print(f'{max(cnt.values()) - min(cnt.values())}')
