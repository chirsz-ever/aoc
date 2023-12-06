#!/usr/bin/env python3

import sys
import math

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

Card = tuple[list[int], list[int]]
cards: list[Card] = []
with open(inputFile) as fin:
    for l in fin:
        _, nums = l.split(':')
        wins, haves = nums.split('|')
        cards.append(([int(w.strip()) for w in wins.split()], [int(h.strip()) for h in haves.split()], ))

# print(f'{cards=}')

s = 0
for wins, haves in cards:
    my_wins = set(haves).intersection(wins)
    # print(f'{my_wins=}')
    if len(my_wins) > 0:
        s += 2 ** (len(my_wins) - 1)

print(f'{s=}')
