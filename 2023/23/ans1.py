#!/usr/bin/env python3

import sys

Coord = tuple[int, int]

tile_to_didjs: dict[str, list[Coord]] = {
    '.': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    '^': [(-1,  0)],
    'v': [( 1,  0)],
    '<': [( 0, -1)],
    '>': [( 0,  1)],
}

def main() -> None:
    inputFile = sys.argv[1]

    map: list[str] = []
    start: Coord = (0, 0)
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            map.append(l)
    rows = len(map)
    cols = len(map[0])
    start = (0, 1)
    end = (rows-1, cols-2)

    visited: set[Coord] = set()

    def get_next_coords(p: Coord) -> list[Coord]:
        ncs = []
        for di, dj in tile_to_didjs[map[p[0]][p[1]]]:
            ni, nj = p[0] + di, p[1] + dj
            if 0 <= ni < rows and 0 <= nj < cols and map[ni][nj] != '#' and (ni, nj) not in visited:
                # print(f'{p} -> {(ni, nj)} [{aval_step}]')
                ncs.append((ni, nj))
        return ncs

    max_path_length = 0
    def visit(p: Coord, step: int) -> None:
        nonlocal max_path_length
        if p == end:
            # print(f'founf end: {step=}')
            max_path_length = max(max_path_length, step)
            return

        p0 = p
        visited.add(p)
        ncs = get_next_coords(p)
        advanced: list[Coord] = []
        while len(ncs) == 1:
            n = ncs[0]
            if n == end:
                # print(f'found end: when advance {p0}, {len(advanced)=}')
                max_path_length = max(max_path_length, step + len(advanced) + 1)
                ncs = []
                break
            visited.add(n)
            advanced.append(n)
            p = n
            ncs = get_next_coords(n)

        if len(ncs) > 1:
            # print(f'{p0} advanced {len(advanced)}, split: {p} -> {ncs}')
            for n in ncs:
                visit(n, step + len(advanced) + 1)

        visited.remove(p0)
        visited.difference_update(advanced)

    visit(start, 0)
    assert len(visited) == 0, visited
    print(max_path_length)

    # for i in range(rows):
    #     for j in range(cols):
    #         if (i, j) in targets:
    #             print('O', end='')
    #         else:
    #             print(map[i][j], end='')
    #     print()

if __name__ == '__main__':
    main()
