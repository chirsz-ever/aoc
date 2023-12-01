#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

test_y = 2000000
if len(sys.argv) >= 3:
    test_y = int(sys.argv[2])

w2d = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def find_nums(s: str)-> list[str]:
    ns = []
    for i in range(0, len(s)):
        if s[i].isdigit():
            ns.append(s[i])
        else:
            for k, v in w2d.items():
                if s.startswith(k, i):
                    ns.append(str(v))
    return ns

s = 0
with open(inputFile) as fin:
    for l in fin:
        ns = find_nums(l)
        # print(f'{ns=}')
        s += int(ns[0] + ns[-1])

print(f'{s=}')
