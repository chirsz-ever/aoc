#!/usr/bin/env python3

import sys
from dataclasses import dataclass

@dataclass
class Vector:
    x: float
    y: float
    z: float

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, a: float) -> Vector:
        return Vector(self.x * a, self.y * a, self.z * a)

    def __truediv__(self, a: float) -> Vector:
        return Vector(self.x / a, self.y / a, self.z / a)

    def product(self, o: Vector) -> float:
        return self.x * o.x + self.y * o.y + self.z * o.z

    def cross(self, o: Vector) -> Vector:
        return Vector(self.y * o.z - self.z * o.y, self.z * o.x - self.x * o.z, self.x * o.y - self.y * o.x)

    def triple_product(self: Vector, b: Vector, c: Vector) -> float:
        return self.cross(b).product(c)

def main() -> None:
    inputFile = sys.argv[1]

    positions: list[Vector] = []
    velocities: list[Vector] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            ps, vs = [[int(x) for x in p.split(", ")] for p in l.split(" @ ")]
            p = Vector(*ps)
            v = Vector(*vs)
            positions.append(p)
            velocities.append(v)
    # print(positions)
    # print(velocities)

    # https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kxqjg33
    p1 = positions[1] - positions[0]
    p2 = positions[2] - positions[0]
    v1 = velocities[1] - velocities[0]
    v2 = velocities[2] - velocities[0]
    t1 = v2.triple_product(p1, p2) / p2.triple_product(v1, v2)
    t2 = v1.triple_product(p1, p2) / p1.triple_product(v1, v2)

    c1 = positions[1] + velocities[1] * t1
    c2 = positions[2] + velocities[2] * t2
    v = (c2 - c1) / (t2 - t1)
    p = c1 - v * t1

    print(f'{t1=}')
    print(f'{t2=}')
    print(f'{v=}')
    print(f'{p=}')
    print(f'{p.x+p.y+p.z=}')

def sub(v1: Vector, v2: Vector) -> Vector:
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def cross2(v1: Vector, v2: Vector) -> float:
    return v1.x * v2.y - v1.y * v2.x

if __name__ == "__main__":
    main()
