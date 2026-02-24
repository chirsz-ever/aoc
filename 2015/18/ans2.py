#!/usr/bin/env python3

import sys
from functools import cache

g2i = {
    ".": 0,
    "#": 1,
}


def main() -> None:
    global width, height
    inputFile = sys.argv[1]
    steps = int(sys.argv[2]) if len(sys.argv) >= 3 else 100

    with open(inputFile) as fin:
        grid: list[list[int]] = [[g2i[c] for c in l] for l in fin.read().splitlines()]
    width = len(grid[0])
    height = len(grid)

    grid[0][0] = grid[0][width - 1] = grid[height - 1][0] = grid[height - 1][width - 1] = 1
    # print('Initial state:')
    # print_grid(grid)

    for st in range(steps):
        grid = step(grid)
        grid[0][0] = grid[0][width - 1] = grid[height - 1][0] = grid[height - 1][width - 1] = 1
        # print(f'\nAfter {st+1} step:')
        # print_grid(grid)
    on_cnt = sum(sum(l) for l in grid)
    print(on_cnt)


def print_grid(grid: list[list[int]]) -> None:
    for l in grid:
        for c in l:
            print(".#"[c], end="")
        print()


def step(grid: list[list[int]]) -> list[list[int]]:
    ng = [[0] * width for _ in range(height)]
    for i in range(height):
        for j in range(width):
            s = grid[i][j]
            on_cnt = count_on_neighbors(grid, i, j)
            # print(f'on_cnt of {(i, j)}: {on_cnt}')
            if s == 1:
                ng[i][j] = int(on_cnt == 2 or on_cnt == 3)
            else:
                ng[i][j] = int(on_cnt == 3)
    return ng

def count_on_neighbors(grid: list[list[int]], i: int, j: int) -> int:
    cnt = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni = i + di
            nj = j + dj
            if 0 <= ni < height and 0 <= nj < width:
                cnt += grid[ni][nj]
    return cnt

if __name__ == "__main__":
    main()
