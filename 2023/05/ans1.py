#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

seeds: list[int] = []
maps: list[list[int]] = []
with open(inputFile) as fin:
    for l in fin:
        l = l.strip()
        if len(l) == 0:
            continue
        words = l.split()
        if words[0] == 'seeds:':
            seeds = [int(w) for w in words[1:]]
        elif words[-1] == 'map:':
            maps.append([])
        else:
            maps[-1].append([int(w) for w in words])

# print(f'{seeds=}')
# print(f'{maps=}')

def map_once(s: int, m: list[list[int]]) -> int:
    t = s
    for dst, src, l in m:
        if src <= s < src + l:
            t = dst + (s - src)
            break
    # print(f'{s} -> {t}')
    return t

def map_seed(s: int) -> int:
    t = s
    for m in maps:
        t = map_once(t, m)
    return t

# for s in seeds:
    # print('----')
    # print(f'{s} -> {map_seed(s)}')

print(min(map_seed(s) for s in seeds))
