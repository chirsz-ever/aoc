#!/usr/bin/env python3

from itertools import repeat
import sys
from typing import Iterator

def find_xmas(map: list[list[str]], i: int, j: int, key: str) -> int:
    cnt = 0
    l = len(key)
    rkey = ''.join(reversed(key))

    if not 1 <= i < len(map) - 1 or not 1 <= j < len(map[i]) - 1:
        return 0

    seq1 = ''.join(map[i + di][j + dj] for di, dj in [(-1, -1), (0, 0), (1, 1)])
    seq2 = ''.join(map[i + di][j + dj] for di, dj in [(-1, 1), (0, 0), (1, -1)])
    if seq1 in [key, rkey] and seq2 in [key, rkey]:
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
    for i in range(1, len(map) - 1):
        for j in range(1, len(map[i]) - 1):
            cnt += find_xmas(map, i, j, 'MAS')
    print(cnt)

if __name__ == '__main__':
    main()
