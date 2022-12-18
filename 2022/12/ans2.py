#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

class Input:
    def __init__(self) -> None:
        self.map: list[list[int]] = [[]]
        self.start: tuple[int, int] = (0, 0)
        self.target: tuple[int, int] = (0, 0)
        self.width: int = 0
        self.height: int = 0

    def at(self, p: tuple[int, int]) -> int:
        return self.map[p[0]][p[1]]


def read_input(fname: str) -> Input:
    input = Input()
    lines = []
    with open(fname) as fin:
        lines = [ l.strip() for l in fin if len(l.strip()) > 0 ]
    input.width = len(lines[0])
    input.height = len(lines)
    input.map = [[0 for _ in range(input.width)] for _ in range(input.height)]
    for y in range(input.height):
        for x in range(input.width):
            c = lines[y][x]
            h = ord(c) - ord('a')
            if c == 'S':
                h = 0
                input.start = (y, x)
            elif c == 'E':
                h = ord('z') - ord('a')
                input.target = (y, x)
            input.map[y][x] = h
    return input

input = read_input(inputFile)

def get_next(p: tuple[int, int]) -> list[tuple[int, int]]:
    y, x = p
    nexts: list[tuple[int, int]] = []
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        y1 = y + dy
        x1 = x + dx
        if 0 <= y1 < input.height and 0 <= x1 < input.width and input.map[y1][x1] - input.map[y][x] >= -1:
            nexts.append((y1, x1))
    return nexts

def bfs() -> tuple[tuple[int,int], dict[tuple[int, int], tuple[int, int]]]:
    visited = set()
    queue = [ input.target ]
    nearest_start = (0, 0)
    prev: dict[tuple[int, int], tuple[int, int]] = dict()
    while len(queue) > 0:
        p = queue.pop()
        if p in visited:
            continue
        visited.add(p)
        if input.at(p) == 0:
            nearest_start = p
            break
        for n in get_next(p):
            if n not in visited and n not in queue:
                queue.insert(0, n)
                prev[n] = p
    return nearest_start, prev 

nearest_start, prev = bfs()

cur = nearest_start
cnt = 0
path = [cur]
while cur != input.target:
    cur = prev[cur]
    path.append(cur)
    cnt += 1

path.reverse()

print(cnt)
# print(path)
