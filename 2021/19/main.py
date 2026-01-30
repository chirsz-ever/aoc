#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Iterator


@dataclass(unsafe_hash=True)
class Coord:
    x: int = 0
    y: int = 0
    z: int = 0

    def __sub__(self, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)


class Scanner:
    def __init__(self) -> None:
        self.beacons: list[Coord] = []


class Mat3:
    def __init__(self, values: Iterator[Iterator[int]]) -> None:
        self.values = [list(row) for row in values]

    def __matmul__(self, other: Coord) -> Coord:
        r1, r2, r3 = self.values
        return Coord(
            r1[0] * other.x + r1[1] * other.y + r1[2] * other.z,
            r2[0] * other.x + r2[1] * other.y + r2[2] * other.z,
            r3[0] * other.x + r3[1] * other.y + r3[2] * other.z,
        )


orientations: list[Mat3] = []


@dataclass
class ScannerGroupItem:
    index: int
    orient: int
    offset: Coord

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

    groups: list[ScannerGroup] = [[ScannerGroupItem(i, 0, Coord())] for i in range(len(scanners))]

    for i in range(len(scanners)):
        for j in range(i, len(scanners)):
            if in_same_group(i, j, groups):
                continue
            if overlap_info := check_overlap(scanners[i], scanners[j]):
                merge_group(i, j, overlap_info, groups)


def in_same_group(i: int, j: int, groups: list[ScannerGroup]) -> bool:
    for g in groups:
        if any(i == s.index for s in g):
            return any(j == s.index for s in g)
        elif any(j == s.index for s in g):
            return any(i == s.index for s in g)
    return False


# return orientation and offset relative to s1
def check_overlap(s1: Scanner, s2: Scanner) -> tuple[int, Coord] | None:
    for b2 in s2.beacons:
        relative_coords2 = set(b - b2 for b in s2.beacons)
        for b1 in s1.beacons:
            relative_coords1 = list(b - b1 for b in s1.beacons)
            for o, orient in enumerate(orientations):
                relative_coords1_orient = set(orient @ b for b in relative_coords1)
                if len(relative_coords1_orient.intersection(relative_coords2)) >= 12:
                    offset = orient @ b1 - b2
                    return o, offset


def merge_group(i: int, j: int, overlap_info: tuple[int, Coord], groups: list[ScannerGroup]) -> None:
    gi, ki = find_scanner_in_groups(i, groups)
    gj, kj = find_scanner_in_groups(i, groups)

    si = groups[gi][ki]
    sj = groups[gj][kj]
    for s in groups[gj]:
        new_orient = combine_orient(si.orient, rev_orient(overlap_info[0]))
        # FIXME
        new_offset = Coord(0, 0)
        groups[gi].append(ScannerGroupItem(s.index, new_orient, new_offset))
    del groups[gj]

def find_scanner_in_groups(i: int, groups: list[ScannerGroup]) -> tuple[int, int]:
    found_gi = False
    gi = -1
    si = -1
    for k, g in enumerate(groups):
        for sk, s in enumerate(groups[k]):
            if i == s.index:
                gi = k
                si = sk
                found_gi = True
                break
        if found_gi:
            break
    assert found_gi
    return (gi, si)

if __name__ == "__main__":
    main()
