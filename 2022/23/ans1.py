#!/usr/bin/env python3

import sys
from itertools import count
from collections import Counter
import math

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

Coord = tuple[int, int]

def read_input(fname) -> set[Coord]:
    elves: set[Coord] = set()
    with open(fname) as fin:
        for row, l in enumerate(fin):
            l = l.rstrip()
            for col, c in enumerate(l):
                if c == '#':
                    elves.add((col, row))
    return elves

def no_neighbor(elves: set[Coord], x: int, y: int) -> bool:
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == dy == 0:
                continue
            if (x + dx, y + dy) in elves:
                return False
    return True

directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def can_move(elves: set[Coord], x: int, y: int, dx: int, dy: int) -> bool:
    if dx == 0:
        for dx1 in [-1, 0, 1]:
            if (x + dx1, y + dy) in elves:
                return False
    else:
        assert dy == 0
        for dy1 in [-1, 0, 1]:
            if (x + dx, y + dy1) in elves:
                return False
    return True

def step(elves: set[Coord], i: int) -> tuple[set[Coord], bool]:
    targets: dict[Coord, Coord] = dict()
    moved = False
    for x, y in elves:
        if no_neighbor(elves, x, y):
            targets[x, y] = (x, y)
            # print(f"{(x,y)} no neighbor")
            continue
        for k in range(i, i + 4):
            dx, dy = directions[k % 4]
            if can_move(elves, x, y, dx, dy):
                # print(f"{(x,y)} can move to {(x + dx, y + dy)}")
                targets[x, y] = (x + dx, y + dy)
                moved = True
                break
        if (x, y) not in targets.keys():
            targets[x, y] = (x, y)
    if not moved:
        return elves, moved
    new_elves = set()
    conflict_targets = { k for k, v in Counter(targets.values()).items() if v > 1 }
    for x, y in elves:
        t = targets[x, y]
        if t not in conflict_targets:
            # print(f"{(x,y)} move to {t}")s
            new_elves.add(t)
        else:
            new_elves.add((x, y))
    return new_elves, moved

def get_edges(elves: set[Coord]) -> tuple[int, int, int, int]:
    l, r, u, d = math.inf, -math.inf, math.inf, -math.inf
    for x, y in elves:
        l = min(x, l)
        r = max(x, r)
        u = min(y, u)
        d = max(y, d)
    return int(l), int(r), int(u), int(d)

def main():
    elves = read_input(inputFile)
    # print(elves)
    for i in count():
        elves, moved = step(elves, i)
        if not moved:
            break
        # l, r, u, d = get_edges(elves)
        # for y in range(u, d + 1):
        #     for x in range(l, r + 1):
        #         print('#' if (x, y) in elves else '.', end='')
        #     print()
        # print()
        if i == 9:
            l, r, u, d = get_edges(elves)
            # print(l, r, u, d)
            print((r - l + 1) * (d - u + 1) - len(elves))
    print(i + 1)


if __name__ == '__main__':
    main()
