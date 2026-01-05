#!/usr/bin/env python3

# from https://www.reddit.com/r/adventofcode/comments/1hj2odw/comment/m6qcv0f/ and https://github.com/goggle/AdventOfCode2024.jl/blob/main/src/day21.jl

from functools import cache
import sys

Coord = tuple[int, int]


def main() -> None:
    inputFile = sys.argv[1]
    N = 2 if len(sys.argv) < 3 else int(sys.argv[2])

    with open(inputFile) as fin:
        codes = list(l.strip() for l in fin if l.strip())

    s = 0
    for code in codes:
        t = 'A' + code
        door_seq = ''.join(min_path(keymap_2, t[i], t[i + 1]) for i in range(len(t) - 1))
        min_cost = cost(door_seq, N)
        # print(f'{code}: {min_cost}, {door_seq}')
        s += min_cost * int(code[:-1])
    print(f'{s=}')

keymap_2 = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                 '0': (3, 1), 'A': (3, 2),
}

keymap_1 = {
                 '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2),
}

def min_path(keymap: dict[str, Coord], a: str, b: str) -> str:
    i1, j1 = keymap[a]
    i2, j2 = keymap[b]
    path = "<" * max(0, j1 - j2) + "v" * max(0, i2-i1) + "^" * max(0, i1-i2) + ">" * max(0, j2-j1)
    if (i1, j2) not in keymap.values() or (i2, j1) not in keymap.values():
        path = path[::-1]
    return path + 'A'

@cache
def min_path_1(a: str, b: str) -> str:
    return min_path(keymap_1, a, b)

@cache
def cost(sequece: str, level: int) -> int:
    if level == 0:
        return len(sequece)
    prev = 'A'
    total = 0
    for c in sequece:
        total += cost(min_path_1(prev, c), level - 1)
        prev = c
    return total

if __name__ == '__main__':
    main()
