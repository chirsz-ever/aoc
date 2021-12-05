#!/usr/bin/env python3

ns = []
with open('input', 'rb') as fin:
    for line in fin:
        ns.append(int(line.strip()))

cnt = 0
for i in range(len(ns) - 1, 0, -1):
    if ns[i] > ns[i - 1]:
        cnt += 1

print(f'{cnt = }')
