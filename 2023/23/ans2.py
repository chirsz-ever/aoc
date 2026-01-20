#!/usr/bin/env python3

import sys
from dataclasses import dataclass

Coord = tuple[int, int]

@dataclass
class SegmentInfo:
    pair: Coord
    prev: Coord | None
    length: int

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
    seg_info: dict[Coord, SegmentInfo] = {}

    def is_visited(c: Coord) -> bool:
        p = seg_info.get(c)
        return c in visited or (p is not None and p.pair in visited)

    def get_next_coords(prev: Coord, c: Coord) -> list[Coord]:
        ncs = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = c[0] + di, c[1] + dj
            if 0 <= ni < rows and 0 <= nj < cols and map[ni][nj] != '#' and (ni, nj) != prev:
                # print(f'{p} -> {(ni, nj)} [{aval_step}]')
                ncs.append((ni, nj))
        return ncs

    max_path_length = 0
    def visit(prev: Coord, c: Coord, step: int) -> None:
        # print(f'visit {c} from {prev}')
        nonlocal max_path_length
        if c == end:
            max_path_length = max(max_path_length, step)
            return

        sinfo = seg_info.get(c)
        if sinfo is None:
            ncs = get_next_coords(prev, c)
            if len(ncs) == 1:
                advanced: list[Coord] = []
                c1 = c
                while len(ncs) == 1:
                    advanced.append(c1)
                    c1, ncs = ncs[0], get_next_coords(c1, ncs[0])
                p = advanced[-1]
                sinfo = seg_info[c] = SegmentInfo(p, advanced[1], len(advanced))
                seg_info[p] = SegmentInfo(c, advanced[-2], len(advanced))
            else:
                sinfo = seg_info[c] = SegmentInfo(c, None, 1)

        if sinfo.pair == end:
            # print(f'found end: {step=}')
            max_path_length = max(max_path_length, step + sinfo.length - 1)
            return

        if sinfo.length > 1 and prev != sinfo.prev:
            psinfo = seg_info[sinfo.pair]
            assert psinfo.prev
            visited.add(c)
            visit(psinfo.prev, sinfo.pair, step + sinfo.length - 1)
            visited.remove(c)
        else:
            # assert sinfo.length == 1
            visited.add(c)
            for n in get_next_coords(prev, c):
                if not is_visited(n):
                    visit(c, n, step + 1)
                # else:
                    # print(f'skip {n}')
            visited.remove(c)


    visit((-1, 1), start, 0)
    # assert len(visited) == 0, visited
    print(max_path_length)
    # print(f'size: {len(visited)}')
    # for c in visited:
    #     sinfo = seg_info[c]
    #     # if sinfo.length != 1:
    #     print(f'{c} -- {sinfo.pair}, len = {sinfo.length}')

    # for i in range(rows):
    #     for j in range(cols):
    #         if (i, j) in targets:
    #             print('O', end='')
    #         else:
    #             print(map[i][j], end='')
    #     print()

if __name__ == '__main__':
    main()
