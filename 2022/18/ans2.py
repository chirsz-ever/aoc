#!/usr/bin/env python3

# thanks to https://www.reddit.com/r/adventofcode/comments/zoqhvy/comment/j12zhet/?utm_source=share&utm_medium=web2x&context=3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

Coord = tuple[int, int, int]

def read_input(fname) -> set[Coord]:
    input: set[Coord] = set()
    with open(fname) as fin:
        for l in fin:
            l = l.strip()
            if len(l) == 0:
                continue
            x, y, z = map(int, l.split(','))
            input.add((x, y, z))
    return input

# print(input)

def get_neighbors(coord: Coord) -> list[Coord]:
    neighbors: list[Coord] = []
    for i in range(3):
        for d in [-1, 1]:
            neighbor = list(coord)
            neighbor[i] += d
            neighbors.append((neighbor[0], neighbor[1], neighbor[2]))
    # print(neighbors)
    return neighbors

Edges = tuple[int, int, int, int, int, int]

def get_edges(cs: set[Coord]) -> Edges:
    x0 = min(x for x, y, z in cs)
    x1 = max(x for x, y, z in cs)
    y0 = min(y for x, y, z in cs)
    y1 = max(y for x, y, z in cs)
    z0 = min(z for x, y, z in cs)
    z1 = max(z for x, y, z in cs)
    return x0, x1, y0, y1, z0, z1

def in_bound(c: Coord, edges: Edges):
    x, y, z = c
    x0, x1, y0, y1, z0, z1 = edges
    return x0 - 1 <= x <= x1 + 1 and y0 - 1 <= y <= y1 + 1 and z0 - 1 <= z <= z1 + 1 

def find_surfaces(lavas: set[Coord], start: Coord, edges: Edges) -> int:
    visited = {start}
    counter = 0
    stack: list[Coord] = [start]
    while len(stack) > 0:
        coord = stack.pop()
        for n in get_neighbors(coord):
            # print(f"  neighbor {n}")
            if not in_bound(n, edges) or n in visited:
                continue
            if n in lavas:
                counter += 1
            else:
                stack.append(n)
                visited.add(n)
    return counter

def main() -> None:
    input = read_input(inputFile)
    edges = get_edges(input)
    x0, x1, y0, y1, z0, z1 = edges
    surfaces = find_surfaces(input, (x0 - 1, y0 - 1, z0 - 1), edges)
    print(surfaces)

if __name__ == '__main__':
    main()
