#!/usr/bin/env python3

import sys

Coord = tuple[int, int]
Node = tuple[Coord, int]

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

    min_scores: dict[Node, int] = {}
    pre_tiles: dict[Node, set[Node]] = {}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # node, pre, score
    queue: list[tuple[Node, Node, int]] = [ ((start, 0), ((start[0], start[1]-1), 0), 0) ]

    # BFS
    while len(queue) > 0:
        node, pnode, mscore = queue.pop(0)
        c, d = node
        # print(f'visit {c} from {pnode[0]} score = {mscore}')
        if node not in min_scores:
            min_scores[node] = mscore
            if c != start:
                pre_tiles[node] = {pnode}
        elif mscore == min_scores[node]:
            if pnode not in pre_tiles[node]:
                pre_tiles[node].add(pnode)
                # print(f'find multiple min path at {c}: {pre_tiles[node]}')
        elif mscore < min_scores[node]:
            # print(f'find more low score path at {pnode[0]} -> {c}')
            min_scores[node] = mscore
            pre_tiles[node].clear()
            pre_tiles[node].add(pnode)
        else:
            continue
        if map[c[0]][c[1]] == 'E':
            continue
        for nd in range(len(directions)):
            di, dj = directions[nd]
            ni, nj = c[0] + di, c[1] + dj
            if (ni, nj) != pnode[0] and map[ni][nj] != '#' and map[ni][nj] != 'S':
                rot_score = 0 if d == nd else 1000
                nscore = mscore + rot_score + 1
                # print(f'add to queue: {c} -> {(ni, nj)} score = {nscore + 1}')
                queue.append((((ni, nj), nd), node, nscore))

    # find all tiles
    tiles: set[Node] = set()
    min_directions = []
    for d, (di, dj) in enumerate(directions):
        node = (end, d)
        if node in min_scores:
            if len(min_directions) == 0:
                min_directions.append(d)
            else:
                cmscore = min_scores[end, d]
                mscore = min_scores[end, min_directions[0]]
                if mscore == cmscore:
                    min_directions.append(d)
                elif cmscore < mscore:
                    min_directions = [d]

    assert min_directions
    q2: list[Node] = [(end, d) for d in min_directions]
    while len(q2) > 0:
        node = q2.pop(0)
        if node in tiles:
            continue
        c, d = node
        tiles.add(node)
        if c != start:
            q2.extend(pre_tiles[node])

    pure_tiles = { t for t, _ in tiles }

    print(len(pure_tiles))
    # print(tiles)

    # for i in range(rows):
    #     for j in range(cols):
    #         if (i, j) in pure_tiles:
    #             print('O', end='')
    #         else:
    #             print(map[i][j], end='')
    #     print()

if __name__ == '__main__':
    main()
