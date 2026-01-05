#!/usr/bin/env python3

import sys
from collections import Counter

Coord = tuple[int, int]

def main() -> None:
    inputFile = sys.argv[1]

    map: list[str] = []
    start: Coord = (0, 0)
    end: Coord = (0, 0)
    with open(inputFile) as fin:
        for i, l in enumerate(fin):
            l = l.strip()
            if 'S' in l:
                start = (i, l.index('S'))
            if 'E' in l:
                end = (i, l.index('E'))
            map.append(l.replace('S', '.').replace('E', '.'))
    
    rows = len(map)
    cols = len(map[0])

    path_nodes = find_shortest_path_nodes(map, start, end)
    # print(f'total {len(path_nodes)-1} steps')

    # for i in range(rows):
    #     for j in range(cols):
    #         if (i, j) in path_nodes:
    #             print('*', end='')
    #         else:
    #             print(map[i][j], end='')
    #     print()

    cheat_step = 20
    didjs: list[Coord] = []
    for i in range(-cheat_step, cheat_step + 1):
        for j in range(-cheat_step, cheat_step + 1):
            if 1 < abs(i) + abs(j) <= cheat_step:
                didjs.append((i, j))
    # print(f'{len(didjs)=}')

    s = 0
    index = { coord: i for i, coord in enumerate(path_nodes) }
    # c = Counter()
    for k in range(len(path_nodes)):
        n = path_nodes[k]
        for di, dj in didjs:
            n1 = (n[0] + di, n[1] + dj)
            k1 = index.get(n1)
            if k1 is None:
                continue
            saved = k1 - k - (abs(di) + abs(dj))
            # print(f'at {n} can save {saved} ps')
            # print(f'step {k} at {n} can save {saved} ps')
            # if saved > 0:
            #     c[saved] += 1
            if saved >= 100:
                s += 1
    # for saved, times in sorted([(k, v) for k, v in c.items()], key=lambda t: (t[0], -t[1])):
    #     if saved >= 50:
    #         print(f'There are {times} cheats that save {saved} picoseconds')
    print(s)

def find_shortest_path_nodes(map: list[str], start: Coord, end: Coord) -> list[Coord]:
    queue = [start]
    pre = {}
    found_end = False
    while len(queue) > 0:
        i, j = queue.pop(0)
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            n = (ni, nj)
            if map[ni][nj] == '#' or n in pre:
                continue
            pre[n] = (i, j)
            if n == end:
                found_end = True
                break
            queue.append(n)
        if found_end:
            break

    if not found_end:
        return []

    nodes = [end]
    while nodes[-1] != start:
        nodes.append(pre[nodes[-1]])
    nodes.reverse()
    return nodes

if __name__ == '__main__':
    main()
