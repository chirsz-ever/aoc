#!/usr/bin/env python3

# See https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21

import sys
from collections import deque

Coord = tuple[int, int]


def main() -> None:
    inputFile = sys.argv[1]
    # steps = int(sys.argv[2])

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
    curr_gen: set[Coord] = {start}
    next_gen: set[Coord] = set()
    visited: dict[Coord, int] = {start: 0}
    step = 0
    while len(curr_gen) > 0:
        step += 1
        for p in curr_gen:
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = (p[0] + di) % rows, (p[1] + dj) % cols
                if (
                    0 <= ni < rows
                    and 0 <= nj <= cols
                    and map[ni][nj] != "#"
                    and (ni, nj) not in visited
                ):
                    # print(f'{p} -> {(ni, nj)} [{aval_step}]')
                    next_gen.add((ni, nj))
                    visited[ni, nj] = step
        curr_gen = next_gen
        next_gen = set()

    # print(curr_gen)
    even_corners = sum(1 for v in visited.values() if v % 2 == 0 and v > 65)
    odd_corners = sum(1 for v in visited.values() if v % 2 == 1 and v > 65)

    even_full = sum(1 for v in visited.values() if v % 2 == 0)
    odd_full = sum(1 for v in visited.values() if v % 2 == 1)

    n = (26501365 - cols // 2) // cols

    result = (
        (n + 1) ** 2 * odd_full
        + n**2 * even_full
        - (n + 1) * odd_corners
        + n * even_corners
    )
    print(result)


if __name__ == "__main__":
    main()
