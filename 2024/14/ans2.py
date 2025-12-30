#!/usr/bin/env python3

import sys
import os
from dataclasses import dataclass
import re

@dataclass
class Robot:
    p: tuple[int, int]
    v: tuple[int, int]

reRobot = re.compile(r'p=([-\d]+),([-\d]+) v=([-\d]+),([-\d]+)')

def main() -> None:
    inputFile = sys.argv[1]
    n = int(sys.argv[2])

    robots: list[Robot] = []
    with open(inputFile) as fin:
        for l in fin:
            if m := reRobot.match(l):
                px, py, vx, vy = int(m[1]), int(m[2]), int(m[3]), int(m[4])
                robots.append(Robot((px, py), (vx, vy)))
    # print(robots)
    width = 101
    height = 103

    for t in range(0, n):
        print(f'---------- {t=} ----------')
        ps = set()
        for r in robots:
            px = (r.p[0] + r.v[0] * t) % width
            py = (r.p[1] + r.v[1] * t) % height
            ps.add((px, py))

        for y in range(0, height):
            for x in range(0, width):
                if (x, y) in ps:
                    print('*', end='')
                else:
                    print('.', end='')
            print()

if __name__ == '__main__':
    main()
