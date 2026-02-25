#!/usr/bin/env python3

import sys
from itertools import combinations, product
from typing import Iterable


def main() -> None:
    inputFile = sys.argv[1]

    with open(inputFile) as fin:
        wights = [int(s) for s in fin.read().split()]

    wights.sort()
    group_wight = sum(wights) // 4

    for n in range(1, len(wights) - 2):
        for ws in combinations(wights, n):
            if sum(ws) != group_wight:
                continue
            if can_split_3(remain(wights, ws), group_wight):
                print(ws)
                print(productsum(ws))
                return

def productsum(ws: Iterable[int]) -> int:
    p = 1
    for w in ws:
        p *= w
    return p

def remain(wights: list[int], ws: Iterable[int]) -> list[int]:
    r = wights[:]
    for w in ws:
        for i in range(len(r)):
            if r[i] == w:
                del r[i]
                break
    return r

def can_split_3(ws: list[int], t: int) -> bool:
    for choose in product([0, 1], repeat=len(ws)):
        if sum(c * w for c, w in zip(choose, ws)) == t and can_split_2(remain(ws, [w for i, w in enumerate(ws) if choose[i] == 1]), t):
            return True
    return False

def can_split_2(ws: list[int], t: int) -> bool:
    for choose in product([0, 1], repeat=len(ws)):
        if sum(c * w for c, w in zip(choose, ws)) == t:
            return True
    return False

if __name__ == "__main__":
    main()
