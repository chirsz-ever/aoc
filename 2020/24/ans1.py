from sys import stdin
from typing import Tuple, List, TextIO
from collections import namedtuple, Counter
import re

class Vec3(namedtuple('Vec3', 'x y z', defaults=(0, 0, 0))):
    __slots__ = ()
    def __add__(self, rhs):
        return Vec3(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)
        

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

def parse_input(f: TextIO) -> List[Vec3]:
    return [parse_line(line) for line in map(str.strip, f) if line]

def norm(v: Vec3) -> Vec3:
    m = min(v.x, v.y, v.z)
    return Vec3(v.x - m, v.y - m, v.z - m)

def main():
    cnts = Counter(norm(vs) for vs in parse_input(stdin))
    #print(f"{cnts=}")
    blacks = sum(1 for _, c in cnts.items() if c % 2 == 1)
    print(f"{blacks=}")

if __name__ == '__main__':
    main()
