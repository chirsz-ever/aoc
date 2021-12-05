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

for inst, n in insts:
    if inst == 'forward':
        position += n
    elif inst == 'down':
        depth += n
    elif inst == 'up':
        depth -= n
    else:
        print(f'unknown inst {inst}')

print(f'{position = }')
print(f'{depth = }')
print(f'{depth * position = }')
