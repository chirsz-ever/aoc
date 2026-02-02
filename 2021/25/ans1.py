#!/usr/bin/env python3

import sys


Coord = tuple[int, int]


def main() -> None:
    inputFile = sys.argv[1]

    map: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            map.append(l)
    rows = len(map)
    cols = len(map[0])

    def step(cucumbers: dict[Coord, str]) -> dict[Coord, str]:
        next_cucumbers: dict[Coord, str] = {}
        east_cucumbers = { c for c, d in cucumbers.items() if d == '>' }
        south_cucumbers = { c for c, d in cucumbers.items() if d == 'v' }
        for c in east_cucumbers:
            nc = (c[0], (c[1] + 1) % cols)
            if nc not in cucumbers:
                next_cucumbers[nc] = '>'
            else:
                next_cucumbers[c] = '>'
        for c in south_cucumbers:
            nc = ((c[0] + 1) % rows, c[1])
            if nc not in next_cucumbers and nc not in south_cucumbers:
                next_cucumbers[nc] = 'v'
            else:
                next_cucumbers[c] = 'v'
        return next_cucumbers

    cucumbers: dict[Coord, str] = {}
    for i in range(0, rows):
        for j in range(0, cols):
            if map[i][j] != ".":
                cucumbers[i, j] = map[i][j]

    def print_cucumbers(cucumbers: dict[Coord, str]):
        for i in range(0, rows):
            for j in range(0, cols):
                c = cucumbers.get((i, j))
                print(c if c else '.', end='')
            print()

    cnt = 0
    while True:
        next_cucumbers = step(cucumbers)
        cnt += 1

        # print(f'\nAfter {cnt} steps:')
        # print_cucumbers(next_cucumbers)

        if next_cucumbers == cucumbers:
            break
        cucumbers = next_cucumbers
    print(cnt)


if __name__ == "__main__":
    main()
