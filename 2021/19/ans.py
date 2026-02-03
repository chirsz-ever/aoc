#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Iterable, overload
from itertools import product, permutations, combinations


@dataclass(unsafe_hash=True)
class Coord:
    x: int = 0
    y: int = 0
    z: int = 0

    def __sub__(self, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self) -> Coord:
        return Coord(-self.x, -self.y, -self.z)


class Scanner:
    def __init__(self) -> None:
        self.beacons: list[Coord] = []


class Mat3:
    def __init__(self, values: Iterable[Iterable[int]]) -> None:
        self.values = [list(row) for row in values]

    @overload
    def __matmul__(self, other: Coord) -> Coord: ...
    @overload
    def __matmul__(self, other: Mat3) -> Mat3: ...

    def __matmul__(self, other: Coord | Mat3) -> Coord | Mat3:
        r1, r2, r3 = self.values
        if isinstance(other, Coord):
            return Coord(
                r1[0] * other.x + r1[1] * other.y + r1[2] * other.z,
                r2[0] * other.x + r2[1] * other.y + r2[2] * other.z,
                r3[0] * other.x + r3[1] * other.y + r3[2] * other.z,
            )
        elif isinstance(other, Mat3):
            c1 = self @ Coord(other.values[0][0], other.values[1][0], other.values[2][0])
            c2 = self @ Coord(other.values[0][1], other.values[1][1], other.values[2][1])
            c3 = self @ Coord(other.values[0][2], other.values[1][2], other.values[2][2])
            return Mat3(
                [
                    [c1.x, c2.x, c3.x],
                    [c1.y, c2.y, c3.y],
                    [c1.z, c2.z, c3.z],
                ]
            )
        else:
            raise TypeError(f"other is {type(other)}")

    def det(self) -> int:
        a = self.values
        return (
            a[0][0] * a[1][1] * a[2][2]
            + a[0][1] * a[1][2] * a[2][0]
            + a[0][2] * a[1][0] * a[2][1]
            - a[0][2] * a[1][1] * a[2][0]
            - a[0][1] * a[1][0] * a[2][2]
            - a[0][0] * a[1][2] * a[2][1]
        )

    def transpose(self) -> Mat3:
        a = self.values
        return Mat3(
            [
                [a[0][0], a[1][0], a[2][0]],
                [a[0][1], a[1][1], a[2][1]],
                [a[0][2], a[1][2], a[2][2]],
            ]
        )

    @staticmethod
    def eye() -> Mat3:
        return Mat3(
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
            ]
        )

    @staticmethod
    def zeros() -> Mat3:
        return Mat3(
            [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]
        )


orientations: list[Mat3] = []


def init_orientations():
    for i, j, k in permutations(range(3), 3):
        for iv, jv, kv in product((1, -1), repeat=3):
            o = Mat3.zeros()
            o.values[0][i] = iv
            o.values[1][j] = jv
            o.values[2][k] = kv
            d = o.det()
            if d == 1:
                orientations.append(o)


init_orientations()
assert len(orientations) == 24, len(orientations)


@dataclass
class Transform:
    orient: Mat3
    offset: Coord

    def inverse(self) -> Transform:
        inv = self.orient.transpose()
        return Transform(inv, -(inv @ self.offset))

    @staticmethod
    def identity() -> Transform:
        return Transform(Mat3.eye(), Coord(0, 0, 0))


@dataclass
class ScannerGroupItem:
    index: int
    transform: Transform


ScannerGroup = list[ScannerGroupItem]


def main() -> None:
    inputFile = sys.argv[1]

    scanners: list[Scanner] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            if l.startswith("---"):
                scanners.append(Scanner())
            else:
                scanners[-1].beacons.append(Coord(*map(int, l.split(","))))
    # print(scanners)

    groups: list[ScannerGroup] = [[ScannerGroupItem(i, Transform.identity())] for i in range(len(scanners))]

    for i in range(len(scanners)):
        for j in range(i + 1, len(scanners)):
            if in_same_group(i, j, groups):
                continue
            # print(f"check overlap for {i} and {j}")
            if overlap_info := check_overlap(scanners[i], scanners[j]):
                print(f"detect overlap in {i} and {j}")
                merge_group(i, j, overlap_info, groups)
                print(f"merge {i}, {j}, groups: {len(groups)}")

    assert len(groups) == 1
    coords: set[Coord] = set()
    for item in groups[0]:
        # print(item)
        coords.update(item.transform.orient @ c + item.transform.offset for c in scanners[item.index].beacons)
    print('ans1:', len(coords))

    scanner_coords: list[Coord] = []
    for item in groups[0]:
        # print(item)
        scanner_coords.append(item.transform.orient @ Coord(0, 0, 0) + item.transform.offset)
    largest_manhattan_distance = max(manhattan_distance(c1, c2) for c1, c2 in combinations(scanner_coords, 2))
    print('ans2:', largest_manhattan_distance)

def manhattan_distance(c1: Coord, c2: Coord) -> int:
    return abs(c1.x - c2.x) + abs(c1.y - c2.y) + abs(c1.z - c2.z)



def in_same_group(i: int, j: int, groups: list[ScannerGroup]) -> bool:
    for g in groups:
        if any(i == s.index for s in g):
            return any(j == s.index for s in g)
        elif any(j == s.index for s in g):
            return any(i == s.index for s in g)
    return False


# return how to transform s2 to s1
def check_overlap(s1: Scanner, s2: Scanner) -> Transform | None:
    for b2 in s2.beacons:
        relative_coords2 = set(b - b2 for b in s2.beacons)
        for b1 in s1.beacons:
            relative_coords1 = list(b - b1 for b in s1.beacons)
            for orient in orientations:
                relative_coords2_orient = set(orient @ b for b in relative_coords2)
                if len(relative_coords2_orient.intersection(relative_coords1)) >= 12:
                    offset = b1 - (orient @ b2)
                    return Transform(orient, offset)


def merge_group(i: int, j: int, tji: Transform, groups: list[ScannerGroup]) -> None:
    gi, ki = find_scanner_in_groups(i, groups)
    gj, kj = find_scanner_in_groups(j, groups)

    # j -> group_i[0]
    tj0 = combine_transform(tji, groups[gi][ki].transform)
    # group_j[0] -> j
    tj_rev = groups[gj][kj].transform.inverse()
    for s in groups[gj]:
        # s -> group_j[0] -> j -> group_i[0]
        new_transform = combine_transform(combine_transform(s.transform, tj_rev), tj0)
        groups[gi].append(ScannerGroupItem(s.index, new_transform))
    del groups[gj]


def combine_transform(t1: Transform, t2: Transform) -> Transform:
    return Transform(t2.orient @ t1.orient, t2.orient @ t1.offset + t2.offset)


def find_scanner_in_groups(i: int, groups: list[ScannerGroup]) -> tuple[int, int]:
    for k, g in enumerate(groups):
        for sk, s in enumerate(g):
            if i == s.index:
                return (k, sk)
    raise RuntimeError(f"cannot find {i} in groups")


if __name__ == "__main__":
    main()
