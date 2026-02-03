#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Iterable, overload
from itertools import product, permutations
import numpy as np

Coord = tuple[int, int, int]

class Scanner:
    def __init__(self) -> None:
        self.beacons: list[np.ndarray] = []


orientations: list[np.ndarray] = []


def init_orientations():
    for i, j, k in permutations(range(3), 3):
        for iv, jv, kv in product((1, -1), repeat=3):
            o = np.zeros((3, 3), dtype=np.int32)
            o[0, i] = iv
            o[1, j] = jv
            o[2, k] = kv
            if np.linalg.det(o) == 1:
                orientations.append(o)


init_orientations()
assert len(orientations) == 24, len(orientations)


@dataclass
class Transform:
    orient: np.ndarray
    offset: np.ndarray

    def inverse(self) -> Transform:
        inv = self.orient.transpose()
        return Transform(inv, -(inv @ self.offset))

    @staticmethod
    def identity() -> Transform:
        return Transform(np.eye(3, 3), np.array([0, 0, 0], dtype=np.int32))


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
                x, y, z = map(int, l.split(","))
                scanners[-1].beacons.append(np.array([x, y, z], dtype=np.int32))
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
        coords.update(tuple(item.transform.orient @ c + item.transform.offset) for c in scanners[item.index].beacons)
    print(len(coords))


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
        relative_coords2 = list(b - b2 for b in s2.beacons)
        for b1 in s1.beacons:
            relative_coords1 = list(tuple(b - b1) for b in s1.beacons)
            for orient in orientations:
                relative_coords2_orient = set(tuple(orient @ b) for b in relative_coords2)
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
