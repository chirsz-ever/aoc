#!/usr/bin/env python3

import sys
from itertools import combinations

def expand(img: list[str]) -> list[list[str]]:
    eimg = [[c for c in l] for l in img]
    r = 0
    while r < len(eimg):
        if all(c == '.' for c in eimg[r]):
            eimg.insert(r, eimg[r].copy())
            r += 2
        else:
            r += 1
    c = 0
    while c < len(eimg[0]):
        if all(eimg[r][c] == '.' for r in range(len(eimg))):
            for row in eimg:
                row.insert(c, '.')
            c += 2
        else:
            c += 1
    return eimg

def print_img(img: list[list[str]]):
    for l in img:
        for c in l:
            print(c, end='')
        print()

Coord = tuple[int, int]

def find_galaxies(img: list[list[str]]) -> list[Coord]:
    gs = []
    for r, row in enumerate(img):
        for c, g in enumerate(row):
            if g == '#':
                gs.append((r, c))
    return gs

def distance(x: Coord, y: Coord) -> int:
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

def main():
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    image: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            image.append(l.strip())

    expanded_image = expand(image)
    # print_img(expanded_image)

    galaxies = find_galaxies(expanded_image)
    s = 0
    for x, y in combinations(galaxies, 2):
        s += distance(x, y)
    print(f'{s=}')



if __name__ == '__main__':
    main()
