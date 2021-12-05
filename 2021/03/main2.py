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

o2ds = [0 for _ in range(len(reports[0]))]
co2ds = [0 for _ in range(len(reports[0]))]

rs = reports.copy()
for b in range(len(reports[0])):
    score = 0
    for r in rs:
        score += 1 if r[b] == '1' else -1
    d = '1' if score >= 0 else '0'
    rs = [r for r in rs if r[b] == d]
    if len(rs) <= 1:
        break
print(f'{rs[0] = }')
o2 = int(rs[0], base=2)

rs = reports.copy()
for b in range(len(reports[0])):
    score = 0
    for r in rs:
        score += 1 if r[b] == '1' else -1
    d = '1' if score < 0 else '0'
    rs = [r for r in rs if r[b] == d]
    if len(rs) <= 1:
        break
print(f'{rs[0] = }')
co2 = int(rs[0], base=2)

print(f'{o2 = }')
print(f'{co2 = }')
print(f'{o2 * co2 = }')
