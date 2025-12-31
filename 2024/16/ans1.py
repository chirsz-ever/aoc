#!/usr/bin/env python3

import sys

Coord = tuple[int, int]

def main() -> None:
    inputFile = sys.argv[1]

    map: list[list[str]] = []
    with open(inputFile) as fin:
        for l in fin:
            if l.strip():
                map.append(list(l.strip()))
    rows = len(map)
    cols = len(map[0])
    start: Coord = (rows - 2, 1)
    end: Coord = (1, cols - 2)
    assert map[start[0]][start[1]] == 'S'
    assert map[end[0]][end[1]] == 'E'

    min_scores: list[list[int]] = [ [-1] * cols for _ in range(rows) ]

    queue: list[tuple[Coord, Coord, int]] = [ (start, (start[0], start[1] - 1), 0) ]

    # BFS
    while len(queue) > 0:
        (ci, cj), (pi, pj), mscore = queue.pop(0)
        if min_scores[ci][cj] == -1 or min_scores[ci][cj] > mscore:
            min_scores[ci][cj] = mscore
        else:
            continue
        if map[ci][cj] == 'E':
            continue
        pdi, pdj = ci - pi, cj - pj
        for di, dj in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            ni, nj = ci + di, cj + dj
            if (ni, nj) != (pi, pj) and map[ni][nj] != '#' and map[ni][nj] != 'S':
                if (di, dj) == (pdi, pdj):
                    inc_score = 1
                else:
                    inc_score = 1000 + 1
                nscore = mscore + inc_score
                queue.append(((ni, nj), (ci, cj), nscore))
    print(min_scores[end[0]][end[1]])

if __name__ == '__main__':
    main()
