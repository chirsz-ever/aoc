#!/usr/bin/env python3

import sys
from dataclasses import dataclass
import re

@dataclass
class Robot:
    p: tuple[int, int]
    v: tuple[int, int]

reRobot = re.compile(r'p=([-\d]+),([-\d]+) v=([-\d]+),([-\d]+)')

def main() -> None:
    inputFile = sys.argv[1]

    robots: list[Robot] = []
    with open(inputFile) as fin:
        for l in fin:
            if m := reRobot.match(l):
                px, py, vx, vy = int(m[1]), int(m[2]), int(m[3]), int(m[4])
                robots.append(Robot((px, py), (vx, vy)))
    # print(robots)
    width = 101
    height = 103

    # width = 11
    # height = 7

    hw = width // 2
    hh = height // 2
    q = [0, 0, 0, 0]

    for r in robots:
        px = (r.p[0] + r.v[0] * 100) % width
        py = (r.p[1] + r.v[1] * 100) % height

        if px < hw and py < hh:
            q[0] += 1
        elif px > hw and py < hh:
            q[1] += 1
        elif px < hw and py > hh:
            q[2] += 1
        elif px > hw and py > hh:
            q[3] += 1

    print(q)
    print(q[0]*q[1]*q[2]*q[3])

if __name__ == '__main__':
    main()
