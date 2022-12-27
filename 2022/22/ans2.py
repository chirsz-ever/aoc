#!/usr/bin/env python3

from argparse import ArgumentParser
import re
from typing import Literal, Optional, cast
from math import gcd

def parse_args() -> tuple[str, str]:
    parser = ArgumentParser()
    parser.add_argument('input', default='input', nargs='?')
    parser.add_argument('input_info', default='input_info', nargs='?')
    n = parser.parse_args()
    return n.input, n.input_info

Coord = tuple[int, int]
Inst = str | int
Side = Literal["up", "down", "left", "right"]
Edges = dict[int, tuple[int, int]]
EdgeInfo = dict[tuple[Side, int], tuple[Side, int, bool]]
Face = Coord

reInfoLine = re.compile(r'(up|down|left|right)\s*(\d+)\s*(---|<->)\s*(up|down|left|right)\s*(\d+)')
reInst = re.compile(r'\d+|[RL]')

class GroveMap:
    def __init__(self) -> None:
        self.map: dict[Coord, str] = {}
        self.edges_col: Edges = {}
        self.edges_row: Edges = {}
        self.width: int = 0
        self.info: EdgeInfo = {}

    def __getitem__(self, p: Coord) -> str:
        return self.map.get(p, ' ')

    def set_edges(self) -> None:
        row_edges: Edges = {}
        col_edges: Edges = {}
        for x, y in self.map.keys():
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
        self.edges_row = row_edges
        self.edges_col = col_edges

def read_input(input: str, input_info: str) -> tuple[GroveMap, list[Inst]]:
    gmap = GroveMap()
    insts: list[Inst] = []
    mapping = True
    w = 0
    h = 0
    with open(input) as fin:
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
                    gmap.map[(col, row)] = c
                w = max(w, len(l))
                h += 1
            else:
                for m in reInst.finditer(l):
                    inst = m[0]
                    if inst in "RL":
                        insts.append(inst)
                    else:
                        insts.append(int(inst))
    gmap.set_edges()
    gmap.width = gcd(w, h)
    print(f"{w=}, {h=}, {gmap.width=}")
    info: EdgeInfo = {}
    with open(input_info) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            m = cast(re.Match[str], reInfoLine.match(l))
            assert m
            assert m[3] in ['<->', '---']
            e1, n1, e2, n2 = cast(Side, m[1]), int(m[2]), cast(Side, m[4]), int(m[5])
            reversed = m[3] == '<->'
            info[e1, n1] = (e2, n2, reversed)
            info[e2, n2] = (e1, n1, reversed)
    gmap.info = info
    return gmap, insts

def get_next(gmap: GroveMap, p: Coord, face: Face) -> tuple[Coord, Face]:
    x, y = p
    dx, dy = face
    side: Optional[Side] = None
    index: int = 0
    offset: int = 0
    next_face = face
    if dx == 0:
        next_x = x
        next_y = y + dy
        ymin, ymax = gmap.edges_row[x]
        if next_y < ymin:
            side = 'up'
        elif next_y > ymax:
            side = 'down'
        index = x // gmap.width
        offset = x % gmap.width
    else:
        assert dy == 0, f"{dx=} {dy=}"
        next_y = y
        next_x = x + dx
        xmin, xmax = gmap.edges_col[y]
        if next_x < xmin:
            side = 'left'
        elif next_x > xmax:
            side = 'right'
        index = y // gmap.width
        offset = y % gmap.width
    if side:
        next_side, next_index, reversed = gmap.info[side, index]
        next_offset = offset if not reversed else (gmap.width - 1 - offset)
        next_k = next_index * gmap.width + next_offset
        if next_side == 'up':
            next_x = next_k
            next_y = gmap.edges_row[next_k][0]
            next_face = (0, 1)
        elif next_side == 'down':
            next_x = next_k
            next_y = gmap.edges_row[next_k][1]
            next_face = (0, -1)
        elif next_side == 'left':
            next_x = gmap.edges_col[next_k][0]
            next_y = next_k
            next_face = (1, 0)
        else:
            assert next_side == 'right', f"{next_side=}"
            next_x = gmap.edges_col[next_k][1]
            next_y = next_k
            next_face = (-1, 0)
    return (next_x, next_y), next_face


f2n: dict[tuple[int, int], int] = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
}

def face_to_n(f: tuple[int, int]) -> int:
    return f2n[f]

def main():
    input, input_info = parse_args()
    gmap, insts = read_input(input, input_info)
    # for y in range(12):
    #     for x in range(16):
    #         c = gmap.get((x, y), ' ')
    #         print(c, end='')
    #     print()
    p = (gmap.edges_col[0][0], 0)
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
                next_p, next_face = get_next(gmap, p, face)
                # print(f"{next_p=}, {gmap[next_p]=}")
                next_ground = gmap[next_p]
                if next_ground == '.':
                    p = next_p
                    face = next_face
                else:
                    assert next_ground == '#', f"gmap[{next_p}] == '{next_ground}'"
                    break
                # print(f"{p=}, {face=}")
    ans1 = 1000 * (p[1] + 1) + 4 * (p[0] + 1) + face_to_n(face)
    print(f"{p=}, {face=}, {face_to_n(face)=}")
    print(ans1)

if __name__ == '__main__':
    main()
