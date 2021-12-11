#!/usr/bin/env python3

import sys
from functools import reduce

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

scoreMap = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

def isMatch(l, r):
    return l + r in ["()", "[]", "{}", "<>"]

def matchBrackets(cs):
    bs = []
    for c in cs:
        if c in '([{<':
            bs.append(c)
        elif c in ')]}>':
            if not (len(bs) > 0 and isMatch(bs.pop(), c)):
                return False
        else:
            print(f"unknown '{c}'")
    return reduce(lambda s, c: s * 5 + scoreMap[c], reversed(bs), 0)


scores = []
with open(inputFile) as fin:
    for line in fin:
        if score := matchBrackets(line.strip()):
            scores.append(score)

scores.sort()
# print(f'{scores = }')
print(f'{scores[len(scores)//2] = }')
