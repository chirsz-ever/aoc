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
Node=tuple[Coord, Coord, int]

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
    pq = pqdict.minpq({ (start, (0,0), 0): 0 })
    S: set[Node] = set()
    prev: dict[Node, Node] = {}

    def can_move(u: Node, nc: Coord) -> bool:
        if not (0 <= nc[0] < rows and 0 <= nc[1] < cols):
            return False
        uc, du, c = u
        if diff(du, uc) == nc:
            return False
        if c < 3:
            return True
        return diff(uc, nc) != du

    def gen_new_node(u: Node, nc: Coord) -> Node:
        d = diff(u[0], nc)
        c = u[2] + 1 if d == u[1] else 1
        return (nc, d, c)

    for u, min_loss_u in pq.popitems():
        if u in S:
            assert min_loss_u >= min_loss[u]
            continue
        # print(f'visit {u}')
        S.add(u)
        min_loss[u] = min_loss_u
        for di, dj in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            ni, nj = u[0][0] + di, u[0][1] + dj
            nc = (ni, nj)
            # print(f'{n=}')
            if can_move(u, nc):
                n = gen_new_node(u, nc)
                alt_loss = min_loss_u + map[ni][nj]
                if n not in pq or alt_loss < pq[n]:
                    # print(f'update min_loss of {n}')
                    pq[n] = alt_loss
                    prev[n] = u

    min_end = None
    min_loss_end = None
    for k in min_loss:
        if k[0] == end:
            min_loss_k = min_loss[k]
            if min_loss_end == None or min_loss_k < min_loss_end:
                min_loss_end = min_loss_k
                min_end = k
            # print(min_loss[k])
    print(f'min loss: {min_loss_end}')

    # assert min_end is not None
    # path_node = [min_end]
    # while path_node[-1][0] != start:
    #     path_node.append(prev[path_node[-1]])
    #     # print(f'append {path_node[-1]}')
    #     if len(path_node) > 100:
    #         break

    # for n in path_node:
    #     print(n)

    # path_coord = [n[0] for n in path_node]
    # for i in range(rows):
    #     for j in range(cols):
    #         print(map[i][j] if (i, j) not in path_coord else '*', end='')
    #     print()

if __name__ == '__main__':
    main()
