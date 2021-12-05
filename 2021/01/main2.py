#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) > 2:
    inputFile = sys.argv[1]

WINDOW = 3
if len(sys.argv) > 3:
    inputFile = int(sys.argv[2].strip())


ns = []
with open(inputFile, 'rb') as fin:
    for line in fin:
        ns.append(int(line.strip()))

cnt = 0
for i in range(len(ns) - 1, WINDOW - 1, -1):
    if ns[i] > ns[i - WINDOW]:
        cnt += 1

print(f'{cnt = }')
