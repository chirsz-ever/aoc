#!/usr/bin/env python3

import sys
from itertools import combinations

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    amap: list[tuple[int, int, str]] = []
    rows = 0
    cols = 0
    with open(inputFile) as fin:
        for r, l in enumerate(fin):
            if cols == 0:
                cols = len(l.strip())
            for c, n in enumerate(l.strip()):
                if n == '.':
                    continue
                amap.append((r, c, n))
            if len(l.strip()) > 0:
                rows = r + 1
    print(f'{rows=}, {cols=}')
    # freqs = { f for _, _, f in amap }
    freq_coords: dict[str, list[tuple[int, int]]] = {}
    for r, c, f in amap:
        if f not in freq_coords:
            coords = freq_coords[f] = []
        else:
            coords = freq_coords[f]
        coords.append((r, c))
    # print(f'{amap=}')
    # print(f'{freq_coords=}')

    antinodes: set[tuple[int, int]] = set()
    for f, coords in freq_coords.items():
        for a, b in combinations(coords, 2):
            c1 = (2 * a[0] - b[0], 2 * a[1] - b[1])
            c2 = (2 * b[0] - a[0], 2 * b[1] - a[1])
            # print(f'{f=}, {a=}, {b=}, {c1=}, {c2=}')
            if 0 <= c1[0] < rows and 0 <= c1[1] < cols:
                antinodes.add(c1)
            if 0 <= c2[0] < rows and 0 <= c2[1] < cols:
                antinodes.add(c2)
    print(f'{len(antinodes)=}')

if __name__ == '__main__':
    main()
