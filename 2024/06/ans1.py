#!/usr/bin/env python3

import sys

def turn_right(d: tuple[int, int]) -> tuple[int, int]:
    if d == (-1, 0):
        return (0, 1)
    elif d == (0, 1):
        return (1, 0)
    elif d == (1, 0):
        return (0, -1)
    elif d == (0, -1):
        return (-1, 0)
    else:
        raise Exception(f'Invalid direction {d}')

def debug_print(map: list[str], guard_pos: tuple[int, int], d: tuple[int, int]) -> None:
    if d == (-1, 0):
        c = '^'
    elif d == (0, 1):
        c = '>'
    elif d == (1, 0):
        c = 'v'
    elif d == (0, -1):
        c = '<'
    else:
        raise Exception(f'Invalid direction {d}')

    for i in range(len(map)):
        for j in range(len(map[i])):
            if (i, j) == guard_pos:
                print(c, end='')
            else:
                print(map[i][j], end='')
        print()
    print('  ' + '-' * len(map[0]))

def would_circle(map: list[str], guard_pos_init: tuple[int, int], p: tuple[int, int]) -> bool:
    d = (-1, 0)
    guard_pos = guard_pos_init
    visited: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    while True:
        if (guard_pos, d) in visited:
            return True
        visited.add((guard_pos, d))
        # debug_print(map, guard_pos, d)
        ni = guard_pos[0] + d[0]
        nj = guard_pos[1] + d[1]
        if ni < 0 or ni >= len(map) or nj < 0 or nj >= len(map[ni]):
            return False
        if map[ni][nj] == '#' or (ni, nj) == p:
            d = turn_right(d)
            continue
        guard_pos = (ni, nj)

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    map: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if len(l) == 0:
                continue
            if '^' in l:
                guard_pos_init = (len(map), l.index('^'))
            map.append(l.replace('^', '.'))
    # print(guard_pos)
    # print(map)

    d = (-1, 0)
    guard_pos = guard_pos_init
    visited = set()
    while True:
        # print(f'on {guard_pos}')
        visited.add(guard_pos)
        ni = guard_pos[0] + d[0]
        nj = guard_pos[1] + d[1]
        if ni < 0 or ni >= len(map) or nj < 0 or nj >= len(map[ni]):
            break
        if map[ni][nj] == '#':
            d = turn_right(d)
            continue
        guard_pos = (ni, nj)
    print(len(visited))
    
    cnt = 0
    for p in visited:
        if p != guard_pos_init:
            if would_circle(map, guard_pos_init, p):
                cnt += 1
    print(cnt)

if __name__ == '__main__':
    main()
