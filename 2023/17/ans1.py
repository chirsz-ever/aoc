#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pqdict>=1.4.1",
# ]
# ///

import sys
from pqdict import pqdict

Coord = tuple[int, int]
Node=tuple[Coord, ...]

def main() -> None:
    inputFile = sys.argv[1]

    map: list[list[int]] = []
    with open(inputFile) as fin:
        map = [[int(c) for c in l.strip()] for l in fin if l.strip()]
    rows = len(map)
    cols = len(map[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)

    def diff(c1: Coord, c2: Coord) -> Coord:
        return (c2[0] - c1[0], c2[1] - c1[1])

    # dijkstra
    
    # Coordination with direction
    min_loss: dict[Node, int] = {}
    pq = pqdict.minpq({ (start,): 0 })
    S: set[Node] = set()
    prev: dict[Node, Node] = {}

    def can_move(u: Node, nc: Coord) -> bool:
        if len(u) > 1 and nc == u[1]:
            return False
        if len(u) < 4:
            return True
        return not (diff(u[3], u[2]) == diff(u[2], u[1]) == diff(u[1], u[0]) == diff(u[0], nc))

    for u, min_loss_u in pq.popitems():
        if u in S:
            continue
        # print(f'visit {u[0]}')
        S.add(u)
        min_loss[u] = min_loss_u
        for di, dj in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            ni, nj = u[0][0] + di, u[0][1] + dj
            nc = (ni, nj)
            # print(f'{n=}')
            if 0 <= ni < rows and 0 <= nj < cols and can_move(u, nc):
                n = (nc,) + u[:3]
                alt_loss = min_loss_u + map[ni][nj]
                if n not in pq or alt_loss < pq[n]:
                    # print(f'update min_loss of {n}')
                    pq[n] = alt_loss
                    prev[n] = u

    min_end = None
    min_end_loss = None
    for k in min_loss:
        if k[0] == end:
            min_loss_k = min_loss[k]
            if min_end_loss == None or min_loss_k < min_end_loss:
                min_end_loss = min_loss_k
                min_end = k
            # print(min_loss[k])
    print(f'min loss: {min_end_loss}')

    # assert min_end is not None
    # path_node = [min_end]
    # while path_node[-1] in prev:
    #     path_node.append(prev[path_node[-1]])

    # for n in path_node:
    #     print(n)

    # path_coord = [n[0] for n in path_node][::-1]
    # for i in range(rows):
    #     for j in range(cols):
    #         print(map[i][j] if (i, j) not in path_coord else '*', end='')
    #     print()

if __name__ == '__main__':
    main()
