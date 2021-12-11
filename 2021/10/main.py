#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

scoreMap = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
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
                return scoreMap[c]
        else:
            print(f"unknown '{c}'")


scores = []
with open(inputFile) as fin:
    for line in fin:
        if score := matchBrackets(line.strip()):
            scores.append(score)

# print(f'{scores = }')
print(f'{sum(scores) = }')
