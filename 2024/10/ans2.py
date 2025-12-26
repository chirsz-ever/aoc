#!/usr/bin/env python3

import sys
from functools import lru_cache

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    tmap: list[list[int]] = []
    with open(inputFile) as fin:
        for l in fin:
            if len(l.strip()) > 0:
                tmap.append([int(c) for c in l.strip()])
    # print(tmap)
    rows = len(tmap)
    cols = len(tmap[0])


    def explore(i: int, j: int, explore_map: dict[tuple[int, int], bool], score_count: list[int]):
        explore_map[i, j] = True
        if tmap[i][j] == 9:
            score_count[0] += 1
        for di, dj in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            ni = i + di
            nj = j + dj
            if (0 <= ni < rows) and (0 <= nj < cols) and (tmap[ni][nj] == tmap[i][j] + 1):
                # print(f'{(i, j)} -> {(ni, nj)} ({tmap[i][j]} -> {tmap[ni][nj]})')
                explore(ni, nj, explore_map, score_count)

    s = 0
    for i in range(rows):
        for j in range(cols):
            if tmap[i][j] == 0:
                score_count = [0]
                explore_map = {}
                # print(f'explore{(i, j)}')
                explore(i, j, explore_map, score_count)
                s += score_count[0]
    print(s)
if __name__ == '__main__':
    main()
