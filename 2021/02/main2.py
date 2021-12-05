#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) > 2:
    inputFile = sys.argv[1]

insts = []
with open(inputFile) as fin:
    for line in fin:
        ws = line.strip().split()
        insts.append((ws[0], int(ws[1])))

position = 0
depth = 0
aim = 0

for inst, x in insts:
    if inst == 'forward':
        position += x
        depth += aim * x
    elif inst == 'down':
        aim += x
    elif inst == 'up':
        aim -= x
    else:
        print(f'unknown inst {inst}')

print(f'{position = }')
print(f'{depth = }')
print(f'{depth * position = }')
