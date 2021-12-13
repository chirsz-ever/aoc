#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

points: list[tuple[int, int]] = []
foldSteps: list[tuple[str, int]] = []
rePoint = re.compile(r'(\d+),(\d+)')
reFold = re.compile(r'fold along ([xy])=(\d+)')
with open(inputFile) as fin:
    for line in fin:
        if m := rePoint.match(line):
            points.append((int(m[1]), int(m[2])))
        elif m := reFold.match(line):
            foldSteps.append((m[1], int(m[2])))

width = max(x for x, _ in points) + 1
height = max(y for _, y in points) + 1

def doFoldX(points: list[tuple[int, int]], fx: int) -> list[tuple[int, int]]:
    return [(2 * fx - x, y) if x > fx else (x, y) for x, y in points]


def doFoldY(points: list[tuple[int, int]], fy: int) -> list[tuple[int, int]]:
    return [(x, 2 * fy - y) if y > fy else (x, y) for x, y in points]

def doFold(points: list[tuple[int, int]], f: tuple[str, int], w: int, h: int) -> tuple[list[tuple[int, int]], int, int]:
    if f[0] == 'x':
        return doFoldX(points, f[1]), w // 2, h
    elif f[0] == 'y':
        return doFoldY(points, f[1]), w, h // 2
    else:
        print("ERROR!")
        exit()

def showPoints(points: list[tuple[int, int]], w: int, h: int):
    for i in range(h):
        for j in range(w):
            if (j, i) in points:
                print('@', end='')
            else:
                print(' ', end='')
        print()

p, w, h = points, width, height
for step in foldSteps:
    p, w, h = doFold(p, step, w, h)
    p = list(set(p))

showPoints(p, w, h)
