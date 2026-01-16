#!/usr/bin/env python3

import sys
from collections import deque

Coord = tuple[int, int]


def main() -> None:
    inputFile = sys.argv[1]
    steps = int(sys.argv[2])

    map: list[str] = []
    start: Coord = (0, 0)
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            if 'S' in l:
                start = (len(map), l.index('S'))
                map.append(l.replace('S', '.'))
            else:
                map.append(l)
    rows = len(map)
    cols = len(map[0])

    visited: set[tuple[Coord, int]] = set()
    targets: set[Coord] = set()
    def visit(p: Coord, aval_step: int) -> None:
        visited.add((p, aval_step))
        if aval_step == 0:
            targets.add(p)
            return
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = p[0] + di, p[1] + dj
            if 0 <= ni < rows and 0 <= nj <= cols and map[ni][nj] != '#' and ((ni, nj), aval_step - 1) not in visited:
                # print(f'{p} -> {(ni, nj)} [{aval_step}]')
                visit((ni, nj), aval_step - 1)

    visit(start, steps)
    print(len(targets))

    # for i in range(rows):
    #     for j in range(cols):
    #         if (i, j) in targets:
    #             print('O', end='')
    #         else:
    #             print(map[i][j], end='')
    #     print()

if __name__ == '__main__':
    main()
