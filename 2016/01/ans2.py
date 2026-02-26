#!/usr/bin/env python3

import sys
from typing import Iterable

def main() -> None:
    inputFile = sys.argv[1]

    with open(inputFile) as fin:
        insts = fin.read().split(', ')
    # print(insts)

    direct = (0, -1)
    coord = (0, 0)
    coords: set[tuple[int, int]] = { coord }

    coord_twice = (0, 0)
    for inst in insts:
        direct = turn(direct, inst[0])
        step = int(inst[1:])
        coord_old = coord
        coord = (coord[0] + direct[0] * step, coord[1] + direct[1] * step)
        # print(f'visit {coord}')
        coords_mid = [(i, j) for i in range_inclusive(coord_old[0], coord[0]) for j in range_inclusive(coord_old[1], coord[1])]
        # print(f'{coords_mid=}')

        find_coord_twice = False
        for c in coords_mid:
            if c != coord_old and c in coords:
                # print(f'find coord_twice: {c}')
                find_coord_twice = True
                coord_twice = c
                break
            coords.add(c)
        if find_coord_twice:
            break

    dist = abs(coord_twice[0]) + abs(coord_twice[1])
    print(coord_twice)
    print(dist)

def range_inclusive(a: int, b: int) -> Iterable[int]:
    if a <= b:
        return range(a, b + 1)
    else:
        return range(b, a + 1)


def turn(d: tuple[int, int], i: str) -> tuple[int, int]:
    x, y = d[0], d[1]
    if i == 'L':
        return (y, -x)
    elif i == 'R':
        return (-y, x)
    else:
        raise RuntimeError(i)

if __name__ == "__main__":
    main()
