#!/usr/bin/env python3

import sys
from collections import Counter

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

hand_bids: list[tuple[str, int]] = []
with open(inputFile) as fin:
    for l in fin:
        h, b = l.split()
        hand_bids.append((h, int(b)))

# print(f'{hands=}')
# print(f'{bids=}')

def hand_type(h: str) -> int:
    cnt = Counter(h)
    p = sorted(cnt.values())
    if p == [5]:
        return 1
    if p == [1, 4]:
        return 2
    elif p == [2, 3]:
        return 3
    elif p == [1, 1, 3]:
        return 4
    elif p == [1, 2, 2]:
        return 5
    elif p == [1, 1, 1, 2]:
        return 6
    else:
        return 7

ds = "AKQJT98765432"[::-1]

def to_digits(h: str) -> str:
    return ''.join(chr(ord('a') + ds.index(c)) for c in h)

hand_bids.sort(key = lambda hb: (-hand_type(hb[0]), to_digits(hb[0])))

s = 0
for e, (h, b) in enumerate(hand_bids):
    r = e + 1
    # print(f'{r}: {h} {b}')
    s += r * b

print(f'{s=}')

