#!/usr/bin/env python3

import sys
from collections import defaultdict

Coord = tuple[int, int]

def main() -> None:
    inputFile = sys.argv[1]
    rows = int(sys.argv[2]) + 1
    cols = int(sys.argv[3]) + 1
    start_count = int(sys.argv[4])

    coords: list[tuple[int, int]] = []
    with open(inputFile) as fin:
        for l in fin:
            if l.strip():
                x, y = l.strip().split(',')
                coords.append((int(x), int(y)))

    end = (cols - 1, rows - 1)

    for count in range(start_count, len(coords)):
        map: dict[Coord, int] = defaultdict(int)
        for i in range(count):
            map[coords[i]] = 1
        queue: list[tuple[Coord, int]] = [ ((0, 0), 0) ]
        visited: dict[Coord, bool] = defaultdict(bool)
        visited[(0, 0)] = True
        while len(queue) > 0:
            c, step = queue.pop(0)
            # print(f'visit {c}')
            if c == end:
                # print(step)
                break
            cx, cy = c
            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                nx, ny = cx + dx, cy + dy
                n = (nx, ny)
                if 0 <= nx < cols and 0 <= ny < rows and map[n] == 0 and not visited[n]:
                    # print(f'  push {(n)}')
                    visited[n] = True
                    queue.append((n, step + 1))
        else:
            print(f'close at {count}: {coords[count - 1]}')
            break

if __name__ == '__main__':
    main()
