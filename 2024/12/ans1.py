#!/usr/bin/env python3

import sys
from dataclasses import dataclass

@dataclass
class Region:
    plant: str
    area: int = 0
    perimeter: int = 0

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
            if not (0 <= ii < rows and 0 <= jj < cols):
                region.perimeter += 1
            elif garden[ii][jj] != region.plant:
                region.perimeter += 1
        
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
        # print(f'Region {r.plant}: {r.area} * {r.perimeter} = {r.area * r.perimeter}')
        s += r.area * r.perimeter
    print(f'{s=}')

if __name__ == '__main__':
    main()
