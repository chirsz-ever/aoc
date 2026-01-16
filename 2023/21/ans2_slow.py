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
            if "S" in l:
                start = (len(map), l.index("S"))
                map.append(l.replace("S", "."))
            else:
                map.append(l)
    rows = len(map)
    cols = len(map[0])

    # BFS
    queue: deque[tuple[Coord, int]] = deque([(start, steps)])
    next_gen: set[Coord] = set()
    next_gen_step = steps - 1
    result = 0
    while len(queue) > 0:
        p, aval_steps = queue.popleft()
        if aval_steps == 0:
            result += 1
            continue
        if aval_steps - 1 != next_gen_step:
            # print(f'next_gen update: {len(next_gen)=}, {aval_steps=}')
            next_gen_step = aval_steps - 1
            next_gen.clear()
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = p[0] + di, p[1] + dj
            if map[ni % rows][nj % cols] != "#" and (ni, nj) not in next_gen:
                # print(f'{p} -> {(ni, nj)} [{aval_step}]')
                next_gen.add((ni, nj))
                queue.append(((ni, nj), aval_steps - 1))

    print(result)


if __name__ == "__main__":
    main()
