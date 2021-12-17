#!/usr/bin/env python3

import sys
from itertools import takewhile

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

entries : list[tuple[list[str], list[str]]] = []
with open(inputFile) as fin:
    for line in fin:
        unique = []
        output = []
        beforeSplit = True
        for w in line.split():
            if beforeSplit:
                if w == '|':
                    beforeSplit = False
                else:
                    unique.append(w)
            else:
                output.append(w)
        entries.append((unique, output))

output1478 = sum(1 for e in entries for o in e[1] if len(o) in (2,4,3,7))
print(f'{output1478 = }')
