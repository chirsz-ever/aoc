#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

insts: list = []

reInstAddx = re.compile(r'addx (-?\d+)')

with open(inputFile) as fin:
    for l in fin:
        l = l.strip()
        if l == 'noop':
            insts.append(None)
        elif m := reInstAddx.match(l):
            insts.append(int(m[1]))
        else:
            print(f"error: {l}")
            exit(1)

# print(insts)
key_points = [20, 60, 100, 140, 180, 220]
key_points_passed = { k: False for k in key_points }

strengths = []

X = 1
cycle = 0
for inst in insts:
    X_dur = X
    if inst == None:
        cycle += 1
    else:
        assert isinstance(inst, int)
        cycle += 2
        X += inst
    for k in key_points:
        if k <= cycle and not key_points_passed[k]:
            strengths.append(k * X_dur)
            key_points_passed[k] = True
            break

# print(strengths)
print(sum(strengths))

X = 1
cycle = 0
h_positon = 0
for inst in insts:
    dX = 0
    dcycle = 1
    if inst == None:
        dcycle = 1
        dX = 0
    else:
        assert isinstance(inst, int)
        dcycle = 2
        dX = inst
    for c in range(cycle + 1, cycle + dcycle + 1):
        if X - 1 <= h_positon <= X + 1:
            print('#', end='')
        else:
            print('.', end='')
        if h_positon == 39:
            print()
            h_positon = 0
        else:
            h_positon += 1
    X += dX
    cycle += dcycle
