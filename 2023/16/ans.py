#!/usr/bin/env python3

import sys

Map = list[str]
Coord = tuple[int, int]

# 00 -> (-1, 0)
# 01 -> (1, 0)
# 10 -> (0, -1)
# 11 -> (0, 1)
Direction = int

def direction_to_dxdy(d: Direction) -> tuple[int, int]:
    assert 0 <= d < 4, d
    dx = [-1, 1, 0, 0][d]
    dy = [0, 0, -1, 1][d]
    return dx, dy

def dxdy_to_direction(dx: int, dy: int) -> Direction:
    match (dx, dy):
        case (-1, 0): return 0
        case (1, 0): return 1
        case (0, -1): return 2
        case (0, 1): return 3
    raise RuntimeError((dx, dy))

def do_raytrace(mp: Map, init_place: Coord, init_direct: Direction) -> set[tuple[Coord, Direction]]:
    height = len(mp)
    width = len(mp[0])
    visited: set[tuple[Coord, Direction]] = set()
    q: list[tuple[Coord, Direction]] = [(init_place, init_direct)]
    def try_enqueue(x: int, y: int, dx: int, dy: int):
        nx = x + dx
        ny = y + dy
        nd = dxdy_to_direction(dx, dy)
        if 0 <= nx < width and 0 <= ny < height and ((nx, ny), nd) not in visited:
            # print(f'enqueue{(nx, ny, nd)}')
            q.append(((nx, ny), nd))
        else:
            # print(f'enter {(nx, ny)} failed')
            pass
    while len(q) != 0:
        for _ in range(len(q)):
            (x, y), drct = q.pop(0)
            visited.add(((x, y), drct))
            dx, dy = direction_to_dxdy(drct)
            match mp[y][x]:
                case '.':
                    try_enqueue(x, y, dx, dy)
                case '/':
                    try_enqueue(x, y, -dy, -dx)
                case '\\':
                    try_enqueue(x, y, dy, dx)
                case '-':
                    if dx == 0:
                        try_enqueue(x, y, -1, 0)
                        try_enqueue(x, y, 1, 0)
                    else:
                        try_enqueue(x, y, dx, dy)
                case '|':
                    if dy == 0:
                        try_enqueue(x, y, 0, -1)
                        try_enqueue(x, y, 0, 1)
                    else:
                        try_enqueue(x, y, dx, dy)
                case g:
                    raise RuntimeError(g)
    return visited

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    input_map: Map = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            input_map.append(l)

    ray_result00 = do_raytrace(input_map, (0, 0), 1)
    lighted00 = set(c for c, _ in ray_result00)
    lighted_cnt00 = len(lighted00)
    print(f"ans1: {lighted_cnt00}")

    cnt_list: list[int] = []
    height = len(input_map)
    width = len(input_map[0])
    for x in range(width):
        cnt_list.append(len(set(c for c, _ in do_raytrace(input_map, (x, 0), 3))))
        cnt_list.append(len(set(c for c, _ in do_raytrace(input_map, (x, height-1), 2))))
    for y in range(width):
        cnt_list.append(len(set(c for c, _ in do_raytrace(input_map, (0, y), 1))))
        cnt_list.append(len(set(c for c, _ in do_raytrace(input_map, (width-1, y), 0))))

    print(f"ans2: {max(cnt_list)}")

if __name__ == '__main__':
    main()
