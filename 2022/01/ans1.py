#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

entries : list[list[int]] = [[]]
with open(inputFile) as fin:
    for l in fin:
        l = l.strip()
        if len(l) == 0:
            entries.append([])
        else:
            entries[-1].append(int(l))

sums = list(map(sum, entries))
sums.sort()

print(sums[-1])
print(sum(sums[-3:]))
