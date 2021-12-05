#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) > 2:
    inputFile = sys.argv[1]

reports = []
with open(inputFile) as fin:
    for line in fin:
        if len(line.strip()) != 0:
            reports.append(line.strip())

digits = [0 for _ in range(len(reports[0]))]
for r in reports:
    for i in range(len(digits)):
        if r[i] == '1':
            digits[i] += 1
        elif r[i] == '0':
            digits[i] -= 1
        else:
            assert False

gamma = int(''.join(map(lambda x: '1' if x >= 0 else '0', digits)), base=2)
epsilon = int(''.join(map(lambda x: '0' if x > 0 else '1', digits)), base=2)

print(f'{gamma = }')
print(f'{epsilon = }')
print(f'{gamma * epsilon = }')
