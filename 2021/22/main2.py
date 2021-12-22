#!/usr/bin/env python3

from collections import defaultdict
from itertools import product

import sys
import re
from typing import Iterable, Optional


def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default


inputFile = getArg(1, "input")
# print(f'{inputFile = }')

Range = tuple[int, int]
Cube = tuple[Range, Range, Range]
Pos = tuple[int, int, int]


def rangeSize(r: Range) -> int:
    return r[1] - r[0] + 1


def genRange(r1: Range, r2: Range, p: int) -> Optional[Range]:
    a = 0
    b = 0
    if p < 0:
        if r2[0] <= r1[0]:
            return None
        a = r1[0]
        b = r2[0] - 1
    elif p == 0:
        if r2[0] > r1[1] or r2[1] < r1[0]:
            return None
        a = max(r1[0], r2[0])
        b = min(r1[1], r2[1])
    else:
        if r2[1] >= r1[1]:
            return None
        a = r2[1] + 1
        b = r1[1]
    assert b >= a
    # print(f"{r1} - {r2} with {p} = {(a, b)}")
    return (a, b)


def cubeSize(cube: Cube) -> int:
    rx, ry, rz = cube
    return rangeSize(rx) * rangeSize(ry) * rangeSize(rz)


def cubeDiff(c1: Cube, c2: Cube) -> set[Cube]:
    subCubes: set[Cube] = set()
    for px, py, pz in product([0, -1, 1], repeat=3):
        if (
            (rx := genRange(c1[0], c2[0], px))
            and (ry := genRange(c1[1], c2[1], py))
            and (rz := genRange(c1[2], c2[2], pz))
        ):
            if (px, py, pz) == (0, 0, 0):
                continue
            sc = (rx, ry, rz)
            subCubes.add(sc)
        elif (px, py, pz) == (0, 0, 0):
            return subCubes
    # print(f"{c1} - {c2} = {subCubes}")
    return subCubes


def cubesDiff(cubes: Iterable[Cube], dc: Cube) -> set[Cube]:
    result: set[Cube] = set()
    for cube in cubes:
        cs = cubeDiff(cube, dc)
        print(f"{cube} - {dc} = {cs}")
        result.update(cs)
    return result


reLine = re.compile(
    r"(off|on) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
)
insts: list[tuple[bool, Cube]] = []
with open(inputFile) as fin:
    for line in fin:
        if m := reLine.match(line):
            onOff = m[1] == "on"
            rx = (int(m[2]), int(m[3]))
            ry = (int(m[4]), int(m[5]))
            rz = (int(m[6]), int(m[7]))
            insts.append((onOff, (rx, ry, rz)))

onCubes: set[Cube] = set()
for on, cube in insts:
    if on:
        newOnCubes = {cube}
        for onCube in onCubes:
            newOnCubes = cubesDiff(newOnCubes, onCube)
            if len(newOnCubes) == 0:
                break
        print(f"{newOnCubes = }")
        onCubes.update(newOnCubes)
    else:
        onCubes = cubesDiff(onCubes, cube)
    print(f"{onCubes = }")
    print(f"{sum(cubeSize(cube) for cube in onCubes) = }")


print(f"{sum(cubeSize(cube) for cube in onCubes) = }")
