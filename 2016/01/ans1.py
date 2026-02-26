#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = sys.argv[1]

    with open(inputFile) as fin:
        insts = fin.read().split(', ')
    # print(insts)

    direct = (0, -1)
    coord = (0, 0)

    for inst in insts:
        direct = turn(direct, inst[0])
        step = int(inst[1:])
        coord = (coord[0] + direct[0] * step, coord[1] + direct[1] * step)

    dist = abs(coord[0]) + abs(coord[1])
    print(coord)
    print(dist)



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
