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

def print_min_steps(ms: list[list[int|None]]):
    for l in ms:
        for g in l:
            if g is None:
                print('.', end='')
            else:
                print(g, end='')
        print()

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
            print(f'test {(nc, nr)}: \'{ng}\' success')
        else:
            print(f'test {(nc, nr)}: \'{ng}\' failed')
    print(f'{step1s=}')
    return step1s

BfsQueueState = tuple[Coord, Coord, int]

def do_bfs(sp: Coord, tm: list[str]) -> list[list[int|None]]:
    min_step: list[list[int|None]] = [[None for _ in tm[0]] for _ in tm]
    min_step[sp[0]][sp[1]] = 0
    max_step = -1
    g1, g2 = get_step1(tm, sp)
    queue: list[BfsQueueState] = [(g1, sp, 1), (g2, sp, 1)]
    while len(queue) != 0:
        (row, col), (prv_row, prv_col), step = queue.pop(0)
        if min_step[row][col] is not None:
            continue
        max_step = max(max_step, step)
        min_step[row][col] = step
        neighbors = get_neighbor_grids(tm, (row, col))
        neighbors.remove((prv_row, prv_col))
        assert len(neighbors) == 1
        queue.append((neighbors[0], (row, col), step + 1))
    print(f'{max_step=}')
    return min_step

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

    min_steps = do_bfs(s_pos, tile_map)
    # print_min_steps(min_steps)

if __name__ == '__main__':
    main()
