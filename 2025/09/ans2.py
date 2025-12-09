#!/usr/bin/env python3

import sys
from functools import lru_cache

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    coords: list[tuple[int, int]] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.removesuffix('\n')
            x, y = map(int, l.split(','))
            coords.append((x, y))
    
    def area(i, j):
        x0, y0 = coords[i]
        x1, y1 = coords[j]
        return (abs(x0 - x1) + 1) * (abs(y1 - y0) + 1)
    
    def crossed(x0, y0, x1, y1, x2, y2, x3, y3):
        # assert x0 == x1 or y0 == y1
        # assert x2 == x3 or y2 == y3
        if x0 == x1:
            return y2 == y3 and (x2 - x0) * (x3 - x0) < 0 and (y0 - y2) * (y1 - y2) < 0
        assert y0 == y1
        return x2 == x3 and (y2 - y0) * (y3 - y0) < 0 and (x0 - x2) * (x1 - x2) < 0

    @lru_cache
    def cross_edges(x0: int, y0: int, x1: int, y1: int) -> bool:
        for i in range(len(coords)):
            ni = (i + 1) % len(coords)
            xi0, yi0 = coords[i]
            xi1, yi1 = coords[ni]
            if crossed(x0, y0, x1, y1, xi0, yi0, xi1, yi1):
                return True
        return False
    
    # ray-test
    @lru_cache
    def is_rg(x: int, y: int) -> bool:
        cnt = 0
        for i in range(len(coords)):
            ni = (i + 1) % len(coords)
            xi0, yi0 = coords[i]
            xi1, yi1 = coords[ni]
            x0, y0 = xi0 - x, yi0 - y
            x1, y1 = xi1 - x, yi1 - y

            assert x0 == x1 or y0 == y1
            # in edge, return True
            if (x0 == x1 == 0 and y0 * y1 <= 0) or (y0 == y1 == 0 and x0 * x1 <= 0):
                # print(f'is_rg{(x, y)}: {True}, {x0=} {y0=} {x1=} {y1=}')
                return True
            if (y0 >= 0 and y1 >=0) or (y0 < 0 and y1 < 0):
                continue
            if x0 > 0:
                cnt += 1
        r = cnt % 2 == 1
        # print(f'is_rg{(x, y)}: {cnt=}')
        return r

    def is_rg_rect(i, j):
        x0, y0 = coords[i]
        x1, y1 = coords[j]
        return (
            is_rg(x0, y1) and
            is_rg(x1, y0) and
            not cross_edges(x0, y0, x0, y1) and
            not cross_edges(x0, y1, x1, y1) and
            not cross_edges(x1, y1, x1, y0) and
            not cross_edges(x1, y0, x0, y0)
        )

    m = None
    mi, mj = -1, -1
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            a = area(i, j)
            if (m is None or a > m) and is_rg_rect(i, j):
                mi, mj, m = i, j, a
    print(coords[mi])
    print(coords[mj])
    print(m)

if __name__ == '__main__':
    main()
