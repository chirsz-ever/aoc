#!/usr/bin/env python3

import sys
from itertools import combinations

Coord = tuple[int, int]
Image = list[str]

def count_empty(img: Image) -> tuple[list[int], list[int]]:
    empty_rows = []
    empty_cols = []
    for r, row in enumerate(img):
        if all(g == '.' for g in row):
            empty_rows.append(r)
    for c in range(len(img[0])):
        if all(img[r][c] == '.' for r in range(len(img))):
            empty_cols.append(c)
    return empty_rows, empty_cols

def find_galaxies(img: list[str]) -> list[Coord]:
    gs = []
    for r, row in enumerate(img):
        for c, g in enumerate(row):
            if g == '#':
                gs.append((r, c))
    return gs

def distance(empty_rows: set[int], empty_cols: set[int], x: Coord, y: Coord, EXPAND_RATIO: int) -> int:
    d = 0
    for r in range(min(x[0], y[0]), max(x[0], y[0])):
        if r in empty_rows:
            d += EXPAND_RATIO
        else:
            d += 1
    for c in range(min(x[1], y[1]), max(x[1], y[1])):
        if c in empty_cols:
            d += EXPAND_RATIO
        else:
            d += 1
    return d

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    EXPAND_RATIO = 2
    if len(sys.argv) >= 3:
        EXPAND_RATIO = int(sys.argv[2])

    image: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            image.append(l.strip())

    empty_rows, empty_cols = map(set, count_empty(image))
    galaxies = find_galaxies(image)
    # print(f'{empty_rows=}')
    # print(f'{empty_cols=}')
    # print(f'{galaxies=}')

    s = 0
    for x, y in combinations(galaxies, 2):
        s += distance(empty_rows, empty_cols, x, y, EXPAND_RATIO)
    print(f'{s=}')



if __name__ == '__main__':
    main()
