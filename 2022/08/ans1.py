#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

tree_map : list[list[int]] = []

with open(inputFile) as fin:
    tree_map = [list(map(int, l.strip())) for l in fin if l.strip()]

# print(tree_map)

rows = len(tree_map)
cols = len(tree_map[0])

def is_visible(i: int, j: int):
    if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
        return True
    h = tree_map[i][j]
    return (
        all(tree_map[x][j] < h for x in range(0, i)) or
        all(tree_map[x][j] < h for x in range(i + 1, rows)) or
        all(tree_map[i][y] < h for y in range(0, j)) or
        all(tree_map[i][y] < h for y in range(j + 1, cols))
    )

print(sum(is_visible(i, j) for i in range(rows) for j in range(cols)))

def take_while_1(p, it):
    for x in it:
        if p(x):
            yield x
        else:
            yield x
            break

def scenic_score(i: int, j: int) -> int:
    if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
        return 0
    h = tree_map[i][j]
    shorter = lambda x: x < h
    l = sum(1 for _ in take_while_1(shorter, (tree_map[x][j] for x in range(i-1, -1, -1))))
    r = sum(1 for _ in take_while_1(shorter, (tree_map[x][j] for x in range(i+1, cols))))
    u = sum(1 for _ in take_while_1(shorter, (tree_map[i][y] for y in range(j-1, -1, -1))))
    b = sum(1 for _ in take_while_1(shorter, (tree_map[i][y] for y in range(j+1, rows))))
    return l * r * u * b

print(max(scenic_score(i, j) for i in range(rows) for j in range(cols)))
