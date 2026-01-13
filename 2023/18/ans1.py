#!/usr/bin/env python3

import sys
import random
from collections import deque

Coord = tuple[int, int]

dir2didj = {
    'U': (-1,  0),
    'D': ( 1,  0),
    'L': ( 0, -1),
    'R': ( 0,  1),
}

def main() -> None:
    inputFile = sys.argv[1]

    plan: list[tuple[str, int, str]] = []
    with open(inputFile) as fin:
        for l in fin:
            if l.strip():
                a, b, c = l.strip().split()
                plan.append((a, int(b), c))

    map: dict[Coord, str] = { (0, 0): '#' }
    i = 0
    j = 0
    for d, size, _ in plan:
        di, dj = dir2didj[d]
        for _ in range(1, size+1):
            i += di
            j += dj
            map[i, j] = '#'

    max_i = max(i for i, j in map)
    min_i = min(i for i, j in map)
    max_j = max(j for i, j in map)
    min_j = min(j for i, j in map)

    # for i in range(min_i, max_i + 1):
    #     for j in range(min_j, max_j + 1):
    #         if (i, j) in map:
    #             print(map[i, j], end='')
    #         else:
    #             print('.', end='')
    #     print()

    # random pick point until pick a inner point
    while True:
        i = random.randint(min_i, max_i)
        j = random.randint(min_j, max_j)

        if (i, j) in map:
            continue

        cross_times = 0
        false_positive = False
        for k in range(j + 1, max_j + 1):
            if (i, k) in map:
                if (i, k + 1) in map:
                    false_positive = True
                    break
                else:
                    cross_times += 1
        if false_positive:
            continue
        if cross_times % 2 == 1:
            break

    map[i, j] = '#'
    queue: deque[Coord] = deque([(i, j)])
    while len(queue) > 0:
        ci, cj = queue.popleft()
        for di, dj in dir2didj.values():
            ni, nj = ci + di, cj + dj
            if (ni, nj) not in map:
                map[ni, nj] = '#'
                queue.append((ni, nj))

    print(len(map))

if __name__ == '__main__':
    main()
