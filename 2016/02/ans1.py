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

    cx, cy = 1, 1

    for l in lines:
        for d in l:
            dx, dy = direct[d]
            cx = clamp(cx + dx, 0, 2)
            cy = clamp(cy + dy, 0, 2)
        print(coord2num(cx, cy), end='')
    print()


direct = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def clamp(x, minVal, maxVal):
    return min(maxVal, max(x, minVal))


def coord2num(x: int, y: int) -> int:
    return y * 3 + x + 1


if __name__ == "__main__":
    main()
