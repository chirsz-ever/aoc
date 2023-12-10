#!/usr/bin/env python3

import sys

def convert_grid(c: str) -> str:
    if c == '|': return '│'
    elif c == '-': return '─'
    elif c == 'L': return '└'
    elif c == 'J': return '┘'
    elif c == '7': return '┐'
    elif c == 'F': return '┌'
    else:
        return c

def print_tile_map(tile_map: list[str]):
    for l in tile_map:
        print(''.join(map(convert_grid, l)))

def find_s_pos(tm: list[str]) -> tuple[int, int]:
    for r, row in enumerate(tm):
        for c, grid in enumerate(row):
            if grid == 'S':
                return (r, c)
    raise RuntimeError

Coord = tuple[int, int]

grid2dxdy: dict[str, list[Coord]] = {
    'L': [(-1, 0), (0, 1)],
    'F': [(1, 0), (0, 1)],
    '7': [(1, 0), (0, -1)],
    'J': [(-1, 0), (0, -1)],
    '-': [(0, 1), (0, -1)],
    '|': [(-1, 0), (1, 0)],
}

def get_neighbor_grids(tm: list[str], p: Coord) -> list[tuple[int, int]]:
    c, r = p
    g = tm[c][r]
    ns = []
    for dx, dy in grid2dxdy[g]:
        nc = c + dx
        nr = r + dy
        ns.append((nc, nr))
    return ns


allowed_neighbor_grids: dict[tuple[int, int], str] = {
    (-1, 0): '7F|',
    (1, 0): 'JL|',
    (0, -1): 'LF-',
    (0, 1): 'J7-'
}

def get_step1(tm: list[str], sp: Coord) -> list[Coord]:
    c, r = sp
    step1s: list[Coord] = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nc = c + dx
        nr = r + dy
        if not (0 <= nc < len(tm) and 0 <= nr < len(tm[0])):
            # print(f'{(nc, nr)} out of range')
            continue
        ng = tm[nc][nr]
        if ng in allowed_neighbor_grids[dx, dy]:
            step1s.append((nc, nr))
    # print(f'{step1s=}')
    return step1s

BfsQueueState = tuple[Coord, Coord]

def get_loop_path(sp: Coord, tm: list[str]) -> list[Coord]:
    min_step: list[list[int|None]] = [[None for _ in tm[0]] for _ in tm]
    min_step[sp[0]][sp[1]] = 0
    visited: set[Coord] = {sp}
    path: list[Coord] = [sp]
    g1, g2 = get_step1(tm, sp)
    queue: list[BfsQueueState] = [(g1, sp)]
    while len(queue) != 0:
        p, prv_p = queue.pop(0)
        if p in visited:
            continue
        path.append(p)
        neighbors = get_neighbor_grids(tm, p)
        neighbors.remove(prv_p)
        assert len(neighbors) == 1
        queue.append((neighbors[0], p))
    return path

def calc_grid_by_neighbors(p: Coord, n1: Coord, n2: Coord) -> str:
    dn1 = (p[0] - n1[0], p[1] - n1[1])
    dn2 = (p[0] - n2[0], p[1] - n2[1])
    allowed_grid = set(allowed_neighbor_grids[dn1]).intersection(allowed_neighbor_grids[dn2])
    assert len(allowed_grid) == 1, allowed_grid
    return allowed_grid.pop()

def calc_inner_grids(tm: list[str], path: set[Coord]) -> int:
    # 0: outer
    # 1: inner
    # 2: up is outer
    # 3: up is inner
    s = 0
    inner_cnt = 0
    for r, row in enumerate(tm):
        for c, g in enumerate(row):
            if (r, c) not in path:
                if s == 1:
                    inner_cnt += 1
                else:
                    assert s == 0
            else: # (r, c) in path
                match (s, g):
                    case (0, '|'): s = 1
                    case (0, 'L'): s = 3
                    case (0, 'F'): s = 2
                    case (1, '|'): s = 0
                    case (1, 'L'): s = 2
                    case (1, 'F'): s = 3
                    case (2, '-'): s = 2
                    case (2, 'J'): s = 1
                    case (2, '7'): s = 0
                    case (3, '-'): s = 3
                    case (3, 'J'): s = 0
                    case (3, '7'): s = 1
                    case _: raise RuntimeError(f"{(r, c)}: {s=} {g=}")
    return inner_cnt

def main():
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    tile_map: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            tile_map.append(l.strip())

    # print_tile_map(tile_map)
    s_pos = find_s_pos(tile_map)
    print(f'{s_pos=}')

    path = get_loop_path(s_pos, tile_map)
    # print(f'{path=}')
    s_grid = calc_grid_by_neighbors(s_pos, path[1], path[-1])
    tile_map[s_pos[0]] = tile_map[s_pos[0]].replace('S', s_grid)
    # print_tile_map(tile_map)

    inner_grids = calc_inner_grids(tile_map, set(path))
    print(inner_grids)

if __name__ == '__main__':
    main()
