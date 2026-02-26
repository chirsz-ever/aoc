#!/usr/bin/env python3

import sys


def main() -> None:
    inputFile = sys.argv[1]

    lines: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            lines.append(l)

    cx, cy = 0, 2

    for l in lines:
        for d in l:
            dx, dy = direct[d]
            nx, ny = cx + dx, cy + dy
            if (nx, ny) in coord2code:
                cx, cy = nx, ny
        print(coord2code[cx, cy], end='')
    print()


direct = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


coord2code = {
    (2, 0): 1,
    (1, 1): 2,
    (2, 1): 3,
    (3, 1): 4,
    (0, 2): 5,
    (1, 2): 6,
    (2, 2): 7,
    (3, 2): 8,
    (4, 2): 9,
    (1, 3): 'A',
    (2, 3): 'B',
    (3, 3): 'C',
    (2, 4): 'D',
}


if __name__ == "__main__":
    main()
