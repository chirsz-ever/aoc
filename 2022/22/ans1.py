#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

reInst = re.compile(r'\d+|[RL]')

Coord = tuple[int, int]
GroveMap = dict[Coord, str]
Inst = str | int

def read_input(fname) -> tuple[GroveMap, list[Inst]]:
    gmap: GroveMap = dict()
    insts: list[Inst] = []
    mapping = True
    with open(fname) as fin:
        for row, l in enumerate(fin):
            l = l.rstrip()
            if len(l) == 0:
                mapping = False
                continue
            if mapping:
                for (col, c) in enumerate(l):
                    if c == ' ':
                        continue
                    assert c in ".#", f"{c=}"
                    gmap[(col, row)] = c
            else:
                for m in reInst.finditer(l):
                    inst = m[0]
                    if inst in "RL":
                        insts.append(inst)
                    else:
                        insts.append(int(inst))
    return gmap, insts

Edges = dict[int, tuple[int, int]]

def get_edges(gmap: GroveMap) -> tuple[Edges, Edges]:
    row_edges: Edges = {}
    col_edges: Edges = {}
    for x, y in gmap.keys():
        if e := row_edges.get(x):
            y0, y1 = e
            if y < y0:
                row_edges[x] = (y, y1)
            elif y > y1: 
                row_edges[x] = (y0, y)
        else:
            row_edges[x] = (y, y)
        if e := col_edges.get(y):
            x0, x1 = e
            if x < x0:
                col_edges[y] = (x, x1)
            elif x > x1: 
                col_edges[y] = (x0, x)
        else:
            col_edges[y] = (x, x)
    return row_edges, col_edges

f2n: dict[tuple[int, int], int] = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
}

def get_next(gmap: GroveMap, p: Coord, face: Coord, edge_row: Edges, edge_col: Edges) -> Coord:
    x, y = p
    dx, dy = face
    if dx == 0:
        yn = y + dy
        y0, y1 = edge_row[x]
        if yn < y0:
            yn = y1
        elif yn > y1:
            yn = y0
        return (x, yn)
    else:
        assert dy == 0, f"{dx=} {dy=}"
        xn = x + dx
        x0, x1 = edge_col[y]
        if xn < x0:
            xn = x1
        elif xn > x1:
            xn = x0
        return (xn, y)


def face_to_n(f: tuple[int, int]) -> int:
    return f2n[f]

def main():
    gmap, insts = read_input(inputFile)
    # for y in range(12):
    #     for x in range(16):
    #         c = gmap.get((x, y), ' ')
    #         print(c, end='')
    #     print()
    edge_row, edge_col = get_edges(gmap)
    p = (edge_col[0][0], 0)
    face = (1, 0)
    for inst in insts:
        # print(f"{p=}, {face=}")
        if inst == 'L':
            face = (face[1], -face[0])
        elif inst == 'R':
            face = (-face[1], face[0])
        else:
            assert isinstance(inst, int), f"{inst=}"
            for _ in range(inst):
                next_p = get_next(gmap, p, face, edge_row, edge_col)
                # print(f"{next_p=}, {gmap[next_p]=}")
                if gmap[next_p] == '.':
                    p = next_p
                else:
                    break
                # print(f"{p=}, {face=}")
    ans1 = 1000 * (p[1] + 1) + 4 * (p[0] + 1) + face_to_n(face)
    # print(f"{p=}, {face=}, {face_to_n(face)=}")
    print(ans1)

if __name__ == '__main__':
    main()
