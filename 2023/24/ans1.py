#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from collections import deque


@dataclass
class Vector:
    x: float
    y: float
    z: float = 0

def main() -> None:
    inputFile = sys.argv[1]
    range_min = int(sys.argv[2])
    range_max = int(sys.argv[3])

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

    count = 0

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            p1 = positions[i]
            v1 = velocities[i]
            p2 = positions[j]
            v2 = velocities[j]

            a1, b1, c1 = v1.y, -v1.x, p1.x * v1.y - p1.y * v1.x
            a2, b2, c2 = v2.y, -v2.x, p2.x * v2.y - p2.y * v2.x
            D = a1 * b2 - a2 * b1
            Dx = c1 * b2 - c2 * b1
            Dy = a1 * c2 - a2 * c1

            if D == 0:
                if Dx == Dy == 0:
                    count += line_pass(p1, v1, range_min, range_max)
                    # print(f'L{i} and L{j} are same, cross the area')
                else:
                    # print(f'L{i} and L{j} are parallel')
                    pass
            else:
                x = Dx / D
                y = Dy / D
                if range_min <= x <= range_max and range_min <= y <= range_max:
                    p = Vector(x, y)
                    t1 = sub(p, p1).x / v1.x if v1.x != 0 else sub(p, p1).y / v1.y
                    t2 = sub(p, p2).x / v2.x if v2.x != 0 else sub(p, p2).y / v2.y
                    if t1 >=0 and t2 >= 0:
                        count += 1
                    # print(f'L{i} and L{j} crossed at {(x, y)}, inside the area')
                else:
                    # print(f'L{i} and L{j} crossed at {(x, y)}, NOT inside the area')
                    pass
    print(count)

def line_pass(p: Vector, v: Vector, r_min: int, r_max: int) -> bool:
    c0 = cross2(v, sub(Vector(r_min, r_min), p))
    c1 = cross2(v, sub(Vector(r_min, r_max), p))
    c2 = cross2(v, sub(Vector(r_max, r_min), p))
    c3 = cross2(v, sub(Vector(r_max, r_max), p))

    cs = [c0, c1, c2, c3]
    return 0 in cs or not (all(c > 0 for c in cs) or all(c < 0 for c in cs))

def sub(v1: Vector, v2: Vector) -> Vector:
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def cross2(v1: Vector, v2: Vector) -> float:
    return v1.x * v2.y - v1.y * v2.x

if __name__ == "__main__":
    main()
