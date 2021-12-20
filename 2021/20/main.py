#!/usr/bin/env python3

from typing import Union

import sys


def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default


inputFile = getArg(1, "input")
# print(f'{inputFile = }')

c2i = {".": 0, "#": 1}

decoder: list[int] = []
rawMap: dict[tuple[int, int], int] = {}
with open(inputFile) as fin:
    decoder = [c2i[c] for c in fin.read(512)]
    fin.read(2)
    y = 0
    while l := fin.readline().strip():
        for x in range(len(l)):
                rawMap[x, y] = c2i[l[x]]
        y += 1

height = max(y + 1 for _, y in rawMap.keys())
width = max(x + 1 for x, _ in rawMap.keys())

print(f"{width = } {height = }")
# print(f"{decoder = }")
