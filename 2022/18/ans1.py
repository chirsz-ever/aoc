#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

def read_input(fname) -> set[tuple[int, int, int]]:
    input: set[tuple[int, int, int]] = set()
    with open(fname) as fin:
        for l in fin:
            l = l.strip()
            if len(l) == 0:
                continue
            x, y, z = map(int, l.split(','))
            input.add((x, y, z))
    return input

input = read_input(inputFile)

# print(input)

def get_neighbors(coord: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    neighbors: list[tuple[int, int, int]] = []
    for i in range(3):
        for d in [-1, 1]:
            neighbor = list(coord)
            neighbor[i] += d
            neighbors.append((neighbor[0], neighbor[1], neighbor[2]))
    return neighbors

surface = 0
for coord in input:
    for neighbor in get_neighbors(coord):
        if neighbor not in input:
            surface += 1
print(surface)
