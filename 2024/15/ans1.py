#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = sys.argv[1]

    robot: list[int] = [0, 0]
    map: list[list[str]] = []
    insts = ''
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if l and l[0] == '#':
                map.append(list(l))
            else:
                insts += l
    rows = len(map)
    cols = len(map[0])
    for i in range(rows):
        for j in range(cols):
            if map[i][j] == '@':
                robot = [i, j]
                map[i][j] = '.'

    for inst in insts:
        move(map, robot, inst)

    for i in range(rows):
        for j in range(cols):
            if [i, j] == robot:
                print('@', end='')
            else:
                print(map[i][j], end='')
        print()

    s = 0
    for i in range(rows):
        for j in range(cols):
            if map[i][j] == 'O':
                s += i * 100 + j
    print(f'{s=}')


def move(map: list[list[str]], robot: list[int], inst: str) -> None:
    ri, rj = robot[0], robot[1]
    if inst == '<':
        di, dj = 0, -1
    elif inst == '^':
        di, dj = -1, 0
    elif inst == '>':
        di, dj = 0, 1
    else:
        assert inst == 'v'
        di, dj = 1, 0
    i, j = ri + di, rj + dj
    if map[i][j] == '.':
        robot[0], robot[1] = i, j
        return
    while map[i][j] == 'O':
        i, j = i + di, j + dj
    if map[i][j] == '.':
        map[i][j] = 'O'
        map[ri + di][rj + dj] = '.'
        robot[0], robot[1] = ri + di, rj + dj
        return
    assert map[i][j] == '#', f'map[{i}][{j}] = {map[i][j]}'


if __name__ == '__main__':
    main()
