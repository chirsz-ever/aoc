#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

hs : list[int] = []
with open(inputFile) as fin:
    hs = [int(x.strip()) for x in fin.read().split(',') if len(x.strip()) != 0]

hs.sort()
mid = hs[len(hs)//2]
minStep = sum(abs(mid - h) for h in hs)
print(f'{minStep = }')
