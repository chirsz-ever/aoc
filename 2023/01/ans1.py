#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

test_y = 2000000
if len(sys.argv) >= 3:
    test_y = int(sys.argv[2])

s = 0
with open(inputFile) as fin:
    for l in fin:
        ns = ''.join(c for c in l if c.isdigit())
        s += int(ns[0] + ns[-1])

print(f'{s=}')
