#!/usr/bin/env python3

import sys
from functools import cache

def main() -> None:
    inputFile = sys.argv[1]

    robot: list[int] = [0, 0]
    map: list[list[str]] = []
    insts = ''
    with open(inputFile) as fin:
        for i, l in enumerate(fin):
            l = l.strip()
            if l and l[0] == '#':
                row = []
                for j, c in enumerate(l):
                    if c == '#':
                        row += ['#', '#']
                    elif c == 'O':
                        row += ['[', ']']
                    elif c == '.':
                        row += ['.', '.']
                    else:
                        assert c == '@'
                        row += ['.', '.']
                        robot = [i, j * 2]
                map.append(row)
            else:
                insts += l
    rows = len(map)
    cols = len(map[0])

    # print_map(map, robot)
    for i, inst in enumerate(insts):
        move(map, robot, inst)
        # print(f'----- after step {i} ({inst}) -----')
        # print_map(map, robot)

    s = 0
    for i in range(rows):
        for j in range(cols):
            if map[i][j] == '[':
                s += i * 100 + j
    print(f'{s=}')

def print_map(map: list[list[str]], robot: list[int]):
    rows = len(map)
    cols = len(map[0])
    for i in range(rows):
        for j in range(cols):
            if [i, j] == robot:
                print('@', end='')
            else:
                print(map[i][j], end='')
        print()

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
    if map[i][j] == '#':
        return

    if inst == '<' or inst == '>':
        while map[i][j] == '[' or map[i][j] == ']':
            i, j = i + di, j + dj
        if map[i][j] == '.':
            while [i, j] != robot:
                map[i][j] = map[i - di][j - dj]
                i, j = i - di, j - dj
            robot[0], robot[1] = ri + di, rj + dj
        else:
            assert map[i][j] == '#', f'map[{i}][{j}] = {map[i][j]}'
        return

    # inst == '^' or inst == 'v'
    @cache
    def can_move(i: int, j: int) -> bool:
        n = map[i + di][j]
        if n == '.':
            return True
        elif n == '[':
            return can_move(i + di, j) and can_move(i + di, j + 1)
        elif n == ']':
            return can_move(i + di, j) and can_move(i + di, j - 1)
        assert n == '#', f'map[{i}][{j}] = {map[i][j]}'
        return False

    @cache
    def do_move(i: int, j: int) -> None:
        n = map[i + di][j]
        if n == '[':
            do_move(i + di, j)
            do_move(i + di, j + 1)
        elif n == ']':
            do_move(i + di, j)
            do_move(i + di, j - 1)
        map[i + di][j] = map[i][j]
        map[i][j] = '.'

    if can_move(ri, rj):
        do_move(ri, rj)
        robot[0], robot[1] = ri + di, rj + dj

if __name__ == '__main__':
    main()
