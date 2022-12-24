#!/usr/bin/env python3

import sys
from collections import deque

inputFile = "input"
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

class Blizzard:
    def __init__(self) -> None:
        self.position: tuple[int, int] = (0, 0)
        self.face: tuple[int, int] = (0, 0)
        self.char: str = ''

    def clone(self) -> 'Blizzard':
        b1 = Blizzard()
        b1.position = self.position
        b1.face = self.face
        b1.char = self.char
        return b1

class ValleyMap:
    def __init__(self) -> None:
        self.blizzs: list[Blizzard] = []
        self.width: int = 0
        self.height: int = 0
        self.start: tuple[int, int] = (0, 0)
        self.target: tuple[int, int] = (0, 0)
        self.blizz_cache: dict[tuple[int, int], list[Blizzard]] = dict()

    def clone(self) -> 'ValleyMap':
        m1 = ValleyMap()
        m1.width = self.width
        m1.height = self.height
        m1.blizzs = [b.clone() for b in self.blizzs]
        m1.start = self.start
        m1.target = self.target
        return m1

    def gne_blizz_cache(self) -> None:
        for b in self.blizzs:
            if bs := self.blizz_cache.get(b.position):
                bs.append(b)
            else:
                self.blizz_cache[b.position] = [b]

def read_input(fname) -> ValleyMap:
    vmap = ValleyMap()
    width = 0
    height = 0
    with open(fname) as fin:
        for row, l in enumerate(fin):
            l = l.rstrip()
            if len(l) == 0:
                continue
            height += 1
            if width == 0:
                width = len(l)
            assert width == len(l), f"{len(l)=}"
            for (col, c) in enumerate(l):
                if c in '.#':
                    continue
                assert c in "^v<>", f"{c=}"
                blizz = Blizzard()
                blizz.position = (col, row)
                blizz.char = c
                if c == '^':
                    blizz.face = (0, -1)
                elif c == 'v':
                    blizz.face = (0, 1)
                elif c == '<':
                    blizz.face = (-1, 0)
                else:
                    assert c == '>'
                    blizz.face = (1, 0)
                vmap.blizzs.append(blizz)
    vmap.width = width
    vmap.height = height
    vmap.start = (1, 0)
    vmap.target = (width - 2, height - 1)
    vmap.gne_blizz_cache()
    return vmap

def step(m: ValleyMap) -> ValleyMap:
    w = m.width
    h = m.height
    m1 = m.clone()
    for b in m1.blizzs:
        x = b.position[0] + b.face[0]
        y = b.position[1] + b.face[1]
        if x < 1:
            x = w - 2
        elif x > w - 2:
            x = 1
        if y < 1:
            y = h - 2
        elif y > h - 2:
            y = 1
        b.position = (x, y)
    m1.gne_blizz_cache()
    return m1

def check_blizz(m: ValleyMap, x: int, y: int) -> None | str:
    if bs := m.blizz_cache.get((x, y)):
        if len(bs) == 1:
            return bs[0].char
        else:
            return str(len(bs))
    return None

def get_time_map(time_map: list[ValleyMap], t: int) -> ValleyMap:
    if 0 <= t < len(time_map):
        return time_map[t]
    assert t == len(time_map)
    time_map.append(step(time_map[-1]))
    return time_map[-1]

def next_pos(m: ValleyMap, x: int, y: int) -> list[tuple[int, int]]:
    target = m.target
    start = m.start
    w = m.width
    h = m.height
    ps: list[tuple[int, int]] = []
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx = x + dx
        ny = y + dy
        if (nx, ny) in [start, target]:
            ps.append((nx, ny))
        elif 0 < nx < w - 1 and 0 < ny < h - 1:
            if not check_blizz(m, nx, ny):
                ps.append((nx, ny))
    ps.sort(key=lambda p: abs(p[0] - target[0]) + abs(p[1] - target[1]))
    # print(f"next_pos({x}, {y}) = {ps}")
    return ps

def print_vmap(m: ValleyMap):
    for y in range(m.height):
        for x in range(m.width):
            if (x, y) in [m.start, m.target]:
                print('.', end='')
            elif x == 0 or x == m.width - 1 or y == 0 or y == m.height - 1:
                print('#', end='')
            elif c := check_blizz(m, x, y):
                print(c, end='')
            else:
                print('.', end='')
        print()

def main() -> None:
    vmap0 = read_input(inputFile)
    time_map: list[ValleyMap] = [vmap0]
    # print_vmap(vmap0, target)
    queue: deque[tuple[int, tuple[int, int]]] = deque([(0, vmap0.start)])
    visited: set[tuple[int, tuple[int, int]]] = set()
    while len(queue) > 0:
        t, (x, y) = queue.popleft()
        # m = get_time_map(time_map, t)
        # if check_blizz(m, x, y):
        #     continue
        # print(f"{t}: {(x, y)}")
        m1 = get_time_map(time_map, t + 1)
        for nx, ny in next_pos(m1, x, y):
            if (nx, ny) == m1.target:
                print(t + 1)
                # for n, vmap in enumerate(time_map):
                #     print(f"{n}: ")
                #     print_vmap(vmap, target)
                exit(0)
            # if not (0 < nx < width - 1 and 0 < ny < height - 1):
            #     continue
            if (t + 1, (nx, ny)) not in visited:
                visited.add((t + 1, (nx, ny)))
                queue.append((t + 1, (nx, ny)))


if __name__ == '__main__':
    main()
