#!/usr/bin/env python3

import sys
import re
from typing import Optional
from pathlib import Path

# inputFile = str(Path(__file__).parent / 'test')
inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

# w = 20
w = 4000000
if len(sys.argv) >= 3:
    w = int(sys.argv[2])

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

exclude_xranges: list[list[tuple[int, int]]] = [[] for _ in range(w + 1)]

# def merge_range(ranges: list[tuple[int, int]], a: int, b: int):
#     a = max(a, 0)
#     b = min(b, w)
#     assert a <= b
#     if len(ranges) == 0:
#         ranges.append((a, b))
#         return
#     for i, (ai, bi) in enumerate(ranges):
#         if a > bi + 1:
#             continue
#         elif b < ai - 1:
#             ranges.insert(i, (a, b))
#             return
#         elif ai - 1 <= b <= bi:
#             ranges[i] = (min(a, ai), bi)
#             return
#         else:
#             end: Optional[int] = None
#             maxbj = 0
#             for j in range(i + 1, len(ranges)):
#                 aj, bj = ranges[j]
#                 maxbj = bj
#                 if aj > b:
#                     end = j
#                     break
#             if end is None:
#                 del ranges[i:]
#                 ranges.append((min(a, ai), max(b, maxbj)))
#             else:
#                 b = max(b, ranges[end-1][1])
#                 del ranges[i:end]
#                 ranges.insert(i + 1, (min(a, ai), b))
#             return
#     ranges.append((a, b))

def merge_range(ranges: list[tuple[int, int]], a: int, b: int):
    a = max(a, 0)
    b = min(b, w)
    assert a <= b
    if len(ranges) == 0:
        ranges.append((a, b))
        return
    ranges.append((a, b))
    ranges.sort(key=lambda t: t[0])
    i = 0
    while i < len(ranges) - 1:
        ai, bi = ranges[i]
        ai1, bi1 = ranges[i + 1]
        if bi >= ai1 - 1:
            ranges[i] = (ai, max(bi, bi1))
            del ranges[i + 1]
        else:
            i += 1

for (sx, sy), b in sensors.items():
    md = abs(sx - b[0]) + abs(sy - b[1])
    for y in myrange(max(sy - md, 0), min(sy + md, w)):
        dx = md - abs(sy - y)
        # print(f"merge range ({sx-dx}, {sx + dx}) on line {y}")
        if y == 9:
            pass
        merge_range(exclude_xranges[y], sx - dx, sx + dx)

def output_coord(x, y):
    print(f"({x}, {y}): {x * w + y}")

for y, xr in enumerate(exclude_xranges):
    for i, (ai, bi) in enumerate(xr):
        if i == 0 and ai != 0:
            # print(f"(0-{ai-1}, {y})")
            for x in range(0, ai):
                output_coord(x, y)
        if i > 0:
            # print(f"({xr[i - 1][1] + 1}-{ai-1}, {y})")
            for x in range(xr[i - 1][1] + 1, ai):
                output_coord(x, y)
        if i == len(xr) - 1 and bi != w:
            # print(f"({bi + 1}-{w-1}, {y})")
            for x in range(bi + 1, w + 1):
                output_coord(x, y)

# print(exclude_xranges)
