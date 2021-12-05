from sys import stdin
from enum import Enum
from typing import Tuple, Dict, Iterable
from itertools import product

Status = Enum('Status', 'Active Inactive')
Coord = Tuple[int, int, int, int]
Map = Dict[Coord, Status]

def rule(g: Status, n: int) -> Status:
    if g == Status.Active and 2 <= n <= 3:
        return Status.Active
    elif g == Status.Inactive and n == 3:
        return Status.Active
    else:
        return Status.Inactive

def readmap(m: Map, c: Coord) -> Status:
    return m.get(c, Status.Inactive)

def neighbers(m: Map, c: Coord) -> Iterable[Coord]:
    x, y, z, w = c
    for dx, dy, dz, dw in product([-1, 0, 1], repeat=4):
        if any([dx, dy, dz, dw]):
            yield (x + dx, y + dy, z + dz, w + dw)

def countneighbers(m: Map, c: Coord) -> int:
    cnt = 0
    for nc in neighbers(m, c):
        if readmap(m, nc) == Status.Active:
            cnt += 1
    return cnt

def stepgrid(m: Map, nm: Map, c: Coord):
    if rule(readmap(m, c), countneighbers(m, c)) == Status.Active:
        nm[c] = Status.Active

def step(m: Map) -> Map:
    nm: Map = {}
    for c, g in m.items():
        stepgrid(m, nm, c)
        if g == Status.Active:
            for nc in neighbers(m, c):
                stepgrid(m, nm, nc)
    return nm

def c2g(c: str) -> Status:
    if c == '#':
        return Status.Active
    else:
        return Status.Inactive

def parse_map(s: str) -> Map:
    m: Map = {}
    for y, l in enumerate(s.splitlines()):
        for x, c in enumerate(l):
            m[x, y, 0, 0] = c2g(c)
    return m

def main():
    m = parse_map(stdin.read())
    for _ in range(6):
        m = step(m)
    actives = sum(1 for a in m.values() if a == Status.Active)
    print(f'{actives}')

if __name__ == '__main__':
    main()
