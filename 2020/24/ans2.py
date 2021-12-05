from sys import stdin
from enum import Enum
from typing import Tuple, List, Dict, TextIO, Iterable
from collections import namedtuple, Counter
import re

class Vec3(namedtuple('Vec3', 'x y z', defaults=(0, 0, 0))):
    __slots__ = ()
    def __add__(self, rhs):
        return Vec3(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)

    def norm(self):
        v = self
        m = min(v.x, v.y, v.z)
        return Vec3(v.x - m, v.y - m, v.z - m)

Status = Enum('Status', 'Black White')
Coord = Vec3
Map = Dict[Coord, Status]

def rule(g: Status, n: int) -> Status:
    if g == Status.Black and (n ==0 or n > 2):
        return Status.White
    elif g == Status.White and n == 2:
        return Status.Black
    else:
        return g

def readmap(m: Map, c: Coord) -> Status:
    return m.get(c, Status.White)

def neighbers(m: Map, c: Coord) -> Iterable[Coord]:
    for dv in d2v.values():
        yield (c + dv).norm()

def adjacent_blacks(m: Map, c: Coord) -> int:
    cnt = 0
    for nc in neighbers(m, c):
        if readmap(m, nc) == Status.Black:
            cnt += 1
    return cnt

def stepgrid(m: Map, nm: Map, c: Coord):
    if rule(readmap(m, c), adjacent_blacks(m, c)) == Status.Black:
        nm[c] = Status.Black

def step(m: Map) -> Map:
    nm: Map = {}
    for c, g in m.items():
        stepgrid(m, nm, c)
        if g == Status.Black:
            for nc in neighbers(m, c):
                stepgrid(m, nm, nc)
    return nm

d_re = re.compile(r'w|e|[ns][we]')

d2v = {
    'e' : Vec3( 1, 0, 0),
    'nw': Vec3( 0, 1, 0),
    'sw': Vec3( 0, 0, 1),
    'w' : Vec3(-1, 0, 0),
    'se': Vec3( 0,-1, 0),
    'ne': Vec3( 0, 0,-1),
}

def parse_line(line: str) -> Vec3:
    v = Vec3()
    for m in d_re.finditer(line):
        v += d2v[m[0]]
    return v

def parse_map(f: TextIO) -> Map:
    cnts = Counter(parse_line(line).norm() for line in map(str.strip, f) if line)
    return {v: Status.Black if c % 2 == 1 else Status.White for v, c in cnts.items()}

def main():
    m = parse_map(stdin)
    for _ in range(100):
        m = step(m)
    blacks = sum(1 for a in m.values() if a == Status.Black)
    print(f'{blacks=}')

if __name__ == '__main__':
    main()
