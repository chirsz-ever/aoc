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

card_cnts: list[int] = [ 1 for _ in cards ]

for i, (wins, haves) in enumerate(cards):
    g = len(set(haves).intersection(wins))
    for j in range(i + 1, i + g + 1):
        card_cnts[j] += card_cnts[i]

print(f'{card_cnts=}')
total = sum(card_cnts)
print(f'{total=}')
