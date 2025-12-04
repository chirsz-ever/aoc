#!/usr/bin/env python3

import sys

def count_around(diagram, i, j):
    cnt = 0
    for a in [i - 1, i, i + 1]:
        for b in [j - 1, j, j + 1]:
            if (0 <= a < h) and (0 <= b < w) and (a, b) != (i, j) and diagram[a][b] == '@':
                cnt += 1
    # print(f'count [{i}, {j}] = {cnt}')
    return cnt

def main() -> None:
    global w, h
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    diagram = []
    with open(inputFile) as fin:
        for l in fin:
            diagram.append(list(l.strip()))
    w = len(diagram[0])
    h = len(diagram)
    cnt = 0
    for i in range(h):
        for j in range(w):
            if diagram[i][j] == '@' and count_around(diagram, i, j) < 4:
                # print(f'{i}, {j}')
                cnt += 1
    print(f'{cnt=}')

if __name__ == '__main__':
    main()
