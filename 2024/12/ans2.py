#!/usr/bin/env python3

import sys
from dataclasses import dataclass, field
from itertools import product

@dataclass
class Region:
    plant: str
    area: int = 0
    edges: list[tuple[int, int, int, int]] = field(default_factory=list)

def main() -> None:
    inputFile = sys.argv[1]

    with open(inputFile) as fin:
        garden: list[str] = [l.strip() for l in fin if len(l.strip()) > 0]

    rows = len(garden)
    cols = len(garden[0])

    visited = [ [False] * cols for _ in range(rows) ]

    def visit_region(i: int, j: int, region: Region) -> None:
        visited[i][j] = True
        region.area += 1
        for di, dj in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            ii = i + di
            jj = j + dj
            if not (0 <= ii < rows and 0 <= jj < cols) or garden[ii][jj] != region.plant:
                region.edges.append((i, j, di, dj))
        
        for di, dj in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            ii = i + di
            jj = j + dj
            if 0 <= ii < rows and 0 <= jj < cols and not visited[ii][jj] and garden[ii][jj] == region.plant:
                visit_region(ii, jj, region)

    regions: list[Region] = []
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                region = Region(garden[i][j])
                regions.append(region)
                visit_region(i, j, region)

    s = 0
    for r in regions:
        cnt_e = count_edges(r.edges)
        # print(f'Region {r.plant}: {r.area} * {cnt_e} = {r.area * cnt_e}')
        s += r.area * cnt_e
    print(f'{s=}')

def count_edges(edges: list[tuple[int, int, int, int]]) -> int:
    eset = set(edges)
    cnt = 0
    while len(eset) > 0:
        ei, ej, di, dj = eset.pop()
        cnt += 1
        if di == 0:
            i = ei + 1
            while (i, ej, di, dj) in eset:
                eset.remove((i, ej, di, dj))
                i += 1
            i = ei - 1
            while (i, ej, di, dj) in eset:
                eset.remove((i, ej, di, dj))
                i -= 1
        else:
            assert dj == 0
            j = ej + 1
            while (ei, j, di, dj) in eset:
                eset.remove((ei, j, di, dj))
                j += 1
            j = ej - 1
            while (ei, j, di, dj) in eset:
                eset.remove((ei, j, di, dj))
                j -= 1
    return cnt

if __name__ == '__main__':
    main()
