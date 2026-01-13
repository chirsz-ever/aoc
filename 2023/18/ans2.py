#!/usr/bin/env python3

import sys
from dataclasses import dataclass

Coord = tuple[int, int]


@dataclass
class Edge:
    start: Coord
    end: Coord
    length: int
    vertical: bool


dir2didj = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]


def main() -> None:
    inputFile = sys.argv[1]

    plan: list[tuple[int, int]] = []
    with open(inputFile) as fin:
        for l in fin:
            if l.strip():
                a, b, c = l.strip().split()
                distance = int(c[2:7], 16)
                direction = int(c[7])
                plan.append((direction, distance))

    # print(plan)

    edges: list[Edge] = []
    vertices: list[Coord] = []
    p = (0, 0)
    for d, size in plan:
        di, dj = dir2didj[d]
        p1 = p[0] + di * size, p[1] + dj * size
        e = Edge(p, p1, size, di != 0)
        edges.append(e)
        vertices.append(p)
        p = p1
    assert p == (0, 0)

    def to_vertical(e: Edge) -> tuple[int, int, int]:
        j = e.start[1]
        i, ni = sorted([e.start[0], e.end[0]])
        return (j, i, ni)

    vertical_edges: list[tuple[int, int, int]] = sorted(
        (to_vertical(e) for e in edges if e.vertical), key=lambda e: e[0]
    )
    vertical_is: list[int] = sorted(
        {e[1] for e in vertical_edges} | {e[2] for e in vertical_edges}
    )
    horizonal_edge_set = set()
    for e in edges:
        if not e.vertical:
            j, nj = sorted([e.start[1], e.end[1]])
            horizonal_edge_set.add((e.start[0], j, nj))

    max_i = max(v[0] for v in vertices)
    min_i = min(v[0] for v in vertices)
    # max_j = max(v[1] for v in vertices)
    # min_j = min(v[1] for v in vertices)

    def is_horizonal_edge(i: int, j: int, nj: int) -> bool:
        return (i, j, nj) in horizonal_edge_set

    content_area = 0
    i = min_i
    while i <= max_i:
        crossed_vertical_edges = [e for e in vertical_edges if e[1] <= i <= e[2]]
        is_inner = False
        has_horizonal_edge = False
        row_area = 0
        for ei in range(len(crossed_vertical_edges) - 1):
            j, topi, downi = crossed_vertical_edges[ei]
            nj, _, _ = crossed_vertical_edges[ei + 1]
            if i != downi:
                is_inner = not is_inner
            c_is_horizonal_edge = is_horizonal_edge(i, j, nj)
            if c_is_horizonal_edge:
                has_horizonal_edge = True
            if is_inner and not c_is_horizonal_edge:
                row_area += nj - j - 1
        if has_horizonal_edge:
            content_area += row_area
            i += 1
        else:
            for vi in vertical_is:
                if vi > i:
                    c_max_i = vi
                    break
            else:
                c_max_i = i + 1
            # not include the terminal point
            span_rows = c_max_i - i
            content_area += row_area * span_rows
            i += span_rows

    edge_area = sum(p[1] for p in plan)
    print(f"total area: {edge_area + content_area}")


if __name__ == "__main__":
    main()
