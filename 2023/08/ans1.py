#!/usr/bin/env python3

import sys
from collections import Counter
from itertools import cycle

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

insts: str = ''
node_map: dict[str, tuple[str, str]] = {}
with open(inputFile) as fin:
    for l in fin:
        l = l.strip()
        if len(l) == 0:
            continue
        if len(insts) == 0:
            insts = l
        else:
            src, tgts = l.split(' = ')
            t_l, t_r = tgts.strip()[1:-1].split(', ')
            node_map[src] = (t_l, t_r)

# print(f'{insts=}')
# print(f'{node_map=}')

cnt = 0
n = 'AAA'
for inst in cycle(insts):
    cnt += 1
    n = node_map[n][0 if inst == 'L' else 1]
    if n == 'ZZZ':
        break

print(f'{cnt=}')
