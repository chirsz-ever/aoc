#!/usr/bin/env python3

import sys
import functools

Map = list[list[str]]
Coord = tuple[int, int]

def print_map(map: Map):
    for row in map:
        for grid in row:
            print(grid, end='')
        print()

def do_slide(map: Map, move_step: tuple[int, int]):
    height = len(map)
    width = len(map[0])

    if move_step[0] != 0:
        d1_size = width
        d2_size = height
        get_map = lambda d1, d2: map[d2][d1]
        set_map = lambda d1, d2, v: map[d2].__setitem__(d1, v)
        d2_step = move_step[0]
    else:
        d1_size = height
        d2_size = width
        get_map = lambda d1, d2: map[d1][d2]
        set_map = lambda d1, d2, v: map[d1].__setitem__(d2, v)
        d2_step = move_step[1]

    if d2_step < 0:
        d2_range = range(0, d2_size)
    else:
        d2_range = range(d2_size - 1, -1, -1)

    # print(f'{move_step=}')
    # print(f'{d2_step=}')
    # print(f'{d2_range=}')

    for d1 in range(0, d1_size):
        slide_target: int|None = None
        for d2 in d2_range:
            match (get_map(d1, d2), slide_target):
                case ('#', _):
                    slide_target = None
                case ('.', None):
                    slide_target = d2
                case ('O', int()) if slide_target < d2_size:
                    # print(f'set {(d1, slide_target)} -> O')
                    set_map(d1, slide_target, 'O')
                    # print(f'set {(d1, d2)} -> .')
                    set_map(d1, d2, '.')
                    slide_target += -d2_step

def calc_load(map: Map) -> int:
    height = len(map)
    load = 0
    for i, row in enumerate(map):
        load += (height - i) * row.count('O')
    return load

input = []

def coords_to_map(coords: tuple[Coord, ...]) -> Map:
    map = [['#' if c == '#' else '.' for c in row] for row in input]
    for r, c in coords:
        map[r][c] = 'O'
    return map

def map_to_coords(map: Map) -> tuple[Coord, ...]:
    coords = []
    for r, row in enumerate(map):
        for c, g in enumerate(row):
            if g == 'O':
                coords.append((r, c))
    return tuple(coords)

def slide(coords: tuple[Coord, ...], move_step: tuple[int, int]) -> tuple[Coord, ...]:
    map = coords_to_map(coords)
    do_slide(map, move_step)
    return map_to_coords(map)

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    global input
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            input.append(list(l))
            pass

    # print_map(input)
    N = 1000000000
    # N = 3

    coords = map_to_coords(input)
    histroy_set = {coords}
    histroy = [coords]
    for k in range(1, N):
        do_slide(input, (-1, 0))
        do_slide(input, (0, -1))
        do_slide(input, (1, 0))
        do_slide(input, (0, 1))
        coords = map_to_coords(input)
        if coords in histroy_set:
            last_idx = histroy.index(coords)
            loop_size = k - last_idx
            print(f"find loop at turn {k}, {last_idx=}, {loop_size=}")
            break
        histroy_set.add(coords)
        histroy.append(coords)
    # last_idx + offset + n * loop_size == N

    # for i in range(1, 4):
    #     print(f"\nhistroy {i}:")
    #     print_map(coords_to_map(histroy[i]))

    offset = (N - last_idx) % loop_size
    e_N = last_idx + offset
    print(f'{e_N=}')
    map_N = histroy[e_N]
    print(f'load={calc_load(coords_to_map(map_N))}')

if __name__ == '__main__':
    main()
