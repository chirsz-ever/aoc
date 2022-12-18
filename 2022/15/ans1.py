#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

test_y = 2000000
if len(sys.argv) >= 3:
    test_y = int(sys.argv[2])

reLine = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

def read_input(fname) -> dict[tuple[int, int], tuple[int, int]]:
    sensors: dict[tuple[int, int], tuple[int, int]] = dict()
    with open(fname) as fin:
        for l in fin:
            if m := reLine.match(l):
                sx, sy, bx, by = map(int, [m[1], m[2], m[3], m[4]])
                sensors[sx, sy] = (bx, by)
    return sensors

def myrange(a, b):
    if a > b:
        a, b = b, a
    return range(a, b + 1)

sensors = read_input(inputFile)
beacons = set(sensors.values())

# print(sensors)

exclude_xs: set[int] = set()

for s, b in sensors.items():
    sx, sy = s
    md = abs(sx - b[0]) + abs(sy - b[1])
    dy = abs(sy - test_y)
    if dy > md:
        continue
    dx = md - dy
    for x in myrange(sx - dx, sx + dx):
        if (x, test_y) not in beacons:
            exclude_xs.add(x)

print(len(exclude_xs))
