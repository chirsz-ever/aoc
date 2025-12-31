#!/usr/bin/env python3

import sys
from collections import defaultdict

Coord = tuple[int, int]

def main() -> None:
    inputFile = sys.argv[1]
    rows = int(sys.argv[2]) + 1
    cols = int(sys.argv[3]) + 1
    bytenums = int(sys.argv[4])

    map: dict[Coord, int] = defaultdict(int)
    with open(inputFile) as fin:
        for l, _ in zip(fin, range(bytenums)):
            if l.strip():
                x, y = l.strip().split(',')
                map[(int(x), int(y))] = 1

    end = (cols - 1, rows - 1)

    queue: list[tuple[Coord, int]] = [ ((0, 0), 0) ]
    visited: dict[Coord, bool] = defaultdict(bool)
    visited[(0, 0)] = True

    # BFS
    while len(queue) > 0:
        c, step = queue.pop(0)
        # print(f'visit {c}')
        if c == end:
            print(step)
            break
        cx, cy = c
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            nx, ny = cx + dx, cy + dy
            n = (nx, ny)
            if 0 <= nx < cols and 0 <= ny < rows and map[n] == 0 and not visited[n]:
                # print(f'  push {(n)}')
                visited[n] = True
                queue.append((n, step + 1))

if __name__ == '__main__':
    main()
