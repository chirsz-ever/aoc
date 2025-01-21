#!/usr/bin/env python3

from itertools import repeat
import sys
from typing import Iterator

def mkrange(start: int, length: int, step: int) -> Iterator[int]:
    if step == 0:
        return repeat(start, length)
    return range(start, start + length * step, step)

def find_xmas(map: list[list[str]], i: int, j: int, key: str) -> int:
    cnt = 0
    l = len(key)
    rkey = ''.join(reversed(key))
    for d in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
        di, dj = d
        if not 0 <= i + di * (l - 1) < len(map) or not 0 <= j + dj * (l - 1) < len(map[i]):
            continue
        seq = ''.join(map[ii][jj] for ii, jj in zip(mkrange(i, l, di), mkrange(j, l, dj)))
        if seq == key or seq == rkey:
            cnt += 1
    return cnt

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    map: list[list[str]] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if len(l) > 0:
                map.append(l)
    cnt = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            cnt += find_xmas(map, i, j, 'XMAS')
    print(cnt)

if __name__ == '__main__':
    main()
