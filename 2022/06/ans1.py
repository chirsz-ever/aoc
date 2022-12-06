#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

reInst = re.compile(r'move (\d+) from (\d+) to (\d+)')

input = ""
with open(inputFile) as fin:
    input = fin.read().strip()

def findN(n: int):
    for i in range(len(input)):
        if len(set(input[i:i+n])) == n:
            print(i + n)
            break

findN(4)
findN(14)
